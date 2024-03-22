import subprocess

def install_hook(project):
    """
    Command to run to complete the project scaffolding setup.

    :param project: the project object
    """
    subprocess.run(["npm", "install"], cwd=project.path)

PROJECT_TEMPLATES = [
    {
        "name": "Node Express Mongoose",
        "path": "node_express_mongoose",
        "description": "A Node.js web application with Express and Mongoose, including session-based authentication, EJS views, and Bootstrap 5.",
        "summary": (
            "This project template includes the following features:\n"
            "* Initial Node.js and Express setup\n"
            "* User model in Mongoose ORM with unique username and hashed password fields\n"
            "* Session-based authentication using username and hashed password in routes/authRoutes.js\n"
            "* Authentication middleware to protect routes that require login\n"
            "* EJS view engine with html head, header, and footer EJS partials, and included Bootstrap 5.x CSS and JS\n"
            "* Routes and EJS views for login, register, and home (main) page\n"
            "* Config loading from environment using dotenv with a placeholder .env.example file: you will need to create a .env file with your own values"
        ),
        "install_hook": install_hook,
    }
]
