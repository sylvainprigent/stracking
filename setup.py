import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stracking",
    version="0.1.4",
    author="Sylvain Prigent",
    author_email="meriadec.prigent@gmail.com",
    description="Particle tracking for 2D+t and 3D+t scientific data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sylvainprigent/stracking",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "scipy>=1.6.3",
        "scikit-image>=0.18.1"
    ],
)
