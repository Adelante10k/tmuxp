"""Tests for .'s helper and utility functions."""
import pytest

from libtmux.server import Server
from libtmux.test import get_test_session_name, temp_session


def test_kills_session(server: Server) -> None:
    server = server
    session_name = get_test_session_name(server=server)

    with temp_session(server=server, session_name=session_name):
        result = server.has_session(session_name)
        assert result

    assert not server.has_session(session_name)


@pytest.mark.flaky(reruns=5)
def test_if_session_killed_before(server: Server) -> None:
    """Handles situation where session already closed within context"""

    server = server
    session_name = get_test_session_name(server=server)

    with temp_session(server=server, session_name=session_name):

        # an error or an exception within a temp_session kills the session
        server.kill_session(session_name)

        result = server.has_session(session_name)
        assert not result

    # really dead?
    assert not server.has_session(session_name)
