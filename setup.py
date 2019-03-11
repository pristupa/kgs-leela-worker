from setuptools import setup


setup(
    name='kgs_leela_worker',
    version='0.1',
    python_requires='>=3.5',
    py_modules=['cli'],
    install_requires=[
        'amqp==2.4.2',
        'billiard==3.5.0.5',
        'celery==4.2.1',
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'Click==7.0',
        'dataclasses==0.6',
        'idna==2.8',
        'kgs-leela-worker==0.1',
        'kombu==4.4.0',
        'psycopg2-binary==2.7.7',
        'pydantic==0.20.1',
        'pytz==2018.9',
        'requests==2.21.0',
        'urllib3==1.24.1',
        'vine==1.2.0',
    ],
    entry_points='''
        [console_scripts]
        kgs_leela_worker=src.cli:cli
    ''',
)
