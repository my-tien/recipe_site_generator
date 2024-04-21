from setuptools import find_packages, setup


setup(
	name = 'recipe_site_generator',
	description = 'Generates browser documents from input recipe files',
	author = 'My-Tien Nguyen',
	author_email = 'my-tien@mails.taipei',
	url = 'https://github.com/my-tien/recipe_site_generator',
	packages = find_packages(),
	install_requires = ('tabulate', 'pyyaml'),
)
