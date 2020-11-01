from setuptools import setup, find_packages

def readme():
    return open('README.md', 'r').read()

setup(
    name="cdremover",
    version="0.4.5",
    scripts=["cdremover"],
    author="Murdo Maclachlan",
    author_email="murdo@maclachlans.org.uk",
    description="A utility for members of the Transcribers of Reddit to remove their claim and done comments.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/claimdoneremover",
    packages=setuptools.find_packages(),
    install_requires=[
        "configparser",
        "expanduser",
        "praw>=7.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL-3.0",
        "Operating System :: OS Independent",
    ]
)
