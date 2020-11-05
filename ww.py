import cv2
import numpy as np
import time
import os

# 均值哈希算法
def aHash(img):
    # 缩放为8*8
    img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
    height=8
    width=8
    # 转换为灰度图
    gray = np.zeros(img.shape, np.uint8)
    for i in range(height):
        for j in range(width):
            # 0.3 0.59 0.11
            gray[i, j] = 0.5 * img[i, j, 0] + 0.12* img[i, j, 1] + 0.38* img[i, j, 2]
            # gray.append(gray1[i,j][0])
            # print("++++++++",gray)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(8):
        for j in range(8):
            s = s + gray[i, j][0]
            # 求平均灰度
    avg = s / 64
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(8):
        for j in range(8):
            if gray[i, j][0] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# 差值感知算法
def dHash(img):
    # 缩放8*8
    img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
    # 转换灰度图
    height = 8
    width = 9
    gray = np.zeros(img.shape, np.uint8)
    for i in range(height):
        for j in range(width):
            # 0.3 0.59 0.11
            gray[i, j] = 0.5 * img[i, j, 0] + 0.12 * img[i, j, 1] + 0.38 * img[i, j, 2]
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j][0] > gray[i, j + 1][0]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# Hash值对比
def cmpHash(hash1, hash2):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return 1 - n / 64


def pHash(imgfile):
    img_list = []
    # 加载并调整图片为32x32灰度图片
    img = cv2.imread(imgfile, 0)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(32, 32)

    # 把二维list变成一维list
    img_list = vis1.flatten()

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i > avg else '1' for i in img_list]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 32 * 32, 4)])


def hammingDist(s1, s2):
    # assert len(s1) == len(s2)
    return 1 - sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)]) * 1. / (32 * 32 / 4)


if __name__ == '__main__':
    path="H:\\graduate-one\\vsg\\mix"
    ls=os.listdir(path)
    count_jpg=0
    for i in ls:
        if os.path.isfile(os.path.join(path, i)):
            count_jpg=count_jpg+1
    print(count_jpg)
    ls = ''.join(ls)
    ls=ls.split('.jpg')
    ls.pop()
    print(ls)

    ls=np.array(ls)
    ls =list(map(int, ls))
    print(ls)
    for i in ls:
        for j in ls:
           print('\n')
           img1 = cv2.imread("H:\\graduate-one\\vsg\\mix\\%d.jpg"%i)
           img2 = cv2.imread("H:\\graduate-one\\vsg\\mix\\%d.jpg" % (j))
           # img1 = cv2.imread('D:/vsg/11/%d.jpg'%i)
           # img2 = cv2.imread('D:/vsg/11/%d.jpg'%(j))
    # img1 = cv2.imread("D:\\graduate-one\\compare_picture\\coordinate\\JPEGImages\\000178.jpg")
    # img2 = cv2.imread("D:\\graduate-one\\compare_picture\\coordinate\\JPEGImages\\000186.jpg")
           hash1 = aHash(img1)
           hash2 = aHash(img2)
           n = cmpHash(hash1, hash2)
           print('均值哈希算法相似度：',i,j, n)
        # time1 = time.time()
           hash1 = dHash(img1)
           hash2 = dHash(img2)
           n = cmpHash(hash1, hash2)
           print('差值哈希算法相似度：',i,j, n)

        # time1 = time.time()
           HASH1 = pHash("H:\\graduate-one\\vsg\\mix\\%d.jpg"%i)
           HASH2 = pHash("H:\\graduate-one\\vsg\\mix\\%d.jpg" % j)
           # HASH2 = pHash("D:\\vsg\\11\\%d.jpg"%j)
           # HASH1 = pHash("D:\\graduate-one\\compare_picture\\coordinate\\JPEGImages\\000178.jpg")
           # HASH2 = pHash("D:\\graduate-one\\compare_picture\\coordinate\\JPEGImages\\000186.jpg")
           out_score = hammingDist(HASH1, HASH2)
           print('感知哈希算法相似度：', i,j,out_score)

# list5=[]
#
# i=0
# list5.append(1)
# for i in range(2,19,2):
#     temp = "list_solo_%d" % i
#     temp = []
#     temp.append(i)
#     temp.append(i+1)
#     list5.append(temp)
# list5.append(20)
# print(list5)
# list1=[12,13]
# lj=13
# if list1 in list5:
#     print(list1)
# t=list5[5][len(list5[5]) - 1]
#
# a=[[22,1],[22,1],[23,1],[22,1]]
# b=[22,22,22,22]
# # a=np.array(a)
# c = a+b
# #

# if len(set(a[2:][1]))==1:
# print(c)
#
# n=[[5,7],[3,6,5],[4,7]]
# m=n[0]+n[1]
# t=[]
# # for i in range(len(np.array(n).shape)-1):
# print("]]]]",len(t))

# print(t)
#
# list3=[[18,33],[5,22],[56,55],[41,62],6]
# if 5 not in list3[1]:
#     print("//",list3)
#
# # for i in list3:
# #     print("...",len(i))
# print(len(list3[1]))
#
#
# list4=[14,25]
# if(list4[0]==14):
#     print(list4)
#     list4[0]=[18,22,33]
# # list3[0].append(list4)
# # list3=[]
# print(list3)