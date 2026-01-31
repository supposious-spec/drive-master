from setuptools import setup

setup(
    name='drive-master',
    version='2.4.0',
    py_modules=['mount_drive'],
    install_requires=['click'],
    entry_points={
        'console_scripts': [
            'drive-master = mount_drive:main',
        ],
    },
)