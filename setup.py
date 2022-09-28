from setuptools import setup

setup(
    name='apython',
    version='0.1.1',
    description='A example Python package',
    url='https://github.com/tonytongqingwu/apython.git',
    author='tonytongqingwu',
    author_email='tony.wu@dexcom.com',
    license='Dexcom',
    packages=['apython'],
    install_requires=['uiautomator',
                      'Appium-Python-Client==1.1.0',
                      ],

    classifiers=[
        'Development Status :: 1 - Testing',
        'Intended Audience :: Development/VnV',
        'License :: Dexcom. Inc.',
        'Operating System :: MacOS :: Linux',
        'Programming Language :: Python :: 3.8.9',
        'Programming Language :: Python :: 3.10',
    ],
)
