import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simtel",
    version="0.0.1",
    author="Robert Stein",
    author_email="robert.stein@desy.de",
    description="Package for simulating astronomy detections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="physics science astronomy",
    url="https://github.com/robertdstein/simtel",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.7',
    install_requires=[
        "setuptools",
        "numpy",
        "matplotlib",
        "astropy",
        "sphinx",
        "jupyter",
        "coveralls",
        "pandas",
        "scipy",
    ],
    package_data={'simtel': [
        'tel_data/*.csv',
        'tel_data/*.dat'
    ]}
)

