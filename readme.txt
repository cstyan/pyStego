Instructions
************
In order to use this steganography application you’ll need Python 2.7, and the Pillow library.
You can install Pillow via pip or easy_install, for example: pip install Pillow.

The application requires a cover image to perform the steganography on.
This image can be of any format, but the application assumes the image is in
RGB mode.  RGBA would also work.  This is because the stego function works by
modifying the LSB of each RGB channel for every pixel in the cover image.
The secret file you wish to hide within the cover image can be of any format, as
long as the cover image has enough space to store it.

Example Usage
*************
Store secretImage.png in coverImage.png:
python pystego.py -m e -s path/to/secretImage.png -i path/to/coverImage.png

This will output stegoImage.bmp, which is the pixels of coverImage.png modified with the bits from secretImage.png.  As the console output states, you should renamed stegoImage.bmp before using it for real life purposes.

Store secretImage.png in coverImage.png as a png:
python pystego.py -m e -s path/to/secretImage.png -i path/to/coverImage.png -o png

This will produce the same output as the previous example, but as a png image instead of a bmp.

Pull secret file out of a stego’d image, save to Desktop:
python pystego.py -m d -s ~/Desktop -i path/to/stegoImage.png

This will pull the data for a secret file out of a stego’d image, including the file name and any header information associated with that filetype.  The file will be saved under the same name as the file that was hidden in the stego’d image.
