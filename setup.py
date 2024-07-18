from setuptools import setup, find_packages

setup(
    name='TeGUI',
    version='0.1',
    description='A GUI-based tool for analysis',
    author='Te Jiang',
    url='https://github.com/TeJiang/TeGUI',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.4',
        'PyQt6==6.4.2',
        'pyqtgraph==0.13.7',
        'setuptools~=68.2.0',
    ],
)