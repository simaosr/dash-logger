import json
import os
from setuptools import setup, find_packages

with open(os.path.join("package.json")) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    author_email=package["author_email"],
    description=package.get("description", package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=package["homepage"],
    packages=find_packages(),
    include_package_data=True,
    license=package["license"],
    install_requires=[
        "dash>=2.0.0",
    ],
    classifiers=[
        "Framework :: Dash",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
