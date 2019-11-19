import re, importlib

import common.utils as UTILS

# Ask the release name to user
def getName():
  print("Enter release name (only A-Za-z0-9.- allowed) :")

  releaseName = ''

  # Only allow A-Z a-z 0-9 . _ and - for release name
  while not re.match(r'^[A-Za-z0-9.-]+$', releaseName):
    releaseName = input("> ")

  print("")

  return releaseName

# Ask user to choose a release type, and return the path to linked module
def getType():
  print("Choose release type :")

  # Get all .py files in releases_modules folder
  releaseModulePath = UTILS.getScriptPath() + "/releases_modules"
  releaseModuleFiles = UTILS.getFilesIn(releaseModulePath, ['.py'])

  moduleList = []
  modulePath = []
  moduleIndex = 1

  for releaseModule in releaseModuleFiles:
    # Extract module name from path
    moduleFilename = releaseModule.rsplit('/', 1)[-1]
    moduleName = moduleFilename.rsplit('.', 1)[0]

    # Import module
    module = importlib.import_module("releases_modules." + moduleName)

    # Store module list and module load path
    moduleList.append(module)
    modulePath.append("releases_modules." + moduleName)

    # Show entry to user
    print(str(moduleIndex) + ". " + module.RELEASE_TYPE)
    moduleIndex += 1

  releaseSelectedIndex = -1
  firstTry = True

  while releaseSelectedIndex not in range(0, len(moduleList)+1):
    if not firstTry:
        print("Invalid release type! Retry")
        print("")

    try:
      releaseSelectedIndex = int(input("> "))
    except:
      print("Please enter a number!")

    firstTry = False

  releaseType = moduleList[releaseSelectedIndex-1].RELEASE_TYPE

  print("")
  print("You have selected %s release..." % releaseType)
  print("")

  return modulePath[releaseSelectedIndex-1]

# Verify if NFO is present
def checkNfo(path):
  print("")
  nfoList = []

  while len(nfoList) != 1:
    print("Checking nfo presence...", end="")

    nfoList = UTILS.getFilesIn(path, ['.nfo'])

    if len(nfoList) == 0:
      input("not found, please check your release folder, and press <ENTER> to"
            " continue...")
      print("")
      del(nfoList[:])
    elif len(nfoList) > 1:
      input("more than one found in the release folder, delete uneeded"
            " and press <ENTER> to continue...")
      print("")
      del(nfoList[:])
    else:
      print("OK")

  return nfoList[0].rsplit('/', 1)[-1]

# Verify if proof is present
def checkProof(path):
  print("Checking proof presence...", end="")

  imageList = UTILS.getFilesIn(path, ['.png', '.jpg'], True)

  if len(imageList) == 0:
    sys.exit("not found, aborting.")
  else:
    print("OK")

# Summary of packing
def showSummary(summary):
  print("")
  print("#### PACKING SUMMARY")
  print("Release name        > " + summary['release_name'])
  print("Nfo                 > " + summary['nfo_name'])
  print("Archive format      > " + summary['archive_format'])
  print("Archive compression > " + summary['archive_compression'])

  print("Archive name        > ", end="")
  for archiveName in summary['archives_names']:
    print(archiveName + " ", end="")
  print("")

  print("Size                > " + str(summary['part_count']) + "x" + str(summary['part_size_mib']) + "MiB")
  print("Checksum format     > " + summary['checksum_format'])
  print("")
