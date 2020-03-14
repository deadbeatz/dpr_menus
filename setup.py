import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dpr-menus", # Replace with your own username
    version="1.9.0",
    author="Analog",
    author_email="analog@deadbeatz.org",
    description="dPR menuing system for Mystic BBS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deadbeatz/dpr_menus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
		python_requires='>=2.7',
)
