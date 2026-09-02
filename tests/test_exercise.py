"""
Autograder for environment-check submissions.

Locates every submissions/<username>/exercise.py file changed on this PR
(diffed against origin/main) and runs the checks below against each of them.
If a diff can't be computed (e.g. running locally on a fresh clone with no
`main` to compare against), falls back to testing every submission found —
which for a student running this locally is just their own single file.
"""

import importlib.util
import math
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
SUBMISSIONS_DIR = ROOT / "submissions"


def _changed_submission_files() -> list[Path]:
    try:
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=ROOT, capture_output=True, timeout=30, check=True,
        )
        diff = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=30, check=True,
        )
        changed = [
            ROOT / line
            for line in diff.stdout.splitlines()
            if line.startswith("submissions/") and line.endswith("/exercise.py")
        ]
        changed = [p for p in changed if p.is_file()]
        if changed:
            return sorted(changed)
    except Exception:
        pass
    return sorted(SUBMISSIONS_DIR.glob("*/exercise.py"))


def _load_submission(path: Path):
    module_name = f"submission_{path.parent.name}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


SUBMISSION_FILES = _changed_submission_files()

if not SUBMISSION_FILES:
    pytest.skip(
        "No submissions/<username>/exercise.py found to test.",
        allow_module_level=True,
    )


@pytest.fixture(params=SUBMISSION_FILES, ids=lambda p: p.parent.name)
def submission(request):
    return _load_submission(request.param)


@pytest.fixture(scope="module")
def sales_df():
    return pd.read_csv(ROOT / "data" / "sales.csv")


@pytest.fixture(scope="module")
def expected_revenue_by_region(sales_df):
    return (
        sales_df.assign(revenue=sales_df["quantity"] * sales_df["unit_price"])
        .groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("region")
        .reset_index(drop=True)
    )


def test_numpy_order_revenues(submission):
    import numpy as np

    quantities = np.array([2, 3, 5])
    unit_prices = np.array([10.0, 4.0, 2.0])
    result = submission.numpy_order_revenues(quantities, unit_prices)
    assert np.allclose(result, [20.0, 12.0, 10.0])


def test_numpy_average_order_value(submission):
    import numpy as np

    quantities = np.array([2, 3, 5])
    unit_prices = np.array([10.0, 4.0, 2.0])
    result = submission.numpy_average_order_value(quantities, unit_prices)
    assert math.isclose(result, 14.0, rel_tol=1e-6)


def test_pandas_revenue_by_region(submission, sales_df, expected_revenue_by_region):
    result = submission.pandas_revenue_by_region(sales_df)
    result_sorted = result.sort_values("region").reset_index(drop=True)
    pd.testing.assert_frame_equal(
        result_sorted[["region", "revenue"]],
        expected_revenue_by_region[["region", "revenue"]],
        check_dtype=False,
    )


def test_pandas_region_share(submission, sales_df):
    result = submission.pandas_region_share(sales_df).sort_values("region").reset_index(drop=True)
    assert {"region", "revenue", "share"}.issubset(result.columns)
    assert math.isclose(result["share"].sum(), 1.0, rel_tol=1e-6)


def test_sql_revenue_by_region(submission, expected_revenue_by_region):
    result = submission.sql_revenue_by_region(ROOT / "data" / "course.db")
    result_sorted = result.sort_values("region").reset_index(drop=True)
    pd.testing.assert_frame_equal(
        result_sorted[["region", "revenue"]],
        expected_revenue_by_region[["region", "revenue"]],
        check_dtype=False,
        check_exact=False,
        rtol=1e-6,
    )


def test_torch_installed(submission):
    result = submission.check_torch_installed()
    assert math.isclose(result, 6.0, rel_tol=1e-6)
