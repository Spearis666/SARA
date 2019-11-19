import os, sys

# Check if folder exist, and try to create it if not
def checkFolder(path):
  if os.path.exists(path):
    return True
  else:
    try:
      os.makedirs(path)
      return True
    except OSError:
      return False

# List files in directory with specific extensions
def getFilesIn(directory, extensions, subdir=False):
    filePaths = []
    for root, directories, files in os.walk(directory):
        if not subdir:
          del(directories[:])

        for filename in files:
          for extension in extensions:
            if filename.endswith(extension):
              filepath = os.path.join(root, filename)
              filePaths.append(filepath)
              break

    return filePaths

# Get script directory
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# Return size of one or multiples files
def getSize(filesList):
  totalSizeBytes = 0

  for filePath in filesList:
    totalSizeBytes += os.path.getsize(filePath)
  
  return totalSizeBytes

# Make path relative (need to be relative for archiver retain
# directory structure, may be useful when it's a bunch of files/folder,
# like blueray/dvd)
def makeRelativePath(rootPath, filesList):
  for i, _ in enumerate(filesList):
    filesList[i] = filesList[i].replace(rootPath + "/", "")

  return filesList

# The million dollar question ? YES or NO ? :p
def queryYesNo(question, default="no"):
    valid = {"yes": True, "y": True,
             "no": False, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt)
        choice = input("> ").lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' "
                  "(or 'y' or 'n').\n")
