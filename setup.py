from setuptools import setup
setup(
    name='atrade',
    author='Chris Palmieri',
    description='Experimental automated algorithmic stock trading platform',
    version='0.1',
    py_modules=['main', 'common', 'scanner', 'handlers', 'classes','ibx', 'market'],
    install_requires=[
        'Click', 'pandas', 'requests_html', 'Blessings', 'PyInquirer', 'scipy', 'aiohttp',
    ],
    entry_points='''
        [console_scripts]
        atrade=main:main
    ''',
)
