"""Explicit transaction composition for conditional recovery; no external worker."""

from contextlib import closing

import pytest

from hermes_cli import kanban_db as kb
from hermes_cli.kanban_db_connect import connect


def test_conditional_block_savepoint_rolls_back_with_owner():
    with closing(connect()) as conn:
        task_id = kb.create_task(conn, title="conditional recovery")
        task = kb.claim_task(conn, task_id)
        with pytest.raises(RuntimeError, match="outer abort"):
            with kb.write_txn(conn):
                current = kb.get_task(conn, task_id)
                assert current.current_run_id == task.current_run_id
                assert kb.block_task(conn, task_id, kind="needs_input", reason="abandoned",
                                     expected_run_id=current.current_run_id, allow_nested=True)
                raise RuntimeError("outer abort")
        assert kb.get_task(conn, task_id).status == "running"
        assert kb.get_run(conn, task.current_run_id).status == "running"
        assert not any(e.kind == "blocked" for e in kb.list_events(conn, task_id))
        with kb.write_txn(conn):
            assert kb.block_task(conn, task_id, kind="needs_input", reason="abandoned",
                                 expected_run_id=task.current_run_id, allow_nested=True)
        assert kb.get_task(conn, task_id).status == "blocked"
        assert kb.get_run(conn, task.current_run_id).outcome == "blocked"


def test_block_still_refuses_implicit_nested_transaction():
    with closing(connect()) as conn:
        task_id = kb.create_task(conn, title="no implicit nesting")
        with kb.write_txn(conn):
            with pytest.raises(RuntimeError, match="already inside"):
                kb.block_task(conn, task_id, kind="needs_input")
            assert kb.get_task(conn, task_id).status == "ready"
