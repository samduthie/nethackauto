# NetHack bot - read this first

## Repository
- `nethack/`: the NetHack auto-player (Python). All new work is here.
- The root (`nq2-autoplayer.user.js`, `tests/`, `tools/`): the old NeoQuest II bot (JavaScript).
  Do not change it for NetHack work. The rules below are for `nethack/` only.
- The full brief: `nethack/docs/nethack-bot-brief.txt`. Read only the sections that the task needs.

## What it is
A rule-based NetHack player on NLE (the NetHack Learning Environment), with an AI in the improvement loop.
The bot plays and records data. The AI reads the records, fixes the code and adds a test.
Targets: M1 depth 5. M2 Minetown or depth 10. M3 Sokoban. (Brief section 1.2.)
Two views of the same loop: watch mode (draws the game in the terminal) and headless mode (fast batches).

## Language
Simplified Technical English (ASD-STE100) in docs, comments, commit messages and log text.
Short sentences. Simple words. One instruction in each sentence.

## Code rules

### Design
- Object-based. Each job is a class.
- One class per file. The file name is the class name in snake_case: `MapParser` is in `map_parser.py`.
- SOLID:
  - Single responsibility: a class does one job. It has one reason to change.
  - Open/closed: add a behaviour with a new class (for example, a new skill). Do not add to a long if/elif chain.
  - Liskov substitution: each implementation of a Protocol works in all places that use the Protocol.
  - Interface segregation: keep Protocols small. A class depends only on the methods that it uses.
  - Dependency inversion: a class gets its dependencies in `__init__`. It does not make them.
    No global state. No module-level singletons.
- DRY: each fact has one source. Game data is in data files. Constants are in one place.
  Shared test setup is in fixtures.
- Tight and isolated: a package uses another package only through its public classes.
  Only `adapter/` imports `nle`. All other code uses our own types (`Observation`, `Action`).
- A file of more than about 200 lines is a sign to split the class.

### Style
- Terse and simple. Short methods (target: less than 15 lines). Early return. No clever code.
- Clear names: `hero_position`, `down_stairs`, `hunger_state`. Not `st`, `w`, `tmp`, `obj2`.
  Short names only for `x`, `y` and loop indices.
- Type hints on all functions. `@dataclass(frozen=True)` for values.
- Each file starts with a docstring of 1 to 3 lines: what the class does, its inputs, its outputs.
- Comments say why, not what. A constant that is a guess has its source: `# source: wiki`, `# source: guess`.
- No dead code. No commented-out code.

### Tests
- pytest. One test file for each class: `tests/<package>/test_<module>.py`.
- One assert per test.
- The test name says the behaviour: `test_finds_down_stairs_when_visible`. Never a version name.
- Shared setup is in fixtures (`conftest.py`). Do not copy setup between tests.
- Unit tests do not start NLE. They use golden files (recorded observations) or a fake adapter.
  Only the adapter tests and the seeded game runs use NLE.
- Each bug fix gets a test made from its incident bundle (incident to test).

## Glossary
Use these names in code and in talk, so that a search finds them. Definitions: brief section 3.
agent-facing telemetry, flight recorder, golden files, record and replay, verify after act, shadow mode,
persistent world model, priors, coverage search, versioned state migrations, checked assumptions, incident to test.

## Module map (planned, `nethack/src/nhbot/`)
- `adapter/`: the only code that talks to NLE. Makes `Observation` objects. Sends `Action` objects.
- `perceive/`: parsers. Screen to facts: map, messages, status, inventory, menus and prompts.
- `world/`: the persistent world model. Levels, the dungeon graph, item knowledge, monsters.
- `nav/`: pathfinding, exploration, coverage search, search for hidden doors.
- `tactics/`: fights. Attack, flee, Elbereth, items in a fight, ranged attacks.
- `survival/`: hunger, eating, prayer, healing, status problems.
- `items_logic/`: pick up, wear, wield, identify, price-identify, drop.
- `strategy/`: goals and stages. The current goal and the next action toward it.
- `act/`: the action executor. Sends keys, answers prompts, handles "--More--", then verify after act.
- `telemetry/`: event log (JSON lines), flight recorder, checked assumptions report.
- `replay/`: loads a recorded game or bundle and runs the decisions again.
- `view/`: watch mode. Draws the screen and a side panel. It only reads; it never changes a decision.

## Facts checked (2026-10-13: NLE 1.3.0, Python 3.13, Linux)
- `pip install nle` works with no build step.
- Use `NetHackScore-v0` or `NetHack-v0` with a high `max_episode_steps`. `NetHackChallenge-v0` does not accept seeds.
- `env.unwrapped.seed(core, disp, False)` gives the same game two times.
- `character="val-dwa-law-fem"` starts a dwarvish Valkyrie.
- Observation keys: `blstats`, `chars`, `colors`, `glyphs`, `inv_glyphs`, `inv_letters`, `inv_oclasses`, `inv_strs`,
  `message`, `misc`, `specials`, `tty_chars`, `tty_colors`, `tty_cursor`.
- NLE alone does about 10,000 steps per second. The bot logic is the slow part.
- `nle.nethack.permonst(i)` gives the monster table (381 monsters): level, speed, AC, MR, resistances, flags.
  It does not give attacks. `nle.nethack.objclass(i)` gives the object table (453 objects).
- NetHack reads the real date (moon phase, Friday the 13th, night). A replay on another day can be different.
  Not solved yet.

## Platforms
Linux and macOS. Windows only with WSL. Python 3.11 or later.

## Commands (planned; tasks T1 and T2 make them)
Run from `nethack/`:
```
run one game:     python -m nhbot.main --seed N
watch one game:   python -m nhbot.main --seed N --watch
run a batch:      python -m nhbot.batch --seeds 1-20
tests:            pytest -q
lint and types:   ruff check . && mypy src
reports:          python tools/run_report.py runs/<game>/events.jsonl
                  python tools/incident_report.py runs/<game>/bundle_<n>/
```

## Work rules
- Read tool output before raw data.
- One module per task when possible.
- Observe first (shadow mode), then write code. Do not write code from a guess about a screen.
- Each new guess goes into the checked assumptions list (`telemetry/`), with a name and a status.
- Each rule in `data/rules/` has a source.
- Before a push: tests, ruff and mypy pass. Re-read the diff.
- A commit message says what changed and why, in STE.
  For a change that should help: write the metric before and after, on the same seeds.
