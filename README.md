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
