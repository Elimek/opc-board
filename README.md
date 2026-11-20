# OPC Board — Your One-Person Company Operating System

> _"The next employee you want to hire doesn't have to be a person. Hire the world's best minds."_

A public notebook for running a one-person company: a landing page, one published mentor skill, and a free weekly checklist.

**What is in this repository**

- One published mentor SKILL: [`skills/strategy/zhangxuefeng/`](skills/strategy/zhangxuefeng/) (张雪峰 / Zhang Xuefeng, CSO, strategy).
- A landing page (`index.html`) and static HTML under `dashboard/`. Those pages are not a live vote.
- Saved meeting JSON under `meetings/`.
- A free weekly checklist: [`checklist/weekly-board-meeting.md`](checklist/weekly-board-meeting.md). The same page in a browser: [`checklist/weekly-board-meeting.html`](checklist/weekly-board-meeting.html).

Other seats are names. They have no SKILL file here, and a seat with no published SKILL does not vote.

Live site: <https://elimek.github.io/opc-board> — GitHub Pages from branch `master`, source directory `/` (the repository root).

---

## 董事会席位

| 角色 | 名字 | 这个仓库里 |
|------|------|------------|
| 💼 CFO | Naval · 巴菲特 · 段永平 | 未蒸馏，不能投票 |
| 🏢 CBO | Trump | 未蒸馏，不能投票 |
| 🧬 CHO | Bryan Johnson · Huberman | 未蒸馏，不能投票 |
| 📱 CMO | Dan Koe | 未蒸馏，不能投票 |
| ⚡ COO | Lidangzzz | 未蒸馏，不能投票 |
| 🚀 CVO | Elon Musk | 未蒸馏，不能投票 |
| 🎯 CSO | 张雪峰 (Zhang Xuefeng) | **已发布** [`skills/strategy/zhangxuefeng/`](skills/strategy/zhangxuefeng/) |

## 快速启动

```bash
git clone https://github.com/Elimek/opc-board.git
cd opc-board
```

GitHub Pages:

1. Settings → Pages
2. Branch: **`master`** (this repo has no `main` branch)
3. Folder: **`/ (root)`**. There is no `/docs` directory.
4. The site that is actually up is <https://elimek.github.io/opc-board>

Open locally with any browser: `index.html`, or `checklist/weekly-board-meeting.html`. No install, no API key, no account.

## 项目结构（与当前树一致）

```
opc-board/
├── index.html
├── _config.yml
├── checklist/
│   ├── weekly-board-meeting.md
│   └── weekly-board-meeting.html
├── skills/strategy/zhangxuefeng/   # the only published SKILL
├── dashboard/                      # static HTML, not a skill runtime
├── meetings/                       # saved meeting JSON
├── assets/css/style.css
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── CICD.md
```

这些路径**不在**这个仓库里。旧 README 写过它们，按那个路径打开是 404：

- `opc.sh`，以及任何 CLI
- `scripts/`（含 `scripts/test-harness.sh`、`quality-harness.sh`）
- `skills/finance/`、`skills/health/`、`skills/media/`、`skills/innovation/`
- `skills/_meta/integration.md`
- `checklist/daily-routine.md`、`checklist/financial-review.md`
- cron，以及「43/43 测试」

不要为了让旧 changelog 读起来成立，再把这些文件补回来。

## 怎么用

每周填 [`checklist/weekly-board-meeting.md`](checklist/weekly-board-meeting.md)。可以打印，可以复制。没有付费 API，没有后端。

### 董事会怎么算数

- **你做决定。** 席位提供材料，不代替你。
- **没有发布 SKILL 的席位不能当投票。** 页面上有名字，不等于有意见。
- **已发布的 SKILL 必须给出：** 一个立场、至少一个反方案、证据、以及置信度。含糊的「可以考虑」不算说完。
- **不要为了好看把分数改到全员 6 分以上。** 低分留下。没有「全部 ≥ 6 才通过」这条规则。

### 以后一份 SKILL 怎样才算完成

批评材料要在；密封测试题不放进运行包；标成完成之前，先和一个裸模型比过一次保真度。现在只有张雪峰这一份算已发布。

### 决策时写下的五个滤镜

1. **复利。** 这件事一年后还在滚吗？
2. **健康。** 它会不会吃掉睡眠、身体或注意力？
3. **内容。** 过程能不能变成可以发布的东西？
4. **第一性原理。** 去掉行业习惯之后，这件事还成立吗？
5. **生存边界。** 这是在赌房租、饭钱，还是一条签证时间线？

## 路线图

- [x] 仓库和落地页
- [x] GitHub Pages（`master`，仓库根目录）
- [x] 张雪峰 SKILL
- [x] 免费每周董事会清单
- [ ] 导师 SKILL 库（未完成。其余席位都还没有文件）
- [ ] CLI（仓库里没有 `opc.sh`，没有「下一版 CLI」）

邮件订阅、周报、暗色模式、自定义域名、付费 Notion 包都还是开放的 Issue，没有做进这个仓库。见 [ROADMAP.md](ROADMAP.md)。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增席位时，请按上面的完成定义来，不要只加一段名人语录。

## License

MIT。

## Live

[https://elimek.github.io/opc-board](https://elimek.github.io/opc-board)

*一个人做决定。一个已发布的席位。一份每周清单。*
