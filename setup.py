import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="get-account",
    version="1.0.0",
    author="Valentin Rudloff",
    author_email="valentin.rudloff.perso@gmail.com",
    description="A python package to retrieve your bankin account balances, store them periodically and display "
                "them in a beautiful graph",
    url="https://github.com/Gamma-Software/GetUpdates",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["show_balance=show_balance:main",
                                      "store_balance=store_balance:main"]},
    python_requires='>=2.7',
)
