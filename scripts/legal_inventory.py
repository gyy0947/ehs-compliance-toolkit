#!/usr/bin/env python3
"""
EHS 法律法规适用性清单生成器
生成企业适用的法律法规清单，按安全生产、职业健康、消防、环保分类
"""

import json
import argparse
from datetime import datetime

# ===== 法规数据库 =====
REGULATIONS = {
    "安全生产": [
        {"name": "中华人民共和国安全生产法", "number": "主席令第88号", "year": 2021, "status": "现行有效"},
        {"name": "生产安全事故报告和调查处理条例", "number": "国务院令第493号", "year": 2007, "status": "现行有效"},
        {"name": "安全生产许可证条例", "number": "国务院令第397号", "year": 2004, "status": "现行有效"},
        {"name": "建设工程安全生产管理条例", "number": "国务院令第393号", "year": 2003, "status": "现行有效"},
        {"name": "危险化学品安全管理条例", "number": "国务院令第591号", "year": 2011, "status": "现行有效"},
        {"name": "生产安全事故应急条例", "number": "国务院令第708号", "year": 2019, "status": "现行有效"},
        {"name": "特种设备安全监察条例", "number": "国务院令第549号", "year": 2009, "status": "现行有效"},
        {"name": "工伤保险条例", "number": "国务院令第586号", "year": 2010, "status": "现行有效"},
        {"name": "生产安全事故应急预案管理办法", "number": "应急管理部令第2号", "year": 2019, "status": "现行有效"},
        {"name": "特种作业人员安全技术培训考核管理规定", "number": "原安监总局令第30号", "year": 2010, "status": "现行有效"},
    ],
    "职业健康": [
        {"name": "中华人民共和国职业病防治法", "number": "主席令第52号", "year": 2018, "status": "现行有效"},
        {"name": "工作场所职业卫生管理规定", "number": "国家卫健委令第5号", "year": 2021, "status": "现行有效"},
        {"name": "职业病危害项目申报办法", "number": "原安监总局令第48号", "year": 2012, "status": "现行有效"},
        {"name": "用人单位职业健康监护监督管理办法", "number": "原安监总局令第49号", "year": 2012, "status": "现行有效"},
        {"name": "职业病诊断与鉴定管理办法", "number": "国家卫健委令第6号", "year": 2021, "status": "现行有效"},
    ],
    "消防安全": [
        {"name": "中华人民共和国消防法", "number": "主席令第6号", "year": 2021, "status": "现行有效"},
        {"name": "机关、团体、企业、事业单位消防安全管理规定", "number": "公安部令第61号", "year": 2001, "status": "现行有效"},
        {"name": "消防产品监督管理规定", "number": "公安部令第122号", "year": 2013, "status": "现行有效"},
    ],
    "环境保护": [
        {"name": "中华人民共和国环境保护法", "number": "主席令第9号", "year": 2014, "status": "现行有效"},
        {"name": "中华人民共和国大气污染防治法", "number": "主席令第31号", "year": 2018, "status": "现行有效"},
        {"name": "中华人民共和国水污染防治法", "number": "主席令第70号", "year": 2017, "status": "现行有效"},
        {"name": "中华人民共和国固体废物污染环境防治法", "number": "主席令第43号", "year": 2020, "status": "现行有效"},
        {"name": "中华人民共和国环境影响评价法", "number": "主席令第24号", "year": 2018, "status": "现行有效"},
        {"name": "排污许可管理条例", "number": "国务院令第736号", "year": 2021, "status": "现行有效"},
    ],
    "应急管理": [
        {"name": "中华人民共和国突发事件应对法", "number": "主席令第69号", "year": 2007, "status": "现行有效"},
        {"name": "国家突发公共事件总体应急预案", "number": "国发〔2005〕11号", "year": 2005, "status": "现行有效"},
        {"name": "应急管理部关于修改〈生产安全事故应急预案管理办法〉的决定", "number": "应急管理部令第2号", "year": 2019, "status": "现行有效"},
    ],
}

INDUSTRY_EXTRA = {
    "化工": [
        {"name": "危险化学品重大危险源监督管理暂行规定", "number": "原安监总局令第40号", "year": 2011, "status": "现行有效"},
        {"name": "危险化学品生产企业安全生产许可证实施办法", "number": "原安监总局令第41号", "year": 2011, "status": "现行有效"},
        {"name": "危险化学品输送管道安全管理规定", "number": "原安监总局令第43号", "year": 2012, "status": "现行有效"},
    ],
    "建筑": [
        {"name": "建筑施工企业安全生产许可证管理规定", "number": "建设部令第128号", "year": 2004, "status": "现行有效"},
        {"name": "建筑施工企业主要负责人、项目负责人和专职安全生产管理人员安全生产管理规定", "number": "住建部令第17号", "year": 2014, "status": "现行有效"},
    ],
    "矿山": [
        {"name": "中华人民共和国矿山安全法", "number": "主席令第65号", "year": 1992, "status": "现行有效"},
        {"name": "矿山安全监察条例", "number": "国务院令第702号", "year": 2018, "status": "现行有效"},
    ],
    "制造": [],
    "一般企业": [],
}

GB_STANDARDS = [
    {"name": "GB/T 29639-2020 生产经营单位生产安全事故应急预案编制导则", "year": 2020},
    {"name": "GB 6441-1986 企业职工伤亡事故分类", "year": 1986},
    {"name": "GB/T 33000-2016 企业安全生产标准化基本规范", "year": 2016},
    {"name": "GBZ 2.1-2019 工作场所有害因素职业接触限值 第1部分：化学有害因素", "year": 2019},
    {"name": "GBZ 158-2003 工作场所职业病危害警示标识", "year": 2003},
    {"name": "GB 50016-2014 建筑设计防火规范（2018年版）", "year": 2018},
    {"name": "GB 50140-2005 建筑灭火器配置设计规范", "year": 2005},
]


def generate_inventory(industry="一般企业", company_name="", output_file=None):
    """生成法律法规适用性清单"""
    lines = []
    
    # 标题
    lines.append(f"# EHS 法律法规适用性清单")
    lines.append(f"")
    lines.append(f"- **编制日期**: {datetime.now().strftime('%Y年%m月%d日')}")
    lines.append(f"- **适用行业**: {industry}")
    if company_name:
        lines.append(f"- **编制单位**: {company_name}")
    lines.append(f"- **说明**: 本清单列出企业 EHS 管理应适用的主要法律法规，供合规性评价参考。")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    total = 0
    for category, regs in REGULATIONS.items():
        lines.append(f"## {category}")
        lines.append(f"")
        lines.append(f"| 序号 | 法律法规名称 | 文号 | 发布年份 | 状态 |")
        lines.append(f"|------|-------------|------|---------|------|")
        
        for i, reg in enumerate(regs, 1):
            lines.append(f"| {i} | {reg['name']} | {reg['number']} | {reg['year']} | {reg['status']} |")
        
        total += len(regs)
        lines.append(f"")
    
    # 行业专项
    if industry in INDUSTRY_EXTRA and INDUSTRY_EXTRA[industry]:
        lines.append(f"## {industry}行业专项法规")
        lines.append(f"")
        lines.append(f"| 序号 | 法律法规名称 | 文号 | 发布年份 | 状态 |")
        lines.append(f"|------|-------------|------|---------|------|")
        
        for i, reg in enumerate(INDUSTRY_EXTRA[industry], 1):
            lines.append(f"| {i} | {reg['name']} | {reg['number']} | {reg['year']} | {reg['status']} |")
        
        total += len(INDUSTRY_EXTRA[industry])
        lines.append(f"")
    
    # 国家标准
    lines.append(f"## 相关标准规范")
    lines.append(f"")
    lines.append(f"| 序号 | 标准编号及名称 | 年份 |")
    lines.append(f"|------|---------------|------|")
    
    for i, std in enumerate(GB_STANDARDS, 1):
        lines.append(f"| {i} | {std['name']} | {std['year']} |")
    
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"*共收录法律法规 {total} 项，标准 {len(GB_STANDARDS)} 项*")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append(f"*⚠️ 法律法规具有时效性，请以官方最新版本为准*")
    
    content = "\n".join(lines)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 清单已生成: {output_file} ({total} 项法规)")
    else:
        print(content)
    
    return content


def main():
    parser = argparse.ArgumentParser(description="EHS 法律法规适用性清单生成器")
    parser.add_argument("--industry", default="一般企业", 
                        choices=list(INDUSTRY_EXTRA.keys()),
                        help="适用行业")
    parser.add_argument("--company", default="", help="编制单位名称")
    parser.add_argument("--output", "-o", default="", help="输出文件路径")
    
    args = parser.parse_args()
    generate_inventory(args.industry, args.company, args.output)


if __name__ == "__main__":
    main()
