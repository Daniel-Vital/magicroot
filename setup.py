import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magicroot",
    version="0.1.44",
    author="Daniel-Vital",
    author_email="author@example.com",
    description="Python like magic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Daniel-Vital/magicroot",
    project_urls={
        "Bug Tracker": "https://github.com/Daniel-Vital/magicroot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)