from pathlib import Path
from setuptools import setup

with open("README.md") as f:
    readme = f.read()

project_directory = Path.home() / ".dib"

setup(
    name="dib",
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
            "ptpython",
        ],
        "validation": [
            "pykwalify",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Operating System :: Linux",
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
