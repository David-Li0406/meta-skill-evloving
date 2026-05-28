#!/usr/bin/env python3
"""Setup script for universal-axiom Python package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="universal-axiom",
    version="0.1.0",
    author="Matt Belanger",
    author_email="matt@epiphanyengine.ai",
    description="The Universal Axiom & The Epiphany Engine - A fundamental framework for modeling intelligence through immutable natural laws",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheUniversalAxiom/pointy-stick",
    project_urls={
        "Homepage": "https://www.epiphanyengine.ai",
        "Bug Tracker": "https://github.com/TheUniversalAxiom/pointy-stick/issues",
        "Documentation": "https://github.com/TheUniversalAxiom/pointy-stick/tree/main/docs",
        "Source Code": "https://github.com/TheUniversalAxiom/pointy-stick",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=["python.universal_axiom"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "universal-axiom",
        "epiphany-engine",
        "intelligence",
        "ai",
        "reasoning",
        "consciousness",
        "mathematics",
        "fibonacci",
        "golden-ratio",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - pure Python implementation
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "pylint>=2.16.0",
        ],
    },
    license="MIT",
    include_package_data=True,
    zip_safe=False,
)
