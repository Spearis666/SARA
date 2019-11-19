import os, sys, subprocess

def chooseChecksumFormat(defaultChecksumFormat):
  checksumFormatList = ['SFV', 'MD5', 'SHA1']

  print("Choose checksum file format (default: %s) :" % defaultChecksumFormat)
  print("1. SFV")
  print("2. MD5")
  print("3. SHA1")

  checksumIndex = -1
  firstTry = True

  while checksumIndex not in range(0, len(checksumFormatList)+1):
    if not firstTry:
        print("Invalid checksum format! Retry")
        print("")

    checksumIndex = int(input("> ") or checksumFormatList.index(defaultChecksumFormat)+1)
    firstTry = False

  checksumType = checksumFormatList[checksumIndex-1]

  print("")
  print("You have selected %s for checksum file..." % checksumType)
  print("")

  return checksumType

# Generate checksum for all files in folder
#
# FIXME: In theory release folder must be empty before archiving, so only
# archive must be present, but maybe he can be good to save list of created
# archive and provide it to cfv
def generate(format, releaseFolder, checksumFilename):
  print("Generating %s..." % format, end="")

  cmd = ['cfv']

  # Disable output
  cmd.append('-VV') 
  cmd.append('-q')
  cmd.append('--progress=no')

  # Go to release folder
  cmd.append('-p' + releaseFolder)

  # Create mode
  cmd.append('-C')

  # sfv/md5/sha1...
  cmd.append('-t' + format.lower())

  # Set checksum filename
  cmd.append('-f' + checksumFilename)

  # Because cfv is a bitch, if we use -t for set checksum filename then last
  # working folder is used to get files list, ignoring -p
  os.chdir(releaseFolder)

  p = subprocess.run(cmd)

  if p.returncode != 0:
    sys.exit("error, aborting.")
  else:
    print("OK")
