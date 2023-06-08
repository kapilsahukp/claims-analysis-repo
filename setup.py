from setuptools import setup, find_packages

setup(
    name='claims_analysis',                     # should match the package folder
    packages=find_packages(),
    version='0.0.1',                            # important for updates
    description='Testing installation of Package',
    author='Kapil Sahu',
    author_email='ksahu@charlesriverdata.com',
    url='https://github.com/charles-river-data/neptune.git',

    # list all packages that the package uses
    install_requires=[
        "python-dotenv==1.0.0",
        "openai>=0.27",
        "langchain>=0.0.170",
        "pandas",
        "pandas-stubs",
        "ipykernel",
        "pypdf"
    ],
)