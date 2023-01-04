from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="Capital Gains CLI",
    version="0.0.1",
    author="Candidate",
    author_email="candidate@nubank.com",
    description=("CLI tool for calculating."),
    license="BSD",
    keywords="cli tax stocks",
    packages=find_packages(),
    long_description=readme,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        "console_scripts": [
            "capital-gains=src.cli:entrypoint",
        ]
    },
    python_requires=">=3.8",
)
