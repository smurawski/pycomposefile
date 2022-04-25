import setuptools
import os

long_desc = open("README.md").read()
required = ['pyyaml']  # Comma seperated dependent libraries name
version = os.environ.get("BUILD_TAG", "0.0.1a1").lstrip("v")

setuptools.setup(
    name="pycomposefile",
    version=version,
    author="Steven Murawski",
    author_email="steven.murawski@microsoft.com",
    license="MIT",
    description="Structured deserialization of Docker Compose files.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/smurawski/pycomposefile",
    packages=setuptools.find_packages(),
    key_words="docker compose",
    install_requires=required,
    python_requires=">=3.6",
)
