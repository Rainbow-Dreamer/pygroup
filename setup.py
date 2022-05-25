from setuptools import setup, find_packages
from os import path

setup(
    name='pygroup',
    py_modules=['pygroup'],
    version='0.14',
    license='LGPLv2.1',
    description='This is a python module about group theory in math',
    author='Rainbow-Dreamer',
    author_email='1036889495@qq.com',
    install_requires=['polynomial', 'matrixpro'],
    url='https://github.com/Rainbow-Dreamer/pygroup',
    download_url=
    'https://github.com/Rainbow-Dreamer/pygroup/archive/0.14.tar.gz',
    keywords=['group theory', 'mathematics', 'statistics'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True)
