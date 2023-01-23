import os
import pandas as pd
import cv2
from unipath import Path


# directory where the pictures are
pic_dir = r'C:\Users\jonas\Documents\Uni\FTZ\copo\5thShot\13_5_L'
# directory where the finished csv file should end up
save_dir = r'C:\Users\jonas\Documents\Uni\FTZ\copo\ergeb'


def click_event(event, x, y, flags, param):

    global saveL
    global counter

    # L/R click pair
    if event == cv2.EVENT_LBUTTONDOWN:
        if not (flags & cv2.EVENT_FLAG_ALTKEY) and not (flags & cv2.EVENT_FLAG_CTRLKEY):
            saveL[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (255, 0, 0), 2)
        # blue
        cv2.imshow('image', img)

    if event == cv2.EVENT_RBUTTONDOWN:
        if not (flags & cv2.EVENT_FLAG_ALTKEY) and not (flags & cv2.EVENT_FLAG_CTRLKEY):
            saveR[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (255, 227, 0), 2)
        # lightblue
        cv2.imshow('image', img)

    # ALT L/ ALT R pair
    if event == cv2.EVENT_LBUTTONDOWN and (flags & cv2.EVENT_FLAG_ALTKEY):
        saveAL[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (0, 255, 0), 2)
        # green
        cv2.imshow('image', img)

    if event == cv2.EVENT_RBUTTONDOWN and (flags & cv2.EVENT_FLAG_ALTKEY):
        saveAR[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (9, 99, 9), 2)
        # darkgreen
        cv2.imshow('image', img)

    # CTRL L / CTRL R pair
    if event == cv2.EVENT_LBUTTONDOWN and (flags & cv2.EVENT_FLAG_CTRLKEY):
        save_CL[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (189, 3, 154), 2)
        # purple
        cv2.imshow('image', img)

    if event == cv2.EVENT_RBUTTONDOWN and (flags & cv2.EVENT_FLAG_CTRLKEY):
        save_CR[counter] = [x, y]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (0, 0, 255), 2)
        # red
        cv2.imshow('image', img)

def open_img(pfad, name):

    global img
    img = cv2.imread(f"{pfad}/{name}", 1)

    if not counter == 1:
        img_old = cv2.imread(f'{pfad}/temp.jpg')
        cv2.imshow('old', img_old)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,
                str(counter),
                (26, 18),
                font,
                0.5,
                (0, 255, 0), 2)
    cv2.putText(img, 'L BUTTON', (8, 511), font, 0.5, (255, 0, 0), 2)
    cv2.putText(img, 'R BUTTON', (98, 511), font, 0.5, (255, 227, 0), 2)
    cv2.putText(img, 'ALT+L BUTTON', (184, 511), font, 0.5, (0, 255, 0), 2)
    cv2.putText(img, 'ALT+R BUTTON', (306, 511), font, 0.5, (9, 99, 9), 2)
    cv2.putText(img, 'CTRL+L BUTTON', (429, 511), font, 0.5, (189, 3, 154), 2)
    cv2.putText(img, 'CTRL+R BUTTON (Kontroll-fussel)', (562, 511), font, 0.5, (0, 0, 255), 2)
    cv2.imshow('image', img)

    cv2.setMouseCallback('image', click_event)
    k = cv2.waitKey(0)
    cv2.imwrite(f'{pfad}/temp.jpg', img)
    if counter == 1:
        cv2.imwrite(f'{pfad}/first_annot.jpg', img)
    cv2.destroyAllWindows()

    if k == ord('a'):
        return 'exit'


if __name__ == '__main__':
    pic_list = []
    p = Path(pic_dir)
    saveL = {}
    saveR = {}
    saveAL = {}
    saveAR = {}
    save_CL = {}
    save_CR = {}

    counter = 1

    for pics in p.listdir():
        if pics.ext == '.jpg':
            pic_list.append(str(pics.name))


    for i in pic_list:
        saveL[counter] = ('Na', 'Na')
        saveR[counter] = ('Na', 'Na')
        saveAL[counter] = ('Na', 'Na')
        saveAR[counter] = ('Na', 'Na')
        save_CL[counter] = ('Na', 'Na')
        save_CR[counter] = ('Na', 'Na')
        if open_img(p, i) == 'exit':
            break
        counter += 1

    # output
    s = Path(save_dir)
    os.chdir(s)
    name = p.name
    names = ['blue_x', 'blue_y', 'lightblue_x', 'lightblue_y', 'green_x', 'green_y',
             'darkgreen_x', 'darkgreen_y', 'purple_x', 'purple_y', 'red_x', 'red_y']
    outL = pd.DataFrame.from_dict(data=saveL, orient='index')
    outR = pd.DataFrame.from_dict(data=saveR, orient='index')
    outAL = pd.DataFrame.from_dict(data=saveAL, orient='index')
    outAR = pd.DataFrame.from_dict(data=saveAR, orient='index')
    outCL = pd.DataFrame.from_dict(data=save_CL, orient='index')
    outCR = pd.DataFrame.from_dict(data=save_CR, orient='index')
    out = pd.concat([outL, outR, outAL, outAR, outCL, outCR], axis=1)
    out.to_csv(f'{name}.csv', header=names)
    print(f'{name}.csv has been saved in {save_dir}')
    os.remove(f'{p}/temp.jpg')
