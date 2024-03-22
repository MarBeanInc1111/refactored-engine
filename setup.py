# Import the necessary modules for building and packaging the Python module
import os
from setuptools import setup, find_packages

# Define the current version of the package
VERSION = "0.1.5"

# Read the list of requirements from the requirements.txt file
here = os.path.abspath(os.path.dirname(__file__))
requirements = open(os.path.join(here, "requirements.txt"), encoding="utf-8").readlines()

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Define the parameters for the setup function
    setup(
        # Define the name of the package
        name='gpt-pilot',
        # Define the version of the package
        version=VERSION,
        # Define the package directory
        packages=find_packages(),
        # Define the URL for the package
        url='https://www.pythagora.ai',
        # Define the license for the package
        license='MIT',
        # Define the email address for the package author
        author_email='info@pythagora.ai',
        # Define a short description of the package
        description='GPT Pilot - an AI developer that works with you to build complex projects',
        # Define a long description of the package in Markdown format
        long_description=open('README.md').read(),
        # Define the content type of the long description
        long_description_content_type='text/markdown',
        # Define the classifiers for the package
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
        # Define the list of required packages
        install_requires=requirements,
        # Define the minimum required version of Python
        python_requires='>=3.9',
    )
