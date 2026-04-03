# Contributing to Revolve

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/eisen0419/revolve
   cd revolve
   ```

2. Run setup wizard to configure your local environment:
   ```
   /revolve-setup
   ```

3. Install Python dev dependencies:
   ```bash
   pip install pytest
   ```

## Project Structure

```
revolve/
├── .claude-plugin/       # Plugin manifest
├── skills/               # Claude Code skills
│   ├── revolve-setup/
│   ├── research-pipeline/
│   ├── evolve-claude-md/
│   └── yt-search/
├── scripts/              # Python sync scripts
├── templates/            # Obsidian templates
├── docs/                 # Documentation
└── config.md.example     # Config template
```

## Contribution Guidelines

### Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md`
2. Follow the existing SKILL.md format
3. Add skill path to `.claude-plugin/plugin.json`
4. Document in README.md and README_CN.md

### Modifying Existing Skills

- Test changes with `/revolve-setup` fresh install
- Ensure paths remain parameterized (no hardcoding)
- Update CHANGELOG.md

### Pull Request Checklist

- [ ] No hardcoded user-specific paths
- [ ] `config.md.example` updated if new config fields added
- [ ] `docs/config-contract.md` updated if config schema changed
- [ ] CHANGELOG.md entry added
- [ ] README.md and README_CN.md updated if user-facing changes
- [ ] Python scripts pass `python3 -m py_compile`

## Commit Message Format

```
<type>(scope): <summary>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:
- `feat(research-pipeline): add PDF file support`
- `fix(evolve-claude-md): handle missing vault path gracefully`
- `docs: update installation steps`

## Reporting Issues

Please include:
- OS and Claude Code version
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs from `~/.config/revolve/sync.log` if applicable

## License

By contributing, you agree your contributions will be licensed under MIT.
