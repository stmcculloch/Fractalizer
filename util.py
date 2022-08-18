import cv2 as cv
import re
from os import listdir
#mirrors an image across 1 or 2 axes
def mirror(type, image, image_pixel_map):
    width, height = image.size
    # flip across y axis
    if type == "x": 
        for i in range(int(width)):
            for j in range(int(height/2)):
                r, g, b = image.getpixel((i, j))
                image_pixel_map[i, height-j-1] = (int(r), int(g), int(b))
    if type == "y": 
        for i in range(int(width/2)):
            for j in range(int(height)):
                r, g, b = image.getpixel((i, j))
                image_pixel_map[width-i-1, j] = (int(r), int(g), int(b))           
     #flip across x axis
    if type == "xy": 
        for i in range(int(width/2)):
            for j in range(int(height/2)):
                r, g, b = image.getpixel((i, j))
                image_pixel_map[width-i-1, height-j-1] = (int(r), int(g), int(b))
                image_pixel_map[i, height-j-1] = (int(r), int(g), int(b))
                image_pixel_map[width-i-1, j] = (int(r), int(g), int(b))
    return

# greyscale - makes an image black and white
def greyscale(image, image_pixel_map):
    width, height = image.size
    for i in range(width):
        for j in range (height):
            r, g, b = image.getpixel((i, j))
            grayscale = (0.299*r + 0.587*g + 0.114*b)
            image_pixel_map[i, j] = (int(grayscale), int(grayscale), int(grayscale))

def patternROI(image, image_pixel_map, ROI, strength, threshold):            
    xcounter = 0
    ycounter = 0
    input_width, input_height = image.size
    roi_width, roi_height = ROI.size

    for i in range(input_width):
        if i >= input_width:
                continue
        xcounter += 1
        if xcounter == roi_width:
            xcounter = 0

        ycounter = 0
        for j in range(input_height):
            if j >= input_height:
                continue
            r1, g1, b1 = image.getpixel((i,j))
            r2, g2, b2 = ROI.getpixel((xcounter, ycounter))
            #compare luminance of base image to the patterned pixel
            luminance_input = (0.299*r1 + 0.587*g1 + 0.114*b1)
            luminance_ROI = (0.299*r2 + 0.587*g2 + 0.114*b2)
            luminance_diff = abs(luminance_input-luminance_ROI)/256 #Value between 0 and 1. 0 = same luminance. 1 = completely different
            
            r_diff = abs(r1-r2)/256
            g_diff = abs(g1-g2)/256
            b_diff = abs(b1-b2)/256

            a = 1.5

            if r_diff > threshold: r_diff = min(1, a*(r_diff - threshold)/(1-threshold))
            if g_diff > threshold: g_diff = min(1, a*(g_diff - threshold)/(1-threshold))
            if b_diff > threshold: b_diff = min(1, a*(b_diff - threshold)/(1-threshold))
            
            rgb_diff = max(r_diff,g_diff,b_diff)
            #Determine difference between pixel brightnesses. Smaller difference = more bias toward fractal.
            luminance_diff = rgb_diff
            luminance_diff = pow(luminance_diff, strength)
            image_pixel_map[i,j] = int((r1*luminance_diff+r2*(1-luminance_diff))), int(g1*luminance_diff+g2*(1-luminance_diff)), int(b1*luminance_diff+b2*(1-luminance_diff))
            

            ycounter += 1
            if ycounter == roi_height:
                ycounter = 0

#mirrors an image across 1 or 2 axes
#blends with original image
def mirror2(type, image, image_pixel_map, amount):
    width, height = image.size
    # flip across y axis
    if type == "x": 
        for i in range(int(width)):
            for j in range(int(height/2)):
                r1, g1, b1 = image.getpixel((i, j))
                r2, g2, b2 = image.getpixel((i, height-j-1))
                image_pixel_map[i, height-j-1] = (int(r1*amount+r2*(1-amount)), int(g1*amount+g2*(1-amount)), int(b1*amount+b2*(1-amount)))

    if type == "y": 
        for i in range(int(width/2)):
            for j in range(int(height)):
                r1, g1, b1 = image.getpixel((i, j))
                r2, g2, b2 = image.getpixel((width-i-1, j))
                image_pixel_map[width-i-1, j] = (int(r1*amount+r2*(1-amount)), int(g1*amount+g2*(1-amount)), int(b1*amount+b2*(1-amount)))    

     #flip across x axis
    if type == "xy": 
        for i in range(int(width/2)):
            for j in range(int(height/2)):
                r1, g1, b1 = image.getpixel((i, j))
                r2, g2, b2 = image.getpixel((width-i-1, j))
                r3, g3, b3 = image.getpixel((i, height-j-1))
                r4, g4, b4 = image.getpixel((width-i-1, height-j-1))
                image_pixel_map[width-i-1, height-j-1] = (int(r1*amount+r4*(1-amount)), int(g1*amount+g4*(1-amount)), int(b1*amount+b4*(1-amount)))
                image_pixel_map[i, height-j-1] = (int(r1*amount+r3*(1-amount)), int(g1*amount+g3*(1-amount)), int(b1*amount+b3*(1-amount)))
                image_pixel_map[width-i-1, j] = (int(r1*amount+r2*(1-amount)), int(g1*amount+g2*(1-amount)), int(b1*amount+b2*(1-amount)))
    return

def findMaxFileNumber(path):
    list_of_files = listdir(path)
    maxn = 0
    for file in list_of_files:
        num = int(re.search('replication_(\d*)', file).group(1))  # assuming filename is "replication_#####"
        # compare num to previous max, e.g.
        maxn = num if num > maxn else maxn
    return "replication_" + str(maxn+1) + ".jpg"