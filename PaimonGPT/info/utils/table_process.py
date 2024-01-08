# *_*coding:utf-8 *_*
# @Author : YueMengRui
def get_center(box):
    return int(box[0] + (box[2] - box[0]) / 2), int(box[1] + (box[3] - box[1]) / 2)


def split_rows(boxes):
    row_boxes = []
    same_row = []
    c_y = 0
    for box in boxes:
        _, center_y = get_center(box)
        if len(same_row) == 0:
            same_row.append(box)
            c_y = center_y
        else:
            if abs(center_y - c_y) < 6:
                same_row.append(box)
                c_y = center_y
            else:
                row_boxes.append(same_row)
                same_row = []
                same_row.append(box)
                c_y = center_y

    if same_row:
        row_boxes.append(same_row)

    return row_boxes
