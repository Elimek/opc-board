# OPC Board 🏢 — Your One-Person Company Operating System

> _"The next employee you want to hire doesn't have to be a person. Hire the world's best minds."_

[![GitHub Pages](https://img.shields.io/badge/deploy-GitHub%20Pages-brightgreen)](https://pages.github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![One Person Company](https://img.shields.io/badge/made%20by-solopreneur-blue)](#)

**OPC Board** 是一个开源的、可部署的个人操作系统。它将 Naval、巴菲特、段永平、Bryan Johnson、Dan Koe、张雪峰、马斯克等顶级思想家的认知框架蒸馏成可执行的 SKILL，让你一个人的公司拥有一个完整的董事会。

---

## 🏛️ 董事会成员

| 角色 | 导师 | 核心原则 |
|------|------|----------|
| **💼 Finance CEO** | Naval · 巴菲特 · 段永平 · 特朗普 | 长期复利 + 杠杆 + 诚信 + 品牌放大 |
| **🧬 Health CEO** | Bryan Johnson · Andrew Huberman | 数据驱动优化 + 神经科学协议 |
| **📱 Media CEO** | Dan Koe | 内容 → 品牌 → 产品闭环 |
| **🧠 Strategy Advisor** | 张雪峰 · lidangzzz | ROI 第一 · 现实主义 · 避坑 |
| **🚀 Innovation CEO** | Elon Musk | 第一性原理 · 快速迭代 |

---

## 🚀 快速启动

```bash
# 把你自己的董事会克隆下来
git clone https://github.com/Elimek/opc-board.git
cd opc-board

# 部署到 GitHub Pages（免费）
# 1. 打开 GitHub 仓库 Settings → Pages
# 2. 选择 main 分支 /docs 目录（或者根目录）
# 3. 等待 2 分钟，你的董事会就上线了

# 或者本地直接打开
open index.html
```

## 📁 项目结构

```
opc-board/
├── index.html              # 🏠 Landing Page（GitHub Pages 入口）
├── opc.sh                  # 🖥️ CLI 工具（本地终端里跑董事会）
├── README.md               # 📖 你现在看到的这个
├── _config.yml             # ⚙️ GitHub Pages 配置
├── LICENSE                 # 📜 MIT 许可证
│
├── skills/                 # 📚 导师 SKILL 库
│   ├── _meta/
│   │   └── integration.md  # 🔗 跨导师集成层（核心）
│   ├── finance/            # 💰 Naval · 巴菲特 · 段永平 · 特朗普
│   ├── health/             # 🧬 Bryan Johnson · Huberman
│   ├── media/              # 📱 Dan Koe
│   ├── strategy/           # 🧠 张雪峰 · lidangzzz
│   └── innovation/         # 🚀 Elon Musk
│
├── dashboard/
│   └── index.html          # 🎛️ 交互式 Dashboard（本地打开即可用）
│
├── checklist/              # ✅ 每周/每日执行模板
│   ├── weekly-board-meeting.md
│   ├── daily-routine.md
│   └── financial-review.md
│
├── assets/                 # 🎨 静态资源
│   └── css/
│       └── style.css
│
└── scripts/                # 🔧 自动化脚本
    ├── setup.sh
    └── deploy.sh
```

---

## 🎯 如何使用 OPC Board

### 模式一：每周董事会会议（推荐）

你作为 CEO，每周花 30-60 分钟召开董事会。每个导师针对你当前的决策给出意见：

```
┌─────────────────────────────────────────────────────┐
│  📋 本周议题: 应该全职做独立开发还是先拿 offer？       │
├─────────────────────────────────────────────────────┤
│                                                      │
│  💼 Finance CEO (段永平):                             │
│  "现金流是企业的生命线。先有稳定收入，再用业余时间      │
│   验证产品。段永平说'不懂不做'，你验证过了吗？"        │
│                                                      │
│  📱 Media CEO (Dan Koe):                             │
│  "你不需要二选一。白天工作积累素材，晚上写内容。       │
│   你的内容就是你的产品原型。"                          │
│                                                      │
│  🧠 Strategy (张雪峰):                               │
│  "普通人家孩子，先拿 offer 保底。香港房租贵，          │
│   别拿生存去赌。拿 offer 同时搞副业，这性价比最高。"    │
│                                                      │
│  🚀 Innovation (马斯克):                             │
│  "周末用 48 小时做个 MVP。验证不了的需求不值得放弃      │
│   一个 offer。"                                       │
└─────────────────────────────────────────────────────┘
```

### 模式二：每日 OS 运行

```
🌅 早晨（Huberman Protocol）
    ├── 看自然光 10 分钟
    ├── 延迟咖啡因 90 分钟
    └── 晨间专注块 60 分钟

💻 白天（Dan Koe 深工作）
    ├── 内容创作 2 小时
    ├── 产品开发 2 小时
    └── 学习/调研 1 小时

🌙 晚上（复盘）
    ├── 日记：今天学了什么
    ├── 追踪：健康数据记录
    └── 计划：明天的 3 个 MIT（Most Important Tasks）
```

### 模式三：决策过滤器

做任何重大决定前，过一遍这五个滤镜：

1. **💼 Finance Filter** (Naval/巴菲特): 这个决定有复利吗？能加杠杆吗？
2. **🧬 Health Filter** (Bryan): 这会损害我的长期健康吗？
3. **📱 Media Filter** (Dan Koe): 我能从中产出内容吗？
4. **🧠 Strategy Filter** (张雪峰): 普通人的 ROI 如何？风险可控吗？
5. **🚀 Innovation Filter** (马斯克): 第一性原理看，这是最优解吗？

---

## 🧠 核心哲学

这个项目诞生于一个简单的问题：

> *如果我能把世界上最聪明的人装进一个系统，让他们为我的决策提供建议，会发生什么？*

这就是 **OPC Board**。

它不是名人语录合集。每个导师的 SKILL 都包含：
- **心智模型**（他们的认知框架）
- **决策启发式**（他们怎么做判断）
- **表达 DNA**（他们怎么说话）
- **反模式**（他们绝对不会做的事）
- **诚实边界**（这个 SKILL 不能做什么）

---

## 🛣️ 路线图

- [x] 项目骨架搭建
- [x] 导师 SKILL 库
- [x] GitHub Pages 部署
- [ ] 交互式董事会 WebUI
- [ ] CLI 工具（终端里开董事会）
- [ ] AI Agent 集成（自动调用导师视角）
- [ ] 付费模板包（Notion 模板 + 复盘系统）
- [ ] 社区版（多人共享董事会）

---

## 🤝 贡献

这是一个人公司项目，但欢迎 PR！
- 新增导师 SKILL
- 改进现有 SKILL 的质量
- 翻译成其他语言
- 提 Issue 分享你的使用案例

---

## 📄 License

MIT — 随便用，随便改，随便赚钱。  
但记得：**健康第一，别透支**。—— Bryan Johnson

---

## 🌐 Live Demo

👉 [opc-board.elimek.com](https://opc-board.elimek.com)

---

*一个人，一个董事会，一个操作系统。*
