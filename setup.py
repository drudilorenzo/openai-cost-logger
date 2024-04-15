from setuptools import setup, find_packages
import os

# Read the README file (reStructuredText format)
with open('README.rst') as f:
    long_description = f.read()

# Get the version number from the environment
# version_number = os.getenv('VERSION_NUMBER')
# version_number = version_number.strip("v")

version_number = '0.2.1'

setup(
    name='openai-cost-logger',
    version=version_number,
    author='Lorenzo Drudi | Mikolaj Boronski | Ivan Zakazov',
    description='OpenAI Cost Logger',
    author_email='lorenzodrudi11@gmail.com',
    url='https://github.com/drudilorenzo/openai-cost-tracker',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords=['openai', 'cost', 'logger', 'tracker'],
    license='MIT',
    packages=find_packages(include=['openai_cost_logger', 'openai_cost_logger.*']),
    requires=['openai', 'pandas', 'matplotlib'],
    install_requires=['openai', 'pandas', 'matplotlib']
)