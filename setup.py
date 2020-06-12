import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="get-account-welpha", # Replace with your own username
    version="0.1.0",
    author="Valentin Rudloff",
    author_email="valentin.rudloff.perso@gmail.com",
    description="A python package to retrieve your bankin account balances, store them periodically and display "
                "them in a beautifull graph",
    url="https://github.com/Gamma-Software/GetUpdates",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)