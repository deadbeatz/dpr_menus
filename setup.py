from distutils.core import setup
setup(
  name = 'dpr-menus',         # How you named your package folder (MyLib)
  packages = ['dpr-menus'],   # Chose the same as "name"
  version = '1.9.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'dPR Team: Menus for Mystic BBS',   # Give a short description about your library
  author = 'Analog',                   # Type in your name
  author_email = 'analog@deadbeatz.org',      # Type in your E-Mail
  url = 'https://github.com/deadbeatz/dpr_menus',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/deadbeatz/dpr_menus/archive/v1.9.0.tar.gz',    # I explain this later on
  keywords = ['Mystic', 'BBS', 'dpr', 'menus'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: BBS Utils',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 2.7',
  ],
)
#import setuptools
#
#with open("README.md", "r") as fh:
#    long_description = fh.read()
#
#setuptools.setup(
#    name="dpr-menus", # Replace with your own username
#    version="1.9.0",
#    author="Analog",
#    author_email="analog@deadbeatz.org",
#    description="dPR menuing system for Mystic BBS",
#    long_description=long_description,
#    long_description_content_type="text/markdown",
#    url="https://github.com/deadbeatz/dpr_menus",
#    packages=setuptools.find_packages(),
#    classifiers=[
#        "Programming Language :: Python :: 2",
#        "License :: OSI Approved :: MIT License",
#        "Operating System :: OS Independent",
#    ],
#		python_requires='>=2.7',
#)
