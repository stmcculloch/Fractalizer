import numpy as np
import cv2 as cv
from os import remove, listdir
import re
from PIL import Image, ImageEnhance, ImageFilter
import util as util


#load the source image and create a pixel map (easily editable RGB values for each pixel)
input_image_file_name = "source_images/"+"trail.jpg"
input_image = Image.open(input_image_file_name)
input_pixel_map = input_image.load()

#get dimensions of the image
input_width, input_height = input_image.size

#Open the image using openCV
im = cv.imread(cv.samples.findFile(input_image_file_name))

#let user select a Region Of Interest (ROI)
bbox = cv.selectROI("ROI Selection Window", im, showCrosshair = False, fromCenter = False)
cv.destroyWindow("ROI Selection Window")

#save coordinates of the region of interest
(ROI_x, ROI_y, ROI_width, ROI_height) = bbox

#save ROI as a separate image file and create a pixel map of it as well
subregion = im [ROI_y : ROI_y + ROI_height, ROI_x : ROI_x + ROI_width]
cv.imwrite('ROI.jpg', subregion)
ROI = Image.open('ROI.jpg')
ROI_pixel_map = ROI.load()

#Mirror ROI across Y
util.mirror("xy",ROI, ROI_pixel_map)
#util.greyscale(ROI, ROI_pixel_map)

for iterations in range(1):
    looping_image = Image.open(input_image_file_name)
    looping_pixel_map = looping_image.load()

    #pattern ROI across the image
    #last two numbers are "Strength" and "threshold"
    #Increase Strength to increase the strength of the symmetry effect
    #Increase Threshold to apply the effect to a wider range of colors. Set to 1 to disable
    util.patternROI(looping_image, looping_pixel_map, ROI, 1.5, 0.43) 

    #mirror final image across Y
    #util.mirror("y",looping_image, looping_pixel_map)

    #Apply saturation effect

    #deNoised = looping_image.filter(ImageFilter.BoxBlur(1))
    #
    #im1 = looping_image.filter(ImageFilter.BLUR)
    smoothed = looping_image.filter(ImageFilter.SMOOTH_MORE)
    enhancer = ImageEnhance.Color(smoothed)
    saturated = enhancer.enhance(1.3)
    saturated.show()

    #Save the file as a new file
    saturated.save("output_images/" + util.findMaxFileNumber("output_images")) 
    remove("ROI.jpg") #delete temporary file
    



##TODO
#when output is finished, ask if you want to do another iteration. ALlow user to select another bbox and pattern a different pattern using a different color.