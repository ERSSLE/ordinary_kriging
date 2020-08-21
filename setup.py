import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'kriging',
    version = '0.0.1',
    author = 'Erssle',
    author_email = 'ersslee@gmail.com',
    description = 'Ordinary Kriging Interpolation',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = '',
    packages = setuptools.find_packages(include=['kriging','kriging.*']),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
        ],
    python_requires = '>=3.6',
    install_requires = ['numpy','shapely','matplotlib'],
    package_data = {
        'kriging':['data/*.json'],
        }
    )
