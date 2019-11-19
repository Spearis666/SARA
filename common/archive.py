import os, sys, subprocess

def chooseArchiveFormat(defaultFormat):
  archiveFormatList = ['RAR', 'ZIP', '7Z']

  print("Choose archive format (default: %s) :" % defaultFormat)
  print("1. RAR")
  print("2. ZIP")
  print("3. 7z")

  archiveIndex = -1
  firstTry = True

  while archiveIndex not in range(0, len(archiveFormatList)+1):
    if not firstTry:
        print("Invalid archive format! Retry")
        print("")

    archiveIndex = int(input("> ") or archiveFormatList.index(defaultFormat)+1)
    firstTry = False

  archiveType = archiveFormatList[archiveIndex-1]

  print("")
  print("You have selected %s for compression..." % archiveType)
  print("")

  return archiveType

def chooseArchivePartSize(defaultPartMultiple, maxPartCount, mkvSize):
  print("Choose archive part size (MiB)(default: %i) :" % defaultPartMultiple)

  valid = False

  while not valid:
    partMultipleMiB = int(input("> ") or defaultPartMultiple)
    partMultipleByte = partMultipleMiB * 1048576
    partRequired = mkvSize / partMultipleByte

    if partMultipleMiB % defaultPartMultiple != 0:
      print("%i is not a multiple of %i, retry" % (partMultipleMiB, defaultPartMultiple))
      print("")
    elif partRequired > maxPartCount:
      print("Max part count is %i. With the part size selected you end up with %i part, retry" % (maxPartCount, partRequired))
      print("")
    else:
      valid = True

  print("")
  print("Archive part size will be %i MiB..." % partMultipleMiB)
  print("")

  return partMultipleByte

def compressToRAR(tempFolder, releaseFolder, archiveName, filesList, partSize, compressionAllowed):
  print("Compressing to RAR...", end="")

  cmd = ['rar']

  # Archive mode
  cmd.append('a')

  # No recursions
  cmd.append('-r-')

  # Max compression or store
  if compressionAllowed:
    cmd.append('-m5')
  else:
    cmd.append('-m0')

  # No output
  cmd.append('-inul') 

  # Volume size (in byte)
  cmd.append('-v' + str(partSize) + 'b')

  # Old naming (.rxx instead of .rar.partxx)
  cmd.append('-vn')

  # Archive path + name
  cmd.append(releaseFolder + '/' + archiveName + '.rar')

  # FIXME: use @list because param may too long in case of a subset of directory
  for filename in filesList:
    cmd.append(filename)

  # Since we use relative path for automatic creation of folder inside archive,
  # we need to be in the release folder
  os.chdir(tempFolder)

  # Run rar
  p = subprocess.run(cmd)

  # Get exitcode
  if p.returncode != 0:
    sys.exit("error, aborting.")
  else:
    print("OK")

def compressTo7Z(tempFolder, releaseFolder, archiveName, filesList, partSize, compressionAllowed):
  print("Compressing to 7z...", end="")

  cmd = ['7z']

  # Archive mode
  cmd.append('a')

  # No recursions
  cmd.append('-r-')

  # Max compression or store
  if compressionAllowed:
    cmd.append('-mx9')
  else:
    cmd.append('-mx0')

  # Disable output
  cmd.append('-bso0') 
  cmd.append('-bse0')
  cmd.append('-bsp0')

  # Size of part (in byte)
  cmd.append('-v' + str(partSize) + 'b')

  # Archive path + name
  cmd.append(releaseFolder + '/' + archiveName + '.7z')

  # FIXME: use @list because param may too long in case of a subset of directory
  for filename in filesList:
    cmd.append(filename)

  # Since we use relative path for automatic creation of folder inside archive,
  # we need to be in the release folder
  os.chdir(tempFolder)

  # Run 7z
  p = subprocess.run(cmd)

  # Get exitcode
  if p.returncode != 0:
    sys.exit("error, aborting.")
  else:
    print("OK")
