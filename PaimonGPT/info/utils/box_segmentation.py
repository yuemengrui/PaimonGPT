# *_*coding:utf-8 *_*
import cv2
import numpy as np
from math import *


def NMS(boxes, thresh=0.3):
    true_boxes = []
    while len(boxes) > 0:
        true_boxes.append(boxes[0])
        boxes.pop(0)
        if len(boxes) == 0:
            break

        for box in boxes[::-1]:
            iou_x1 = max(true_boxes[-1][0], box[0])
            iou_y1 = max(true_boxes[-1][1], box[1])
            iou_x2 = min(true_boxes[-1][2], box[2])
            iou_y2 = min(true_boxes[-1][3], box[3])
            if iou_x2 - iou_x1 <= 0 or iou_y2 - iou_y1 <= 0:
                continue

            iou_area = (iou_x2 - iou_x1) * (iou_y2 - iou_y1)
            box_area = abs(true_boxes[-1][2] - true_boxes[-1][0]) * abs(true_boxes[-1][3] - true_boxes[-1][1])
            if iou_area / box_area > thresh:
                boxes.remove(box)

    return true_boxes


def filter_box(boxes, exc_box_h_threshold):
    filter_boxes_list = []
    temp = []
    for box in boxes:
        if len(temp) == 0:
            temp.append(box)
        else:
            if abs(box[1] - temp[-1][3]) < exc_box_h_threshold or abs(box[0] - temp[-1][2]) < exc_box_h_threshold:
                temp.append(box)
            else:
                filter_boxes_list.append(temp)
                temp = []
                temp.append(box)
    else:
        filter_boxes_list.append(temp)

    return filter_boxes_list


def rotate_image(img, angle, scale=1.0):
    size = img.shape
    h = size[0]
    w = size[1]
    center = (w / 2, h / 2)
    heightNew = int(w * fabs(sin(radians(angle))) + h * fabs(cos(radians(angle))))
    widthNew = int(h * fabs(sin(radians(angle))) + w * fabs(cos(radians(angle))))

    M = cv2.getRotationMatrix2D(center, angle, scale)
    M[0, 2] += (widthNew - w) / 2
    M[1, 2] += (heightNew - h) / 2
    rotate_img = cv2.warpAffine(img, M, (widthNew, heightNew), borderValue=(255, 255, 255))
    return rotate_img


def get_slope(line, col=False):
    x1, y1, x2, y2 = line

    if y2 == y1 or x1 == x2:
        return 0
    else:
        if x1 < x2:
            x_start = x1
            x_end = x2
            y_start = y1
            y_end = y2
        else:
            x_start = x2
            x_end = x1
            y_start = y2
            y_end = y1

    if col:
        return -degrees(asin(((x_end - x_start) / (y_end - y_start))))

    return degrees(asin(((y_end - y_start) / (x_end - x_start))))


def get_angle(row_lines, col_lines):
    slope_list = []
    for i in row_lines:
        try:
            slope = get_slope(i)
        except:
            pass
        else:
            if slope != 0:
                slope_list.append(slope)

    for j in col_lines:
        try:
            slope = get_slope(j, col=True)
        except:
            pass
        else:
            if slope != 0:
                slope_list.append(slope)

    slope_list.sort()

    if len(slope_list) < 5:
        angle_list = slope_list[1:-1]
    else:
        angle_list = slope_list[2:-2]

    if len(angle_list) == 0:
        return 0

    angle = np.mean(angle_list)

    return angle


def get_lines(mask, origin_w, origin_h, row=False, col=False):
    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 30, 0)
    lines_list = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if row:
                if abs(x2 - x1) < 0.3 * origin_w:
                    continue

            if col:
                if abs(y2 - y1) < 0.3 * origin_h:
                    continue

            lines_list.append(line[0].tolist())

    return lines_list


def lines_image_processing(origin_image):
    image = origin_image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    th2_copy = binary.copy()

    row_scale = 31
    rows, cols = gray.shape
    horizontalsize = cols // row_scale
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
    row_erosion = cv2.erode(binary, horizontalStructure, iterations=1)
    row_dilation = cv2.dilate(row_erosion, horizontalStructure, iterations=3)

    col_scale = 31
    horizontalsize2 = rows // col_scale
    horizontalStructure2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, horizontalsize2))
    col_erosion = cv2.erode(th2_copy, horizontalStructure2, iterations=1)
    col_dilation = cv2.dilate(col_erosion, horizontalStructure2, iterations=2)

    return binary, row_dilation, col_dilation


def box_image_processing(origin_image, row_dil_iter, col_dil_iter):
    image = origin_image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    th2_copy = binary.copy()

    row_scale = 31
    rows, cols = gray.shape
    horizontalsize = cols // row_scale
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontalsize, 1))
    row_erosion = cv2.erode(binary, horizontalStructure, iterations=1)
    row_dilation = cv2.dilate(row_erosion, horizontalStructure, iterations=int(row_dil_iter))

    col_scale = 31
    horizontalsize2 = rows // col_scale
    horizontalStructure2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, horizontalsize2))
    col_erosion = cv2.erode(th2_copy, horizontalStructure2, iterations=1)
    col_dilation = cv2.dilate(col_erosion, horizontalStructure2, iterations=int(col_dil_iter))
    mask = row_dilation + col_dilation

    return mask


def get_box(origin_image,
            row_dil_iter=2,
            col_dil_iter=1,
            area_threshold=200,
            h_threshold=10,
            w_threshold=20,
            hw_rate_threshold=100,
            row_h_threshold=10,
            is_remove_seal=0):

    # if is_remove_seal == 1:
    #     origin_image = remove_seal_by_color_channel(origin_image)

    origin_h, origin_w = origin_image.shape[:2]

    binary, row_mask, col_mask = lines_image_processing(origin_image)

    col_lines = get_lines(binary, origin_w, origin_h, col=True)
    row_lines = get_lines(binary, origin_w, origin_h, row=True)

    angle = get_angle(row_lines, col_lines)
    if angle == 0:
        col_lines = get_lines(col_mask, origin_w, origin_h, col=True)
        row_lines = get_lines(row_mask, origin_w, origin_h, row=True)
        angle = get_angle(row_lines, col_lines)

    rotate_img = rotate_image(origin_image, angle=angle)

    mask = box_image_processing(rotate_img, row_dil_iter, col_dil_iter)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    length = len(contours)
    small_rects = []
    for i in range(length):
        cnt = contours[i]
        area = cv2.contourArea(cnt)

        if area < area_threshold:
            continue
        approx = cv2.approxPolyDP(cnt, 3, True)
        x, y, w, h = cv2.boundingRect(approx)

        if h < h_threshold or w < w_threshold:
            continue

        small_rects.append([x, y, x + w, y + h])

    small_rects.sort(key=lambda x: x[1])

    if len(small_rects) == 0:
        return rotate_img, []

    for i in range(1, len(small_rects)):
        if abs(small_rects[i][1] - small_rects[i - 1][1]) < row_h_threshold:
            small_rects[i][1] = small_rects[i - 1][1]

    small_rects.sort(key=lambda x: (x[1], x[0]))
    boxes = []
    for i, box in enumerate(small_rects):
        box_h = box[3] - box[1]
        box_w = box[2] - box[0]
        if box_h > hw_rate_threshold * box_w:
            continue

        boxes.append(box)

    boxes.sort(key=lambda x: ((x[2] - x[0]) * (x[3] - x[1])))

    all_boxes = NMS(boxes)
    all_boxes.sort(key=lambda x: (x[1], x[0]))

    true_boxes = []
    if len(all_boxes) == 0:
        true_boxes = [[0, 0, rotate_img.shape[1], rotate_img.shape[0]]]
    # elif len(all_boxes) > 2:
    #     boxes_list = filter_box(all_boxes, exc_box_h_threshold)
    #     for boxes in boxes_list:
    #         if len(boxes) > exc_box_num_threshold:
    #             true_boxes.extend(boxes)
    else:
        true_boxes.extend(all_boxes)

    return rotate_img, true_boxes
