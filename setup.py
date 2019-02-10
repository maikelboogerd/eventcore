import setuptools


setuptools.setup(
    name='eventcore',
    version='0.3.4',
    description='Produce and consume events with any queue.',
    author='Maikel van den Boogerd',
    author_email='maikelboogerd@gmail.com',
    url='https://github.com/maikelboogerd/eventcore',
    keywords=['events', 'queue', 'producer', 'consumer', 'dispatch', 'sqs'],
    packages=[
        'eventcore',
        'eventcore.sqs'
    ],
    install_requires=[],
    extras_require={
        'sqs': ['boto3==1.9.*']
    },
    license='MIT',
    zip_safe=False
)
