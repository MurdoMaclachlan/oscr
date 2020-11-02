from setuptools import setup, find_packages

def readme():
    return open('README.md', 'r').read()

setup(
    name="cdremover",
    version="1.0.1",
    scripts=["cdremover"],
    author="Murdo Maclachlan",
    author_email="murdo@maclachlans.org.uk",
    description="A utility for members of the Transcribers of Reddit to remove their claim and done comments.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/claimdoneremover",
    packages=find_packages(),
    install_requires=[
        "configparser",
        "praw>=7.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
