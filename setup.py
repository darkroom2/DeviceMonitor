from setuptools import find_packages, setup

setup(
    name='devicemonitorlib',
    packages=find_packages(include=['devicemonitorlib']),
    version='0.1.1',
    description='A library for monitoring various types of devices.',
    author='Radoslaw Komorowski',
    license='MIT',
    install_requires=['numpy'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)
