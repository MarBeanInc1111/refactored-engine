class MockQuestionary:
    """
    A mock questionary class that simulates user input for testing purposes.
    """

    def __init__(self, answers: list = None, initial_state: str = 'project_description'):
        """
        Initialize the MockQuestionary object with a list of answers and an initial state.

        :param answers: A list of strings representing the user's answers
        :param initial_state: The initial state of the questionary
        """
        if answers is None:
            answers = []
        self.answers = iter(answers)
        self.state = initial_state

    def display_text(self, question: str, style: str = None) -> 'MockQuestionary':
        """
        Display a question to the user and update the state based on the question.

        :param question: The question to display
        :param style: The style of the question
        :return: The MockQuestionary object
        """
        print('AI: ' + question)
        if question.startswith('User Story'):
            self.state = 'user_stories'
        elif question.endswith('write "DONE"'):
            self.state = 'DONE'
        return self

    def ask(self) -> str:
        """
        Ask the user a question and return their answer.

        :return: The user's answer
        """
        try:
            return next(self.answers)
        except StopIteration:
            raise ValueError("No more answers available")

    def unsafe_ask(self) -> str:
        """
        Ask the user a question without any validation or error handling.

        :return: The user's answer
        """
        if self.state == 'user_stories':
            return next(self.answers)

    def reset(self) -> 'MockQuestionary':
        """
        Reset the questionary to its initial state.

        :return: The MockQuestionary object
        """
        self.answers = iter(self.answers)
        self.state = 'project_description'
        return self
