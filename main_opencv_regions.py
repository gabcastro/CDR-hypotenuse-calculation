import os
import sys
import cv2
import math
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

IMG_PATH = 'images\\'
ILM_LAYER_PATH = 'layer-ILM\\'
RPE_LAYER_PATH = 'layer-RPE\\'
MERGED_PATH = 'merged\\'

def hipotenuse_calc(adjacent, opposite):
    return math.hypot(opposite, adjacent)

def ctd(merged_image, coord, direction):
    # direction = 1 go to the left
    # direction = 2 go to the right
    lis_ctd = list([0, 0])
    y = coord[0] 
    x = coord[1]
    while(1):
        img_block = merged_image[y, x]
        if (img_block[0] in range(248, 255) and 
            img_block[1] in range(248, 255) and 
            img_block[2] in range(248, 255)):
            lis_ctd = list([y, x])
            break
        else:
            if direction == 1:
                x -= 1    
            else:
                x += 1
    
    return lis_ctd

def merged_image(img_name, lcoord, rcoord, dcoord, ucoord):
    background = Image.open(IMG_PATH + ILM_LAYER_PATH + img_name)
    foreground = Image.open(IMG_PATH + RPE_LAYER_PATH + img_name)

    background.paste(foreground, (0, 0), foreground)
    background.save(IMG_PATH + MERGED_PATH + img_name)

    merged_image = cv2.imread(IMG_PATH + MERGED_PATH + img_name)
    merged_image = cv2.resize(merged_image, (320, 320))

    # draw a line bt RPE points
    merged_image = cv2.line(
        merged_image, 
        (lcoord[1], lcoord[0]), # 1° x, y
        (rcoord[1] + int(merged_image.shape[0]/2), rcoord[0]), # 2° x, y
        (0, 0, 255), 
        thickness=2
    )

    # draw a line bt RPE line and deep point find on ilm layer
    merged_image = cv2.line(
        merged_image, 
        (dcoord[1], dcoord[0]), 
        (ucoord[1], ucoord[0]), 
        (0, 0, 255), 
        thickness=2
    )

    # find points bt RPE and closer part of ilm layer
    # consider as cup to disc 
    ctd_left = ctd(merged_image, ucoord, 1)
    ctd_right = ctd(merged_image, ucoord, 2)

    merged_image = cv2.line(
        merged_image, 
        (ctd_left[1], ctd_left[0] - 50),
        (ctd_left[1], ctd_left[0] + 50),
        (255, 0, 0),
        thickness=2
    )
    merged_image = cv2.line(
        merged_image, 
        (ctd_right[1], ctd_right[0] - 50),
        (ctd_right[1], ctd_right[0] + 50),
        (255, 0, 0),
        thickness=2
    )

    print('--> CTD:: left coordinate: \t\t\t', ctd_left)
    print('--> CTD:: right coordinate: \t\t\t', ctd_right)

    adjacent_value = ctd_right[1] - ctd_left[1]
    opposite_value = dcoord[0] - ucoord[0]

    print('--> Adjacent value:: \t\t\t\t', adjacent_value)
    print('--> Opposite value:: \t\t\t\t', opposite_value)

    coord_label_adjacent = [ucoord[0] - 10, ucoord[1]] # y, x
    coord_label_opposite = [dcoord[0] - int(opposite_value/2), ucoord[1] + 10] # y, x

    cv2.putText(
        merged_image, 
        str(adjacent_value), 
        (coord_label_adjacent[1], coord_label_adjacent[0]), # x, y
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.4, 
        (36,255,12), 
        1
    )

    cv2.putText(
        merged_image, 
        str(opposite_value), 
        (coord_label_opposite[1], coord_label_opposite[0]), # x, y
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.4, 
        (36,255,12), 
        1
    )

    return merged_image, adjacent_value, opposite_value


def find_coord_bt_ilm_rpe(deeper_coord, rpe_line):
    center_up_coord = list([0, 0])
    for y in range(rpe_line.shape[0]):
        aux_stop = 0
        img_block = rpe_line[y, deeper_coord[1]]
        if (img_block[2] == 255) and (center_up_coord[0] < y):
            center_up_coord = list([y, deeper_coord[1]])
            aux_stop = 1
        elif (img_block[2] < 200 and (center_up_coord[0] < y) and (aux_stop == 1)):
            break

    return center_up_coord

def find_deeper_coordinate(img):
    center_down_coordinate = list([0, 0])
    for x in range(img.shape[1]): 
        aux_stop = 0
        for y in range(img.shape[0]): 
            img_block = img[y, x]
            if (img_block in range(238, 250)) and (center_down_coordinate[0] < y):
                center_down_coordinate = list([y, x])
                aux_stop = 1
            elif (img_block < 200 and (center_down_coordinate[0] < y) and (aux_stop == 1)):
                break

    return center_down_coordinate

def find_best_coordinate(half_img):
    # find the deep point
    best_coordinate = list([0, 0])
    for x in range(half_img.shape[1]): # x
        aux_stop = 0
        for y in range(half_img.shape[0]): # y
            img_block = half_img[y, x]
            if (img_block in range(238, 250)) and (best_coordinate[0] < y):
                best_coordinate = list([y, x])
                aux_stop = 1
            elif (img_block < 200 and (best_coordinate[0] < y) and (aux_stop == 1)):
                break
    
    return best_coordinate


# - find extreme points in this layer
# return the coordinate to use as part to reach the layer ILM 
def rpe_coordinates(actual_img):
    rpe_img_original = cv2.imread(IMG_PATH + RPE_LAYER_PATH + actual_img)
    rpe_img_edited = cv2.cvtColor(rpe_img_original, cv2.COLOR_BGR2GRAY)
    rpe_img_edited = cv2.resize(rpe_img_edited, (320, 320))

    # get from 0 - 160 points (x axis)
    left_coord = find_best_coordinate(rpe_img_edited[0:rpe_img_edited.shape[0], 0:int(rpe_img_edited.shape[0]/2)])

    # get from  161 - 320 (x axis)
    right_coord = find_best_coordinate(rpe_img_edited[0:rpe_img_edited.shape[0], (int(rpe_img_edited.shape[0]/2) + 1):rpe_img_edited.shape[0]])
    
    rpe_line = cv2.line(
        cv2.resize(rpe_img_original, (320, 320)), 
        (left_coord[1], left_coord[0]), 
        (right_coord[1] + int(rpe_img_edited.shape[0]/2), right_coord[0]), 
        (0, 0, 255), 
        thickness=2
    )

    return left_coord, right_coord, rpe_line


def ilm_coordinates(actual_img, rpe_line):
    ilm_img_original = cv2.imread(IMG_PATH + ILM_LAYER_PATH + actual_img)
    ilm_img_edited = cv2.cvtColor(ilm_img_original, cv2.COLOR_BGR2GRAY)
    ilm_img_edited = cv2.resize(ilm_img_edited, (320, 320))

    # get the edge deeper from ilm layer
    deeper_coord = find_deeper_coordinate(ilm_img_edited)

    # get points at the same x from 'deeper_coord' but from x of rpe
    cross_coord = find_coord_bt_ilm_rpe(deeper_coord, rpe_line)

    return deeper_coord, cross_coord

if __name__ == "__main__":
    imgs_ILM = os.listdir(IMG_PATH + ILM_LAYER_PATH)
    
    img = imgs_ILM[1]
    imgs_ILM = [img]

    for img in imgs_ILM:
        rpe_coord_left, rpe_coord_right, rpe_line = rpe_coordinates(img)

        print('--> RPE LAYER:: left coordinate: \t\t', rpe_coord_left)
        print('--> RPE LAYER:: right coordinate: \t\t', rpe_coord_right)

        ilm_deeper_coord, ilm_cross_coord = ilm_coordinates(img, rpe_line)

        print('--> ILM LAYER:: deeper coordinate: \t\t', ilm_deeper_coord)
        print('--> ILM LAYER:: cross coordinate: \t\t', ilm_cross_coord)

        mimage, adjacent_value, opposite_value = merged_image(img, rpe_coord_left, rpe_coord_right, ilm_deeper_coord, ilm_cross_coord)

        hipotenuse = hipotenuse_calc(adjacent_value, opposite_value)

        print('--> Hipotenuse value:: \t\t\t\t', hipotenuse)

        cv2.imshow('', mimage)
        cv2.waitKey(0)  
        cv2.destroyAllWindows() 