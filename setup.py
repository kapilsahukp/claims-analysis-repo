from setuptools import setup, find_packages

setup(
    name='claims_analysis',                     # should match the package folder
    packages=find_packages(),
    version='0.0.1',                            # important for updates
    description='Claims Processing with LLMs',
    author='Charles River Data',
    author_email='mdezube@charlesriverdata.com',
    url='https://github.com/charles-river-data/neptune.git',

    # list all packages that the package uses
    install_requires=[
        "python-dotenv",
        "openai",
        "langchain",
        "pandas",
        "pandas-stubs",
        "ipykernel",
        "pypdf"
    ],
)