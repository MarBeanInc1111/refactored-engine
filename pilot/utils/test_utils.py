from typing import Optional

from .utils import should_execute_step

class TestShouldExecuteStep:
    """Tests for the `should_execute_step` function."""

    def test_no_step_arg(self, teststep: str, currentstep: Optional[str]) -> None:
        """
        Test that `should_execute_step` returns True when no step is provided.
        """
        assert should_execute_step(teststep, currentstep) is True, (
            f"Expected True, but got False "
            f"when teststep='{teststep}' and currentstep='{currentstep}'"
        )

    def test_skip_step(self, teststep: str, currentstep: str) -> None:
        """
        Test that `should_execute_step` returns True when the current step matches the test step.
        """
        assert should_execute_step(teststep, currentstep) is True, (
            f"Expected True, but got False "
            f"when teststep='{teststep}' and currentstep='{currentstep}'"
        )

    def test_skip_step_different_case(self, teststep: str, currentstep: str) -> None:
        """
        Test that `should_execute_step` returns True when the current step matches the test step,
        even if their cases are different.
        """
        assert should_execute_step(teststep.lower(), currentstep.upper()) is True, (
            f"Expected True, but got False "
            f"when teststep='{teststep}' and currentstep='{currentstep}'"
        )

    def test_unknown_step(self, teststep: str, currentstep: Optional[str]) -> None:
        """
        Test that `should_execute_step` returns False when the test step is not a known step.
        """
