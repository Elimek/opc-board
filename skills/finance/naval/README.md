# NavalSKILL — Naval Ravikant Perspective / 纳瓦尔视角

> **中文一句话**：这是一个基于 Naval Ravikant 公开思想材料整理出来的 AI Skill，用来帮助你用“财富、杠杆、特定知识、长期游戏、内在自由”的框架思考问题。
> **English in one sentence**: This is an AI skill based on public Naval Ravikant materials. It helps you think through wealth, leverage, specific knowledge, long-term games, and inner freedom.

**Version / 版本**: v3.0.0

---

## 1. 这是什么？ / What is this?

### 中文

NavalSKILL 是一个可以复制到 AI Agent 里的 Markdown Skill。你可以把它理解成一份“思考说明书”：当你问职业、创业、财富、地位、欲望、长期选择时，AI 会尝试用 Naval Ravikant 风格的框架来回答。

它不是 Naval 本人，也不代表 Naval 当前观点。它是基于公开资料和研究提炼出来的“视角模拟”。

### English

NavalSKILL is a Markdown skill that you can give to an AI agent. Think of it as an instruction manual for a specific way of thinking. When you ask about career, startups, wealth, status, desire, or long-term choices, the AI can answer through a Naval Ravikant-style framework.

It is not Naval Ravikant himself. It does not represent his current personal views. It is a perspective simulation based on public materials and research synthesis.

---

## 2. v3 更新了什么？ / What changed in v3?

### 中文

v3 在 v2 短答体验之上，补了**可运行的失败路径与检查点**（达尔文式结构加固）：

- 新增 **Step 2.5 失败模式 if-then 表**：工具失败 / 来源冲突 / 主体含糊 / 处方请求 / 空结果 / 危机 / 低资源 / 退出。
- 展开模式增加 **🔴 CHECKPOINT**（进入前 + 发出前）与 **🛑 STOP**（危机与具体投资/医疗/法律处方）。
- 快速运行卡强制「查失败表」，禁止假装已核验。
- 固化 `test-prompts.json`（默认短答 / 展开 / 危机 / 未核验）便于回归。
- 来源摘要去掉硬编码本机绝对路径。
- 本地回归（skill 约束模拟）：6/6 PASS，危机题与未核验题通过；**不是** Naval 本人，也不是实时 Telegram 全量会话日志。

### English

v3 keeps the short-oracle UX from v2 and adds **runnable failure paths and checkpoints** (structure hardening):

- **Step 2.5 failure if-then table**: tool failure / conflicting sources / vague subject / prescription requests / empty results / crisis / low-resource / exit.
- Expand mode **🔴 CHECKPOINT** (before enter + before send) and **🛑 STOP** (crisis; investment / medical / legal prescriptions).
- Quick-run card forces the failure table; never pretend facts were verified.
- Ships `test-prompts.json` for short / expand / crisis / unverified regression cases.
- Source notes no longer hard-code machine absolute paths.
- Local regression under skill constraints: 6/6 PASS including crisis and unverified paths. **Not** Naval the person, and **not** a full live Telegram multi-turn log.

v2 回顾 / v2 recap：默认更短、默认 vs 展开分离、当前事实先查再判。

---

## 3. 适合谁？ / Who is this for?

### 中文

适合你，如果你想用 AI 帮你思考：

- 我该不该离职、创业、做独立开发？
- 我现在追求的是财富、钱，还是地位？
- 我的特定知识（specific knowledge）是什么？
- 我有没有杠杆，还是只是在出售时间？
- 这个选择能不能长期复利？
- 我是不是被欲望、头衔、身份焦虑牵着走？

### English

Use this if you want an AI to help you think about:

- Should I quit, start a company, or become an indie hacker?
- Am I chasing wealth, money, or status?
- What is my specific knowledge?
- Do I have leverage, or am I only selling time?
- Can this choice compound over the long term?
- Am I being driven by desire, titles, identity, or status anxiety?

---

## 4. 3 分钟快速开始 / 3-minute quick start

### 方法 A：不懂命令行也能用 / Method A: No command line needed

1. 打开 `SKILL.md`。
2. 全选复制里面的内容。
3. 粘贴到你的 AI Agent、聊天工具、项目说明或自定义指令里。
4. 再问一个问题，例如：

```text
用 Naval 视角回答：我该不该离职做独立开发？
```

English:

1. Open `SKILL.md`.
2. Copy all the text.
3. Paste it into your AI agent, chat tool, project instructions, or custom instructions.
4. Ask a question like:

```text
Use the Naval skill to answer: should I quit my job to build an indie product?
```

### 方法 B：用 Git 下载 / Method B: Download with Git

如果你懂一点命令行，可以运行：

```bash
git clone https://github.com/carollefkowitr0-a11y/NavalSKILL.git
cd NavalSKILL
```

What this does:

- `git clone` downloads this repo.
- `cd NavalSKILL` enters the downloaded folder.

然后把 `SKILL.md` 放进你使用的 Agent 工具里，或者在提问时附上它。

Then add `SKILL.md` to your agent tool, or attach/paste it when you ask questions.

---

## 5. 默认短答 vs 展开模式 / Short mode vs expanded mode

### 中文

这个 Skill 默认**非常短**。

默认效果通常是：

```text
别先问离职。先问你有没有能复利的资产。
```

如果你想要详细教学，必须明确说：

```text
请详细展开，用 Naval Skill 教我分析：我现在追求的是财富、钱，还是地位？
```

触发展开模式的词包括：`展开`、`详细讲`、`举例`、`给框架`、`一步步`、`teach`、`explain in detail`、`examples`、`framework`。

### English

This skill is **very short by default**.

A default answer may look like this:

```text
Do not ask whether to quit first. Ask whether you already have an asset that can compound.
```

If you want a detailed explanation, ask clearly:

```text
Explain in detail using the Naval skill: am I chasing wealth, money, or status?
```

Words that trigger expanded mode include: `expand`, `explain in detail`, `teach`, `examples`, `framework`, `step by step`, `详细讲`, `展开`, `举例`.

---

## 6. 在不同 Agent 里怎么用？ / How to use it in different agents

> 不同工具的菜单和版本会变化。下面只写稳妥方法，不编造未验证的具体按钮。
> Tool menus and versions change. The steps below use safe general methods instead of unverified exact UI paths.

### 6.1 Hermes Agent

#### 中文

如果你使用 Hermes Agent：

1. 把本仓库放到 Hermes skills 目录，或把 `SKILL.md` 复制成一个 Hermes skill。
2. 在对话里明确触发：

```text
用 naval-ravikant-perspective 这个 skill 回答：我该不该继续做这份工作？
```

也可以说：

```text
用 Naval 视角回答：我现在是在积累资产，还是只是在卖时间？
```

如果问题涉及当前事实，例如公司、市场、价格、政策、新闻，Hermes 应该先使用工具查资料，再用 Naval 框架分析。

#### English

If you use Hermes Agent:

1. Put this repo in your Hermes skills folder, or copy `SKILL.md` as a Hermes skill.
2. Trigger it clearly in chat:

```text
Use the naval-ravikant-perspective skill to answer: should I stay in this job?
```

Or:

```text
Use the Naval perspective: am I building assets, or only selling time?
```

If your question depends on current facts, such as a company, market, price, policy, or news event, Hermes should research first and then apply the Naval framework.

---

### 6.2 Claude Code

#### 中文

Claude Code 主要是编码 Agent，但也可以读取项目文件和说明。简单用法：

1. 把 `SKILL.md` 放进你的项目，例如：

```text
.claude/skills/naval-ravikant-perspective.md
```

或直接让 Claude Code 读取这个仓库里的 `SKILL.md`。

2. 在提示词里写：

```text
Read SKILL.md. When I ask for "Naval perspective", follow that skill. Now answer: should I quit my job to build an indie product?
```

注意：不要把 API key、密码、私人资料一起粘贴进去。

#### English

Claude Code is mainly a coding agent, but it can also read project files and instructions. Simple method:

1. Put `SKILL.md` in your project, for example:

```text
.claude/skills/naval-ravikant-perspective.md
```

Or ask Claude Code to read the `SKILL.md` in this repo.

2. Use this prompt:

```text
Read SKILL.md. When I ask for "Naval perspective", follow that skill. Now answer: should I quit my job to build an indie product?
```

Do not paste API keys, passwords, or private secrets into the context.

---

### 6.3 Codex / coding-agent style tools

#### 中文

Codex 这类工具通常更偏代码任务。如果你想让它使用这个 Skill，可以把 `SKILL.md` 当成上下文文件：

```text
Read SKILL.md and use it as the behavior guide. Use the Naval skill to analyze this product idea: [paste your idea here]
```

如果你的 Codex 环境没有长期记忆，每次新会话都需要重新附上或引用 `SKILL.md`。

#### English

Codex-style tools usually focus on coding. To use this skill, treat `SKILL.md` as a context file:

```text
Read SKILL.md and use it as the behavior guide. Use the Naval skill to analyze this product idea: [paste your idea here]
```

If your Codex environment has no persistent memory, attach or reference `SKILL.md` again in each new session.

---

### 6.4 OpenClaw / OpenCode-like agents

#### 中文

OpenClaw、OpenCode-like Agent、其他本地/开源 Agent 的设置方式可能不同。稳妥方法是：

1. 如果工具支持 custom instructions / system prompt / memory file，把 `SKILL.md` 内容放进去。
2. 如果工具支持项目说明文件，把 `SKILL.md` 放在项目根目录，并要求 Agent 先读它。
3. 如果都不支持，就在每次提问前粘贴这个简短触发块：

```text
请使用我提供的 NavalSKILL 行为方式回答。默认极短；只有我明确说“展开/详细讲/举例/teach/explain in detail”时才详细说明。不要声称你是 Naval 本人。涉及当前事实时先查证。

问题：我该不该离职做独立开发？
```

#### English

OpenClaw, OpenCode-like agents, and other local/open-source agents may use different settings. Safe general method:

1. If the tool supports custom instructions, system prompts, or memory files, put the content of `SKILL.md` there.
2. If the tool supports project instruction files, put `SKILL.md` in the project root and ask the agent to read it first.
3. If neither exists, paste this compact trigger before your question:

```text
Use the NavalSKILL behavior I provide. Default to extremely short answers. Only explain in detail when I explicitly say "expand", "explain in detail", "teach", "examples", or "framework". Do not claim to be Naval Ravikant. If the question depends on current facts, verify them first.

Question: should I quit my job to build an indie product?
```

---

### 6.5 通用 AI Agent / Generic AI agents

#### 中文

如果你不知道自己的工具属于哪一类，就用最简单的方法：复制 `SKILL.md`，然后粘贴这句话：

```text
请把上面的 SKILL.md 当作你的回答规则。之后当我说“Naval 视角”或“Naval Skill”时，请按这个 Skill 回答。
```

测试是否生效：

```text
用 Naval 视角回答：什么是财富？
```

预期风格应该很短，例如：

```text
财富不是钱。财富是睡觉时还工作的资产。
```

#### English

If you do not know what kind of tool you use, use the simplest method: copy `SKILL.md`, then paste this:

```text
Treat the SKILL.md above as your behavior guide. When I say "Naval perspective" or "Naval Skill", answer according to this skill.
```

Test it:

```text
Use the Naval perspective: what is wealth?
```

The expected style should be short, for example:

```text
Wealth is not money. Wealth is assets that work while you sleep.
```

---

## 7. 示例提示词 / Example prompts

### 中文短答

```text
用 Naval 视角回答：我该不该离职做独立开发？
```

```text
纳瓦尔怎么看财富和工资的区别？
```

```text
用纳瓦尔视角帮我做一次欲望审计：我为什么总想换更高头衔？
```

### 中文展开

```text
请详细展开，用 Naval Skill 教我分析：我现在追求的是财富、钱，还是地位？
```

```text
用 Naval 框架一步步分析：这个创业想法有没有 specific knowledge 和 leverage？
```

### English short mode

```text
Use the Naval skill to answer: should I quit my job to build an indie product?
```

```text
Use the Naval perspective: what is the difference between wealth and salary?
```

```text
Use the Naval perspective to audit this desire: why do I keep wanting a higher title?
```

### English expanded mode

```text
Explain in detail using the Naval skill: am I chasing wealth, money, or status?
```

```text
Use the Naval framework step by step: does this startup idea have specific knowledge and leverage?
```

---

## 8. 好提示词 vs 坏提示词 / Good prompts vs bad prompts

### 中文

好提示词：

```text
用 Naval 视角回答：这份工作给我的是资产、技能复利，还是只是工资？
```

坏提示词：

```text
让我一年内必赚一百万。
```

为什么不好：这个 Skill 不保证财富结果，也不做投机承诺。

### English

Good prompt:

```text
Use the Naval perspective: does this job give me assets, compounding skills, or only salary?
```

Bad prompt:

```text
Make me earn one million dollars this year.
```

Why it is bad: this skill does not guarantee wealth outcomes or make speculative promises.

---

## 9. 不能做什么？ / What it cannot do

### 中文

这个 Skill 不适合：

- 个性化投资建议。
- 法律建议。
- 医疗或心理治疗。
- 保证创业、职业或财富结果。
- 不查资料就判断当前公司、市场、价格、政策、新闻。
- 用“个人选择”去责备贫困、创伤、抑郁或结构性限制中的人。

Naval 风格短答是一种压缩视角，不是普适真理。

### English

This skill is not for:

- Personalized investment advice.
- Legal advice.
- Medical or mental-health treatment.
- Guaranteed startup, career, or wealth outcomes.
- Claims about current companies, markets, prices, policies, or news without checking sources.
- Blaming people in poverty, trauma, depression, or structural constraint as if everything is just personal choice.

A Naval-style short answer is a compressed perspective, not universal truth.

---

## 10. 常见问题排查 / Troubleshooting

### 10.1 回答太普通，不像 Naval / The answer feels generic

原因：Agent 没有读到 `SKILL.md`，或你没有明确触发。

修复：

```text
请先阅读 SKILL.md，然后用 Naval 视角回答。默认短答，不要写鸡汤。
```

English fix:

```text
Read SKILL.md first, then answer using the Naval perspective. Default to a short answer. Do not give generic self-help advice.
```

### 10.2 回答太长 / The answer is too long

修复：

```text
按 NavalSKILL 默认模式回答，只给一句话。
```

English fix:

```text
Use the default NavalSKILL mode. Give me only one sentence.
```

### 10.3 回答太短 / The answer is too short

修复：

```text
请展开，给我框架、例子和边界。
```

English fix:

```text
Please expand. Give me the framework, examples, and boundaries.
```

### 10.4 Agent 说“我不能扮演 Naval” / The agent refuses to be Naval

这是正常边界。你不需要让它声称自己是 Naval。你可以说：

```text
不要扮演本人。请基于 NavalSKILL，用公开资料提炼出的 Naval 视角回答。
```

English:

```text
Do not pretend to be Naval himself. Use the NavalSKILL framework based on public materials.
```

### 10.5 新会话里忘了 Skill / The agent forgot the skill in a new chat

原因：很多 Agent 没有长期记忆。

修复：重新附上 `SKILL.md`，或把它保存到工具的 custom instructions / memory / skills 目录。

English: attach `SKILL.md` again, or save it into your tool's custom instructions, memory, or skills folder.

### 10.6 我用的工具没写在这里 / My tool is not listed here

用通用方法：把 `SKILL.md` 作为系统提示词、项目说明、记忆文件或普通上下文提供给 Agent。

English: use the generic method. Give `SKILL.md` to the agent as a system prompt, project instruction, memory file, or normal context.

---

## 11. 仓库文件说明 / Files in this repo

- `SKILL.md` — main skill definition / 主 Skill 文件。
- `test-prompts.json` — regression prompts (short / expand / crisis / unverified) / 回归题集。
- `references/` — research and extraction references / 调研与提炼参考资料。
- `scripts/quality_check.py` — content quality gate / 内容质量检查。
- `scripts/validate_skill_package.py` — package structure gate / 包结构检查。
- `CHANGELOG.md` — release history / 版本记录。
- `LICENSE` — license file / 许可证。

---

## 12. 本地验证 / Local validation

如果你下载了仓库，可以运行：

```bash
python3 scripts/quality_check.py SKILL.md
python3 scripts/validate_skill_package.py
```

Expected result / 预期结果：

```text
结果: 6/6 通过
🎉 全部通过，可以交付
PASS: package structure OK
```

---

## 13. License / 许可证

See `LICENSE`.

---

## 14. Final note / 最后说明

### 中文

这个 Skill 最好的使用方式不是“问它怎么暴富”，而是用它检查：我是不是在卖时间？我有没有特定知识？我有没有杠杆？这个选择能不能复利？我是在追求财富，还是地位？

### English

The best use of this skill is not asking how to get rich quickly. Use it to check: Am I selling time? Do I have specific knowledge? Do I have leverage? Can this compound? Am I chasing wealth, or status?
