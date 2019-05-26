import setuptools


tests_require = [
    'pytest>=3.7.4',
    'pytest-cov',
    'mockito',
]

setuptools.setup(
    name='eventcore',
    version='0.4.0rc2',
    description='Produce and consume events with any queue.',
    author='Maikel van den Boogerd',
    author_email='maikelboogerd@gmail.com',
    url='https://github.com/maikelboogerd/eventcore',
    keywords=['events', 'queue', 'producer', 'consumer', 'dispatch', 'sqs'],
    packages=[
        'eventcore',
        'eventcore.dummy',
        'eventcore.sqs',
    ],
    install_requires=[],
    extras_require={
        'testing': tests_require,
        'sqs': ['boto3==1.9.*']
    },
    license='MIT',
    zip_safe=False
)
