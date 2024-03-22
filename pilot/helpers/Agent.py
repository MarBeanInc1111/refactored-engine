class Agent:
    """Agent class representing an agent with a role and project."""

    def __init__(self, role: str, project: str):
        """Initialize the Agent instance with a role and project.

        Args:
            role (str): The role of the agent.
            project (str): The project the agent is working on.

        Raises:
            ValueError: If the role or project is not a string.
        """
        if not isinstance(role, str) or not isinstance(project, str):
            raise ValueError("Role and project must be strings.")

        self.role = role
        self.project = project

    def __repr__(self):
        """Return a string representation of the Agent instance.

        Returns:
            str: A string representation of the Agent instance.
        """
        return f"Agent(role='{self.role}', project='{self.project}')"

    def __eq__(self, other):
        """Check if two Agent instances are equal.

        Args:
            other: The other Agent instance to compare to.

        Returns:
            bool: True if the Agent instances have the same role and project,
                False otherwise.
        """
        if not isinstance(other, Agent):
            return False
        return self.role == other.role and self.project == other.project
