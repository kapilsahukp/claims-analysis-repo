from setuptools import setup, find_packages

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='claims_analysis_pkg',                           # should match the package folder
    packages=find_packages(),
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='Testing installation of Package',
    author='Kapil Sahu',
    author_email='ksahu@charlesriverdata.com',
    url='https://github.com/kapilsahukp/claims-analysis-repo.git',
    install_requires=["python-dotenv==1.0.0",
                      "openai>=0.27",
                      "langchain>=0.0.170",
                      "pandas", "pandas-stubs",
                      "ipykernel", "pypdf"
                      ],                  # list all packages that your package uses
    # classifiers=[                                   # https://pypi.org/classifiers
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'Topic :: Software Development :: Documentation',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    # ],

    # download_url="https://github.com/kapilsahukp/claims-analysis-repo/archive/refs/tags/0.0.1.tar.gz",
)