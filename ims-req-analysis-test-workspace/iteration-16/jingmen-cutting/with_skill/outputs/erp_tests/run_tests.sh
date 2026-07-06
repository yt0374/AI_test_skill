#!/bin/bash
# =============================================================================
# run_tests.sh - Jingmen Cutting System 2.0 Test Runner
# =============================================================================
# Usage:
#   ./run_tests.sh                  # 默认: 冒烟测试 (P0)
#   ./run_tests.sh smoke            # 冒烟测试 P0
#   ./run_tests.sh api              # API 测试（暂无，占位）
#   ./run_tests.sh functional       # 功能测试 P1
#   ./run_tests.sh full             # P0+P1+P2 全量
#   ./run_tests.sh integration      # 集成测试 P3
#   ./run_tests.sh complete         # 全部测试 P0+P1+P2+P3
#   ./run_tests.sh headed           # 有头模式运行冒烟测试
#   ./run_tests.sh boundary         # 边界测试 P2
#   ./run_tests.sh debug            # 调试模式（有头+慢速+单文件）
# =============================================================================

set -euo pipefail

# ---- 项目根目录 ----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---- 颜色输出 ----
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info()  { echo -e "${BLUE}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ---- 环境检查 ----
check_dependencies() {
    log_info "检查 Python 环境..."
    if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
        log_error "未找到 Python，请安装 Python 3.9+"
        exit 1
    fi

    PYTHON=$(command -v python3 || command -v python)
    PYTHON_VERSION=$($PYTHON --version 2>&1)
    log_ok "Python 版本: $PYTHON_VERSION"

    log_info "检查 pytest..."
    if ! $PYTHON -m pytest --version &>/dev/null; then
        log_error "未安装 pytest，请运行: pip install pytest"
        exit 1
    fi
    PYTEST_VERSION=$($PYTHON -m pytest --version 2>&1 | head -1)
    log_ok "pytest 版本: $PYTEST_VERSION"

    log_info "检查 playwright..."
    if ! $PYTHON -c "import playwright" &>/dev/null; then
        log_error "未安装 playwright，请运行: pip install playwright && playwright install chromium"
        exit 1
    fi
    log_ok "playwright 已安装"

    # 检查可选依赖
    if $PYTHON -c "import pytest_rerunfailures" &>/dev/null 2>&1; then
        log_ok "pytest-rerunfailures 已安装"
    else
        log_warn "建议安装 pytest-rerunfailures: pip install pytest-rerunfailures"
    fi

    if $PYTHON -c "import pytest_timeout" &>/dev/null 2>&1; then
        log_ok "pytest-timeout 已安装"
    else
        log_warn "建议安装 pytest-timeout: pip install pytest-timeout"
    fi
}

# ---- 显示帮助 ----
show_help() {
    echo ""
    echo "=============================================================================="
    echo "  荆门鹰美裁剪系统 2.0 - Playwright 自动化测试"
    echo "=============================================================================="
    echo ""
    echo "用法: ./run_tests.sh [模式]"
    echo ""
    echo "模式:"
    echo "  smoke        冒烟测试 (P0) - 核心流程，8 个测试用例"
    echo "  functional   功能测试 (P1) - 主要功能，18 个测试用例"
    echo "  boundary     边界测试 (P2) - 边界条件，29 个测试用例"
    echo "  integration  集成测试 (P3) - 端到端流程，6 个测试用例"
    echo "  full         P0 + P1 + P2 全量"
    echo "  complete     P0 + P1 + P2 + P3 全部测试"
    echo "  api          API 测试（暂无，占位）"
    echo "  headed       有头模式运行冒烟测试"
    echo "  debug        调试模式（有头 + 慢速 + 单个文件）"
    echo ""
    echo "环境变量:"
    echo "  BASE_URL=http://bak.jmym.dtsimple.pro   (默认)"
    echo "  HEADED=1                                 有头模式"
    echo "  SLOW_MO=500                              操作间隔(ms)"
    echo ""
    echo "示例:"
    echo "  ./run_tests.sh smoke"
    echo "  ./run_tests.sh functional"
    echo "  ./run_tests.sh complete"
    echo "  HEADED=1 ./run_tests.sh debug"
    echo ""
}

# ---- 安装依赖 ----
install_deps() {
    log_info "安装测试依赖..."
    $PYTHON -m pip install playwright pytest pytest-rerunfailures pytest-timeout pytest-html pytest-xdist \
        --quiet 2>/dev/null || log_warn "部分依赖安装可能失败，请检查网络"
    $PYTHON -m playwright install chromium --with-deps 2>/dev/null || \
        log_warn "Chromium 安装可能失败，请手动执行: playwright install chromium"
    log_ok "依赖安装完成"
}

# ---- 运行测试 ----
run_tests() {
    local mode="${1:-smoke}"
    local extra_args="${2:-}"

    log_info "============================================"
    log_info "开始运行测试"
    log_info "模式: $mode"
    log_info "目标环境: ${BASE_URL:-http://bak.jmym.dtsimple.pro}"
    log_info "============================================"
    echo ""

    local pytest_args=()

    case "$mode" in
        smoke)
            log_info "运行冒烟测试 (P0)..."
            pytest_args=(-m "p0" --tb=short)
            ;;
        functional)
            log_info "运行功能测试 (P1)..."
            pytest_args=(-m "p1" --tb=short)
            ;;
        boundary)
            log_info "运行边界测试 (P2)..."
            pytest_args=(-m "p2" --tb=short)
            ;;
        integration)
            log_info "运行集成测试 (P3)..."
            pytest_args=(-m "p3" --tb=long)
            ;;
        full)
            log_info "运行全量测试 (P0+P1+P2)..."
            pytest_args=(-m "p0 or p1 or p2" --tb=short)
            ;;
        complete)
            log_info "运行全部测试 (P0+P1+P2+P3)..."
            pytest_args=(-m "p0 or p1 or p2 or p3" --tb=long)
            ;;
        api)
            log_warn "API 测试暂无具体用例实现，运行占位测试..."
            pytest_args=(test_data/api_payloads.json --tb=short 2>/dev/null || true)
            log_ok "API 测试占位完成"
            return 0
            ;;
        headed)
            log_info "有头模式运行冒烟测试..."
            pytest_args=(-m "p0" --headed --tb=short)
            ;;
        debug)
            log_info "调试模式运行..."
            pytest_args=(--headed --slow-mo=500 --tb=long -s -x "test_smoke.py")
            ;;
        *)
            log_error "未知模式: $mode"
            show_help
            exit 1
            ;;
    esac

    # 追加额外参数
    if [ -n "$extra_args" ]; then
        pytest_args+=($extra_args)
    fi

    # 执行测试
    log_info "执行: pytest ${pytest_args[*]}"
    echo ""

    set +e
    $PYTHON -m pytest "${pytest_args[@]}"
    local exit_code=$?
    set -e

    echo ""
    if [ $exit_code -eq 0 ]; then
        log_ok "============================================"
        log_ok "所有测试通过!"
        log_ok "============================================"
    else
        log_error "============================================"
        log_error "测试失败，退出码: $exit_code"
        log_error "============================================"
        log_info "提示: 查看上方的错误详情，或运行 ./run_tests.sh debug 进行调试"
    fi

    return $exit_code
}

# ---- Main ----
main() {
    local mode="${1:-smoke}"

    # 环境变量覆盖
    export BASE_URL="${BASE_URL:-http://bak.jmym.dtsimple.pro}"
    export HEADED="${HEADED:-0}"
    export SLOW_MO="${SLOW_MO:-0}"

    case "$mode" in
        help|--help|-h)
            show_help
            exit 0
            ;;
        install)
            check_dependencies
            install_deps
            exit 0
            ;;
        check)
            check_dependencies
            log_ok "环境检查完成"
            exit 0
            ;;
    esac

    check_dependencies
    run_tests "$mode"
}

main "$@"
