# Session 2 — Environment Setup Check

Goal: by the end of today's session, you have a real, working local Python
environment for this course — not just today's stack (NumPy/Pandas/SQL), but
the deep learning libraries (PyTorch) you'll need in later modules too — and
you can prove it with a green checkmark on a pull request.

## What you're submitting

You'll fill in a handful of small functions in `exercise_template.py`
(vectorized NumPy, a Pandas groupby/merge, a SQL query, and a PyTorch sanity
check), open a pull request against this repo, and wait for the
**Verify Environment Setup** GitHub Action to pass on it. Then paste your PR
URL into the Blackboard submission before you leave.

No partial credit for effort here — the point is a working environment, and
the check is pass/fail.

---

## 1. Install `uv`

`uv` manages both your Python install and your virtual environment — you don't
need to separately install Python, pip, or conda first.

**macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then close and reopen your terminal, and confirm it worked:
```bash
uv --version
```

## 2. Fork and clone this repo

1. Click **Fork** at the top of this repo's GitHub page (creates your own copy
   under your GitHub account).
2. Clone *your fork* (not this repo directly):
   ```bash
   git clone https://github.com/<your-github-username>/DAIIST-session2-env-check.git
   cd DAIIST-session2-env-check
   ```

## 3. Set up the environment

```bash
uv sync
```

This reads `pyproject.toml` and `.python-version`, downloads Python 3.12 if you
don't already have it, creates a `.venv/` folder, and installs every dependency
(NumPy, Pandas, scikit-learn, PyTorch, etc.) into it. The PyTorch install is
CPU-only, so this should take a couple of minutes, not tens of minutes.

## 4. Open the project in VS Code and select the interpreter

```bash
code .
```

Then: `Cmd/Ctrl+Shift+P` → **Python: Select Interpreter** → pick the one inside
`.venv` (it'll be listed as something like `.venv/bin/python` or show as
"Recommended"). This is what makes VS Code (and its Jupyter extension, if you
use it) actually run your code with the environment you just built, instead of
whatever Python happens to be on your system already.

## 5. Do the exercise

1. Create a folder under `submissions/` named after your **GitHub username**,
   and copy the template into it:
   ```bash
   mkdir -p submissions/<your-github-username>
   cp exercise_template.py submissions/<your-github-username>/exercise.py
   ```
2. Open `submissions/<your-github-username>/exercise.py` and fill in every
   `TODO`. The data you're working with is in `data/sales.csv` (same data also
   loaded into `data/course.db` as a SQLite `sales` table, for the SQL task).
3. Sanity-check your own output by just running the file:
   ```bash
   uv run python submissions/<your-github-username>/exercise.py
   ```
4. Run the actual autograder locally before you push:
   ```bash
   uv run pytest tests/test_exercise.py -v
   ```
   All 6 tests should pass. If something fails, the assertion message tells
   you what was expected vs. what you returned.

## 6. Push and open a pull request

```bash
git checkout -b add-<your-github-username>
git add submissions/<your-github-username>
git commit -m "Add environment check for <your-github-username>"
git push -u origin add-<your-github-username>
```

Then on GitHub, open a pull request from your fork's branch **back to this
repo's `main` branch**. GitHub Actions will automatically run the same
autograder against your submission.

> **First-time contributor note:** GitHub sometimes holds the very first
> workflow run from a new contributor for maintainer approval on public repos.
> If your checks show "Waiting for approval," that's expected — flag it to the
> instructor in the room, it's a one-click approval on their end.

## 7. Submit on Blackboard

Once the **Verify Environment Setup** check shows a green checkmark on your
PR, copy the PR's URL and submit it to the Blackboard assignment for this
session — before the session ends.

---

## Troubleshooting

- **`uv sync` is slow / hangs on torch:** the CPU-only PyTorch wheel is still
  a few hundred MB — this is normal on the first run. Let it finish; it's
  cached after that.
- **VS Code doesn't see my packages:** you selected the wrong interpreter in
  step 4, or ran `uv sync` in a different folder than the one VS Code has
  open. Re-check both.
- **`git push` fails / permission denied:** make sure your `origin` remote
  points at *your fork*, not this repo — check with `git remote -v`.
- **My PR's check is failing but the script "looks right":** re-run
  `uv run pytest tests/test_exercise.py -v` locally and read the specific
  assertion that failed — it tells you exactly which function and what value
  it expected.
