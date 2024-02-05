from setuptools import setup, find_packages

setup(
    name='translucent_full_loading',
    version='0.1.0',
    author='Zaaferani',
    author_email='zaaferani.arta@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'translucent_full_loading.ico': ['loading.gif']},
    description='PyQt thread which overlays the translucent loading screen with label on the whole window like some generic application loading screen.',
    url='https://github.com/zaaferani/translucent_full_loading.git',
    install_requires=[
        'PyQt6>=6.1'
    ]
)