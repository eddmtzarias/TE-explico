"""
Setup configuration for PixARR Design system.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README_PIXARR.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="pixarr-design",
    version="1.0.0",
    description="Autonomous supervision system for graphic design artifacts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="PixARR Design Team",
    author_email="tokraagcorp@gmail.com",
    url="https://github.com/eddmtzarias/TE-explico",
    packages=find_packages(exclude=["tests", "scripts", "docs"]),
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "python-dateutil>=2.8.2",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "mypy>=1.5.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
        ],
        "cli": [
            "click>=8.1.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pixarr-setup=scripts.setup_environment:setup_environment",
            "pixarr-simulate=scripts.run_simulation:run_simulation",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="audit security design graphics monitoring supervision",
    project_urls={
        "Bug Reports": "https://github.com/eddmtzarias/TE-explico/issues",
        "Source": "https://github.com/eddmtzarias/TE-explico",
    },
)
