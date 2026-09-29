"""多场景平衡改读战斗模拟写回的运行结果，不再调用旧技能引擎。"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def run(workbook: str | Path | None = None) -> dict[str, Any]:
    del workbook
    return {
        "ok": False,
        "原因": "旧战斗引擎已移除。先用 启动_战斗模拟.py --write 写出运行结果，再在这里汇总。",
    }
