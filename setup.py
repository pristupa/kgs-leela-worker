from setuptools import setup


setup(
    name='kgs_leela_worker',
    version='0.1',
    python_requires='>=3.5',
    py_modules=['cli'],
    install_requires=[
        'Click==7.0',
        'psycopg2-binary==2.7.7',
        'pydantic==0.20.1',
        'requests==2.21.0',
    ],
    entry_points='''
        [console_scripts]
        kgs_leela_worker=src.cli:cli
    ''',
)
