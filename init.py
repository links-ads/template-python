import os
import re
from datetime import datetime

DEFAULT_PY_VERSION = ">=3.10"


def query_params(validate: bool = True):
    """
    Query the user for the project parameters.
    """
    while True:
        while not (name := input("What is your name? ")):
            print("Please enter your name, or press Ctrl+C to exit.")

        while not (email := input("What is your email address? ")):
            print("Please enter your email address, or press Ctrl+C to exit.")

        while not (project_name := input("What should we call your project? ")):
            print("Please enter a project name, or press Ctrl+C to exit.")

        while not (project_description := input("What is your project about? ")):
            print("Please enter a project description, or press Ctrl+C to exit.")

        py_version = (
            input(f"What minimum version of Python do you want to use? (default: {DEFAULT_PY_VERSION}) ")
            or DEFAULT_PY_VERSION
        )

        if validate:
            print("So far, we have:")
            print(f" - Author: {name} <{email}>")
            print(f" - Project name: {project_name}")
            print(f" - Project description: {project_description}")
            print(f" - Python version: {py_version}")
            if input("Is this correct? (y/n) ").lower() != "y":
                print("Understood, let's try again.")
                continue
        return name, email, project_name, project_description, py_version


def rename_project(project_name: str):
    """
    Rename the project by recursively replacing the string "project_name" with the project name.
    """
    for path in os.listdir("."):
        if os.path.isdir(path):
            rename_project(path)
        elif os.path.isfile(path):
            with open(path) as f:
                data = f.read()
            with open(path, "w") as f:
                f.write(data.replace("project_name", project_name))


def update_license(name: str):
    """
    Replace the <year> and <name> placeholders in the LICENSE file with the actual values.
    At the moment the license is hardcoded to MIT.
    """
    with open("LICENSE") as f:
        data = f.read()
    data = data.replace("<year>", str(datetime.now().year))
    data = data.replace("<name>", name)
    with open("LICENSE", "w") as f:
        f.write(data)


def update_toml_property(data: str, key: str, value: str):
    """
    Update a property in a toml string.
    """
    return re.sub(f"{key} = .*", f'{key} = "{value}"', data)


def main():
    try:
        with open("pyproject.toml") as f:
            data = f.read()
    except FileNotFoundError:
        print("No pyproject.toml found, exiting.")
        exit(1)

    try:
        print("Hi! Let's get started.")
        print("Please answer the following questions to help us get you set up.")
        name, email, project_name, project_description, py_version = query_params()
        update_toml_property(data, "name", project_name)
        update_toml_property(data, "description", project_description)
        update_toml_property(data, "requires-python", py_version)
        update_toml_property(data, "authors", f'[{{name = "{name}", email = "{email}"}}]')
        update_toml_property(data, "version", f'{{attr = "{project_name}.__version__"}}')

        print("Updating license...")
        update_license(name)

        # storing the updated pyproject.toml
        print("Updating pyproject.toml...")
        with open("pyproject.toml", "w") as f:
            f.write(data)

        # update package name and dynamic versioning
        print("Renaming project files and folders...")
        rename_project(project_name)
        os.rename("src/project_name", f"src/{project_name}")

        print("Your project is ready. Deleting myself from existence, farewell!")
        # os.remove(__file__)

    except KeyboardInterrupt:
        print("Exiting.")


if __name__ == "__main__":
    main()
