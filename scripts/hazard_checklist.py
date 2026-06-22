#!/usr/bin/env python3
"""
安全隐患排查检查表生成器
按检查类型生成标准化排查清单，支持输出 Markdown
"""

import argparse
from datetime import datetime

CHECKLISTS = {
    "用电安全": [
        "配电箱（柜）门是否完好、锁闭",
        "配电箱内有无杂物堆积、积尘",
        "接地（接零）保护是否完好",
        "漏电保护器是否定期测试（按试验按钮）",
        "电缆线路有无破损、老化、过热现象",
        "临时用电是否有审批手续",
        "移动电具是否使用安全电压（≤36V）",
        "电气设备周边是否堆放易燃物品",
        "开关、插座是否固定牢固、无破损",
        "电气作业人员是否持证上岗",
        "防雷接地设施是否检测合格",
        "电缆沟、电缆井封堵是否完好",
    ],
    "消防安全": [
        "疏散通道、安全出口是否畅通",
        "应急照明灯是否正常（拔插头测试）",
        "疏散指示标志是否清晰、指向正确",
        "灭火器是否在有效期内、压力表指针是否在绿区",
        "灭火器是否按规定配置、无遮挡",
        "室内消火栓是否完好、配件齐全",
        "消防水带是否完好、无霉变开裂",
        "自动喷淋系统末端试水压力是否正常",
        "火灾自动报警系统是否正常运行",
        "防火门是否常闭、闭门器完好",
        "消防控制室是否24小时双人值班",
        "动火作业是否有审批手续",
        "易燃可燃物品存放是否符合要求",
    ],
    "高处作业": [
        "作业人员是否经培训合格",
        "作业人员是否正确佩戴安全带",
        "安全带是否挂在可靠锚点（高挂低用）",
        "安全带、安全绳是否在有效期内、外观完好",
        "脚手架是否验收合格、挂牌",
        "作业下方是否设置警戒区",
        "临边洞口防护是否到位",
        "梯子是否稳固、防滑垫完好",
        "恶劣天气（≥6级大风、雷雨）是否停止高处作业",
        "作业票是否审批签字",
        "交叉作业是否有隔离措施",
    ],
    "机械设备": [
        "设备安全防护罩是否齐全、完好",
        "急停按钮是否灵敏可靠",
        "设备接地保护是否完好",
        "联锁保护装置是否正常工作",
        "设备运行中有无异响、异振、异味",
        "操作台仪表指示是否正常",
        "润滑系统工作是否正常",
        "传动部件是否有防护罩",
        "操作人员是否佩戴劳保用品（手套、护目镜等）",
        "设备操作规程是否上墙可见",
        "维修保养记录是否完整",
        "设备运行记录是否按时填写",
    ],
    "危化品管理": [
        "危化品是否专区存放、双人双锁管理",
        "存储区域通风设施是否正常运行",
        "危化品容器标识是否清晰（名称、危险性、GHS标签）",
        "是否使用防爆电气设备",
        "现场是否配备对应的应急物资（吸附棉、中和剂等）",
        "化学品安全技术说明书（SDS）是否齐全",
        "危化品台账是否账物相符",
        "废弃物是否分类暂存",
        "可燃气体/有毒气体报警仪是否正常运行",
        "人体静电释放装置是否有效",
        "分装容器是否有合规标签",
    ],
    "劳动防护": [
        "安全帽是否在有效期内、外观完好",
        "劳保鞋是否符合标准",
        "防尘口罩/防毒面具是否配备且正确使用",
        "防护手套是否按工种配备",
        "护目镜/面罩是否完好",
        "耳塞/耳罩是否配备、正确使用",
        "安全带、安全绳是否定期检验",
        "劳保用品领用记录是否完整",
        "劳动防护用品是否过期未更换",
    ],
}


def generate_checklist(check_type="用电安全", company="", project="", output_file=None):
    """生成安全隐患排查表"""
    
    items = CHECKLISTS.get(check_type)
    if not items:
        available = ", ".join(CHECKLISTS.keys())
        print(f"❌ 不支持的检查类型: {check_type}")
        print(f"   可选类型: {available}")
        return
    
    lines = []
    lines.append(f"# 安全隐患排查检查表 — {check_type}")
    lines.append("")
    lines.append("- **检查日期**: ____年____月____日")
    lines.append(f"- **检查类型**: {check_type}")
    if company:
        lines.append(f"- **受检单位**: {company}")
    if project:
        lines.append(f"- **项目/区域**: {project}")
    lines.append("- **检查人员**: __________")
    lines.append("")
    lines.append("| 序号 | 检查项目 | 结果(✔/✘/N/A) | 问题描述 | 整改措施 | 整改责任人 | 完成期限 |")
    lines.append("|------|---------|--------------|---------|---------|----------|--------|")
    
    for i, item in enumerate(items, 1):
        lines.append(f"| {i} | {item} | | | | | |")
    
    lines.append("")
    lines.append("## 检查结论")
    lines.append("")
    lines.append("- 合格项: _____ 项")
    lines.append("- 不合格项: _____ 项")
    lines.append("- 不适用项: _____ 项")
    lines.append("- 总体评价: □ 合格  □ 基本合格  □ 不合格")
    lines.append("")
    lines.append("---")
    lines.append(f"*生成工具: EHS Compliance Toolkit | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    content = "\n".join(lines)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 检查表已生成: {output_file}")
    else:
        print(content)
    
    return content


def main():
    parser = argparse.ArgumentParser(description="安全隐患排查检查表生成器")
    parser.add_argument("--type", default="用电安全",
                        choices=list(CHECKLISTS.keys()),
                        help="检查类型")
    parser.add_argument("--company", default="", help="受检单位")
    parser.add_argument("--project", default="", help="项目/区域")
    parser.add_argument("--output", "-o", default="", help="输出文件路径")
    
    args = parser.parse_args()
    generate_checklist(args.type, args.company, args.project, args.output)


if __name__ == "__main__":
    main()
