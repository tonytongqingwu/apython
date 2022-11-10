from setuptools import setup, find_packages

setup(
    name='apython',
    version='1.1.3',
    description='An Android Python package',
    url='https://github.com/tonytongqingwu/apython.git',
    author='tonytongqingwu',
    author_email='tony.wu@dexcom.com',
    license='Dexcom',
    packages=find_packages(),
    install_requires=['uiautomator',
                      'Appium-Python-Client==1.1.0',
                      'word2number',
                      'grpc-requests'
                      ],

    classifiers=[
        'Development Status :: 1 - Testing',
        'Intended Audience :: Development/VnV',
        'License :: Dexcom. Inc.',
        'Operating System :: MacOS :: Linux',
        'Programming Language :: Python :: 3.8.9',
        'Programming Language :: Python :: 3.10.8',
    ],
)
