from setuptools import setup

long_description = '''
UltiPro SOAP Python is a Python client that wraps the UltiPro SOAP API.
'''

setup(
    name='ultipro',
    version='0.0.2',
    url='https://github.com/call/ultipro-soap-python',
    author='Brian Call',
    author_email='callbrian@gmail.com',
    packages=['ultipro', 'ultipro.services'],
    license='Apache License 2.0',
    install_requires=[
        'backoff>=1.4.3',
        'click>=6.7',
        'configparser>=3.5.0',
        'zeep>=2.0.0'
    ],
    keywords=['UltiPro', 'SOAP API', 'Wrapper', 'Client'],
    description='Python Client for the UltiPro SOAP API',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'ultipro=ultipro.cli:cli',
        ],
    },
)
