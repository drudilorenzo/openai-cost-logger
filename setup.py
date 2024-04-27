from setuptools import setup, find_packages

# Read the README file (reStructuredText format)
with open('README.rst') as f:
    long_description = f.read()

version_number = '0.3.1'

setup(
    name='openai-cost-logger',
    version=version_number,
    author='Lorenzo Drudi | Mikolaj Boronski | Ivan Zakazov',
    description='OpenAI Cost Logger',
    author_email='lorenzodrudi11@gmail.com',
    url='https://github.com/drudilorenzo/openai-cost-tracker',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords=['openai', 'cost', 'logger', 'tracker', 'viz', 'llms'],
    license='MIT',
    packages=find_packages(include=['openai_cost_logger', 'openai_cost_logger.*']),
    requires=['openai', 'pandas', 'matplotlib'],
    install_requires=['openai', 'pandas', 'matplotlib']
)