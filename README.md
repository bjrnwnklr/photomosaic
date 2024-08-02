# Photomosaic

A simple photo mosaic generator, based on the ideas from [robertheaton.com - programming-project-4-photomosaics](https://robertheaton.com/2018/11/03/programming-project-4-photomosaics/)

# Steps to implement

1. Use an image processing library to load an input image into your code. Paste your input image into a new output image. Mess around with it - rotate it, resize it, add a caption, and generally get familiar with your image processing library.
2. Divide the input image into squares, and calculate the average color of each square
3. A quick diversion - create an output image out of squares of these average colors. This will be a pixellated version of your input image!
4. Find an initial set of 100 source images. Write a script that crops them all to squares and saves the cropped versions
5. Calculate the average color of each source image
6. For each section of the input image, find the source image with the closest average color
7. Paste each of these source images into the output image in the appropriate location. You have a photomosaic!

## Ideas

-   Create cache for the average color - use a JSON file that stores the file name, date processed and average color
-   Create a more efficient way of finding the nearest average color. Ideas:
    -   split the color room into cubes and store the cube of each image's average color in the JSON cache file
    -   this will make it easier to locate images that are close in average color to the source image
    -   Possibly use overlapping cubes (e.g. cube size 50, overlap every 25 steps):
    ```
        |---------|--------|
              |--------|
    ```

# EXIF tags

[EXIF Tags](https://exiftool.org/TagNames/EXIF.html)

Embedded in images:

```python
im = Image.open(src_img)
print(im.getexif())

{296: 2, 282: 72.0, 34853: 950, 34665: 214, 271: 'samsung', 272: 'SM-G950F', 305: 'G950FXXU5DSFB', 274: 6, 306: '2019:09:07 16:17:11', 531: 1, 283: 72.0}
```

Orientation is stored in `0x0112` = 274:

0x0112 Orientation int16u IFD0
1 = Horizontal (normal)
2 = Mirror horizontal
3 = Rotate 180
4 = Mirror vertical
5 = Mirror horizontal and rotate 270 CW
6 = Rotate 90 CW
7 = Mirror horizontal and rotate 90 CW
8 = Rotate 270 CW
