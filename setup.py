"""Pip configuration."""
# https://github.com/pypa/sampleproject/blob/main/setup.py

from setuptools import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

with open("requirements.txt", "r") as fp:
    requirements = fp.read()

setup(
    name="kusanagi",
    version="0.0.4",
    packages=[
        "kusanagi",
        "kusanagi.core",
        "kusanagi.core.compressor",
        "kusanagi.core.encoder",
        "kusanagi.core.filter",
        "kusanagi.core.obfuscator",
        "kusanagi.core.parser",
        "kusanagi.core.payload",
        "kusanagi.core.payload.cmd",
        "kusanagi.core.payload.code",
        "kusanagi.core.payload.file",
        "kusanagi.core.permutator",
        "kusanagi.core.sorter",
        "kusanagi.core.typing",
        "kusanagi.lib",
        "kusanagi.lib.clipboard",
        "kusanagi.lib.template",
        "kusanagi.lib.yaml",
    ],
    package_data={
        "kusanagi": [
            "files/obfuscators/cmd.yml",
            "files/payloads/cmd/bash.yml",
            "files/payloads/cmd/nc.yml",
        ],
    },
    entry_points={
        "console_scripts": [
            # cmd = package[.module]:func
            "kusa=kusanagi:main",
        ],
    },
    install_requires=requirements,
    description="Kusanagi is a bind and reverse shell payload generator with obfuscation and badchar support.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["payload", "bind shell", "reverse shell", "generator", "shell", "kusanagi"],
    author="cytopia",
    author_email="cytopia@everythingcli.org",
    url="https://github.com/cytopia/kusanagi",
    project_urls={
        "Source Code": "https://github.com/cytopia/kusanagi",
        "Bug Tracker": "https://github.com/cytopia/kusanagi/issues",
    },
    python_requires=">=3.6",
    classifiers=[
        # https://pypi.org/classifiers/
        #
        # How mature is this project
        "Development Status :: 3 - Alpha",
        # How does it run
        "Environment :: Console",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        # License
        "License :: OSI Approved :: MIT License",
        # Where does it run
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        # Project topics
        "Topic :: Internet",
        "Topic :: Security",
        "Topic :: System :: Shells",
        "Topic :: System :: Systems Administration",
        "Topic :: Terminals",
        "Topic :: Utilities",
        # Typed
        "Typing :: Typed",
    ],
)
