from setuptools import setup, find_packages

setup(
    name="edgar_api",
    version="0.1.0",
    packages=["edgar_api"],
    package_dir={"edgar_api": "src"},
    python_requires=">=3.8",
)