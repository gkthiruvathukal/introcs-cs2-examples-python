from collections import Counter
import sys

import pytest


def pytest_collection_finish(session):
    groups = Counter(item.nodeid.split("::", 1)[0] for item in session.items)
    terminal = session.config.pluginmanager.get_plugin("terminalreporter")

    if not terminal or not groups:
        return

    terminal.write_sep("=", "test groups")
    for path, count in sorted(groups.items()):
        terminal.write_line(f"{path}: {count} tests")


@pytest.fixture
def temporary_recursion_limit():
    original_limit = sys.getrecursionlimit()

    def set_limit(limit):
        sys.setrecursionlimit(limit)

    yield set_limit
    sys.setrecursionlimit(original_limit)
