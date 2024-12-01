
from setuptools import setup, find_packages
setup(
    name="connect4",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    entry_points={
    'console_scripts': [
        'connect4 = connect4.play:run',
    ]}
)


