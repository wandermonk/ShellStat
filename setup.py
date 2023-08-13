from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name="shellstat",
    version="0.1.0",
    author="Phani Kumar Yadavilli",
    author_email="phanikumaryadavilli@gmail.com",
    description="A tool for shell history analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wandermonk/shellstat",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
