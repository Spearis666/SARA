# SARA - Scene Automatic Release Archiver
#
# Allow you to compress (RAR/7z/ZIP) and generate file checksum (sfv, sha1, md5)
#
# Since it work with dynamic module, you can easy extend to handle specific
# case, like archive format to use, size of a movie, presence of nfo or
# not etc...

import os, configparser, sys, importlib

import common.utils as UTILS
import common.release as RELEASE    

# GLOBAL
SCRIPT_NAME = 'SARA - Scene Automatic Release Archiver'
VERSION = '0.1.2'

def loadConfig():
  print("Loading config...", end="")

  userFolder = os.path.expanduser("~")
  defaultConfig = configparser.ConfigParser()

  # Store default config as fallback
  defaultConfig['GENERAL'] = {}
  defaultConfig['GENERAL']['interactive'] = 'off'

  defaultConfig['PATH'] = {'releases_folder': userFolder + '/Releases',
                           'temp_folder': '%(releases_folder)s/tmp'}

  # Check if config folder is writable, and create it if not exist
  if not UTILS.checkFolder(userFolder + "/.sara"):
    print("unable to create config folder, default settings will be used.")
    return defaultConfig

  # Try to load config file
  configPath = userFolder + "/.sara/sara.conf"

  if not os.path.isfile(configPath):
    try:
      f = open(configPath, 'w')
    except IOError:
      print('unable to write config file, default settings will be used.')
      return defaultConfig
    else:
      with f:
        defaultConfig.write(f)

  config = configparser.ConfigParser()
  config.read_file(open(configPath))

  print("OK")

  return config

if __name__ == '__main__':
  os.system('clear')
  print("################################################################################")
  print("#                 " + SCRIPT_NAME + " v" + VERSION + "                 #")
  print("#                No affiliation with Robot, not even with iShip                #")
  print("################################################################################")
  print("")

  # Load config
  config = loadConfig()

  print("Checking working folder...", end="")

  # Check if main release folder is writable, and create it if not exist
  mainReleaseFolder = config['PATH']['releases_folder']

  if not UTILS.checkFolder(mainReleaseFolder):
    sys.exit("unable to create releases folder (%s), aborting." % mainReleaseFolder)

  # Check if temp release folder is writable, and create it if not exist
  tempReleaseFolder = config['PATH']['temp_folder']

  if not UTILS.checkFolder(tempReleaseFolder):
    sys.exit("unable to create temp releases folder (%s), aborting." % tempReleaseFolder)

  print("OK")

  print("")
  print("### FILLING REQUIRED INFO")

  # Ask user for release name
  releaseName = RELEASE.getName()

  print("Checking release folder...", end="")

  # Check if release folder is writable, and create it if not exist
  finalReleaseFolder = config['PATH']['releases_folder'] + "/" + releaseName

  if not UTILS.checkFolder(finalReleaseFolder):
    sys.exit("unable to create final release folder (%s), aborting." % finalReleaseFolder)

  print("OK")

  # Ask user for release type. See releases_modules if you want to extend
  # release type
  print("")
  releaseModulePath = RELEASE.getType()

  # Loaded module depend on user selection
  releaseModule = importlib.import_module(releaseModulePath)
  
  # Release module must have a function named "make$TYPE$". $TYPE$  is stored in
  # variable RELEASE_TYPE at top of module. - is not allowed in func name,
  # so we remove it
  funcName = 'make' + releaseModule.RELEASE_TYPE.replace("-", "")
  prepareRelease = getattr(releaseModule, funcName)

  # Prepare release (check size, nfo, subs etc...compress, generate checksum...)
  prepareRelease(releaseName, config)

  # All finished correctly
  print("")
  print("ARCHIVING FINISHED")
