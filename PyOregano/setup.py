
import sys
if not sys.platform.lower().startswith('win'):
    raise Exception("Oregano is only supported under Windows")

packagesNames = ['Oregano', 'Oregano']
packagesDirs = {'Oregano' : ''}

from distutils.core import setup
setup(
	name = 'Oregano',
	version = '1.0',
	description = 'Tracing tools',
	author = 'Assaf Nativ',
	author_email = 'Nativ.Assaf@gmail.com',
	packages = packagesNames,
    package_dir = packagesDirs,
	data_files = [('Lib\\\site-packages', ('Oregano.pth',))]
	)


