# 智面星途 商业计划书图表 - Mermaid代码

> 本文件包含商业计划书中所有流程图、架构图的Mermaid代码。
> 可以在支持Mermaid的Markdown编辑器中预览，或使用 [Mermaid Live Editor](https://mermaid.live/) 在线渲染导出PNG/SVG。

---

## 图表1: 技术架构图

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '16px' }}}%%
block-beta
    columns 5
    
    block:采集层:1
        columns 1
        采集["数据采集层"]
        A1["音视频流"]
        A2["WebRTC"]
        A3["设备检测"]
    end
    
    block:分析层:1
        columns 1
        分析["单模态分析层"]
        B1["语音分析"]
        B2["视觉分析"]
        B3["NLP分析"]
    end
    
    block:融合层:1
        columns 1
        融合["多模态融合层"]
        C1["时序对齐"]
        C2["特征融合"]
        C3["注意力机制"]
    end
    
    block:评测层:1
        columns 1
        评测["智能评测层"]
        D1["能力建模"]
        D2["综合评分"]
        D3["维度量化"]
    end
    
    block:报告层:1
        columns 1
        报告["报告生成层"]
        E1["能力雷达图"]
        E2["问题定位"]
        E3["改进建议"]
    end
    
    采集层 --> 分析层 --> 融合层 --> 评测层 --> 报告层
    
    block:底座:5
        columns 4
        底座标题["讯飞星火大模型能力底座"]
        space
        space
        space
        F1["智能追问"]
        F2["质量评估"]
        F3["个性化建议"]
        F4["人格模拟"]
    end
    
    底座 -- "赋能" --> 分析层
    底座 -- "赋能" --> 融合层
    底座 -- "赋能" --> 评测层
    底座 -- "赋能" --> 报告层

    style 采集层 fill:#e3f2fd,stroke:#1976d2
    style 分析层 fill:#e8f5e9,stroke:#388e3c
    style 融合层 fill:#fff3e0,stroke:#f57c00
    style 评测层 fill:#fce4ec,stroke:#c2185b
    style 报告层 fill:#f3e5f5,stroke:#7b1fa2
    style 底座 fill:#e0f7fa,stroke:#0097a7
```

### 备选方案（flowchart简化版）

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '18px' }}}%%
flowchart LR
    subgraph 采集层["📥 数据采集层"]
        A1[音视频流]
        A2[WebRTC]
        A3[设备检测]
    end
    
    subgraph 分析层["🔍 单模态分析层"]
        B1[语音分析]
        B2[视觉分析]
        B3[NLP分析]
    end
    
    subgraph 融合层["🧠 多模态融合层"]
        C1[时序对齐]
        C2[特征融合]
        C3[注意力机制]
    end
    
    subgraph 评测层["📊 智能评测层"]
        D1[能力建模]
        D2[综合评分]
        D3[维度量化]
    end
    
    subgraph 报告层["📋 报告生成层"]
        E1[能力雷达图]
        E2[问题定位]
        E3[改进建议]
    end
    
    采集层 --> 分析层 --> 融合层 --> 评测层 --> 报告层
    
    style 采集层 fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style 分析层 fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style 融合层 fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style 评测层 fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    style 报告层 fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

**讯飞星火大模型能力底座**（单独展示）:
- 智能追问生成 | 内容质量评估 | 个性化建议 | 面试官人格模拟
- 为上述所有层提供 AI 能力支撑

---

## 图表2: 多模态融合示意图

```mermaid
flowchart LR
    subgraph 输入["多模态输入"]
        S1["🎤 语音特征<br/>语速/语调/情感"]
        S2["👁️ 视觉特征<br/>微表情/肢体语言"]
        S3["📝 文本特征<br/>内容/逻辑/专业度"]
    end
    
    subgraph 融合["Cross-Modal Attention"]
        CA["跨模态<br/>注意力机制"]
    end
    
    subgraph 输出["融合输出"]
        O1["融合特征向量"]
    end
    
    S1 --> CA
    S2 --> CA
    S3 --> CA
    CA --> O1
    
    subgraph 关联挖掘["关联挖掘示例"]
        E1["说'很有信心'时眼神闪躲<br/>→ 可能言不由衷"]
        E2["语速加快 + 微表情紧张<br/>→ 敏感话题"]
        E3["内容专业 + 表达流畅 + 姿态自然<br/>→ 高匹配度候选人"]
    end
    
    O1 --> 关联挖掘
    
    style 输入 fill:#e3f2fd,stroke:#1976d2
    style 融合 fill:#fff3e0,stroke:#f57c00
    style 输出 fill:#e8f5e9,stroke:#388e3c
    style 关联挖掘 fill:#fce4ec,stroke:#c2185b
```

---

## 图表3: 商业模式图

```mermaid
flowchart TB
    subgraph 智面星途商业模式["智面星途 商业模式"]
        direction TB
        
        subgraph SaaS["第一维度：SaaS订阅（主营收）"]
            S1["按年订阅，按面试次数分档"]
            S2["基础版：¥2万/年（3000次面试）"]
            S3["专业版：¥5万/年（10000次面试+高级分析）"]
            S4["企业版：¥8万+/年（无限次数+定制化）"]
            S5["毛利率：70%+"]
        end
        
        subgraph 增值["第二维度：增值服务"]
            V1["评测维度定制：根据企业岗位特点定制评估模型"]
            V2["题库定制：行业专属面试题库"]
            V3["数据报告：招聘数据分析与人才洞察报告"]
            V4["定价：项目制，¥2-10万/项目"]
        end
        
        subgraph 求职者["第三维度：求职者端（未来拓展）"]
            C1["模拟面试训练：求职者付费练习"]
            C2["能力提升课程：与培训机构合作分成"]
            C3["定价：¥99-299/次模拟面试"]
        end
    end
    
    style SaaS fill:#e3f2fd,stroke:#1976d2
    style 增值 fill:#e8f5e9,stroke:#388e3c
    style 求职者 fill:#fff3e0,stroke:#f57c00
```

---

## 图表4: 团队架构图

```mermaid
flowchart TB
    PM["项目总负责人<br/>（呈现组组长）"]
    
    PM --> Tech["技术组<br/>（4人）"]
    PM --> BP["商业计划组<br/>（4人）"]
    PM --> Show["呈现组<br/>（4人）"]
    
    subgraph 技术组详情["技术组"]
        T1["技术组长"]
        T2["前端工程师"]
        T3["后端工程师"]
        T4["算法工程师"]
    end
    
    subgraph 商业计划组详情["商业计划组"]
        B1["BP主笔"]
        B2["市场分析师"]
        B3["财务分析师"]
        B4["商业文案"]
    end
    
    subgraph 呈现组详情["呈现组"]
        S1["主讲人"]
        S2["视觉设计师"]
        S3["演示设计师"]
        S4["答辩支持"]
    end
    
    Tech --> 技术组详情
    BP --> 商业计划组详情
    Show --> 呈现组详情
    
    style PM fill:#ffeb3b,stroke:#f57f17,stroke-width:2px
    style Tech fill:#e3f2fd,stroke:#1976d2
    style BP fill:#e8f5e9,stroke:#388e3c
    style Show fill:#fce4ec,stroke:#c2185b
```

---

## 图表5: 发展路线图

```mermaid
gantt
    title 智面星途 发展路线图
    dateFormat  YYYY-MM
    axisFormat  %Y-%m
    
    section MVP验证期
    参赛提交           :milestone, m1, 2025-06, 0d
    MVP开发            :a1, 2025-06, 3M
    MVP完成/终审擂台赛  :milestone, m2, 2025-09, 0d
    种子客户获取        :a2, 2025-09, 3M
    首年营收¥50万      :milestone, m3, 2025-12, 0d
    
    section 产品打磨期
    产品迭代优化        :b1, 2026-01, 6M
    50+付费客户        :milestone, m4, 2026-06, 0d
    HR生态合作接入      :b2, 2026-06, 6M
    年营收¥300万       :milestone, m5, 2026-12, 0d
    
    section 规模扩张期
    开放平台建设        :c1, 2027-01, 6M
    求职者端上线        :c2, 2027-06, 6M
    200+客户/营收¥1000万 :milestone, m6, 2027-12, 0d
```

### 时间线版本（备选）

```mermaid
timeline
    title 智面星途 发展路线图
    
    2025.06 : 参赛提交
    2025.09 : MVP完成 : 终审擂台赛
    2025.12 : 种子客户 : 首年营收¥50万
    2026.06 : 50+付费客户 : HR生态合作
    2026.12 : 年营收¥300万
    2027.12 : 开放平台上线 : 求职者端上线 : 营收¥1000万
```

---

## 使用说明

### 方法一：VS Code 预览
1. 安装 VS Code 扩展：`Markdown Preview Mermaid Support`
2. 打开此文件，按 `Ctrl+Shift+V` 预览

### 方法二：在线渲染
1. 访问 [Mermaid Live Editor](https://mermaid.live/)
2. 复制上方任意 Mermaid 代码块
3. 粘贴到编辑器左侧
4. 右侧实时预览，可导出 PNG/SVG

### 方法三：命令行导出
```bash
# 安装 mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# 导出为PNG
mmdc -i mermaid_charts.md -o output.png
```

---

## 配色说明

| 组件 | 颜色 | 含义 |
|------|------|------|
| 蓝色系 | `#e3f2fd` | 技术/数据相关 |
| 绿色系 | `#e8f5e9` | 分析/增长相关 |
| 橙色系 | `#fff3e0` | 核心/融合相关 |
| 粉色系 | `#fce4ec` | 评测/呈现相关 |
| 紫色系 | `#f3e5f5` | 输出/报告相关 |
| 青色系 | `#e0f7fa` | 底层能力/支撑 |

