from setuptools import find_packages, setup

setup(
    name="hackernews",
    description="Hackernews scraper",
    version="1",
    author="ibukun",
    author_email="ioluwayo@gmail.com",
    scripts=["hackernews.py"],
    install_requires=[
        dependency.strip() for dependency in open("requirements.txt").readlines()
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["hackernews=hackernews:main"]},
)
