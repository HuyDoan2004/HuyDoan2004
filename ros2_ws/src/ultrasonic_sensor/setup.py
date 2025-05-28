from setuptools import setup

package_name = 'ultrasonic_sensor'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='Ultrasonic sensor node publishing LaserScan',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'ultrasonic_sensor = ultrasonic_sensor.ultrasonic_sensor:main',
        ],
    },
)
