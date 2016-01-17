from setuptools import setup, find_packages
import sys, os

version = '2.0'

setup(name='agithub',
      version=version,
      description="A lightweight, transparent syntax for REST clients",
      long_description="""\
multi-line""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='api REST GitHub Facebook SalesForce',
      author='Jonathan Paugh',
      author_email='jpaugh@gmx.us',
      url='https://github.com/jpaugh/agithub',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
