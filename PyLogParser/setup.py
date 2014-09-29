
from distutils.core import setup
import shutil
import sys

if '32 bit' in sys.version:
    is32Bit = True
elif '64 bit' in sys.version:
    is64Bit = False
else:
    raise Exception("Unknown platform")

setup(
        name = 'LogParser',
        version = '1.0',
        description = 'Parsing Oregano log',
        author = 'Assaf Nativ',
        author_email = 'Nativ.Assaf@gmail.com',
        packages = ['OreganoLog'],
        package_dir = {'OreganoLog' : 'parser'},
        data_files = [
            ('Lib\\site-packages', ('OreganoLog.pth',)),
            ('Lib\\site-packages\\OreganoLog', (
                'LogParserx86.dll',
                'LogParserx86.pdb',
                'LogParserx64.dll',
                'LogParserx64.pdb'))]
        )

