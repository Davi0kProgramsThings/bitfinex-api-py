from distutils.core import setup

setup(
    name='bitfinex-api-py',
    version='3.0.0',
    packages=['bfxapi', 'bfxapi.websocket'],
    url='https://github.com/bitfinexcom/bitfinex-api-py',
    license='OSI Approved :: Apache Software License',
    author='Bitfinex',
    author_email='support@bitfinex.com',
    description='Official Bitfinex Python API',
    keywords='bitfinex,api,trading',
    install_requires=[
        'asyncio~=3.0',
        'websockets~=10.4',
        'typing_extensions~=4.4.0',
        'pyee~=9.0.4'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/bitfinexcom/bitfinex-api-py/issues',
        'Source': 'https://github.com/bitfinexcom/bitfinex-api-py',
    }
)
