from setuptools import setup
import proxy

setup(
    name='proxy',
    version=proxy.__version__,
    description='http sniffer',
    long_description='',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: AsyncIO',
        'Framework :: aiohttp',
    ],
    keywords='http tcp proxy',
    url='http://github.com/businka/HttpSniffer',
    author='Razgovorov Mikhail',
    author_email='',
    license='Apache 2',
    packages=['HttpSniffer'],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
    ],
    # include_package_data=True,
    zip_safe=False,
    data_files=['HttpSniffer']
)
