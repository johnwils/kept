from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "fixtures" / "sample"


@pytest.fixture
def sample_dir() -> Path:
    return SAMPLE
