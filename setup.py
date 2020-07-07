# from distutils.core import setup
from setuptools import setup
setup(
  name = 'dpr-menus',
  packages = ['dpr-menus'],
  version = '1.9.1',
  license='MIT',
  description = 'dPR Team: Menus for Mystic BBS',
  author = 'Analog',
  author_email = 'analog@deadbeatz.org',
  url = 'https://github.com/deadbeatz/dpr_menus',
  download_url = 'https://github.com/deadbeatz/dpr_menus/archive/v1.9.0.tar.gz',
  keywords = ['Mystic', 'BBS', 'dpr', 'menus'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
  ],
)