from setuptools import setup


setup(
    name='kgs_leela_worker',
    version='0.1',
    python_requires='>=3.5',
    py_modules=['cli'],
    install_requires=[
        'Click==7.0',
        'pika==0.13.1',
        'psycopg2-binary==2.7.7',
        'configparser==3.7.3',
        'tqdm==4.31.1',
    ],
    entry_points='''
        [console_scripts]
        kgs_leela_worker=src.cli:cli
    ''',
)
