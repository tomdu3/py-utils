from PIL import Image
import sys
import os

# ASCII characters ordered by increasing brightness (dark to light)
# Since terminal backgrounds are usually dark, we map dark pixels to dense characters
# and light pixels to sparse characters.
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resize_image(image, new_width=100):
    """
    Resizes the image to the specified width while keeping the aspect ratio.
    Also adjusts the height to compensate for the fact that terminal ASCII characters
    are taller than they are wide.
    """
    (width, height) = image.size

    # Calculate aspect ratio of the image
    aspect_ratio = height / width

    # Adjust height because ASCII characters have a height-to-width ratio of approx 1.8.
    # Multiplying by 0.55 squishes the image vertically so the output ASCII art doesn't look stretched.
    new_height = int(aspect_ratio * new_width * 0.55)

    new_image = image.resize((new_width, new_height))
    return new_image


def grayify(image):
    """
    Converts the image to grayscale ('L' mode).
    This maps each pixel to a single intensity value from 0 (black) to 255 (white).
    """
    return image.convert("L")


def pixels_to_ascii(image):
    """
    Maps each grayscale pixel value to its corresponding ASCII character.
    """
    # Use get_flattened_data() if available (Pillow 12+) to avoid deprecation warnings,
    # otherwise fall back to getdata().
    if hasattr(image, "get_flattened_data"):
        pixels = image.get_flattened_data()
    else:
        pixels = image.getdata()

    # Map pixel brightness range [0, 255] onto the indices of the ASCII character set.
    # (pixel_val * (len - 1)) // 255 yields a valid index [0, len-1].
    characters = "".join(
        [ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255] for pixel in pixels]
    )
    return characters


def image2ascii(image_path, new_width=100):
    """
    Convert an image to ASCII art.

    Args:
        image_path: Path to the input image.
        new_width: Target width in characters (default 100).

    Returns:
        A string containing the ASCII art representation of the image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        image = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Unable to open image: {e}")

    # Process pipeline: Resize -> Convert to Grayscale -> Map pixels to ASCII
    new_image_data = pixels_to_ascii(grayify(resize_image(image, new_width)))

    # Format the long flat string of ASCII characters into rows matching the target width
    pixel_count = len(new_image_data)
    ascii_image = "\n".join(
        [
            new_image_data[index : (index + new_width)]
            for index in range(0, pixel_count, new_width)
        ]
    )
    return ascii_image


def main():
    # attempt to open image from user-inoout
    if len(sys.argv) < 2:
        print("Usage: python image2ascii.py <image_path> [width]")
        sys.exit(1)

    image_path = sys.argv[1]
    new_width = 100

    # Optional custom width argument
    if len(sys.argv) == 3:
        try:
            new_width = int(sys.argv[2])
        except ValueError:
            print("Width must be an integer. Using default value 100.")

    try:
        # Convert image to ASCII
        ascii_art = image2ascii(image_path, new_width)
        print(ascii_art)

        # Save the ASCII representation to a text file next to the original image
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        directory = os.path.dirname(image_path)
        output_path = os.path.join(directory, f"{base_name}_ascii.txt")
        with open(output_path, "w") as f:
            f.write(ascii_art)
        print(f"ASCII art saved to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
