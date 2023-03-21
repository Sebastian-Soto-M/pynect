import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynect",
    version="0.1.0",
    author="Sebastian Soto M",
    author_email="s.m.sebastian.n@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sebastian-Soto-M/pynect",
    packages=setuptools.find_packages(exclude=["tests.*", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.2.0",
        "requests>=2.25.0"
    ],
    zip_safe=False,
)
