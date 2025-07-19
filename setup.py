"""Packaging configuration for the ocrcli project."""

from pathlib import Path
from setuptools import setup, find_packages

# Read the requirements from requirements.txt
reqs_path = Path(__file__).resolve().with_name("requirements.txt")
install_requires = [
    line.strip()
    for line in reqs_path.read_text().splitlines()
    if line.strip() and not line.startswith("#")
]

setup(
    name='ocrcli',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'ocrcli=src.cli:main',
        ],
    },
    description='Command-line OCR pipeline.',
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
