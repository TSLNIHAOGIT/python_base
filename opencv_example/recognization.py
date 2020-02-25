
import cv2

import numpy as np
import os
from PIL import Image, ImageEnhance
# 读取图片

imagePath = './cv.png'
imagePath='./grades.jpg'
if os.path.exists(imagePath):
    img = cv2.imread(imagePath)
else:
    print('err','路径不存在')

orig = img.copy()

# # 图像增强
# img = Image.fromarray(img)
# img = ImageEnhance.Contrast(img).enhance(8)  # 增加对比度
# img = ImageEnhance.Sharpness(img).enhance(3)  # 增加锐度
# img = np.array(img)
#
# src = cv2.GaussianBlur(img, (5, 3), 0)
# # 再锐化
# blur_img = cv2.GaussianBlur(src, (0, 0), 8)
# img = cv2.addWeighted(src, 1.5, blur_img, -0.5, 0)

# # 灰度图+降噪
# fx = max(int(2500 / img.shape[1]), 1)
# fy = max(int(3500 / img.shape[0]), 1)
# img = cv2.resize(img, (0, 0), fx=fx, fy=fy)

# 转化成灰度图
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('raw img', img)
cv2.waitKey(0)
cv2.imshow('gray', gray)
cv2.waitKey(0)
# cv2.destroyAllWindows()
# 利用Sobel边缘检测生成二值图

sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0,ksize=3)
# 二值化

ret, binary = cv2.threshold(sobel, 0, 255,cv2.THRESH_OTSU + cv2.THRESH_BINARY)
cv2.imshow('binary', binary)
cv2.waitKey(0)

# 膨胀、腐蚀
#原来都是5,2,不加数据预处理，element2改成5,1之后需要计算iou用nms进行去重
element1 = cv2.getStructuringElement(cv2.MORPH_RECT,(5,2 ))#6,2

element2 =cv2.getStructuringElement(cv2.MORPH_RECT, (5,1 ))#6,1
# cv2.imshow('element1', element1)
# cv2.waitKey(0)
#

# cv2.imshow('element2', element2)
# cv2.waitKey(0)

# 膨胀一次，让轮廓突出

dilation = cv2.dilate(binary, element2,iterations=2)
cv2.imshow('dilation1', dilation)
cv2.waitKey(0)



# 腐蚀一次，去掉细节

erosion = cv2.erode(dilation, element1,iterations=2)
cv2.imshow('erosion1', erosion)
cv2.waitKey(0)

# 再次膨胀，让轮廓明显一些

dilation2 = cv2.dilate(erosion, element2,iterations=2)
cv2.imshow('dilation2', dilation)
cv2.waitKey(0)
#  查找轮廓和筛选文字区域

region = []

binary, contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# binary, contours, hierarchy = cv2.findContours(dilation2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):

    cnt = contours[i]
    # print('cnt',cnt)

    # # 计算轮廓面积，并筛选掉面积小的
    #
    area = cv2.contourArea(cnt)
    print('area',area)

    if (area < 1000 or area >5000):
        continue

    # 找到最小的矩形

    rect = cv2.minAreaRect(cnt)


    print("rect is: ")

    print(rect)

    # box是四个点的坐标

    box = cv2.boxPoints(rect)

    box = np.int0(box)

    # 计算高和宽

    height = abs(box[0][1] - box[2][1])

    width = abs(box[0][0] - box[2][0])

    # 根据文字特征，筛选那些太细的矩形，留下扁的

    if (height > width * 1.3):
        continue

    region.append(box)
# 绘制轮廓
print('regon',np.array(region).shape,np.array(region))
for box in region:

   cv2.drawContours(img, [box], 0, (0, 255, 0), 2)

cv2.imshow('img', img)

cv2.waitKey(0)

# NMS 方法（Non Maximum Suppression，非极大值抑制）

def nms(boxes, overlapThresh):

    if len(boxes) == 0:

        return []



    if boxes.dtype.kind == "i":

        boxes = boxes.astype("float")



    pick = []



    # 取四个坐标数组

    x1 = boxes[:, 0]

    y1 = boxes[:, 1]

    x2 = boxes[:, 2]

    y2 = boxes[:, 3]



    # 计算面积数组

    area = (x2 - x1 + 1) * (y2 - y1 + 1)



    # 按得分排序（如没有置信度得分，可按坐标从小到大排序，如右下角坐标）

    idxs = np.argsort(y2)



    # 开始遍历，并删除重复的框

    while len(idxs) > 0:

        # 将最右下方的框放入pick数组

        last = len(idxs) - 1

        i = idxs[last]

        pick.append(i)



        # 找剩下的其余框中最大坐标和最小坐标

        xx1 = np.maximum(x1[i], x1[idxs[:last]])

        yy1 = np.maximum(y1[i], y1[idxs[:last]])

        xx2 = np.minimum(x2[i], x2[idxs[:last]])

        yy2 = np.minimum(y2[i], y2[idxs[:last]])



        # 计算重叠面积占对应框的比例，即 IoU

        w = np.maximum(0, xx2 - xx1 + 1)

        h = np.maximum(0, yy2 - yy1 + 1)

        overlap = (w * h) / area[idxs[:last]]



        # 如果 IoU 大于指定阈值，则删除

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))



    return boxes[pick].astype("int")

keep=[]
for each in region:
    keep.append([each[1][0],each[1][1],each[3][0],each[3][1]])
keep2 = np.array(keep)
print('keep2',np.array(keep2).shape)
pick = nms(keep2, 0.96)

print("[x] after applying non-maximum, %d bounding boxes" % (len(pick)))

# loop over the picked bounding boxes and draw them

for (startX, startY, endX, endY) in pick:

    cv2.rectangle(orig, (startX, startY), (endX, endY), (255, 0, 0), 1)

cv2.imshow("After NMS", orig)



cv2.waitKey(0)

cv2.destroyAllWindows()

