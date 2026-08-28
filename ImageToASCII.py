from PIL import Image
from rich.console import Console
import cv2

CHAR_DENSITY = ".,-~:;_!^*|/\\ircvunxzoa()[]?#&8B@%$MW"
IMAGE_SCALE = 5
LIVE_IMAGE_NAME = "live_photo"
console = Console()

def take_picture():
    # connect to camera
    camera = cv2.VideoCapture(0)
    print("Live feed started. Press 'Space' to take picture. 'Esc' to exit.")

    while True:
        # take picture
        result, frame = camera.read()

        # tell the user when camera fails
        if not result:
            print("Camera failed.")
            break

        # disp;ay camera feed
        cv2.imshow("Live Camera Feed", frame)

        # wait for key press
        key = cv2.waitKey(1) & 0XFF

        # save image
        if key == 32:
            img_name = LIVE_IMAGE_NAME + ".jpg"
            cv2.imwrite(img_name, frame)
            print(f"Picture saved successfully as '{img_name}'!")
            break
        elif key == 27:
            print("Closing camera...")
            break


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
    take_picture()

    # open the image to be converted
    picture_name = LIVE_IMAGE_NAME
    img = Image.open(picture_name + ".jpg")
    
    # convert the image
    ASCII_img = convert_image(img)

    # close the image
    img.close()

    # write the ascii image to a new file
    ascii_img_name = picture_name + "_img.txt"
    with open(ascii_img_name, "w") as file:
        file.write(ASCII_img)
        print(f"ASCII image saved successfully as '{ascii_img_name}'!")

main()