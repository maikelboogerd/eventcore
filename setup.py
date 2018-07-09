import setuptools


setuptools.setup(
    name='eventcore',
    version='0.0.7',
    description='Produce and consume events with any queue.',
    author='Maikel van den Boogerd',
    author_email='maikelboogerd@gmail.com',
    url='https://github.com/maikelboogerd/python-eventcore',
    keywords=['event', 'queue', 'producer', 'consumer'],
    packages=['eventcore', 'eventcore.core', 'eventcore.queues'],
    install_requires=['boto3'],
    license='MIT',
    zip_safe=False,
)
