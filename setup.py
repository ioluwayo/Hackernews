from setuptools import setup, find_packages

setup(
    name="hackernews",
    description="Hackernews scraper",
    version="3",
    author="ibukun",
    author_email="ioluwayo@gmail.com",
    install_requires=[
        dependency.strip() for dependency in open("requirements.txt").readlines()
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["hackernews=hackernews:main",]},
)
