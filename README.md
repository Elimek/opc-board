# OPC Board — Your One-Person Company Operating System

> _"The next employee you want to hire doesn't have to be a person. Hire the world's best minds."_

A public notebook for running a one-person company: a landing page, mentor SKILL files for seven named people, and a free weekly checklist. Three named people still have no SKILL file here.

**What is in this repository**

A seat counts as published when its `SKILL.md` is in this tree. Published does not mean a completeness check was run, and it does not mean the seat votes for you.

- CSO 张雪峰 / Zhang Xuefeng — [`skills/strategy/zhangxuefeng/`](skills/strategy/zhangxuefeng/). Already here. Those files were not changed.
- CFO Naval Ravikant — [`skills/finance/naval/`](skills/finance/naval/). Copied from [carollefkowitr0-a11y/NavalSKILL](https://github.com/carollefkowitr0-a11y/NavalSKILL) (MIT).
- CFO Warren Buffett — [`skills/finance/buffett/`](skills/finance/buffett/). Copied from [will2025btc/buffett-perspective](https://github.com/will2025btc/buffett-perspective) (MIT).
- CFO 段永平 / Duan Yongping — [`skills/finance/duanyongping/`](skills/finance/duanyongping/). Copied from [anneheartrecord/duanyongping-perspective](https://github.com/anneheartrecord/duanyongping-perspective) (MIT).
- CBO Donald Trump — [`skills/finance/trump/`](skills/finance/trump/). Copied from [yangbuyiya/trump-perspective-skill](https://github.com/yangbuyiya/trump-perspective-skill) (MIT). The seat is CBO. The path is under `skills/finance/` so the copied file has one stable place. It is not a fourth CFO.
- CMO Dan Koe — [`skills/media/dan-koe/`](skills/media/dan-koe/). Copied from [Elimek/dan-koe-perspective](https://github.com/Elimek/dan-koe-perspective) (MIT).
- CVO Elon Musk — [`skills/innovation/elon-musk/`](skills/innovation/elon-musk/). Copied from [showharLaw/musk-perspective](https://github.com/showharLaw/musk-perspective) (MIT).

Each copied folder keeps the upstream license file and a `SOURCE.md` with the repo URL, owner, and commit. The SKILL text was not rewritten.

No SKILL file, so these names do not vote:

- CHO Bryan Johnson and Andrew Huberman. No licensed single-skill distillation was copied.
- COO Lidangzzz. [Elimek/lidangzzz-perspective](https://github.com/Elimek/lidangzzz-perspective) has a `SKILL.md`, and the README there says "MIT", but the `LICENSE` file is the 14-byte text `404: Not Found`. That is not an MIT license, so the files were not copied.

Also here:

- A landing page (`index.html`) and static HTML under `dashboard/`. Those pages are not a live vote.
- Saved meeting JSON under `meetings/`.
- A free weekly checklist: [`checklist/weekly-board-meeting.md`](checklist/weekly-board-meeting.md). The same page in a browser: [`checklist/weekly-board-meeting.html`](checklist/weekly-board-meeting.html).

Live site: <https://elimek.github.io/opc-board> — GitHub Pages from branch `master`, source directory `/` (the repository root).

---

## 董事会席位

| 角色 | 名字 | 这个仓库里 |
|------|------|------------|
| 💼 CFO | Naval Ravikant | **已发布** [`skills/finance/naval/`](skills/finance/naval/) · [NavalSKILL](https://github.com/carollefkowitr0-a11y/NavalSKILL) |
| 💼 CFO | 巴菲特 (Warren Buffett) | **已发布** [`skills/finance/buffett/`](skills/finance/buffett/) · [buffett-perspective](https://github.com/will2025btc/buffett-perspective) |
| 💼 CFO | 段永平 (Duan Yongping) | **已发布** [`skills/finance/duanyongping/`](skills/finance/duanyongping/) · [duanyongping-perspective](https://github.com/anneheartrecord/duanyongping-perspective) |
| 🏢 CBO | Trump | **已发布** [`skills/finance/trump/`](skills/finance/trump/) · [trump-perspective-skill](https://github.com/yangbuyiya/trump-perspective-skill) |
| 🧬 CHO | Bryan Johnson · Huberman | 未蒸馏，不能投票 |
| 📱 CMO | Dan Koe | **已发布** [`skills/media/dan-koe/`](skills/media/dan-koe/) · [dan-koe-perspective](https://github.com/Elimek/dan-koe-perspective) |
| ⚡ COO | Lidangzzz | 未放入。上游 `LICENSE` 不是 MIT，不能投票 |
| 🚀 CVO | Elon Musk | **已发布** [`skills/innovation/elon-musk/`](skills/innovation/elon-musk/) · [musk-perspective](https://github.com/showharLaw/musk-perspective) |
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
├── skills/strategy/zhangxuefeng/     # CSO, already in the repo
├── skills/finance/naval/             # CFO, copied
├── skills/finance/buffett/           # CFO, copied
├── skills/finance/duanyongping/      # CFO, copied
├── skills/finance/trump/             # CBO, copied
├── skills/media/dan-koe/             # CMO, copied
├── skills/innovation/elon-musk/      # CVO, copied
├── dashboard/                        # static HTML, not a skill runtime
├── meetings/                         # saved meeting JSON
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
- `skills/health/`（Bryan Johnson、Huberman）
- `skills/strategy/lidangzzz/`
- `skills/_meta/integration.md`
- `checklist/daily-routine.md`、`checklist/financial-review.md`
- cron，以及「43/43 测试」

不要为了让旧 changelog 读起来成立，再把这些文件补回来。v2.2.0 里的短 stub（例如 `skills/finance/naval.md`）也没有恢复。

## 怎么用

每周填 [`checklist/weekly-board-meeting.md`](checklist/weekly-board-meeting.md)。可以打印，可以复制。没有付费 API，没有后端。

### 董事会怎么算数

- **你做决定。** 席位提供材料，不代替你。
- **没有发布 SKILL 的席位不能当投票。** 页面上有名字，不等于有意见。
- **已发布的 SKILL 必须给出：** 一个立场、至少一个反方案、证据、以及置信度。含糊的「可以考虑」不算说完。
- **不要为了好看把分数改到全员 6 分以上。** 低分留下。没有「全部 ≥ 6 才通过」这条规则。

### 已发布，和「完成」，是两件事

仓库里有 `SKILL.md`，这一席就算已发布。复制进来的文件按上游原样保留，没有在这里重写，也没有在这里做完成度检查。

标成完成之前，批评材料要在；密封测试题不放进运行包；先和一个裸模型比过一次保真度。这次复制没有做这三步。

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
- [x] 另外六份已有许可证的 SKILL 文件（Naval、巴菲特、段永平、Trump、Dan Koe、Elon Musk），从上游原样复制
- [x] 免费每周董事会清单
- [ ] 导师 SKILL 库（未完成。Bryan Johnson、Huberman、Lidangzzz 还没有文件）
- [ ] CLI（仓库里没有 `opc.sh`，没有「下一版 CLI」）

邮件订阅、周报、暗色模式、自定义域名、付费 Notion 包都还是开放的 Issue，没有做进这个仓库。见 [ROADMAP.md](ROADMAP.md)。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新增席位时，请按上面的完成定义来，不要只加一段名人语录。第三方文件要带着上游许可证一起放进来。

## License

这个仓库的许可证是 MIT。每个复制进来的目录另有上游 `LICENSE`（Trump 那份文件名是 `License`）。见该目录里的 `SOURCE.md`。

## Live

[https://elimek.github.io/opc-board](https://elimek.github.io/opc-board)

*一个人做决定。七份 SKILL 文件在仓库里。Bryan Johnson、Huberman、Lidangzzz 没有文件。一份每周清单。*
