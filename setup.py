import setuptools


setuptools.setup(
    name='eventbus',
    version='0.0.1',
    description='',
    url='https://github.com/maikelboogerd/python-eventbus.git',
    author='Maikel van den Boogerd',
    author_email='maikelboogerd@gmail.com',
    license='MIT',
    packages=['eventbus'],
    install_requires=['transaction', 'boto3'],
    zip_safe=False,
)
