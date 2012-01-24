from distutils.core import setup, Extension, os
class PkgConfig(object):
    def __init__(self, names):
        def stripfirsttwo(string):
            return string[2:]
        self.libs = map(stripfirsttwo, os.popen("pkg-config --libs-only-l %s" % names).read().split())
        self.libdirs = map(stripfirsttwo, os.popen("pkg-config --libs-only-L %s" % names).read().split())
        self.incdirs = map(stripfirsttwo, os.popen("pkg-config --cflags-only-I %s" % names).read().split())
 	
flags = PkgConfig("gtk+-2.0 pygtk-2.0")

module1 = Extension('hardkeys',
                    sources = ['hardkeys.c'],
                    include_dirs = flags.incdirs + ['.'],
                    libraries = flags.libs,
                    library_dirs = flags.libdirs,
                    runtime_library_dirs = flags.libdirs
                    )

setup (name = 'HardKeys',
       version = '1.0',
       description = 'A package for disabling hardware keys',
       ext_modules = [module1],
       )
