from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

version = '2.2.2'

setup(name='agithub',
      version=version,
      description="A lightweight, transparent syntax for REST clients",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      keywords=['api', 'REST', 'GitHub', 'Facebook', 'SalesForce'],
      author='Jonathan Paugh',
      author_email='jpaugh@gmx.us',
      url='https://github.com/mozilla/agithub',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      )
