"""!
@author atomicfruitcake

@date 2018

Setup file for Husk
"""

from setuptools import setup
setup(
    name='ballet',
    packages=['ballet'],
    version='0.1',
    description='Parallel SSH execution GUI application',
    long_description='Parallel SSH execution GUI application',
    license='GPG',
    author='Sam Bass',
    author_email='sam@wirewax.com',
    url='https://github.com/atomicfruitcake/ballet',
    download_url='https://github.com/atomicfruitcake/ballet/archive/0.1.tar.gz',
    keywords=['ssh', 'fabric', 'Tkinter', 'orchestration'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=['fabric'],
)
