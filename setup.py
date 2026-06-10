from setuptools import setup, find_packages

setup(
    name="astrology-engine",
    version="1.0.0",
    description="Open-source astrology chart calculation library using Swiss Ephemeris",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dominec369",
    author_email="",
    url="https://github.com/Dominec369/astrology-engine",
    project_urls={
        "GitHub": "https://github.com/Dominec369/astrology-engine",
        "Gitee": "https://gitee.com/dominec/astrology-engine",
    },
    py_modules=["calculator", "config", "formatter"],
    python_requires=">=3.8",
    install_requires=[
        "swisseph",
        "pytz",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
