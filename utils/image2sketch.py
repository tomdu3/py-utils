import cv2
import os
import sys


def image2sketch(image_path):
    """
    Convert an image to a sketch.

    Args:
        image_path: Path to the input image.

    Returns:
        Path to the output sketch image.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    invert = 255 - gray
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    directory = os.path.dirname(image_path)
    output_path = os.path.join(directory, f"{base_name}_sketch.png")
    cv2.imwrite(output_path, sketch)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python image2sketch.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    output_path = image2sketch(image_path)
    print(f"Image converted to sketch: {output_path}")
