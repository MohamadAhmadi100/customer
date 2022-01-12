from setuptools import setup
import os

requirements_dir = os.getcwd() + "/requirements.txt"
with open(requirements_dir, "r") as f:
    file = f.readlines()
    requirements = [line.rstrip() for line in file]

setup(
    name='customer',
    version='0.1.0',
    author='ehsan asadi khorrami',
    author_email='ehsankhorram72@gmail.com',
    packages=['customer'],
    install_requires=requirements,
    zip_safe=False
)
