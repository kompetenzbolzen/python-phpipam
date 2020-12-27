from distutils.core import setup
import setuptools

setup(
    name='phpipam',
    version='0.0.0-dev',
    author="Jonas Gunz",
    description="phpIPAM API implementation",
    packages=['phpipam'],
    install_requires=[
        "requests>=2.25.1"
    ],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
)

