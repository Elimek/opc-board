# Contributing

OPC Board is a one-person company, but contributions are welcome.

## Ways to Contribute

### Add a New Advisor Skill
1. Study the existing skills in `skills/` for format reference
2. Create `skills/<category>/<name>.md` with:
   - YAML frontmatter (name, description, trigger conditions)
   - 3-6 core mental models
   - Decision heuristics table
   - Expression DNA
   - Anti-patterns and honest boundaries
3. Add your skill to the category README.md
4. Submit a PR

### Improve Existing Skills
- Found a missing mental model? Open an issue or PR.
- Know a better expression of a principle? Edit the file.
- Translations welcome.

### Bug Reports & Feature Requests
Open a [GitHub Issue](https://github.com/Elimek/opc-board/issues/new).

## Style Guide
- Skills are markdown files with YAML frontmatter
- Use emoji prefixes for sections
- Keep it executable — every principle should answer "what do I DO with this?"
- No fluff. Every sentence should either teach or guide.

## Running Tests
```bash
bash scripts/test-harness.sh
```
43 tests should all pass.

## License
MIT — do whatever you want.
