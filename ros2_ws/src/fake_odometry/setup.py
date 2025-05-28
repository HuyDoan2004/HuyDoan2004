from setuptools import setup

package_name = 'fake_odometry'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='Fake odometry broadcaster',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'fake_odometry = fake_odometry.fake_odometry:main',
        ],
    },
)
