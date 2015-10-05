import imageFunctions
import binascii
from PIL import Image

# Function: stegoImage
# Parameters:
#  - args: object containing command line arguments
# Author: Callum Styan
#
# This function stores all data from a secret file into the cover image by
# looping through each pixel in the cover image and modifying the least significant
# bit for each RGB channel in the pixel.  At the end of the loop it creates a new
# file with the same dimensions as the original and stores the modified pixels in
# it as stegoImage.bmp or stegoImage.png.
def stegoImage(args):
  global allSecretData
  allSecretData = imageFunctions.constructData(args)
  # setup file data
  coverImage = Image.open(args.coverImagePath).convert('RGB')
  coverImagePixels = list(coverImage.getdata())

  # counter for indexing into the bits of the secretFile
  secretDataIndex = 0
  coverImageIndex = 0
  breakFlag = False

  # loop through the pixels in the cover image
  for pixel in coverImagePixels:
    if breakFlag is True:
      break

    # get a list of all the bits for each byte in the RGB representation of
    # the current pixel
    red = list(bin(pixel[0])[2:])
    green = list(bin(pixel[1])[2:])
    blue = list(bin(pixel[2])[2:])
    # modify the LSB
    if imageFunctions.modifyLSB(secretDataIndex, len(allSecretData), list([red, green, blue])) == 1:
      breakFlag = True
    # secretDataIndex in modifyLSB is immutable, so we need to update it
    secretDataIndex = secretDataIndex + 3
    # covert each RGB bit represenatation back into an integer value
    red = int(''.join(red), 2)
    green = int(''.join(green), 2)
    blue = int(''.join(blue), 2)
    # assign the RGB values back to the current pixel of the cover image
    coverImagePixels[coverImageIndex] = (red, green, blue)
    coverImageIndex = coverImageIndex + 1

  stegoImage = Image.new('RGB', (coverImage.size[0], coverImage.size[1]), (255, 255, 255))
  stegoImage.putdata(coverImagePixels)
  if args.outputMode == "png":
    stegoImage.save('stegoImage.png')
  else:
    stegoImage.save('stegoImage.bmp')
  print "stegoImage should exist now in your working directory."
  print "Be sure to rename the image before sending it to someone."

# Function: unstegoImage
# Parameters:
#  - args: object containing command line arguments
# Author: Callum Styan
#
# This function copies the secret data out of a stego'd image and saves it by
# pulling all the least significant bits out of the stego'd image into a string
# and then splitting the string into three based on the first to null terminators.
# The third string from the split contains the secret file data, the first is the
# secret files name and the second is the secret files size in bytes.
def unstegoImage(args):
  leastSignificantBits = imageFunctions.getBits(args)
  lsbString = binascii.unhexlify('%x' % int(''.join(leastSignificantBits), 2))
  filename, filesize, data = lsbString.split('\0', 2)
  print "secret filename " + filename
  w = open(filename, 'w')
  w.write(data[: int(filesize)])
  print "Secret file has been saved."