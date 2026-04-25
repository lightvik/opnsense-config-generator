from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).parent
SNAPSHOTS_DIR = TESTS_DIR / "snapshots"
GOLDEN_DIR = TESTS_DIR / "golden"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-snapshots",
        action="store_true",
        default=False,
        help="Regenerate snapshot / golden files instead of comparing",
    )


@pytest.fixture
def update_snapshots(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption("--update-snapshots"))
