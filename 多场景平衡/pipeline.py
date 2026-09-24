
def _publish_out(name: str):
    from pathlib import Path
    dest = Path(__file__).resolve().parents[1] / "out" / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest

"""多场景平衡：只提案，不静默改表。权重与时长只来自框架簿。"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from ssot import 框架路径
from 场景覆盖.calc.sim_bridge import 流派对木桩命中
from 战斗模拟.内核.技能引擎 import 诊断技能栏
from 战斗模拟.世界 import 加载世界


def run(workbook: str | Path | None = None) -> dict[str, Any]:
    path = Path(workbook) if workbook else 框架路径()
    w = 加载世界(path, 加载技能效果=True)
    hits = 流派对木桩命中(path)
    scenes = list(w.场景.values())
    本期 = [s for s in scenes if str((s.原始行 or {}).get("本期是否跑") or "").strip() == "是"]
    扫描源 = 本期 or scenes

    缺时长 = [s.名称 for s in 扫描源 if s.战斗时长秒 is None]
    缺种子 = [s.名称 for s in 扫描源 if s.复现种子 is None]
    缺A = [s.名称 for s in 扫描源 if not s.友方构筑]
    缺B = [s.名称 for s in 扫描源 if not s.敌方构筑]

    allies = []
    for s in 扫描源:
        allies.extend(s.友方构筑)
    unique_allies = sorted(set(allies))
    技能诊断 = {name: 诊断技能栏(w, name) for name in unique_allies}

    命中层 = {}
    for name in unique_allies:
        row = hits.get(name) or {}
        if "error" in row:
            命中层[name] = {"error": row["error"]}
        else:
            命中层[name] = {
                "最终伤害": row.get("最终伤害"),
                "武器": row.get("武器"),
                "通道": row.get("通道") or row.get("伤害类型"),
            }

    weights = []
    for s in 扫描源:
        raw = s.原始行 or {}
        wval = raw.get("地图价值")
        if wval is None:
            wval = raw.get("玩法价值")
        if wval is None or str(wval).strip() in ("", "—", "-"):
            continue
        try:
            weights.append((s.名称, float(wval)))
        except (TypeError, ValueError):
            continue
    wsum = sum(v for _, v in weights)
    加权 = None
    if wsum > 0:
        加权 = {n: v / wsum for n, v in weights}

    可跑构筑 = [n for n, d in 技能诊断.items() if d.get("可跑数")]
    skip_reasons = Counter()
    for d in 技能诊断.values():
        for sk in d.get("跳过") or []:
            skip_reasons[sk.get("原因") or "未知"] += 1

    out = {
        "状态": "提案",
        "说明": "不发明 DPS 带；技能 DES 仅在动作/GCD/伤害段齐套时才可跑。",
        "场景总数": len(scenes),
        "本期是否跑=是": len(本期),
        "扫描场景数": len(扫描源),
        "数据缺口": {
            "缺战斗时长秒": 缺时长,
            "缺复现种子": 缺种子,
            "缺A方构筑": 缺A,
            "缺B方构筑": 缺B,
        },
        "地图价值加权": 加权,
        "地图价值合计": wsum,
        "命中层": 命中层,
        "技能诊断": 技能诊断,
        "可跑技能DES的构筑": 可跑构筑,
        "跳过原因计数": dict(skip_reasons),
        "提案": [
            {
                "项": "补技能总表伤害段/动作毫秒/公共冷却毫秒/数值类型",
                "因": "构筑槽技能当前无法进入真实 DES",
                "跳过原因计数": dict(skip_reasons),
            },
            {
                "项": "不写均匀场景权重",
                "因": "地图价值合计为 0 时禁止兜底均分" if wsum == 0 else "已用表内地图价值归一",
            },
        ],
    }
    dest = _publish_out("multi_scene_balance.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    out["写出"] = str(dest)
    return out
