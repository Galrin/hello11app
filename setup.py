from setuptools import setup # type: ignore

setup(
    name='hello11app',
    version='1.0.1',
    author='Ge3eR',
    description='SBER APP',
    url='https://github.com/Galrin/hello11app',
    license='MIT License',
    packages=['hello11app'],
    python_requires='>=3.8',
    install_requires=[
        'Flask',
        'pony',
        'pymysql',
    ],
)
