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
    install_requires=[
        'Flask'>=2.3.2,
        'matplotlib'>=3.7.2,
        'numpy'>=1.25.2,
        'pandas'>=2.0.3,
        'scikit-learn'>=1.3.0,
        'scipy'>=1.11.1,
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'shellstat=src.cli:main',
        ],
    },
    keywords='shell analytics',
)
