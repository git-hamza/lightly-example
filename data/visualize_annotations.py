import xml.etree.ElementTree as ET 
import os
import cv2
import argparse
from matplotlib import colors
import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
import numpy as np
import time

STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]

def draw_bounding_box_on_image_cv(image,ymin,xmin,ymax,xmax,color,thickness,display_str_list):
    (r,g,b,a) = colors.to_rgba(color)
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (int(r*255),int(g*255),int(b*255))
    im_height,im_width,_ = image.shape
    #bounding boxes
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=color,thickness=thickness)
    #label
    cv2.rectangle(image, (xmin-1, ymin-1),(xmax-1, ymin-10), color, -1)
    #labeltext
    cv2.putText(image,display_str_list,(xmin,ymin-2), font, 0.22,(0,0,0),1,cv2.LINE_AA)
    return image


def draw_bounding_box_on_image_array(image, ymin, xmin, ymax, xmax, color='red', thickness=4,display_str_list=()):
    """Adds a bounding box to an image (numpy array).

    Bounding box coordinates can be specified in either absolute (pixel) or
    normalized coordinates by setting the use_normalized_coordinates argument.

    Args:
    image: a numpy array with shape [height, width, 3].
    ymin: ymin of bounding box.
    xmin: xmin of bounding box.
    ymax: ymax of bounding box.
    xmax: xmax of bounding box.
    color: color to draw bounding box. Default is red.
    thickness: line thickness. Default value is 4.
    display_str_list: list of strings to display in box
                      (each to be shown on its own line).
    use_normalized_coordinates: If True (default), treat coordinates
      ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat
      coordinates as absolute.
    """
  
    image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
    draw_bounding_box_on_image(image_pil, ymin, xmin, ymax, xmax, color,
                             thickness, display_str_list)
    np.copyto(image, np.array(image_pil))

def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color='red',
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image.

    Bounding box coordinates can be specified in either absolute (pixel) or
    normalized coordinates by setting the use_normalized_coordinates argument.

    Each string in display_str_list is displayed on a separate line above the
    bounding box in black text on a rectangle filled with the input 'color'.
    If the top of the bounding box extends to the edge of the image, the strings
    are displayed below the bounding box.

    Args:
    image: a PIL.Image object.
    ymin: ymin of bounding box.
    xmin: xmin of bounding box.
    ymax: ymax of bounding box.
    xmax: xmax of bounding box.
    color: color to draw bounding box. Default is red.
    thickness: line thickness. Default value is 4.
    display_str_list: list of strings to display in box
                      (each to be shown on its own line).
    use_normalized_coordinates: If True (default), treat coordinates
      ymin, xmin, ymax, xmax as relative to the image.  Otherwise treat
      coordinates as absolute.
    """
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size

    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
    if thickness > 0:
        draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)
    try:
        font = ImageFont.truetype('arial.ttf', 10)
    except IOError:
        font = ImageFont.load_default()

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = bottom + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle(
            [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                              text_bottom)],
            fill=color)
        draw.text(
            (left + margin, text_bottom - text_height - margin),
            display_str,
            fill='black',
            font=font)
        text_bottom -= text_height - 2 * margin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a","--annotations", type =str,help="path to annotations folder")
    ap.add_argument("-i","--images", type =str,help="path to images folder")
    ap.add_argument("-c","--classes_txt", type =str,help="path to images folder")
    args = vars(ap.parse_args())

    ## This flag will determine the speed at which bounding box is drawn on the image
    ## This being true means, it will use cv function to draw which will be fast but not very clear label names
    ## This being false will mean, it will use PIL functions to draw which will be slow but have clear label names
    Speed_Flag = False

    IN_ANN = args["annotations"]
    IN_IMG = args["images"]
    classes_txt = args["classes_txt"]

    classes_names = []
    with open(classes_txt, "r") as f:
        lines = f.readlines()
        for line_ in lines:
            classes_names.append(line_.strip())


    OUT_IMG = 'visualizations/'
    if not os.path.isdir(OUT_IMG):
        os.mkdir(OUT_IMG)
    count = 0
    Labels = {}
    for img_file in os.listdir(IN_IMG):
        filename = os.path.splitext(img_file)[0]

        image = cv2.imread(os.path.join(IN_IMG, img_file))
        image_height, image_width, _ = image.shape

        with open(os.path.join(IN_ANN, f"{filename}.txt"), "r") as f:
          lines = f.readlines()

        for line in lines:
            data = line.strip().split(" ")

            label = int(data[0])
            txt =  classes_names[label]
            if len(Labels) ==0:
                Labels[txt] = STANDARD_COLORS[count]
                count +=1
            else:
                if txt in Labels.keys():
                    pass
                else:
                    Labels[txt] = STANDARD_COLORS[count]
                    count +=1

            x = float(data[1])
            y = float(data[2])
            w = float(data[3])
            h = float(data[4])

            xmin = max(0, int((x - w / 2) * image_width))
            ymin = max(0, int((y - h / 2) * image_height))
            xmax = min(int((x + w / 2) * image_width), image_width)
            ymax = min(int((y + h / 2) * image_height), image_height)

            if Speed_Flag:
                img = draw_bounding_box_on_image_cv(image,ymin,xmin,ymax,xmax,
                  Labels[txt],2,
                  txt)
            else:
                draw_bounding_box_on_image_array(
                    image,
                    ymin,
                    xmin,
                    ymax,
                    xmax,
                    color=Labels[txt],
                    thickness=6,
                    display_str_list=[str(txt)])

        # print("Inference_Time : " + str(time.time()-fetch_time))
        cv2.imwrite(os.path.join(OUT_IMG,img_file),image)
        print(Labels)

if __name__ == '__main__':
  main()
