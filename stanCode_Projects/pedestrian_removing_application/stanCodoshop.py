"""
File: stanCodoshop.py
Name: Jerry
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

This program can compare several photos, find out the best pixel,
and generate a new photo without sundries or strangers.
(prepared photos should be the same size)
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    color_dis = ((red - pixel.red) ** 2 +
                 (green - pixel.green) ** 2 +
                 (blue - pixel.blue) ** 2) ** 0.5
    return color_dis


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    red_total = 0
    green_total = 0
    blue_total = 0
    avg_color = []         # A list of average red, green, and blue values of all the pixels
    for each_pixel in pixels:
        red_total += each_pixel.red
        green_total += each_pixel.green
        blue_total += each_pixel.blue
    avg_color.append(red_total//len(pixels))
    avg_color.append(green_total//len(pixels))
    avg_color.append(blue_total//len(pixels))
    return avg_color


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    short_dis = []     # A list stores the pixel that has the shortest color distance to the average
    avg_color_list = get_average(pixels)

    # First pixel will temporarily own the shortest color distance to the average
    shortest = get_pixel_dist(pixels[0], avg_color_list[0], avg_color_list[1], avg_color_list[2])
    short_dis.append(pixels[0])

    for pixel in pixels:
        color_dis = get_pixel_dist(pixel, avg_color_list[0], avg_color_list[1], avg_color_list[2])
        if color_dis <= shortest:    # The pixel with shorter color distance will replace short_dis list
            shortest = color_dis
            short_dis[0] = pixel
    return short_dis[0]


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #
    # Write code to populate image and create the 'ghost' effect
    for x in range(width):
        for y in range(height):
            pixel_list = []    # A list of pixels locating at the same position coordinate within all images
            for img in images:
                pixel = img.get_pixel(x, y)
                pixel_list.append(pixel)
            new_pixel = result.get_pixel(x, y)
            new_pixel.red = get_best_pixel(pixel_list).red
            new_pixel.green = get_best_pixel(pixel_list).green
            new_pixel.blue = get_best_pixel(pixel_list).blue
    # ----- YOUR CODE ENDS HERE ----- #

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):         # 所有檔案
        if filename.endswith('.jpg'):        # 找.jpg結尾的，因為還有很多是人類看不到的
            filenames.append(os.path.join(dir, filename))      # 合併資料夾和檔名，變成dir/filename的合理路徑
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
