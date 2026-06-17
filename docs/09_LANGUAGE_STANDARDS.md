# Language Standards Baseline

CairnDev uses established language standards as the baseline for code style,
formatting, and idioms. It does not define a custom house style unless a project
has a documented reason to narrow the default.

## Policy

- Follow the target language's official or widely adopted style guide first.
- Run the project's configured formatter, linter, and type checker when present.
- Add local rules only when they protect architecture, reliability, security, or
  platform boundaries that generic language tools do not cover.
- Keep production declarations at module/package level unless the language,
  framework, or encapsulation need clearly justifies local scope.
- Local test doubles may live inside a single test function when they are tiny,
  single-use, and clearer than a shared fixture.

## Reference Baselines

| Language area | Baseline references |
|---|---|
| Python | [PEP 8](https://peps.python.org/pep-0008/), [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), [Ruff](https://docs.astral.sh/ruff/) |
| TypeScript/JavaScript | [TypeScript Documentation](https://www.typescriptlang.org/docs/) plus project ESLint/Prettier config |
| Go | [Effective Go](https://go.dev/doc/effective_go) plus `gofmt`/`go vet` |
| Java | [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) |
| Swift | [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/) |
| Rust | [Rust learning and tooling references](https://www.rust-lang.org/learn) plus `rustfmt`/`clippy` |

## Review Notes

For Python specifically, a class inside a function is acceptable for a narrow
test-local fake or fixture. In production modules, prefer top-level classes and
functions so public boundaries, type checking, documentation, and reuse remain
clear.
