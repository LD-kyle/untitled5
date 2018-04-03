#!C:\Users\Jason\PycharmProjects\untitled1\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'ZODB==5.3.0','console_scripts','fsrefs'
__requires__ = 'ZODB==5.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('ZODB==5.3.0', 'console_scripts', 'fsrefs')()
    )
