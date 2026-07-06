# =============================================================================
# run_tests.ps1 - Jingmen Cutting System 2.0 Test Runner (PowerShell)
# =============================================================================
# Usage:
#   .\run_tests.ps1                    # 默认: 冒烟测试 (P0)
#   .\run_tests.ps1 smoke              # 冒烟测试 P0
#   .\run_tests.ps1 api                # API 测试（暂无，占位）
#   .\run_tests.ps1 functional         # 功能测试 P1
#   .\run_tests.ps1 full               # P0+P1+P2 全量
#   .\run_tests.ps1 integration        # 集成测试 P3
#   .\run_tests.ps1 complete           # 全部测试 P0+P1+P2+P3
#   .\run_tests.ps1 headed             # 有头模式运行冒烟测试
#   .\run_tests.ps1 boundary           # 边界测试 P2
#   .\run_tests.ps1 debug              # 调试模式（有头+慢速+单文件）
# =============================================================================

param(
    [Parameter(Position = 0)]
    [ValidateSet("smoke", "api", "functional", "boundary", "full", "integration", "complete", "headed", "debug", "install", "check", "help")]
    [string]$Mode = "smoke"
)

# ---- 颜色输出 ----
function Write-Info  { Write-Host "[INFO]  $args" -ForegroundColor Blue }
function Write-Ok    { Write-Host "[OK]    $args" -ForegroundColor Green }
function Write-Warn  { Write-Host "[WARN]  $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $args" -ForegroundColor Red }

# ---- 设置 ----
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# 环境变量默认值
if (-not $env:BASE_URL) { $env:BASE_URL = "http://bak.jmym.dtsimple.pro" }
if (-not $env:HEADED)   { $env:HEADED = "0" }
if (-not $env:SLOW_MO)  { $env:SLOW_MO = "0" }

# ---- 环境检查 ----
function Check-Dependencies {
    Write-Info "检查 Python 环境..."

    $pythonCmd = $null
    if (Get-Command python3 -ErrorAction SilentlyContinue) {
        $pythonCmd = "python3"
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonCmd = "python"
    } else {
        Write-Error "未找到 Python，请安装 Python 3.9+"
        Write-Info "下载地址: https://www.python.org/downloads/"
        exit 1
    }

    $pyVersion = & $pythonCmd --version 2>&1
    Write-Ok "Python 版本: $pyVersion"

    Write-Info "检查 pytest..."
    $pytestCheck = & $pythonCmd -m pytest --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "未安装 pytest，请运行: pip install pytest"
        exit 1
    }
    Write-Ok "pytest: $($pytestCheck[0])"

    Write-Info "检查 playwright..."
    $pwCheck = & $pythonCmd -c "import playwright; print(playwright.__file__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "未安装 playwright，请运行: pip install playwright && playwright install chromium"
        exit 1
    }
    Write-Ok "playwright 已安装"

    # 可选依赖
    $rerunCheck = & $pythonCmd -c "import pytest_rerunfailures" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "pytest-rerunfailures 已安装"
    } else {
        Write-Warn "建议安装: pip install pytest-rerunfailures"
    }

    $timeoutCheck = & $pythonCmd -c "import pytest_timeout" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Ok "pytest-timeout 已安装"
    } else {
        Write-Warn "建议安装: pip install pytest-timeout"
    }

    # 返回 Python 命令
    return $pythonCmd
}

# ---- 帮助 ----
function Show-Help {
    Write-Host ""
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "  荆门鹰美裁剪系统 2.0 - Playwright 自动化测试" -ForegroundColor Cyan
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法: .\run_tests.ps1 [模式]"
    Write-Host ""
    Write-Host "模式:"
    Write-Host "  smoke        冒烟测试 (P0) - 核心流程，8 个测试用例"
    Write-Host "  functional   功能测试 (P1) - 主要功能，18 个测试用例"
    Write-Host "  boundary     边界测试 (P2) - 边界条件，29 个测试用例"
    Write-Host "  integration  集成测试 (P3) - 端到端流程，6 个测试用例"
    Write-Host "  full         P0 + P1 + P2 全量"
    Write-Host "  complete     P0 + P1 + P2 + P3 全部测试"
    Write-Host "  api          API 测试（暂无，占位）"
    Write-Host "  headed       有头模式运行冒烟测试"
    Write-Host "  debug        调试模式（有头 + 慢速 + 单文件）"
    Write-Host "  install      安装依赖"
    Write-Host "  check        仅检查环境"
    Write-Host ""
    Write-Host "环境变量:"
    Write-Host "  `$env:BASE_URL = 'http://bak.jmym.dtsimple.pro'"
    Write-Host "  `$env:HEADED = '1'"
    Write-Host "  `$env:SLOW_MO = '500'"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\run_tests.ps1 smoke"
    Write-Host "  .\run_tests.ps1 functional"
    Write-Host "  .\run_tests.ps1 complete"
    Write-Host "  `$env:HEADED='1'; .\run_tests.ps1 debug"
    Write-Host ""
}

# ---- 安装依赖 ----
function Install-Deps {
    param([string]$PythonCmd)

    Write-Info "安装测试依赖..."
    & $PythonCmd -m pip install playwright pytest pytest-rerunfailures pytest-timeout pytest-html pytest-xdist --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "部分依赖安装可能失败，请检查网络"
    }

    Write-Info "安装 Chromium 浏览器..."
    & $PythonCmd -m playwright install chromium --with-deps
    if ($LASTEXITCODE -ne 0) {
        Write-Warn "Chromium 安装可能失败，请手动执行: playwright install chromium"
    } else {
        Write-Ok "Chromium 安装完成"
    }

    Write-Ok "依赖安装完成"
}

# ---- 运行测试 ----
function Invoke-Tests {
    param(
        [string]$Mode,
        [string]$PythonCmd
    )

    Write-Info "============================================"
    Write-Info "开始运行测试"
    Write-Info "模式: $Mode"
    Write-Info "目标环境: $env:BASE_URL"
    Write-Info "============================================"
    Write-Host ""

    $pytestArgs = @()

    switch ($Mode) {
        "smoke" {
            Write-Info "运行冒烟测试 (P0)..."
            $pytestArgs = @("-m", "p0", "--tb=short")
        }
        "functional" {
            Write-Info "运行功能测试 (P1)..."
            $pytestArgs = @("-m", "p1", "--tb=short")
        }
        "boundary" {
            Write-Info "运行边界测试 (P2)..."
            $pytestArgs = @("-m", "p2", "--tb=short")
        }
        "integration" {
            Write-Info "运行集成测试 (P3)..."
            $pytestArgs = @("-m", "p3", "--tb=long")
        }
        "full" {
            Write-Info "运行全量测试 (P0+P1+P2)..."
            $pytestArgs = @("-m", "p0 or p1 or p2", "--tb=short")
        }
        "complete" {
            Write-Info "运行全部测试 (P0+P1+P2+P3)..."
            $pytestArgs = @("-m", "p0 or p1 or p2 or p3", "--tb=long")
        }
        "api" {
            Write-Warn "API 测试暂无具体用例实现"
            Write-Ok "API 测试占位完成"
            return 0
        }
        "headed" {
            Write-Info "有头模式运行冒烟测试..."
            $pytestArgs = @("-m", "p0", "--headed", "--tb=short")
        }
        "debug" {
            Write-Info "调试模式运行..."
            $pytestArgs = @("--headed", "--slow-mo=500", "--tb=long", "-s", "-x", "test_smoke.py")
        }
    }

    # 追加环境变量相关参数
    if ($env:HEADED -eq "1" -and $Mode -ne "headed" -and $Mode -ne "debug") {
        $pytestArgs += "--headed"
    }
    if ($env:SLOW_MO -ne "0" -and $Mode -ne "debug") {
        $pytestArgs += @("--slow-mo", $env:SLOW_MO)
    }

    # 执行测试
    Write-Info "执行: pytest $($pytestArgs -join ' ')"
    Write-Host ""

    $ErrorActionPreference = "Continue"
    & $PythonCmd -m pytest @pytestArgs
    $exitCode = $LASTEXITCODE
    $ErrorActionPreference = "Stop"

    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Ok "============================================"
        Write-Ok "所有测试通过!"
        Write-Ok "============================================"
    } else {
        Write-Error "============================================"
        Write-Error "测试失败，退出码: $exitCode"
        Write-Error "============================================"
        Write-Info "提示: 查看上方的错误详情，或运行 .\run_tests.ps1 debug 进行调试"
    }

    return $exitCode
}

# ---- Main ----
function Main {
    if ($Mode -eq "help" -or $Mode -eq "--help" -or $Mode -eq "-h") {
        Show-Help
        return 0
    }

    $pythonCmd = Check-Dependencies

    if ($Mode -eq "install") {
        Install-Deps -PythonCmd $pythonCmd
        return 0
    }

    if ($Mode -eq "check") {
        Write-Ok "环境检查完成"
        return 0
    }

    return Invoke-Tests -Mode $Mode -PythonCmd $pythonCmd
}

# ---- 入口 ----
$exitCode = Main
exit $exitCode
