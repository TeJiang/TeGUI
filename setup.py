from setuptools import setup, find_packages

setup(
    name='TeGUI',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/TeJiang/TeGUI',
    license='MIT',
    author='Te Jiang',
    author_email='',  # Omitted as per your request
    description='A GUI tool for hyperspectral image analysis',
    install_requires=[
        'numpy==1.26.4',
        'PyQt6==6.4.2',
        'pyqtgraph==0.13.7',
        'setuptools~=68.2.0'
    ],
)