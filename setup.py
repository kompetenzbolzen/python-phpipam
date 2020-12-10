from distutils.core import setup
import setuptools

setup(
    name='phpipam',
    version='0.0.0-dev',
    author="Jonas Gunz",
    description="phpIPAM API implementation",
    packages=setuptools.find_packages(),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
)

