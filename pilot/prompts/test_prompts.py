from .prompts import get_prompt

def test_prompt_ran_command():
    """Test that the ran_command prompt is generated correctly for different exit codes."""

    def _assert_ran_command_prompt(exit_code):
        # Given
        cli_response = 'stdout:\n```\nsuccess\n```'
        command = './scripts/run_tests'
        additional_message = 'Some additional message\n'

        # When
        prompt = get_prompt('dev_ops/ran_command.prompt', {
            'cli_response': f'stdout:\n```\n{cli_response}\n```',
            'command': command,
            'additional_message': additional_message,
            'exit_code': exit_code
        })

        # Then
        expected_prompt = get_expected_ran_command_prompt(cli_response, command, additional_message)
        if exit_code is None:
            assert prompt == expected_prompt + "BUG\n", f"Expected: {expected_prompt + 'BUG\n'}\nActual: {prompt}"
        else:
            assert prompt == expected_prompt + "DONE\n", f"Expected: {expected_prompt + 'DONE\n'}\nActual: {prompt}"

    def get_expected_ran_command_prompt(cli_response, command, additional_message):
        return (
            f"{additional_message}\n"
            "I ran the command `{command}`. The output was:\n"
            "stdout:\n"
            "```\n"
            f"{cli_response}\n"
            "```\n"
            "Think about this output and not any output in previous messages. "
            "If the command was successfully executed, respond with `DONE`. "
            "If it wasn't, respond with `BUG`.\n"
            "Do not respond with anything other than these two keywords.\n"
        ).strip()

    test_prompt_ran_command(None)
    test_prompt_ran_command(0)

def test_parse_task_no_processes():
    """Test that the parse_task prompt is generated correctly when there are no running processes."""

    # Given
    prompt = get_prompt('development/parse_task.prompt', {
        'running_processes': {}
    })

    # Then
    assert 'the following processes' not in prompt, f"Expected: 'the following processes' not in prompt
