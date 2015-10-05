import argparse
import os
from PIL import Image
import imageFunctions
import stegoFunctions

# Funcion: checkSizes
# Author: Callum Styan
#
# This funcion is used to check if the cover image has enough space to store the
# header + secret file, this is done by comparing the number of pixels in the
# cover image * 3 to the size of the secret file
# returns 1 if the secret file will not fit in the cover image
def checkSizes():
  coverImage = Image.open(args.coverImagePath)
  # get the number of bits we can possbily store in the cover image
  numBits = coverImage.size[0] * coverImage.size[1] * 3
  # compare the filesize to the number of bits we can store
  if os.path.getsize(args.secretFilePath) > numBits / 8:
    return 1

# parse the command line arguments
parser = argparse.ArgumentParser(description='Super Cool Stegonography')
parser.add_argument('-m'
                   , '--mode'
                   , dest='mode'
                   , help="'e' stego an image, or 'd' pull data out of a stego'd image"
                   , required=True)
parser.add_argument('-i'
                   , '--image'
                   , dest='coverImagePath'
                   , help="Path to image (original image if mode is 'e', stego image if mode is 'd')"
                   , required=True)
parser.add_argument('-s'
                   , '--secret'
                   , dest='secretFilePath'
                   , help="Path to secret file (secret file location if mode is 'e', path to output secret file if mode is 'd')"
                   , required=True)
parser.add_argument('-o'
                   , '--outputMode'
                   , dest='outputMode'
                   , help="Optional argument if in 'e', mode, changes the filetype of the stego image. Default type is bmp, but you can set it to png.")
args = parser.parse_args()

# start of actual execution
# first make sure the mode is e or d
if args.mode != "e" and args.mode != "d":
  print "Invalid mode, please see the help output."
  exit()
# if the mode is e make sure both the arguments are files
elif args.mode == "e" and not (os.path.isfile(args.secretFilePath) and os.path.isfile(args.coverImagePath)):
  print "An argument for -s or for -i was not a file."
  print "Please the help output."
  exit()
# if the mode is d make sure -s argument was a directory
elif args.mode == "d" and not (os.path.isdir(args.secretFilePath) and os.path.isfile(args.coverImagePath)):
  print "Your argument for -s was not a directory OR your argument for -i was not a file."
  print "Please see the help output."
  exit()

# if we didn't exit in any of the last three cases then we're probably safe to continue
# check to see if the cover image has enough space to hide the secret file
if checkSizes() == 1:
  print "Cover image does not have enough space to hide the secret file."
  print "Please try a larger cover image or compress your secret file."
  exit()

# at this point the mode is either e or d
if args.mode == "e":
  if args.outputMode and args.outputMode != "png":
    print "Invalid output mode. Please see the help output."
    exit()
  stegoFunctions.stegoImage(args)
else:
  print "Unstego " + args.coverImagePath
  stegoFunctions.unstegoImage(args)