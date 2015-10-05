from PIL import Image
import ntpath
import os
allSecretData = []

# Function: modifyLSB
# Parameters:
#  - count: current count index from the pixels loop in stego
#  - sizeOfFile: the size of the secret file data, includng the header info
#  - pixel: a list of the RGB values for the current pixel, mutable object
#  Author: Callum Styan
#
# This function loops through the RGB channels of the current pixel and assigns
# a bit from the secret file data to the LSB of the RGB channel.  Returns 1 if
# the counter index reaches the end of the secret data.
def modifyLSB(count, sizeOfFile, pixel):
  global allSecretData
  run = 0
  # loop 3 times, once for each channel in RGB
  while run < 3:
    # if the count index is larger than the number of bits in the file
    if count >= sizeOfFile:
      return 1

    pixel[run][-1] = allSecretData[count]
    run = run + 1
    count = count + 1

# Function: getBits
# Parameters:
#  - args: object containing command line arguments
# Author: Callum Styan
#
# Get the least significant bits out of a stego'd image by looping through all
# of it's pixels, and determining if the value for each RGB channel in a pixel
# is odd or even, and appending the correct value to a list of bits.  Returns the
# list of all least significant bits in the stego'd image.
def getBits(args):
  stegoImage = Image.open(args.coverImagePath)
  pixels = list(stegoImage.getdata())
  bitList = []
  for pixel in pixels:
    red = pixel[0] % 2
    green = pixel[1] % 2
    blue = pixel[2] % 2
    # check if red was odd or even
    if red == 0:
      bitList.append('0')
    else:
      bitList.append('1')
    # check if green was odd or even
    if green == 0:
      bitList.append('0')
    else:
      bitList.append('1')
    # check if blue was odd or even
    if blue == 0:
      bitList.append('0')
    else:
      bitList.append('1')

  return bitList

# Function: getBinaryData
# Parameters:
#  - args: object containing command line arguments
# Author: Callum Styan
#
# Open the secretFile and return it's data as a list of bits by converting each
# byte to a list of bits.
def getBinaryData(args):
  fileDescriptor = open(args.secretFilePath, 'rb')
  fileData = bytearray(fileDescriptor.read())
  binaryData = ""
  # convert each byte of data in the file to bits
  for byte in fileData:
    binaryData = binaryData + bin(byte)[2:].zfill(8)

  # return the binary data as a list of individual bits
  return list(binaryData)

# Function: constructHeader
# Parameters:
#  - args: object containing command line arugments
# Author: Callum Styan
#
# Constructs a string containing filename\0filesize\0, then turns each byte in the
# string into a binary, returns the header for our stego as a list of bits.
def constructHeader(args):
  # get the file name from the secretFilePath and append a null terminator
  header = ntpath.basename(args.secretFilePath) + '\0'
  # get the file size of the secret file and append a null terminator
  header = header + str(os.path.getsize(args.secretFilePath)) + '\0'
  header = bytearray(header)
  headerBits = ""
  # convert each byte of the data in the header to bits
  for byte in header:
    headerBits = headerBits + bin(byte)[2:].zfill(8)

  # return as a list of individual bits
  return list(headerBits)

# Function: constructData
# Parameters:
#  - args: object containing command line arguments
# Author: Callum Styan
#
# This function builds one large object with all the bits required to store the
# secret file in a cover image by calling constructHeader and getBinaryData.
# Returns that data..
def constructData(args):
  global allSecretData
  # append header and file data to all data
  allSecretData = allSecretData + constructHeader(args) + getBinaryData(args)
  return allSecretData