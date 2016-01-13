from setuptools import setup, find_packages


setup(
        name="agithub",
        version="1.3",
        packages=find_packages(),
        scripts=[
            'agithub.py',
            'Facebook.py',
            'SalesForce.py'
        ],
        package_data={
            '':['COPYING', '*.md']
        }
)