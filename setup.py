import importlib.metadata
from setuptools import setup, find_packages

__name__ = importlib.metadata.name()
__version__ = importlib.metadata.version()

package_dir = \
{'': 'src'}

packages = \
['factory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': __name__,
    'version': __version__,
    'description': '',
    'long_description': '',
    'author': 'Michael Verhulst',
    'author_email': 'michael@terminallabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'include_package_data': True,
    'python_requires': '>=3.8,<4.0',
    'install_requires': ["flask",],
    'entry_points': '''
        [console_scripts]
        factory=factory.ux.cli:cli
        ''',
}

setup(**setup_kwargs)