from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
 
py2exe_options = {
        "includes": ["sip"],  # 如果打包文件中有PyQt代码，则这句为必须添加的
        "dll_excludes": ["MSVCP90.dll",], 
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,  # 关于这个参数请看第三部分中的问题(2)
        }
 
setup(
      name = 'NetEase',
      version = '1.0',
      windows = ['widget.py','api.py'],   # 括号中更改为你要打包的代码文件名
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )