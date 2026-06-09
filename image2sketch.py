from PIL import Image
import cv2


def image2sketch(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = 255 - gray
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    cv2.imwrite("sketch.png", sketch)
    return "Image converted to sketch"


if __name__ == "__main__":
    image2sketch("pumpa.jpeg")
