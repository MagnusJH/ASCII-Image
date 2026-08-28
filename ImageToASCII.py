from PIL import Image
from rich.console import Console

CHAR_DENSITY = ".,-~:;_!^*|/\\ircvunxzoa()[]?#&8B@%$MW"
IMAGE_SCALE = 15
console = Console()

def convert_image(img):

    # get the size of the image
    width, height = img.size

    # convert the height to print only 1,000 lines
    scaled_height = int(height / IMAGE_SCALE)
    # convert the width to the same ratio as the height
    scaled_width = int(width / IMAGE_SCALE)

    # convert the image to grayscale
    grayscale_img = img.convert('L')

    line = ""
    full_text = ""
    # loop through the pixels on the image
    for h in range(0, scaled_height):
        full_text += line + "\n"
        line = ""
        for w in range(0, scaled_width):

            # grab the brightness of the specific pixel
            brightness = grayscale_img.getpixel((w*IMAGE_SCALE, h*IMAGE_SCALE))

            # convert brightness scale to ascii brightness scale
            p = int(brightness * ((len(CHAR_DENSITY)-1) / 255))
            line += CHAR_DENSITY[p] + CHAR_DENSITY[p] + " "

    return full_text

def main():
    # open the image to be converted
    img = Image.open("meOnMountain.jpg")
    
    # convert the image
    ASCII_img = convert_image(img)

    # close the image
    img.close()

    # write the ascii image to a new file
    with open("ascii_img.txt", "w") as file:
        file.write(ASCII_img)

main()