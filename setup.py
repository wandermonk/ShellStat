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
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'shellstat=src.cli:main',
        ],
    },
    keywords='shell analytics',
)
