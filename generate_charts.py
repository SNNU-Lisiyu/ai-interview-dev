# -*- coding: utf-8 -*-
"""
智面星途 商业计划书图表生成脚本
==============================

本脚本使用 matplotlib 和 plotly 生成商业计划书中的各类统计图表。
运行前请确保安装了以下依赖：
    pip install matplotlib plotly pandas numpy kaleido

生成的图表将保存到 ./图表/ 目录下。
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import matplotlib.font_manager as fm

# 设置中文字体支持 - 使用微软雅黑，它对符号支持更好
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# 设置默认字体大小
plt.rcParams['font.size'] = 10

# 创建输出目录
OUTPUT_DIR = './图表'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 配色方案
COLORS = {
    'primary': '#1976d2',      # 蓝色 - 技术相关
    'success': '#388e3c',      # 绿色 - 增长相关
    'warning': '#f57c00',      # 橙色 - 核心相关
    'danger': '#c2185b',       # 粉色 - 评测相关
    'info': '#0097a7',         # 青色 - 底层能力
    'purple': '#7b1fa2',       # 紫色 - 输出相关
}

PALETTE = ['#1976d2', '#388e3c', '#f57c00', '#c2185b', '#0097a7', '#7b1fa2', '#ffc107']


def chart_1_market_size():
    """
    图表6: AI招聘市场规模增长趋势
    柱状图 + 折线图
    """
    years = ['2022', '2023', '2024', '2025E', '2026E', '2027E']
    market_size = [100, 140, 180, 250, 360, 500]  # 亿元
    growth_rate = [None, 40, 28.6, 38.9, 44, 38.9]  # %
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # 柱状图 - 市场规模
    bars = ax1.bar(years, market_size, color=COLORS['primary'], alpha=0.8, label='市场规模（亿元）')
    ax1.set_xlabel('年份', fontsize=12)
    ax1.set_ylabel('市场规模（亿元）', fontsize=12, color=COLORS['primary'])
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1.set_ylim(0, 600)  # 设置Y轴上限，给500的柱子和标签留出空间
    
    # 在柱子上显示数值
    for bar, value in zip(bars, market_size):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 折线图 - 增长率
    ax2 = ax1.twinx()
    valid_years = years[1:]
    valid_growth = growth_rate[1:]
    ax2.plot(valid_years, valid_growth, color=COLORS['danger'], marker='o', 
             linewidth=2, markersize=8, label='同比增长率（%）')
    ax2.set_ylabel('同比增长率（%）', fontsize=12, color=COLORS['danger'])
    ax2.tick_params(axis='y', labelcolor=COLORS['danger'])
    ax2.set_ylim(20, 55)  # 设置增长率Y轴范围，确保标签不会飞出框外
    
    # 显示增长率数值（调整偏移量）
    for x, y in zip(valid_years, valid_growth):
        ax2.text(x, y + 1.5, f'{y:.1f}%', ha='center', fontsize=9, color=COLORS['danger'])
    
    plt.title('中国AI招聘市场规模增长趋势', fontsize=14, fontweight='bold', pad=20)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表6-AI招聘市场规模.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表6-AI招聘市场规模.png 已生成')


def chart_2_survey_enterprise():
    """
    图表7: 调研企业规模分布
    饼图
    """
    labels = ['大型企业\n(>1000人)', '中型企业\n(100-1000人)', '小型企业\n(<100人)']
    sizes = [35, 45, 20]
    colors = [COLORS['primary'], COLORS['success'], COLORS['warning']]
    explode = (0, 0.05, 0)  # 突出中型企业
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                       autopct='%1.0f%%', startangle=90,
                                       textprops={'fontsize': 11},
                                       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    # 设置百分比文字样式
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('调研企业规模分布', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表7-调研企业规模分布.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表7-调研企业规模分布.png 已生成')


def chart_3_survey_industry():
    """
    图表8: 调研企业行业分布
    饼图
    """
    labels = ['互联网/科技', '金融/咨询', '制造/工业', '教育/培训']
    sizes = [40, 25, 20, 15]
    colors = [COLORS['primary'], COLORS['warning'], COLORS['success'], COLORS['purple']]
    
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                       autopct='%1.0f%%', startangle=90,
                                       textprops={'fontsize': 11},
                                       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('调研企业行业分布', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表8-调研企业行业分布.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表8-调研企业行业分布.png 已生成')


def chart_4_pain_points():
    """
    图表9: 行业痛点数据对比
    水平条形图
    """
    pain_points = [
        'AI评测结果与实际表现偏差',
        '求职者体验"生硬、不自然"',
        '求职者无法展示真正优势',
        '优秀候选人因体验差流失',
        'HR需人工复面验证AI结果',
        '求职者获得有价值反馈'
    ]
    percentages = [68, 73, 81, 25, 65, 28]
    colors = [COLORS['danger'] if p > 50 else COLORS['success'] for p in percentages]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_pos = np.arange(len(pain_points))
    bars = ax.barh(y_pos, percentages, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pain_points, fontsize=10)
    ax.set_xlabel('占比（%）', fontsize=12)
    ax.set_xlim(0, 100)
    
    # 在条形上显示数值
    for bar, pct in zip(bars, percentages):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2, 
                f'{pct}%', ha='left', va='center', fontsize=10, fontweight='bold')
    
    ax.set_title('AI面试行业痛点调研数据', fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()  # 翻转Y轴
    
    # 添加图例
    red_patch = mpatches.Patch(color=COLORS['danger'], label='痛点（>50%）')
    green_patch = mpatches.Patch(color=COLORS['success'], label='不足（<50%）')
    ax.legend(handles=[red_patch, green_patch], loc='lower right')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表9-行业痛点数据.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表9-行业痛点数据.png 已生成')


def chart_5_competitor_radar():
    """
    图表10: 竞品对标雷达图
    """
    categories = ['模态支持', '融合深度', '评测维度', '追问能力', '可解释性', '性价比']
    
    # 各产品评分（满分5分）
    products = {
        '传统方案': [1, 0, 2, 1, 1, 3],
        '国际竞品(HireVue)': [3, 2, 4, 2, 3, 1],
        '国内竞品': [3, 2, 3, 2, 2, 3],
        '智面星途': [5, 5, 5, 5, 5, 5]
    }
    
    # 雷达图角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    colors_map = {
        '传统方案': '#9e9e9e',
        '国际竞品(HireVue)': COLORS['warning'],
        '国内竞品': COLORS['info'],
        '智面星途': COLORS['primary']
    }
    
    for product, scores in products.items():
        values = scores + scores[:1]  # 闭合
        ax.plot(angles, values, 'o-', linewidth=2, label=product, color=colors_map[product])
        ax.fill(angles, values, alpha=0.15, color=colors_map[product])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9)
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.title('竞品对标分析', fontsize=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表10-竞品对标雷达图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表10-竞品对标雷达图.png 已生成')


def chart_6_capability_radar():
    """
    图表11: 候选人能力评测雷达图（示例）
    """
    categories = ['专业知识\n水平', '语言表达\n能力', '逻辑思维\n能力', '应变抗压\n能力', '岗位匹配度']
    
    # 示例候选人评分
    candidate_a = [4.2, 3.8, 4.5, 3.5, 4.0]
    candidate_b = [3.5, 4.5, 3.8, 4.2, 3.2]
    job_requirement = [4.0, 4.0, 4.0, 3.5, 4.0]  # 岗位要求
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # 候选人A
    values_a = candidate_a + candidate_a[:1]
    ax.plot(angles, values_a, 'o-', linewidth=2, label='候选人A', color=COLORS['primary'])
    ax.fill(angles, values_a, alpha=0.2, color=COLORS['primary'])
    
    # 候选人B
    values_b = candidate_b + candidate_b[:1]
    ax.plot(angles, values_b, 's-', linewidth=2, label='候选人B', color=COLORS['warning'])
    ax.fill(angles, values_b, alpha=0.2, color=COLORS['warning'])
    
    # 岗位要求线
    values_req = job_requirement + job_requirement[:1]
    ax.plot(angles, values_req, '--', linewidth=2, label='岗位要求', color=COLORS['danger'])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    plt.title('候选人能力评测对比', fontsize=14, fontweight='bold', pad=30)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表11-能力评测雷达图.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表11-能力评测雷达图.png 已生成')


def chart_7_financial_projection():
    """
    图表12: 三年财务预测
    堆叠柱状图
    """
    years = ['2025H2', '2026年', '2027年']
    saas_revenue = [40, 240, 750]
    service_revenue = [10, 60, 200]
    c_end_revenue = [0, 0, 50]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x = np.arange(len(years))
    width = 0.5
    
    # 堆叠柱状图
    bars1 = ax.bar(x, saas_revenue, width, label='SaaS订阅', color=COLORS['primary'])
    bars2 = ax.bar(x, service_revenue, width, bottom=saas_revenue, label='增值服务', color=COLORS['success'])
    bars3 = ax.bar(x, c_end_revenue, width, 
                   bottom=[s+v for s,v in zip(saas_revenue, service_revenue)], 
                   label='求职者端', color=COLORS['warning'])
    
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('营收（万元）', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(years)
    
    # 显示总营收
    totals = [s+v+c for s,v,c in zip(saas_revenue, service_revenue, c_end_revenue)]
    for i, total in enumerate(totals):
        ax.text(i, total + 20, f'{total}万元', ha='center', fontsize=11, fontweight='bold')
    
    ax.legend(loc='upper left')
    plt.title('三年财务预测（保守估计）', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表12-三年财务预测.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表12-三年财务预测.png 已生成')


def chart_8_cost_comparison():
    """
    图表13: 面试成本对比
    条形图
    """
    methods = ['人工面试', '智面星途\n基础版', '智面星途\n专业版']
    costs = [50, 6.7, 5]
    colors = [COLORS['danger'], COLORS['primary'], COLORS['success']]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    bars = ax.bar(methods, costs, color=colors, edgecolor='white', linewidth=2)
    
    # 显示数值和降幅
    ax.text(0, costs[0] + 2, f'{costs[0]}元/次', ha='center', fontsize=12, fontweight='bold')
    ax.text(1, costs[1] + 2, f'{costs[1]}元/次\n↓87%', ha='center', fontsize=11, fontweight='bold', color=COLORS['primary'])
    ax.text(2, costs[2] + 2, f'{costs[2]}元/次\n↓90%', ha='center', fontsize=11, fontweight='bold', color=COLORS['success'])
    
    ax.set_ylabel('单次面试成本（元）', fontsize=12)
    ax.set_ylim(0, 65)
    
    plt.title('面试成本对比', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表13-面试成本对比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表13-面试成本对比.png 已生成')


def chart_9_efficiency_comparison():
    """
    图表14: 智面星途效率提升对比
    使用子图分别展示各指标，避免数据比例悬殊问题
    """
    # 数据定义
    data = [
        {'metric': '初面效率', 'unit': '人/天', 'traditional': 20, 'zhimian': 500, 'improvement': '25倍↑', 'better': 'higher'},
        {'metric': '候选人等待', 'unit': '天', 'traditional': 7, 'zhimian': 0.5, 'improvement': '93%↓', 'better': 'lower'},
        {'metric': '评测维度', 'unit': '项', 'traditional': 4, 'zhimian': 12, 'improvement': '3倍↑', 'better': 'higher'},
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 6))
    fig.suptitle('智面星途 vs 传统方式效率对比', fontsize=16, fontweight='bold', y=0.98)
    
    for idx, d in enumerate(data):
        ax = axes[idx]
        x = np.array([0, 1])
        values = [d['traditional'], d['zhimian']]
        colors = [COLORS['danger'], COLORS['primary']]
        labels = ['传统方式', '智面星途']
        
        bars = ax.bar(x, values, width=0.5, color=colors, edgecolor='white', linewidth=2)
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=11)
        ax.set_ylabel(d['unit'], fontsize=11)
        ax.set_title(f"{d['metric']}", fontsize=13, fontweight='bold', pad=10)
        
        # 设置Y轴从0开始，留出标注空间
        y_max = max(values) * 1.35
        ax.set_ylim(0, y_max)
        
        # 在柱子上方显示数值
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + y_max*0.02,
                   f'{val}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 显示提升效果（放在图表上方中间位置）
        ax.text(0.5, 0.92, d['improvement'],
               ha='center', fontsize=14, fontweight='bold', color=COLORS['success'],
               transform=ax.transAxes)
    
    plt.subplots_adjust(top=0.85, bottom=0.1, wspace=0.3)
    plt.savefig(f'{OUTPUT_DIR}/图表14-效率提升对比.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表14-效率提升对比.png 已生成')


def chart_10_ltv_cac():
    """
    图表15: LTV/CAC 单位经济模型
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    
    metrics = ['CAC\n客户获取成本', 'LTV\n客户生命周期价值', 'LTV/CAC\n比值']
    values = [0.5, 5, 10]  # 万元
    colors = [COLORS['danger'], COLORS['success'], COLORS['primary']]
    
    bars = ax.bar(metrics, values, color=colors, edgecolor='white', linewidth=2)
    
    # 显示数值
    ax.text(0, values[0] + 0.2, '5,000元', ha='center', fontsize=12, fontweight='bold')
    ax.text(1, values[1] + 0.2, '50,000+元', ha='center', fontsize=12, fontweight='bold')
    ax.text(2, values[2] + 0.2, '10x\n(健康>3x)', ha='center', fontsize=12, fontweight='bold', color=COLORS['success'])
    
    ax.set_ylabel('数值（万元 / 倍数）', fontsize=12)
    ax.set_ylim(0, 12)
    
    plt.title('单位经济模型', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/图表15-单位经济模型.png', dpi=300, bbox_inches='tight')
    plt.close()
    print('✅ 图表15-单位经济模型.png 已生成')


def chart_multimodal_fusion():
    """
    图表2: 多模态融合示意图（无关联挖掘示例）
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 颜色定义
    colors = {
        '输入': ('#e3f2fd', '#1976d2'),
        '融合': ('#fff3e0', '#f57c00'),
        '输出': ('#e8f5e9', '#388e3c'),
    }
    
    # 左侧：多模态输入
    input_x, input_y = 0.5, 1.5
    input_w, input_h = 3.5, 5.5
    fill, border = colors['输入']
    
    rect = mpatches.FancyBboxPatch((input_x, input_y), input_w, input_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        facecolor=fill, edgecolor=border, linewidth=2)
    ax.add_patch(rect)
    ax.text(input_x + input_w/2, input_y + input_h - 0.3, '多模态输入',
           ha='center', va='top', fontsize=15, fontweight='bold', color=border)
    
    # 输入子项
    input_items = [
        ('语音特征', '语速/语调/情感'),
        ('视觉特征', '微表情/肢体语言'),
        ('文本特征', '内容/逻辑/专业度'),
    ]
    for i, (title, desc) in enumerate(input_items):
        y = input_y + input_h - 1.5 - i * 1.5
        item_rect = mpatches.FancyBboxPatch((input_x + 0.3, y - 0.9), 2.9, 1.1,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor='white', edgecolor=border, linewidth=1.5)
        ax.add_patch(item_rect)
        ax.text(input_x + 0.3 + 1.45, y - 0.25, title, ha='center', va='center',
               fontsize=13, fontweight='bold', color='#333')
        ax.text(input_x + 0.3 + 1.45, y - 0.6, desc, ha='center', va='center',
               fontsize=11, color='#666')
    
    # 中间：融合模块
    fusion_x, fusion_y = 5, 2.5
    fusion_w, fusion_h = 3, 3
    fill, border = colors['融合']
    
    rect = mpatches.FancyBboxPatch((fusion_x, fusion_y), fusion_w, fusion_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        facecolor=fill, edgecolor=border, linewidth=2)
    ax.add_patch(rect)
    ax.text(fusion_x + fusion_w/2, fusion_y + fusion_h - 0.3, 'Cross-Modal',
           ha='center', va='top', fontsize=14, fontweight='bold', color=border)
    ax.text(fusion_x + fusion_w/2, fusion_y + fusion_h/2, '跨模态\n注意力机制',
           ha='center', va='center', fontsize=15, color='#333')
    
    # 箭头：输入 → 融合
    for i in range(3):
        y = input_y + input_h - 1.5 - i * 1.5 - 0.35
        ax.annotate('', xy=(fusion_x, fusion_y + fusion_h/2), 
                   xytext=(input_x + input_w, y),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
    
    # 输出模块
    output_x, output_y = 9, 3
    output_w, output_h = 2.5, 2
    fill, border = colors['输出']
    
    rect = mpatches.FancyBboxPatch((output_x, output_y), output_w, output_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        facecolor=fill, edgecolor=border, linewidth=2)
    ax.add_patch(rect)
    ax.text(output_x + output_w/2, output_y + output_h/2, '融合\n特征向量',
           ha='center', va='center', fontsize=14, fontweight='bold', color='#333')
    
    # 箭头：融合 → 输出
    ax.annotate('', xy=(output_x, output_y + output_h/2), 
               xytext=(fusion_x + fusion_w, fusion_y + fusion_h/2),
               arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    
    ax.text(6, 7.7, '多模态融合示意图', ha='center', va='center',
           fontsize=18, fontweight='bold', color='#333')
    plt.savefig(f'{OUTPUT_DIR}/图表2-多模态融合示意图.png', dpi=300, bbox_inches='tight',
               facecolor='white')
    plt.close()
    print('✅ 图表2-多模态融合示意图.png 已生成')


def chart_business_model():
    """
    图表3: 商业模式图
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    colors = {
        'saas': ('#e3f2fd', '#1976d2'),
        '增值': ('#e8f5e9', '#388e3c'),
        '求职': ('#fff3e0', '#f57c00'),
    }
    
    # 标题
    ax.text(7, 9.5, '智面星途 商业模式', ha='center', va='center',
           fontsize=20, fontweight='bold', color='#333')
    
    # 三个维度 - 调整位置使排列均匀
    dimensions = [
        {
            'title': '第一维度：SaaS订阅（主营收）',
            'color': 'saas',
            'x': 0.5, 'y': 1, 'w': 4, 'h': 7.8,
            'items': [
                '按年订阅，按面试次数分档',
                '基础版：¥2万/年\n（3000次面试）',
                '专业版：¥5万/年\n（10000次+高级分析）',
                '企业版：¥8万+/年\n（无限次数+定制化）',
                '毛利率：70%+',
            ]
        },
        {
            'title': '第二维度：增值服务',
            'color': '增值',
            'x': 5, 'y': 1, 'w': 4, 'h': 7.8,
            'items': [
                '评测维度定制：\n根据企业岗位特点\n定制评估模型',
                '题库定制：\n行业专属面试题库',
                '数据报告：\n招聘数据分析与\n人才洞察报告',
                '定价：项目制\n¥2-10万/项目',
            ]
        },
        {
            'title': '第三维度：求职者端（未来）',
            'color': '求职',
            'x': 9.5, 'y': 1, 'w': 4, 'h': 7.8,
            'items': [
                '模拟面试训练：\n求职者付费练习',
                '能力提升课程：\n与培训机构合作分成',
                '定价：\n¥99-299/次模拟面试',
            ]
        },
    ]
    
    for dim in dimensions:
        fill, border = colors[dim['color']]
        n_items = len(dim['items'])
        
        # 大框
        rect = mpatches.FancyBboxPatch(
            (dim['x'], dim['y']), dim['w'], dim['h'],
            boxstyle="round,pad=0.05,rounding_size=0.2",
            facecolor=fill, edgecolor=border, linewidth=2.5)
        ax.add_patch(rect)
        
        # 标题
        ax.text(dim['x'] + dim['w']/2, dim['y'] + dim['h'] - 0.4, dim['title'],
               ha='center', va='top', fontsize=13, fontweight='bold', color=border)
        
        # 计算子项高度和间距，使其均匀分布
        content_start_y = dim['y'] + dim['h'] - 1.2  # 标题下方
        content_end_y = dim['y'] + 0.3  # 底部留边
        total_content_height = content_start_y - content_end_y
        item_h = min(1.4, (total_content_height - 0.2 * (n_items - 1)) / n_items)
        gap = (total_content_height - item_h * n_items) / max(1, n_items - 1) if n_items > 1 else 0
        
        for i, item in enumerate(dim['items']):
            y_top = content_start_y - i * (item_h + gap)
            item_rect = mpatches.FancyBboxPatch(
                (dim['x'] + 0.2, y_top - item_h), dim['w'] - 0.4, item_h,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor='white', edgecolor=border, linewidth=1.5)
            ax.add_patch(item_rect)
            ax.text(dim['x'] + dim['w']/2, y_top - item_h/2, item,
                   ha='center', va='center', fontsize=12, color='#333')
    
    plt.savefig(f'{OUTPUT_DIR}/图表3-商业模式图.png', dpi=300, bbox_inches='tight',
               facecolor='white')
    plt.close()
    print('✅ 图表3-商业模式图.png 已生成')


def chart_team_structure():
    """
    图表4: 团队架构图
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    colors = {
        'PM': ('#ffeb3b', '#f57f17'),
        '技术': ('#e3f2fd', '#1976d2'),
        'BP': ('#e8f5e9', '#388e3c'),
        '呈现': ('#fce4ec', '#c2185b'),
    }
    
    # 标题
    ax.text(7, 9.7, '团队架构图', ha='center', va='center',
           fontsize=20, fontweight='bold', color='#333')
    
    # 项目总负责人
    pm_x, pm_y = 5.5, 8
    pm_w, pm_h = 3, 1.2
    fill, border = colors['PM']
    rect = mpatches.FancyBboxPatch((pm_x, pm_y), pm_w, pm_h,
        boxstyle="round,pad=0.05,rounding_size=0.2",
        facecolor=fill, edgecolor=border, linewidth=3)
    ax.add_patch(rect)
    ax.text(pm_x + pm_w/2, pm_y + pm_h/2, '项目总负责人\n（呈现组组长）',
           ha='center', va='center', fontsize=14, fontweight='bold', color='#333')
    
    # 三个组
    groups = [
        {'name': '技术组', 'sub': '（4人）', 'color': '技术', 'x': 1,
         'members': ['技术组长', '前端工程师', '后端工程师', '算法工程师']},
        {'name': '商业计划组', 'sub': '（4人）', 'color': 'BP', 'x': 5.5,
         'members': ['BP主笔', '市场分析师', '财务分析师', '商业文案']},
        {'name': '呈现组', 'sub': '（4人）', 'color': '呈现', 'x': 10,
         'members': ['主讲人', '视觉设计师', '演示设计师', '答辩支持']},
    ]
    
    group_y = 5.5
    group_w, group_h = 3, 1.2
    
    for group in groups:
        fill, border = colors[group['color']]
        
        # 组框
        rect = mpatches.FancyBboxPatch((group['x'], group_y), group_w, group_h,
            boxstyle="round,pad=0.05,rounding_size=0.2",
            facecolor=fill, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(group['x'] + group_w/2, group_y + group_h/2,
               f"{group['name']}\n{group['sub']}",
               ha='center', va='center', fontsize=13, fontweight='bold', color='#333')
        
        # 从PM到组的箭头
        ax.annotate('', xy=(group['x'] + group_w/2, group_y + group_h),
                   xytext=(pm_x + pm_w/2, pm_y),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=2))
        
        # 成员详情框
        detail_y = 0.5
        detail_h = 4.5
        detail_rect = mpatches.FancyBboxPatch((group['x'], detail_y), group_w, detail_h,
            boxstyle="round,pad=0.05,rounding_size=0.2",
            facecolor=fill, edgecolor=border, linewidth=2, alpha=0.5)
        ax.add_patch(detail_rect)
        
        # 成员
        for i, member in enumerate(group['members']):
            y = detail_y + detail_h - 0.6 - i * 1.0
            member_rect = mpatches.FancyBboxPatch(
                (group['x'] + 0.2, y - 0.7), group_w - 0.4, 0.8,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor='white', edgecolor=border, linewidth=1.5)
            ax.add_patch(member_rect)
            ax.text(group['x'] + group_w/2, y - 0.3, member,
                   ha='center', va='center', fontsize=12, color='#333')
        
        # 从组到详情的箭头
        ax.annotate('', xy=(group['x'] + group_w/2, detail_y + detail_h),
                   xytext=(group['x'] + group_w/2, group_y),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
    
    plt.savefig(f'{OUTPUT_DIR}/图表4-团队架构图.png', dpi=300, bbox_inches='tight',
               facecolor='white')
    plt.close()
    print('✅ 图表4-团队架构图.png 已生成')


def chart_roadmap():
    """
    图表5: 发展路线图
    """
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # 颜色
    phase_colors = [
        ('#e3f2fd', '#1976d2'),  # MVP验证期
        ('#e8f5e9', '#388e3c'),  # 产品打磨期
        ('#fff3e0', '#f57c00'),  # 规模扩张期
    ]
    
    # 标题
    ax.text(8, 7.7, '智面星途 发展路线图', ha='center', va='center',
           fontsize=20, fontweight='bold', color='#333')
    
    # 时间轴
    ax.plot([1, 15], [4, 4], color='#666', linewidth=3, zorder=1)
    
    # 三个阶段
    phases = [
        {
            'name': 'MVP验证期',
            'x_start': 1, 'x_end': 5,
            'milestones': [
                ('2025.06', '参赛提交'),
                ('2025.09', 'MVP完成\n终审擂台赛'),
                ('2025.12', '种子客户\n营收¥50万'),
            ]
        },
        {
            'name': '产品打磨期',
            'x_start': 5, 'x_end': 10,
            'milestones': [
                ('2026.06', '50+付费客户\nHR生态合作'),
                ('2026.12', '年营收¥300万'),
            ]
        },
        {
            'name': '规模扩张期',
            'x_start': 10, 'x_end': 15,
            'milestones': [
                ('2027.06', '开放平台\n求职者端上线'),
                ('2027.12', '200+客户\n营收¥1000万'),
            ]
        },
    ]
    
    for i, phase in enumerate(phases):
        fill, border = phase_colors[i]
        
        # 阶段背景
        rect = mpatches.FancyBboxPatch(
            (phase['x_start'], 2), phase['x_end'] - phase['x_start'], 4,
            boxstyle="round,pad=0.05,rounding_size=0.3",
            facecolor=fill, edgecolor=border, linewidth=2, alpha=0.3)
        ax.add_patch(rect)
        
        # 阶段名称
        ax.text((phase['x_start'] + phase['x_end'])/2, 6.5, phase['name'],
               ha='center', va='center', fontsize=16, fontweight='bold', color=border)
        
        # 里程碑
        n_milestones = len(phase['milestones'])
        for j, (date, event) in enumerate(phase['milestones']):
            x = phase['x_start'] + (j + 0.5) * (phase['x_end'] - phase['x_start']) / n_milestones
            
            # 里程碑点
            circle = plt.Circle((x, 4), 0.25, color=border, zorder=3)
            ax.add_patch(circle)
            
            # 日期（上方）
            ax.text(x, 4.6, date, ha='center', va='bottom', fontsize=12,
                   fontweight='bold', color=border)
            
            # 事件（下方）
            ax.text(x, 3.3, event, ha='center', va='top', fontsize=12, color='#333')
    
    plt.savefig(f'{OUTPUT_DIR}/图表5-发展路线图.png', dpi=300, bbox_inches='tight',
               facecolor='white')
    plt.close()
    print('✅ 图表5-发展路线图.png 已生成')


def chart_0_tech_architecture():
    """
    图表1: 技术架构图
    5个业务层横向排列 + 底座在下方
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 颜色定义
    layer_colors = {
        '采集': ('#e3f2fd', '#1976d2'),  # 浅蓝/深蓝
        '分析': ('#e8f5e9', '#388e3c'),  # 浅绿/深绿
        '融合': ('#fff3e0', '#f57c00'),  # 浅橙/深橙
        '评测': ('#fce4ec', '#c2185b'),  # 浅粉/深粉
        '报告': ('#f3e5f5', '#7b1fa2'),  # 浅紫/深紫
        '底座': ('#e0f7fa', '#0097a7'),  # 浅青/深青
    }
    
    # 5个业务层的数据
    layers = [
        {'name': '数据采集层', 'items': ['音视频流', 'WebRTC', '设备检测'], 'color': '采集', 'x': 0.5},
        {'name': '单模态分析层', 'items': ['语音分析', '视觉分析', 'NLP分析'], 'color': '分析', 'x': 3.5},
        {'name': '多模态融合层', 'items': ['时序对齐', '特征融合', '注意力机制'], 'color': '融合', 'x': 6.5},
        {'name': '智能评测层', 'items': ['能力建模', '综合评分', '维度量化'], 'color': '评测', 'x': 9.5},
        {'name': '报告生成层', 'items': ['能力雷达图', '问题定位', '改进建议'], 'color': '报告', 'x': 12.5},
    ]
    
    # 绘制5个业务层
    box_width = 2.5
    box_height = 5.5
    top_y = 9.2
    
    for layer in layers:
        x = layer['x']
        fill_color, border_color = layer_colors[layer['color']]
        
        # 绘制大框
        rect = mpatches.FancyBboxPatch(
            (x, top_y - box_height), box_width, box_height,
            boxstyle="round,pad=0.05,rounding_size=0.2",
            facecolor=fill_color, edgecolor=border_color, linewidth=2.5
        )
        ax.add_patch(rect)
        
        # 层标题
        ax.text(x + box_width/2, top_y - 0.4, layer['name'],
               ha='center', va='top', fontsize=14, fontweight='bold', color=border_color)
        
        # 绘制子项
        item_height = 0.9
        item_width = 2.1
        start_y = top_y - 1.3
        
        for i, item in enumerate(layer['items']):
            item_y = start_y - i * (item_height + 0.3)
            item_rect = mpatches.FancyBboxPatch(
                (x + 0.2, item_y - item_height), item_width, item_height,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor='white', edgecolor=border_color, linewidth=1.5
            )
            ax.add_patch(item_rect)
            ax.text(x + 0.2 + item_width/2, item_y - item_height/2, item,
                   ha='center', va='center', fontsize=13, color='#333')
    
    # 绘制层之间的箭头
    arrow_y = top_y - box_height/2
    for i in range(4):
        x_start = layers[i]['x'] + box_width
        x_end = layers[i+1]['x']
        ax.annotate('', xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=2))
    
    # 绘制底座
    base_y = 0.5
    base_height = 2.2
    base_width = 14.5
    base_x = 0.5
    
    fill_color, border_color = layer_colors['底座']
    base_rect = mpatches.FancyBboxPatch(
        (base_x, base_y), base_width, base_height,
        boxstyle="round,pad=0.05,rounding_size=0.3",
        facecolor=fill_color, edgecolor=border_color, linewidth=3
    )
    ax.add_patch(base_rect)
    
    # 底座标题
    ax.text(base_x + base_width/2, base_y + base_height - 0.35, 
           '讯飞星火大模型能力底座',
           ha='center', va='top', fontsize=16, fontweight='bold', color=border_color)
    
    # 底座子项
    base_items = ['智能追问生成', '内容质量评估', '个性化建议', '面试官人格模拟']
    item_width = 3.0
    item_height = 0.8
    start_x = base_x + 0.8
    item_y = base_y + 0.4
    
    for i, item in enumerate(base_items):
        item_x = start_x + i * (item_width + 0.5)
        item_rect = mpatches.FancyBboxPatch(
            (item_x, item_y), item_width, item_height,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor='white', edgecolor=border_color, linewidth=1.5
        )
        ax.add_patch(item_rect)
        ax.text(item_x + item_width/2, item_y + item_height/2, item,
               ha='center', va='center', fontsize=13, color='#333')
    
    # 绘制赋能虚线箭头（从底座向上）
    for i, layer in enumerate(layers[1:], 1):  # 跳过采集层
        target_x = layer['x'] + box_width/2
        # 虚线箭头
        ax.annotate('', xy=(target_x, top_y - box_height), 
                   xytext=(target_x, base_y + base_height),
                   arrowprops=dict(arrowstyle='->', color=border_color, 
                                 lw=1.5, linestyle='--', alpha=0.7))
    
    # 标题居中
    ax.text(8, 9.7, '智面星途 技术架构图', ha='center', va='center',
           fontsize=20, fontweight='bold', color='#333')
    
    plt.savefig(f'{OUTPUT_DIR}/图表1-技术架构图.png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    plt.close()
    print('✅ 图表1-技术架构图.png 已生成')


def main():
    """主函数：生成所有图表"""
    print('='*50)
    print('智面星途 商业计划书图表生成')
    print('='*50)
    print()
    
    # 生成架构/流程图（原Mermaid图表）
    chart_0_tech_architecture()   # 图表1: 技术架构图
    chart_multimodal_fusion()     # 图表2: 多模态融合示意图
    chart_business_model()        # 图表3: 商业模式图
    chart_team_structure()        # 图表4: 团队架构图
    chart_roadmap()               # 图表5: 发展路线图
    
    # 生成数据图表
    chart_1_market_size()         # 图表6: AI招聘市场规模
    chart_2_survey_enterprise()   # 图表7: 调研企业规模分布
    chart_3_survey_industry()     # 图表8: 调研企业行业分布
    chart_4_pain_points()         # 图表9: 行业痛点数据
    chart_5_competitor_radar()    # 图表10: 竞品对标雷达图
    chart_6_capability_radar()    # 图表11: 能力评测雷达图
    chart_7_financial_projection()# 图表12: 三年财务预测
    chart_8_cost_comparison()     # 图表13: 面试成本对比
    chart_9_efficiency_comparison()# 图表14: 效率提升对比
    chart_10_ltv_cac()            # 图表15: 单位经济模型
    
    print()
    print('='*50)
    print(f'✅ 所有图表已生成，保存在 {OUTPUT_DIR}/ 目录下')
    print('='*50)


if __name__ == '__main__':
    main()
