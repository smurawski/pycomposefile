import setuptools

long_desc = open("README.md").read()
required = ['pyyaml']  # Comma seperated dependent libraries name

setuptools.setup(
    name="pycomposefile",
    version="0.0.1a1",
    author="Steven Murawski",
    author_email="steven.murawski@microsoft.com",
    license="MIT",
    description="Structured deserialization of Docker Compose files.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/smurawski/pycomposefile",
    packages=['pycomposefile'],
    key_words="docker compose",
    install_requires=required,
    python_requires=">=3.6",
)
