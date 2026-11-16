# GoblinScript language notes

GoblinScript is an experimental beginner-friendly language. Programs use the `.gob` extension and run with Python 3.

```sh
python goblin.py examples/hello.gob
```

## Commands

- `say "hello"` — print text.
- `set score = 10` — create a variable.
- `add score 5` / `take score 2` — change a number.
- `repeat 3 ... end` — repeat a block (0–1000 times).
- `if score > 10 ... else ... end` — conditional block.
- `roll 20` — random number from 1 to 20.
- `flip` — coin flip.
- `show` — show variables.
- `# comment` — ignored line.

Expressions support numbers, strings, variable names, + - * / %, comparisons, and/or/not. No Python eval, imports, file access, or system commands are exposed to GoblinScript programs.

This is a tiny v0.1 language, not a production programming language. The interpreter is intentionally small and safe to experiment with.
