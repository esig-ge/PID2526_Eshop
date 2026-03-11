# Project PID 2526

**Team:** Osman, Anthony, Abel, Mégane

## Installation

Command to install the requirements:

    pip install -r requirements.txt

### Adding New Dependencies
If you install a new package during development, you must update the requirements file so others can use it. Run this command:

    pip freeze > requirements.txt

## Usage

Run the script to add products:

    python populate_eshop.py

## Testing

To run the automated test suite for the project, use the following command:

    python manage.py test eshop

This will execute the unit tests located in the `eshop/tests/` directory, which cover models, views, and forms.

## Admin Panel Setup

To access the `/admin` interface, you need to create a superuser account. Run the following command and follow the prompts to set your username and password:

    python manage.py createsuperuser

## API Key Setup

### 1. Set the environment variable

**For Windows:**
Open PowerShell and run the following command (replace "your-api-key-here" with your actual key):

    setx API_KEY_OLLAMA "your-api-key-here"

*(Note: You may need to restart your terminal or IDE after running this command.)*

**For Linux / macOS / PythonAnywhere:**
Open your terminal (Bash) and run the following commands:

    echo 'export API_KEY_OLLAMA="your-api-key-here"' >> ~/.bashrc
    source ~/.bashrc

### 2. Python Implementation
In your Python file, use the following code to retrieve the key:

    import os

    api_key = os.getenv("API_KEY_OLLAMA")
    if not api_key:
        raise ValueError("API_KEY_OLLAMA not set in environment")