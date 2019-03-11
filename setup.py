from setuptools import setup


setup(
    name='kgs_leela_worker',
    version='0.1',
    python_requires='>=3.5',
    py_modules=['cli'],
    install_requires=[
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'Click==7.0',
        'dataclasses==0.6',
        'idna==2.8',
        'kgs-leela-worker==0.1',
        'pika==0.13.1',
        'psycopg2-binary==2.7.7',
        'pydantic==0.20.1',
        'requests==2.21.0',
        'urllib3==1.24.1',
    ],
    entry_points='''
        [console_scripts]
        kgs_leela_worker=src.cli:cli
    ''',
)
