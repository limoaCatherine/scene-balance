#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""策划入口：启动_多场景平衡.py"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path
from typing import Optional, cast

if hasattr(sys.stdout, "reconfigure"):
    cast(io.TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    cast(io.TextIOWrapper, sys.stderr).reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_SIBLING_REPOS = ("combat-sim", "scene-coverage", "attr-value", "scene-balance", "numeric-ssot", "doc-format")
for _name in _SIBLING_REPOS:
    _p = ROOT.parent / _name
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def main(argv: Optional[list[str]] = None) -> int:
    from 多场景平衡.pipeline import run

    out = run()
    slim = {
        "状态": out.get("状态"),
        "场景总数": out.get("场景总数"),
        "本期是否跑=是": out.get("本期是否跑=是"),
        "地图价值合计": out.get("地图价值合计"),
        "可跑技能DES的构筑": out.get("可跑技能DES的构筑"),
        "跳过原因计数": out.get("跳过原因计数"),
        "写出": out.get("写出"),
    }
    print(slim)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

