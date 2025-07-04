from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pdf-processor",
    version="1.0.0",
    author="Oscar Song",
    author_email="oscar2song@gmail.com",  # Update with your email
    description="Comprehensive Python toolkit for PDF processing operations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oscar2song/pdf-processor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdf-processor=pdf_processor:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/oscar2song/pdf-processor/issues",
        "Source": "https://github.com/oscar2song/pdf-processor",
    },
)
