import shutil
import subprocess

import pytest

from src.config.config import BASE_DIR


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_ruff_raises_no_warnings():
    exit_code = subprocess.call([shutil.which("ruff"), "check", str(BASE_DIR)])  # noqa: S603
    assert exit_code == 0
