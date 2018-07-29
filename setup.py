import re
from codecs import open
from setuptools import setup


with open('play_scraper/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='play_scraper',
    version=version,
    description='Google Play Store application scraper',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/danieliu/play-scraper',
    author='Daniel Liu',
    author_email='idaniel.liu@gmail.com',
    packages=['play_scraper'],
    license='MIT License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'beautifulsoup4==4.4.1',
        'lxml==3.6.0',
        'requests-futures==0.9.7',
        'requests[security]==2.9.1',
    ],
)
