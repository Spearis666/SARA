import os, sys, math, shutil

import common.utils as UTILS
import common.release as RELEASE
import common.archive as ARCHIVE
import common.checksum as CHECKSUM

RELEASE_TYPE = 'MOVIE-X264-HD'
MODULE_VERSION = '0.1.0'

def makeMOVIEX264HD(releaseName, config):
  # Basic scene rules
  partMultipleMiB = 50
  maxPartCount = 99
  archiveFormat = 'RAR'
  compressionAllowed = False
  checksumFormat = 'SFV'

  # Are we in interactive mode ?
  interactive = config['GENERAL'].getboolean('interactive')

  # Get temp release folder
  tempReleaseFolder = config['PATH']['temp_folder'] + "/" + releaseName

  # Get final release folder
  releasesFolder = config['PATH']['releases_folder'] + "/" + releaseName

  # Get list of mkv files (only one must be present)
  mkvList = []

  while len(mkvList) != 1:
    print("Getting mkv filename...", end="")

    mkvList = UTILS.getFilesIn(tempReleaseFolder, ['.mkv'])

    if len(mkvList) == 0:
      input("not found, please check your release folder, and press <ENTER> to"
            " continue...")
      print("")
      del(mkvList[:])
    elif len(mkvList) > 1:
      input("more than one found in the release folder, delete uneeded"
            " and press <ENTER> to continue...")
      print("")
      del(mkvList[:])
    else:
      print("OK")

  # Check mkv size
  print("Checking mkv size...", end="")

  mkvSizeBytes = UTILS.getSize(mkvList)
  mkvSizeMiB = mkvSizeBytes / 1048576
  divisible = mkvSizeMiB % 1120

  # HD release must be superior at minimum multiple and not be 40 MiB undersize
  # when in multiple of 1120, or be exactly 2713/8140
  #
  # FIXME: Include DVD5/x rules
  if mkvSizeMiB < 1120:
    sys.exit("under 1120 MiB, it's indeed not an HD release, aborting.")
  elif divisible > 40 and mkvSizeMiB != (2713 or 8140):
    sys.exit("there is %i MiB undersize, aborting." % divisible)
  else:
    print("OK")

  # Check nfo presence
  nfoName = RELEASE.checkNfo(tempReleaseFolder)

  # Check proof presence
  RELEASE.checkProof(tempReleaseFolder)

  # Calculating part size (multiple of 50 MiB) & count (max 99)
  print("Calculating part size/count...", end="")

  partMultipleByte = 0
  partNeeded = -1
  currentMultiple = 1

  while partNeeded < 0 or partNeeded > maxPartCount:
    partMultipleByte += partMultipleMiB * 1048576
    partNeeded = math.ceil(mkvSizeBytes / partMultipleByte)

  partSizeMiB = partMultipleByte / 1048576

  print("OK")

  # Get mkv filename (without path)
  mkvName = mkvList[0].rsplit('/', 1)[-1]

  # Get archive name (mkv filename minus .mkv)
  archiveName = mkvName.rsplit('.', 1)[0]

  # Prepare path for files archived
  finalFilesList = UTILS.makeRelativePath(tempReleaseFolder, mkvList)

  # Show summary
  summary = {'release_name': releaseName, 'nfo_name': nfoName,
             'archive_format': archiveFormat, 'archives_names': [archiveName],
             'archive_compression': 'Store', 'part_count': partNeeded,
             'part_size_mib': partSizeMiB, 'checksum_format': checksumFormat}

  RELEASE.showSummary(summary)

  # Just wait user input before continue
  input("Press <ENTER> to compress/generate sfv/copy nfo...")
  print("")

  # Compress to RAR
  funcName = 'compressTo' + archiveFormat
  compress = getattr(ARCHIVE, funcName)
  compress(tempReleaseFolder, releasesFolder, archiveName, finalFilesList,
           partMultipleByte, compressionAllowed)

  # Generate SFV (use nfo name for checksum filename)
  CHECKSUM.generate(checksumFormat, releasesFolder,
                    nfoName.replace('.nfo', '.sfv'))

  # Copy NFO
  print("Copying nfo...", end="")
  try:
    shutil.copy2(tempReleaseFolder + "/" + nfoName, releasesFolder)
    print("OK")
  except IOError:
    sys.exit("unable to copy, aborting.")
