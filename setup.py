"""Setup package installation"""

import os

import setuptools


def load_requirements(path: str) -> list:
    """Load requirements from the given relative path."""
    with open(path, encoding="utf-8") as file:
        requirements = []
        for line in file.read().split("\n"):
            if line.startswith("-r"):
                dirname = os.path.dirname(path)
                filename = line.split(maxsplit=1)[1]
                requirements.extend(load_requirements(os.path.join(dirname, filename)))
            elif line and not line.startswith("#"):
                requirements.append(line.replace("==", ">="))
        return requirements


if __name__ == "__main__":
    with open("README.md") as file:
        long_desc = file.read()

    setuptools.setup(
        name="writefreely-py",
        description="A Python package wrapping the WriteFreely / Write.as API",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        author="adbenitez",
        author_email="adbenitez@nauta.cu",
        url="https://github.com/adbenitez/writefreely-py",
        setup_requires=["setuptools_scm"],
        use_scm_version=True,
        package_dir={"": "src"},
        packages=setuptools.find_packages("src"),
        license="MIT",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
        ],
        python_requires=">=3.5",
        install_requires=load_requirements("requirements/requirements.txt"),
        extras_require={
            "test": load_requirements("requirements/requirements-test.txt"),
            "dev": load_requirements("requirements/requirements-dev.txt"),
        },
    )
