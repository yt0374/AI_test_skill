# =============================================================================
# test_data_loader.py - 测试数据加载工具
# 荆门鹰美裁剪系统 2.0 Playwright 测试项目
# =============================================================================

import json
import csv
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestDataLoader:
    """测试数据加载器，支持 JSON 和 CSV 两种格式。

    用法:
        loader = TestDataLoader()
        data = loader.load_json("test_data.json")
        rows = loader.load_csv("cpo_list.csv")
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """初始化加载器。

        Args:
            data_dir: 测试数据目录路径，默认为项目根目录下的 test_data/
        """
        if data_dir is None:
            self.data_dir = Path(__file__).resolve().parent.parent / "test_data"
        else:
            self.data_dir = Path(data_dir)

    # ------------------------------------------------------------------
    # JSON 加载
    # ------------------------------------------------------------------
    def load_json(self, filename: str) -> Any:
        """加载 JSON 文件并返回解析后的 Python 对象。

        Args:
            filename: JSON 文件名（不含路径）

        Returns:
            解析后的 dict / list

        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON 解析失败
        """
        filepath = self._resolve_path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"JSON 测试数据文件不存在: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data and filename != "api_payloads.json":
            raise ValueError(f"JSON 文件为空: {filepath}")

        return data

    def load_json_safe(self, filename: str, default: Any = None) -> Any:
        """安全加载 JSON，文件不存在时返回默认值。"""
        try:
            return self.load_json(filename)
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            if filename == "api_payloads.json":
                return {}
            return default if default is not None else {}

    # ------------------------------------------------------------------
    # CSV 加载
    # ------------------------------------------------------------------
    def load_csv(self, filename: str) -> List[Dict[str, str]]:
        """加载 CSV 文件并返回字典列表。

        Args:
            filename: CSV 文件名（不含路径）

        Returns:
            list[dict]: 每行数据作为一个字典，键名为表头

        Raises:
            FileNotFoundError: 文件不存在
        """
        filepath = self._resolve_path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f"CSV 测试数据文件不存在: {filepath}")

        rows = []
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 跳过完全空行
                if any(v.strip() for v in row.values() if v):
                    rows.append(row)

        return rows

    def load_csv_as_dicts(self, filename: str, key_column: str) -> Dict[str, Dict[str, str]]:
        """加载 CSV 并以指定列作为键组织数据。

        Args:
            filename: CSV 文件名
            key_column: 用作字典键的列名

        Returns:
            dict: {key_value: {column: value, ...}, ...}
        """
        rows = self.load_csv(filename)
        return {row[key_column]: row for row in rows if key_column in row}

    # ------------------------------------------------------------------
    # 参数化数据提取
    # ------------------------------------------------------------------
    def get_parametrize_data(self, filename: str, section: str) -> List[tuple]:
        """从 JSON 文件中提取 pytest parametrize 格式的数据。

        期望 JSON 结构:
            {
                "section_name": [
                    {"id": "case_1", "input": "val1", "expected": "val2"},
                    ...
                ]
            }

        Args:
            filename: JSON 文件名
            section: JSON 中的节点名称

        Returns:
            list of tuples: [(row_dict,), ...] 或 [(val1, val2), ...]
        """
        data = self.load_json(filename)
        section_data = data.get(section, [])

        if not section_data:
            raise ValueError(f"JSON 节点 '{section}' 不存在或为空: {filename}")

        result = []
        for item in section_data:
            # 单值参数化: (value,)
            if isinstance(item, (str, int, float, bool)):
                result.append((item,))
            # 字典参数化: (row_dict,)
            elif isinstance(item, dict):
                result.append((item,))
            else:
                result.append((item,))

        return result

    # ------------------------------------------------------------------
    # 工具方法
    # ------------------------------------------------------------------
    def list_files(self) -> List[str]:
        """列出测试数据目录中的所有数据文件。"""
        files = []
        for ext in ("*.json", "*.csv"):
            files.extend(
                f.name for f in self.data_dir.glob(ext)
            )
        return sorted(files)

    def file_exists(self, filename: str) -> bool:
        """检查数据文件是否存在。"""
        return self._resolve_path(filename).exists()

    def _resolve_path(self, filename: str) -> Path:
        """解析文件名到完整路径。"""
        return self.data_dir / filename


# =============================================================================
# 模块级便捷函数
# =============================================================================
_default_loader: Optional[TestDataLoader] = None


def get_loader() -> TestDataLoader:
    """获取默认 TestDataLoader 单例。"""
    global _default_loader
    if _default_loader is None:
        _default_loader = TestDataLoader()
    return _default_loader


def load_json(filename: str) -> Any:
    """便捷函数：加载 test_data 目录下的 JSON 文件。"""
    return get_loader().load_json(filename)


def load_csv(filename: str) -> List[Dict[str, str]]:
    """便捷函数：加载 test_data 目录下的 CSV 文件。"""
    return get_loader().load_csv(filename)
