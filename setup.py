import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

ignored_dependencies = []


def get_dependencies():
    with open('requirements.txt', 'r') as fh:
        requirements = fh.read()
        requirements = requirements.split('\n')
        map(lambda r: r.strip(), requirements)
        requirements = [r for r in requirements if r not in ignored_dependencies]
        return requirements


setuptools.setup(
    name='get-account',
    version='1.0.0',
    author='Valentin Rudloff',
    author_email='valentin.rudloff.perso@gmail.com',
    description='A python package to retrieve your bankin account balances, store them periodically and display '
                'them in a beautiful graph',
    url='https://github.com/Gamma-Software/GetUpdates',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=get_dependencies(),
    entry_points={'console_scripts': ['setup_bank_balance=bank_balance.setup_oauth:init',
                                      'show_balance=bank_balance.show_balance:show_balance',
                                      'store_balance=bank_balance.store_balance:store_balance']},
    python_requires='>=2.7',
)
