# 多场景平衡（scene-balance）

基于战斗模拟写回的运行结果，生成多场景平衡提案。只出提案，不静默修改正式配置表。

本仓库**不包含**框架表。

## 状态

当前入口依赖新版战斗模拟的写回结果。请先在 `combat-sim` 中执行：

```bash
python 启动_战斗模拟.py --write
```

再运行本仓库入口做汇总。若尚未写出运行结果，入口会返回明确原因，而不是伪造权重。

## 同级依赖

| 仓库 | 用途 |
|------|------|
| `combat-sim` | 战斗模拟与公共层 |
| `scene-coverage` | 覆盖率相关桥接（可选） |
| `numeric-ssot` | 框架路径 |

## 运行

需要 Python 3.11+。

```bash
pip install -r requirements.txt
python 启动_多场景平衡.py
```

提案与中间产物写到本仓库 `out/`。

## 许可

[MIT](LICENSE)
