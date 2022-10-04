from setuptools import setup, find_packages
from oscrcore.globals import VERSION


def readme():
    return open('README.md', 'r').read()


setup(
    name="oscr",
    version=VERSION,
    scripts=["oscr"],
    author="Murdo Maclachlan",
    author_email="murdomaclachlan@duck.com",
    description=(
        "A utility allowing users to delete blacklisted comments from their "
        + "Reddit profile once they have passed a cutoff time."
    ),
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/oscr",
    packages=find_packages(),
    install_requires=[
        "smooth_logger",
        "smooth_progress",
        "configparser",
        "plyer",
        "praw>=7.1.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    license='GPLv3+'
)
