from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()
    print(required)

setup(
    name='pdanonymizer',
    version='0.6.0',
    description='Personal Data Anonymizer',
    url='https://github.com/ignatovskiy/PersonalDataAnonymizer',
    author='Nikita Ignatovsky',
    license='MIT',
    packages=['pdanonymizer'],
    install_requires=required)
