from distutils.core import setup
import setuptools

setup(
    name='phpipam-api',
    version='1.0.0',
    author="Jonas Gunz",
    author_email="himself@jonasgunz.de",
    url="https://github.com/kompetenzbolzen/python-phpipam",
    description="phpIPAM API implementation",
    packages=['phpipam_api'],
    install_requires=[
        "requests>=2.25.1",
        "python-dateutil>=2.8.1"
    ],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

