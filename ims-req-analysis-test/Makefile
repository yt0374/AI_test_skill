# IMS ERP Test — 一键执行 Makefile
# 用法: make all SPEC=spec.md ENV=sit
#       make smoke SPEC=spec.md
#       make report RESULTS=test_results.json

SPEC ?= spec.md
ENV ?= sit
RESULTS ?= test_results.json

.PHONY: all probe generate test report feedback clean

# ===== 全流程 =====
all: probe generate test report feedback
	@echo "✅ Step 0-6 全流程完成"

# ===== Step 0: 环境探测 =====
probe:
	@echo "🔍 Step 0: 环境探测..."
	python scripts/probe_env.py $(SPEC) --env $(ENV)

# ===== Step 1-2: Skill 生成（需手动触发） =====
generate:
	@echo "📝 Step 1-2: 请在 Claude 中运行 Skill..."
	@echo "   Task: 根据需求文档生成完整测试方案"

# ===== Step 3: 编译执行 =====
test:
	@echo "🧪 Step 3-4: 编译+执行..."
	python scripts/generate_pytest.py $(SPEC) -o test_api.py
	pytest erp_tests/ -v --tb=short --html=reports/test_report.html

# ===== 快速模式 =====
smoke:
	pytest erp_tests/ -m p0 -v --tb=line

functional:
	pytest erp_tests/ -m "p0 or p1" -v

full:
	pytest erp_tests/ -m "p0 or p1 or p2" -v

api:
	pytest erp_tests/test_api.py -v

# ===== Step 5: 报告 =====
report:
	@echo "📊 Step 5: 生成报告..."
	python scripts/ingest_feedback.py $(RESULTS) -o reports/

# ===== Step 6: 反馈闭环 =====
feedback:
	@echo "🔄 Step 6: 反馈闭环..."
	@test -f reports/lessons_learned.md && echo "  lessons_learned.md 已生成" || echo "  请先运行 make report"

# ===== 工具 =====
clean:
	rm -rf reports/ *.pyc __pycache__ .pytest_cache
	@echo "🧹 清理完成"

init:
	pip install pytest pytest-playwright pytest-html pytest-rerunfailures pytest-xdist httpx pyyaml
	python -m playwright install chromium

help:
	@echo "IMS ERP Test Makefile"
	@echo "  make all      — 全流程 (probe→generate→test→report→feedback)"
	@echo "  make probe    — 环境探测"
	@echo "  make test     — 编译+执行"
	@echo "  make smoke    — 仅冒烟测试"
	@echo "  make report   — 生成报告+反馈"
	@echo "  make clean    — 清理临时文件"
	@echo "  make init     — 安装依赖"
	@echo ""
	@echo "  环境变量: SPEC=spec.md ENV=sit RESULTS=test_results.json"
