from pathlib import Path
from setuptools import setup

project_directory = Path.home() / ".dib"
script = Path(project_directory) / "run_cd.sh"


def create_cd_script():
    if not script.exists():
        with script.open(mode="w", encoding="utf-8") as file:
            file.write("#!/bin/bash\n\ncd $1\n$SHELL")
            script.chmod(0o744)


with open("README.md") as f:
    readme = f.read()

setup(
    name="dibrowse",
    version="0.0.1",
    description="CLI tool ",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Viktor Berg",
    author_email="viktor.david.berg@gmail.com",
    maintainer="Viktor Berg",
    maintainer_email="viktor.david.berg@gmail.com",
    license="",
    packages=["dib"],
    url="http://github.com/naestia/dib",
    entry_points={
        "console_scripts": [
            "dib = dib.cli:cli_entrypoint",
        ],
    },
    install_requires=[
        "docopt>=0.6.2",
        "packaging>=21.3",
        "pyperclip>=1.8.2",
    ],
    python_requires=">=3.8",
    extras_require={
        "test": [
            "pytest",
            "pytest-mock",
            "flake8",
        ],
        "dev": [
            "pylint",
        ],
    },
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
)

if not project_directory.exists():
    project_directory.mkdir()
    script.touch()
    create_cd_script()

script.touch()
