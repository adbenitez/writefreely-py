import setuptools

if __name__ == "__main__":
    with open("README.md") as file:
        long_desc = file.read()
    with open("requirements.txt") as file:
        install_requires = [
            line.replace("==", ">=")
            for line in file.read().split("\n")
            if line and not line.startswith(("#", "-"))
        ]

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
        install_requires=install_requires,
    )
