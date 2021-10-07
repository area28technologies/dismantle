import shutil
from pathlib import Path
import pytest


@pytest.fixture(scope='function')
def datadir(tmpdir, request):
    """Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = Path(request.module.__file__)
    test_dir = Path(filename.parent, 'data', filename.stem)

    if test_dir.is_dir():
        shutil.rmtree(str(tmpdir), ignore_errors=True)
        shutil.copytree(test_dir, str(tmpdir))

    return tmpdir


@pytest.fixture(scope="session")
def httpserver_listen_address():
    """Use port 9090 for testing."""
    return ("127.0.0.1", 9090)
