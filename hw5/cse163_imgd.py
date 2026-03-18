"""
Suh Young Choi
Checks student output against expected output
and produces images showing the pixel differences.
"""
from PIL import ImageDraw, Image, ImageFont, ImageChops
import numpy as np
import os

import hw5

PLOTS = [
    "county_food_access.png",
    "county_population_map.png",
    "low_access.png",
    "map.png",
    "population_map.png"
]


def no_diffs() -> None:
    """
    Replaces a blank generated diff image with one that has
    "No Differences Found" written on it
    """
    msg = "No Differences Found"
    ttf = "DejaVuSans.ttf"

    image = Image.open("diff.png")
    width, height = image.size

    fontsize = 1
    font = ImageFont.truetype(ttf, fontsize)
    fraction = 0.5

    while font.getlength(msg) < fraction * width:
        # iterate until the text size is just larger
        #    than the criteria
        fontsize += 1
        font = ImageFont.truetype(ttf, fontsize)

    ImageDraw.Draw(image).text((width / 4, height / 2),
                               msg, font=font, fill=(0, 0, 0))
    image.save("diff.png")


def run_imgd(expected: str, actual: str, args: list[str] = None) -> None:
    """
    Compares student output against expected using PIL.
    Produces diff image only if both student and expected output exist.
    """
    if not os.path.exists(actual):
        print(f"Could not find: {actual}. Be sure you're calling all plot"
              " functions in main\n")
    elif not os.path.exists(expected):
        print(f"Could not find: {expected}\n")
    else:
        print(f"Running image comparison tool on {actual}...")
        
        img1 = Image.open(expected)
        img2 = Image.open(actual)
        
        if img1.size != img2.size:
            print(f"Your image's dimensions ({img2.size}) don't match "
                  f"expected dimensions ({img1.size})")
            print("Be sure that you're using bbox_inches='tight'\n")
            diffx = abs(img1.size[0] - img2.size[0])
            diffy = abs(img1.size[1] - img2.size[1])
            if (diffx > 5) or (diffy > 5):
                return
        
        diff = ImageChops.difference(img1, img2)
        diff_array = np.array(diff)
        
        total_pixels = diff_array.size
        diff_pixels = np.count_nonzero(diff_array)
        similarity = (total_pixels - diff_pixels) / total_pixels * 100
        
        print(f"Images are {similarity:.2f}% similar")
        
        diff_filename = f"{os.path.splitext(actual)[0]}_diff.png"
        
        if similarity >= 99.0:
            diff_blank = Image.new('RGB', img1.size, 'white')
            diff_blank.save("diff.png")
            no_diffs()
            os.rename("diff.png", diff_filename)
        else:
            diff.save(diff_filename)
        
        print(f"Diff image saved as: {diff_filename}")
        print()
    print()


def main():
    print("Running all functions in your main method."
          " This may take a minute or so:")
    hw5.main()
    print()
    for plot_name in PLOTS:
        run_imgd(f"expected/{plot_name}", plot_name)


if __name__ == "__main__":
    main()