# Changelog

## [Unreleased] — 2026-11-21

Copied six already-published mentor skills into the tree. The SKILL text was not rewritten. `skills/strategy/zhangxuefeng/` was not edited. No CLI, no release, and no claim that all ten named people have a file.

### Added

- `skills/finance/naval/` from [carollefkowitr0-a11y/NavalSKILL](https://github.com/carollefkowitr0-a11y/NavalSKILL) at `b7d6ccbc` (MIT)
- `skills/finance/buffett/` from [will2025btc/buffett-perspective](https://github.com/will2025btc/buffett-perspective) at `e18afcfc` (MIT)
- `skills/finance/duanyongping/` from [anneheartrecord/duanyongping-perspective](https://github.com/anneheartrecord/duanyongping-perspective) at `2f3f6ef9` (MIT)
- `skills/finance/trump/` from [yangbuyiya/trump-perspective-skill](https://github.com/yangbuyiya/trump-perspective-skill) at `2ec37980` (MIT). CBO seat.
- `skills/media/dan-koe/` from [Elimek/dan-koe-perspective](https://github.com/Elimek/dan-koe-perspective) at `37200c45` (MIT)
- `skills/innovation/elon-musk/` from [showharLaw/musk-perspective](https://github.com/showharLaw/musk-perspective) at `ac1d22ed` (MIT)

Each copied folder keeps the upstream license and adds `SOURCE.md`.

### Not added

- Lidangzzz. [Elimek/lidangzzz-perspective](https://github.com/Elimek/lidangzzz-perspective) at `5c73de06` has a `SKILL.md`, and the README says "MIT", but `LICENSE` is the 14-byte text `404: Not Found`.
- Bryan Johnson and Andrew Huberman. No licensed single-skill distillation was copied.
- The short stub files from tag `v2.2.0`.
- `carollefkowitr0-a11y/naval-ravikant-perspective` (no license file).

## [Unreleased] — 2026-11-20

Documentation and a free checklist. No new mentor skill, no CLI, and no tests added to make an old claim true.

### Corrected

The public docs described a repository this tree does not contain.

| What the docs said | What is true |
| --- | --- |
| Mentor SKILL library complete; 9 executable SKILLs | One published SKILL: `skills/strategy/zhangxuefeng/` (Zhang Xuefeng) |
| CLI `opc.sh` | Not in the repo |
| `scripts/test-harness.sh`, `quality-harness.sh`, 43/43 tests | Not in the repo |
| Three cron jobs | Not in the repo |
| `checklist/daily-routine.md` and `checklist/financial-review.md` | Not in the repo |
| Quick start on branch `main`, folder `/docs` | Branch is `master`. Pages source is the repository root |
| Canonical URL `https://opc-board.is-a.dev` | Live demo is https://elimek.github.io/opc-board. The custom domain is Issue #4 and is not active |
| Issue #7 fixes shipped (Naval stance table, engineering-only Musk) | Issue #7 is still open. Those skill files are not in this repo |
| "Zhang Xuedong" in the changelog, site, and Pages config | The name is Zhang Xuefeng (张雪峰) |
| A decision passes only if all 10 seats score ≥ 6 | Removed from the landing page. The owner decides. Scores are not raised so the row looks unanimous |

### Added

- `checklist/weekly-board-meeting.md`
- `checklist/weekly-board-meeting.html` (same checklist, opened in a browser; nothing is submitted)

## [1.0.0] — 2026-05-21

The bullets that used to live here listed a CLI, nine SKILLs, checklist templates, cron jobs, and a 43-test harness. Those paths are not in the public tree at `7efafbb` (pushed 2026-06-10). Read the 2026-11-20 correction above instead of treating that list as files you can open.

What that era still accounts for on `master`:

- A static landing page and static dashboard HTML
- GitHub Pages with no backend in the repo
- Commit `7efafbb` (2026-06-09) adding `skills/strategy/zhangxuefeng/`

The strategy seat in the old notes was spelled Zhang Xuedong. The name is Zhang Xuefeng.
