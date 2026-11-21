# musk-perspective（马斯克 · 认知操作系统）

> *"The only rules you have to follow are the laws of physics — everything else is a recommendation."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)

蒸馏 Elon Musk 的认知操作系统。**不是语录合集，是可运行的思维框架。**

基于 Isaacson 授权传记、30+ 小时长播客（Rogan/Lex Fridman/Everyday Astronaut）、X/Twitter、SEC 文件、法庭证词等 40+ 一手来源，提炼 **7 个核心心智模型**（每个通过三重验证：跨≥2领域复现 + 可推断新立场 + 明确排他性）、**10 条决策启发式**（附来源故事）、完整**表达DNA** 与 **5-Phase 回答工作流**。

v3.0 同时提供「15个思维模型」科普清单 → 可执行模块的映射表，兼顾入门索引与实战操作。

## 目录结构

```
musk-perspective/
├── SKILL.md                 # 主文件：触发词工程 + 7模型 + 工作流 + 表达DNA（AI 加载此文件）
├── references/
│   ├── cases.md             # 7个模型的跨域复现详案 + 生成力迁移案例
│   ├── heuristics.md        # 10条启发式的来源故事
│   ├── fallback.md          # 失败模式 Fallback 树 + 反例黑名单
│   └── research/            # 上游调研文档（思想体系/决策模式/即兴思考）
├── examples/
│   └── demo-conversation.md # 标准响应模式示例（SaaS成本/失败重建/职业选择）
└── evals/
    └── trigger-tests.md     # 触发词命中 + 15模型映射 + 表达DNA 回归测试
```

## 安装

**镜像**：国内用户可从 Gitee 镜像获取：[gitee.com/showhar-law/musk-perspective](https://gitee.com/showhar-law/musk-perspective)

**Skills Hub（推荐，多平台同步）**：在 Skills Hub 中「从 Git/本地安装」，勾选目标工具（Claude Code / Codex / Cursor / OpenCode / Hermes 等 46 个适配器），中央库一份、各平台 junction 同步。

**手动**：把本目录放入你的 Agent skills 目录（如 `~/.claude/skills/musk-perspective/`）。

## 触发示例

- 「用马斯克的视角看看这个方案」
- 「这个成本合理吗？白痴指数是多少？」
- 「从第一性原理想想」「五步算法」「要不要垂直整合」

**退出**：说「退出」「切回正常」即恢复正常模式。

## 融合与致谢

v3.0 融合了 [alchaincyf/elon-musk-skill](https://github.com/alchaincyf/elon-musk-skill)（MIT License, Copyright (c) 2026 Huashu/花叔）的触发词工程、EXIT 机制、问题分类路由、存在主义锚定模型、快速迭代模型、Fallback 树与调研文档；保留并增强了本机版的三重验证框架、跨域复现证据、生成力案例、失效条件与来源故事。

## 免责声明

本 Skill 基于公开信息提炼的思维框架，非马斯克本人观点。输出不构成投资、法律或工程安全建议。时间线类预估请自行乘以 2-3 倍系数。
