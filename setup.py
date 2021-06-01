import io
from setuptools import setup, find_packages
from typing import List

requirements: List[str] = ["logzero", "click", "flask", "more_itertools", "hpi_api"]

# use the readme.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="auth_my_api",
    version="0.0.1",
    url="https://github.com/hpi/auth_hpi_api",
    author="Madeline",
    author_email="maddie@qnzl.co",
    description=("""an (authenticated) automatic json api for hpi"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="mit",
    packages=find_packages(include=["auth_my_api"]),
    install_requires=requirements,
    keywords="data server",
    entry_points={"console_scripts": ["auth_hpi_api = auth_my_api.__main__:main"]},
    classifiers=[
        "license :: osi approved :: mit license",
        "programming language :: python",
        "programming language :: python :: 3",
        "programming language :: python :: 3.7",
        "programming language :: python :: 3.8",
    ],
)

