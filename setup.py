import setuptools


tests_require = [
    'pytest>=3.7.4',
    'pytest-cov',
    'mockito',
]

setuptools.setup(
    name='eventcore',
    version='0.4.0',
    description='Produce and consume events with any queue.',
    author='Maikel van den Boogerd',
    author_email='maikelboogerd@gmail.com',
    url='https://github.com/maikelboogerd/eventcore',
    keywords=['events', 'sqs', 'kafka'],
    packages=[
        'eventcore',
        'eventcore.sqs',
        'eventcore.kafka',
    ],
    install_requires=[],
    extras_require={
        'testing': tests_require,
        'sqs': ['boto3==1.9.*'],
        'kafka': ['confluent-kafka==0.11.*'],
    },
    license='MIT',
    zip_safe=False
)
