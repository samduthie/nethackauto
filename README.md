# nhbot

A rule-based NetHack auto-player on the NetHack Learning Environment (NLE).
The design and the plan are in `docs/nethack-bot-brief.txt`. The rules for the code are in `CLAUDE.md`.

## Set up (Linux or macOS, Python 3.11 or later)

```
git clone https://github.com/samduthie/nethackauto && cd nethackauto
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

If pip has no NLE wheel for your system, it builds NLE from source. That needs `cmake` and a C compiler.

## Play

```
.venv/bin/nhbot --seed 3 --steps 1000           # headless: prints one summary line
.venv/bin/nhbot --seed 3 --watch --delay 0.1    # watch the game in the terminal
```

Keys in watch mode: space pauses or resumes, `.` plays one step, `+` and `-` change the speed,
ctrl-c stops. The terminal must be at least 112 columns wide.

The same seed plays the same game each time.

Each run writes its files to `runs/<date>-<time>-seed<N>/`: `events.jsonl` (what happened) and one
`bundle-<NN>-<incident>.jsonl` for each incident (death, stall or crash) with the last 50 screens.
The first time that a new prompt or message appears, one sample of the screen goes to `samples/`.
