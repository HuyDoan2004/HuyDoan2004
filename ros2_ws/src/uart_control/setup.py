from setuptools import setup

package_name = 'uart_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@example.com',
    description='UART control node',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'uart_control = uart_control.uart_control:main',
        ],
    },
)
