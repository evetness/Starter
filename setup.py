from distutils.core import setup

setup(
    name='starter',
    version='1.0',
    scripts=[
        'main.py',
        'dependency/theme.py',
        'dependency/status.py',
        'dependency/installer.py'
        ],
    packages=['dependency'],
    install_requires=['inquirer', 'blessings']
)
