from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
options = {'build_exe': {
    'packages': ['os', 'yaml', 'boto', 'numpy', 'scipy', 'matplotlib', 'io', 'zlib',
                 'zipfile', 'bz2', 'math', 'datetime', 'dateutil', 'time', 'h5py',
                 'pyaudio', 'sys', 'io', 'simplejson'],
    'include_files': ['Audio/', 'SID/', 'SIDClient/', 'SIDRest/'],
    'excludes': [],
    "build_exe": '../build/Output/Win32/'
}
}

executable_to_build = [
    Executable('SendToSidWatchServer.py',
               base='console',
               targetDir='../build/Output/Win32/'),
    Executable('SidDataCollector.py',
               base='console',
               targetDir='../build/Output/Win32/')
]

setup(name='pySidWatch',
      version='0.1.0.0',
      description='SidWatch Data Collector',
      options=options,
      executables=executable_to_build
)
