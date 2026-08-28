from PIL import Image
from rich.console import Console
import cv2

CHAR_DENSITY = ".,-~:;_!^*|/\\ircvunxzoa()[]?#&8B@%$MW"
IMAGE_SCALE = 2
LIVE_CAPTURE_NAME = "live_video"
console = Console()

def take_video():
    # connect to camera
    cam = cv2.VideoCapture(0)
    print("Live feed started. Hold 'Space' to record. 'Q' to exit.")

    # get the frame width and height
    frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # open file to append to
    file = open(LIVE_CAPTURE_NAME + ".txt", "w")

    # start video with the space bar
    while True:
        # capture frames
        ret, frame = cam.read()

        # notify user if camera fails
        if not ret:
            print("Camera failed...")
            break

        # write the current frame if space is being pressed
        if cv2.waitKey(1) == ord(" "):
            # save image
            img_name = LIVE_CAPTURE_NAME + ".jpg"
            cv2.imwrite(img_name, frame)

            # convert frame to text
            with Image.open(img_name) as img:
                file.write(convert_image(img))

        # display the frame
        cv2.imshow("Live Camera Feed", frame)

        # stop video with q
        if cv2.waitKey(1) == ord("q"):
            print("Closing camera...")
            break

    # close the camera objects
    cam.release()
    cv2.destroyAllWindows()

    # close the text file
    file.close()


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

    # put new lines at the end
    for _ in range(299 - scaled_height):
        full_text += "\n"

    return full_text

def main():
    take_video()
    
main()