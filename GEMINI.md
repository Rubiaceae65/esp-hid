# Using Python Virtual Environments (venv)

This guide explains how to use Python virtual environments (`venv`) to manage project-specific dependencies, ensuring your projects are isolated and don't interfere with your system's Python installation.

## 1. Create a Virtual Environment

Navigate to your project directory in the terminal and run the following command. This will create a new directory named `venv` (you can choose a different name) inside your project, containing a fresh Python environment.

```bash
python3 -m venv venv
```

## 2. Activate the Virtual Environment

Before working on your project, you need to activate the virtual environment. This modifies your shell's `PATH` to use the Python and `pip` executables within your `venv` directory.

*   **On Linux/macOS:**
    ```bash
    source venv/bin/activate
    ```

*   **On Windows (Command Prompt):**
    ```bash
    venv\Scripts\activate.bat
    ```

*   **On Windows (PowerShell):**
    ```powershell
    venv\Scripts\Activate.ps1
    ```

You'll know the environment is active when your terminal prompt changes, usually by prepending `(venv)` to it.

## 3. Install Dependencies

Once activated, you can install any Python packages required for your project using `pip`. These packages will only be installed within your virtual environment, keeping your global Python environment clean.

```bash
pip install your-package-name
pip install -r requirements.txt # If you have a requirements file
```

## 4. Deactivate the Virtual Environment

When you're done working on your project, you can deactivate the virtual environment. This reverts your shell's `PATH` to its original state, allowing you to use your system's Python again.

```bash
deactivate
```

## Best Practices

*   **Include `venv` in `.gitignore`:** Add `venv/` to your project's `.gitignore` file to prevent committing your virtual environment to version control.
*   **Use `requirements.txt`:** Generate a `requirements.txt` file to list your project's dependencies. This makes it easy for others (or your future self) to set up the environment.
    ```bash
    pip freeze > requirements.txt
    ```
