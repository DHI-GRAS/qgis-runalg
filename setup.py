from setuptools import setup, find_packages

setup(
    name='qgis_runalg',
    version='0.1',
    description='Run QGIS algorithms from outside of QGIS',
    author='Jonas Solvsteen',
    author_email='josl@dhigroup.com',
    packages=find_packages(),
    include_package_data=True)
