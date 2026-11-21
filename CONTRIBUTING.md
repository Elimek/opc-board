# Contributing

OPC Board is a one-person company. Pull requests are welcome. Please describe the repository that exists, not the one older docs imagined.

## What you can open today

Published mentor skills are the directories under `skills/` that contain a `SKILL.md`. Zhang Xuefeng's directory is the format reference and was not rewritten when the other files were copied: [`skills/strategy/zhangxuefeng/`](skills/strategy/zhangxuefeng/). Copied skills keep their upstream license and a `SOURCE.md`. A name with no `SKILL.md` is not distilled.

There is no `scripts/test-harness.sh` and no `quality-harness.sh`. Do not add a commit that claims "43 tests passed."

## Add a mentor skill

1. Read `skills/strategy/zhangxuefeng/` before inventing a new layout.
2. Add `skills/<category>/<name>/SKILL.md` with a stance a person can follow, at least one counter-option, the evidence you used, and a confidence level.
3. A skill is complete only when criticism materials are included, sealed test items are kept out of the runtime package, and a fidelity check against a bare model has been done before you call it complete.
4. Until that bar is met, say the seat is not yet distilled. A name on the landing page is not a vote.
5. Open a pull request against `master`.

## Improve the published skill

Corrections to Zhang Xuefeng's file are in scope: a missing decision rule, a bad quote, a clearer limit. Do not paste a new celebrity into the page and call the library finished.

## Bugs and ideas

Open a [GitHub Issue](https://github.com/Elimek/opc-board/issues/new).

## Style

- Markdown with YAML frontmatter for a SKILL.
- Every line should tell the reader what to do, or what not to do.
- Vague lines ("consider", "适当配置", "可以考虑") are not a finished answer.
- The owner decides. Do not add a rule that the board passes only when every seat scores 6 or higher.

## License

MIT.
