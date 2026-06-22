#!/usr/bin/env python3
"""
作业安全分析（JSA / JHA）表生成器
按作业类型生成标准化的风险分析表
"""

import argparse
from datetime import datetime

JSA_TEMPLATES = {
    "高处作业": [
        {"step": "作业准备", "hazard": "未系安全带或安全带挂点不可靠", "control": "安全带高挂低用，挂点承重≥500kg，检查安全带外观无破损"},
        {"step": "作业准备", "hazard": "梯子不稳、滑倒", "control": "梯子专人扶护，放置于坚实地面，防滑脚垫完好"},
        {"step": "登高操作", "hazard": "工具脱落伤人", "control": "工具放入工具袋，手递手传递，严禁抛掷"},
        {"step": "登高操作", "hazard": "作业下方未设警戒区", "control": "下方拉设警戒带，设监护人，无关人员禁止进入"},
        {"step": "作业过程", "hazard": "恶劣天气（大风≥6级/雷雨）", "control": "遇恶劣天气立即停止作业，撤离至安全区域"},
        {"step": "作业结束", "hazard": "材料遗留在高处", "control": "工完料净场地清，确认无遗留物后方可撤离"},
    ],
    "动火作业": [
        {"step": "作业准备", "hazard": "未清理易燃物", "control": "动火点周围10m内清理可燃物，配备灭火器+消防水带"},
        {"step": "作业准备", "hazard": "未办理动火作业票", "control": "严格执行动火审批制度，确认审批手续齐全"},
        {"step": "作业准备", "hazard": "可燃气体浓度超标", "control": "动火前30min内进行可燃气体检测，合格后方可动火"},
        {"step": "动火操作", "hazard": "火花飞溅引燃", "control": "设置防火布遮挡，监护人全程值守"},
        {"step": "动火操作", "hazard": "氧气瓶/乙炔瓶间距不足", "control": "气瓶间距≥5m，距动火点≥10m，直立固定"},
        {"step": "作业结束", "hazard": "余火未熄灭", "control": "作业后持续监护30min以上，确认无火种残留"},
    ],
    "受限空间作业": [
        {"step": "作业准备", "hazard": "未办理受限空间作业票", "control": "严格执行审批制度，确认作业票有效"},
        {"step": "作业准备", "hazard": "有毒有害气体浓度未知", "control": "作业前检测 O₂（19.5-23.5%）、H₂S、CO、可燃气体"},
        {"step": "作业准备", "hazard": "未进行隔离/上锁挂牌", "control": "与工艺系统可靠隔离，断开管道或加盲板"},
        {"step": "作业过程", "hazard": "监护人脱岗", "control": "监护人全程在入口处值守，不得离开"},
        {"step": "作业过程", "hazard": "通风不良导致缺氧", "control": "持续机械通风，严禁用纯氧通风"},
        {"step": "作业过程", "hazard": "未佩戴防护用品", "control": "根据检测结果选择防毒面具/空气呼吸器"},
        {"step": "紧急情况", "hazard": "救援不当导致二次伤亡", "control": "救援人员必须佩戴空气呼吸器，严禁盲目施救"},
    ],
    "临时用电": [
        {"step": "线路敷设", "hazard": "电缆破损漏电", "control": "电缆过路穿管保护，架空≥2.5m，无接头"},
        {"step": "配电系统", "hazard": "未采用 TN-S 系统", "control": "三级配电两级保护，一机一闸一漏"},
        {"step": "用电设备", "hazard": "设备未接地", "control": "金属外壳可靠接地，接地电阻≤4Ω"},
        {"step": "使用过程", "hazard": "私拉乱接", "control": "临时用电须专业人员操作，严禁私自接线"},
        {"step": "使用结束", "hazard": "用电结束后未断电拆除", "control": "作业完成后及时拆除临时线路，恢复原状"},
    ],
    "吊装作业": [
        {"step": "作业准备", "hazard": "起重设备未检验合格", "control": "检查起重设备年检标志及维保记录"},
        {"step": "作业准备", "hazard": "吊索具外观不合格", "control": "检查钢丝绳断丝数、吊带磨损、卸扣变形等"},
        {"step": "吊装过程", "hazard": "超负荷吊装", "control": "确认吊物重量≤额定载荷，使用称重仪"},
        {"step": "吊装过程", "hazard": "吊物下方站人", "control": "吊臂及吊物下方严禁站人，设警戒区域"},
        {"step": "吊装过程", "hazard": "吊物捆绑不牢", "control": "吊物捆绑牢固，棱角处加垫保护"},
        {"step": "吊装过程", "hazard": "信号指挥不清", "control": "专人指挥，手势/口哨/对讲机信号明确统一"},
    ],
}


def generate_jsa(job_type="高处作业", company="", location="", output_file=None):
    """生成作业安全分析表"""
    
    steps = JSA_TEMPLATES.get(job_type)
    if not steps:
        available = ", ".join(JSA_TEMPLATES.keys())
        print(f"❌ 不支持的作业类型: {job_type}")
        print(f"   可选类型: {available}")
        return
    
    lines = []
    lines.append(f"# 作业安全分析（JSA）表 — {job_type}")
    lines.append(f"")
    lines.append(f"| 项目 | 内容 |")
    lines.append(f"|------|------|")
    lines.append(f"| 作业类型 | {job_type} |")
    lines.append(f"| 作业区域 | {location or '__________'} |")
    lines.append(f"| 作业单位 | {company or '__________'} |")
    lines.append(f"| 作业人员 | __________ |")
    lines.append(f"| 监护人 | __________ |")
    lines.append(f"| 作业日期 | ____年____月____日 ____:____ ~ ____:____ |")
    lines.append(f"")
    lines.append(f"## 风险分析")
    lines.append(f"")
    lines.append(f"| 序号 | 作业步骤 | 潜在风险 | 控制措施 | 责任人 | 确认 |")
    lines.append(f"|------|---------|---------|---------|------|------|")
    
    for i, step in enumerate(steps, 1):
        lines.append(f"| {i} | {step['step']} | {step['hazard']} | {step['control']} | | |")
    
    lines.append(f"")
    lines.append(f"## 作业审批")
    lines.append(f"")
    lines.append(f"- **作业负责人**: ________ | **日期**: ________")
    lines.append(f"- **安全监护人**: ________ | **日期**: ________")
    lines.append(f"- **EHS 审批**: ________ | **日期**: ________")
    lines.append(f"")
    lines.append(f"## 完工确认")
    lines.append(f"")
    lines.append(f"- 作业现场已清理: □ 是 □ 否")
    lines.append(f"- 安全设施已恢复: □ 是 □ 否")
    lines.append(f"- 作业票已关闭: □ 是 □ 否")
    lines.append(f"- **确认人**: ________ | **日期**: ________")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*生成工具: EHS Compliance Toolkit | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    content = "\n".join(lines)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ JSA 表已生成: {output_file}")
    else:
        print(content)
    
    return content


def main():
    parser = argparse.ArgumentParser(description="作业安全分析（JSA）表生成器")
    parser.add_argument("--job", default="高处作业",
                        choices=list(JSA_TEMPLATES.keys()),
                        help="作业类型")
    parser.add_argument("--company", default="", help="作业单位")
    parser.add_argument("--location", default="", help="作业区域")
    parser.add_argument("--output", "-o", default="", help="输出文件路径")
    
    args = parser.parse_args()
    generate_jsa(args.job, args.company, args.location, args.output)


if __name__ == "__main__":
    main()
