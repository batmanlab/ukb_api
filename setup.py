import setuptools
import ukb_api
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ukb_api",                     # This is the name of the package
    version=ukb_api.__version__,                        # The initial release version
    author="Tigmanshu Chaudhary",                     # Full name of the author
    description="UKB API",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["ukb_api"],             # Name of the python package
    #package_dir={'':'ukb_api/src'},     # Directory of the source code of the package
    install_requires=['pandas==1.1.5','datalad','pandas-plink','numpy','dataclasses']                     # Install other dependencies if any
)
