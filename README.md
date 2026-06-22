# EHS 合规工具集 (EHS Compliance Toolkit)

> 面向中国 EHS 安全管理人员的实用合规工具集
> 适用于：化工、建筑、制造、矿业等行业的现场安全管理

## 📦 工具清单

| 工具 | 用途 |
|------|------|
| `scripts/legal_inventory.py` | 生成企业 EHS 法律法规适用性清单 |
| `scripts/hazard_checklist.py` | 生成安全隐患排查检查表 |
| `scripts/jsa_generator.py` | 生成作业安全分析（JSA/JHA）表 |

## 🚀 快速开始

```bash
# 法律合规清单
python scripts/legal_inventory.py --industry 化工 --output report.md

# 隐患排查表
python scripts/hazard_checklist.py --type 用电安全 --output checklist.md

# 作业安全分析
python scripts/jsa_generator.py --job 高处作业 --output jsa.md
```

## 🧩 适用场景

- **年度法律法规合规性评价** — 自动匹配适用法规条款
- **日常安全检查** — 按专业类型生成检查项目清单
- **作业许可审批** — 生成 JSA 分析表辅助风险辨识
- **隐患排查治理** — 标准化排查记录，支持整改闭环

## 📋 法规数据来源

法规数据基于：
- 《安全生产法》及修正案
- 《职业病防治法》
- 《消防法》
- 《环境保护法》
- 各行业专项安全规程
- GB 标准及行业标准

> ⚠️ 法律法规具有时效性，请在使用前确认最新版本。

## 🤝 贡献

欢迎提交 Issue 或 PR，共同完善 EHS 工具生态。

## 📄 许可证

MIT
