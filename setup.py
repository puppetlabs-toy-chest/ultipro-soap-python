from setuptools import setup

long_description = '''
UltiPro SOAP Python is a Python client that wraps the UltiPro SOAP API.
'''

setup(
    name='ultiprosoap',
    version= '0.0.1',
    url='https://github.com/call/ultipro-soap-python',
    author='Brian Call',
    author_email='callbrian@gmail.com',
    packages=['ultiprosoap', 'ultiprosoap.helper'],
    license='Apache License 2.0',
    install_requires=[
        'zeep>=1.4.1',
    ],
    keywords = ['UltiPro', 'SOAP API', 'Wrapper', 'Client'],
    description='Python Client for the UltiPro SOAP API',
    long_description=long_description
)
