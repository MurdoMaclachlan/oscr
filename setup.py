from setuptools import setup, find_packages
from oscrmodules.gvars import version

def readme():
    return open('README.md', 'r').read()

setup(
    name="oscr",
    version=version,
    scripts=["oscr"],
    author="Murdo Maclachlan",
    author_email="murdo@maclachlans.org.uk",
    description="A utility allowing users to delete blacklisted comments from their Reddit profile once they have passed a cutoff time.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/oscr",
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
