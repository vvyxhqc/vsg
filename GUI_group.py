import numpy as np
import cv2
import pandas as pd
import dataframe
import math
import itertools

# 1是Image-图片
# 2是OnOffSwitch-开关
# 3是RadioButton-按钮
# 4是Text-文本
# 5是Checkbox-复选框
def element_Data(data,data_i,image_num):
    data_class = data.copy()
    # 预处理图片上的内容，消除
    count_pre = []
    for i in range(0, len(data_class)):
        for j in range(0, len(data_class)):
            if (i == j):
                continue
            if ((data_class[j, 1] < (data_class[i, 1] or data_class[i, 3]) < data_class[j, 3]) and
                    (data_class[j, 1] < (data_class[i, 1] + (data_class[i, 1] + data_class[i, 3]) / 2) < data_class[j, 3]) and
                    (data_class[j, 2] < (data_class[i, 2] or data_class[i, 4]) < data_class[j, 4]) and
                    (data_class[j, 2] < (data_class[i, 2] + (data_class[i, 2] + data_class[i, 4]) / 2) < data_class[
                        j, 4])):
                count_pre.append(i)

    count = 0
    for i in count_pre:
        data_class = np.delete(data_class, i - count, 0)
        count = count + 1

    # 根据元素横坐标结合高度筛选出从左到右，从上到下的排列序号
    data_class = data_class[data_class[:, 2].argsort()]
    print(data_class)
    for i in range(0, len(data_class)):
        for j in range(i+1, len(data_class)):
            # 上边或者下边和另一个元素差距50以内，并且换掉的两个元素必须相交
            if (data_class[i, 1] > data_class[j, 1] and data_class[i, 3] > data_class[j, 3]
                and ((data_class[j, 2] >= data_class[i, 2] ) or (data_class[j, 4] - data_class[i, 4] <= 50))
                and data_class[i, 4] > data_class[j, 2]):
                print("1", i, j)
                temp1 = np.copy(data_class[i])
                data_class[i] = data_class[j]
                data_class[j] = temp1

    element_num = []  # 存储每个元素序号
    for i in range(len(data_class)):
        element_num.append(i)
    # 把一列元素序号加入数组中
    data_class = np.column_stack((data_class, np.array(element_num)))
    print(data_class)

    # img = cv2.imread('H:/graduate-one/vsg/numpy_type/%d.jpg'%(data_i[image_num - 1]))
    # for i in range(len(data_class)):
    #     cv2.imwrite('H:/graduate-one/vsg/mix/%s'  % (data_i[image_num - 1]) + '_' + "%d.jpg" % (i + 1),
    #                 img[int(data_class[i, 2]):int(data_class[i, 4]), int(data_class[i, 1]):int(data_class[i, 3])])
    # 预处理数据合并阈值范围内的上下文本
    count_pre2 = []
    for i in range(len(data_class)):
        for j in range(i + 1, len(data_class)):
            if (((data_class[j, 1] < (data_class[i, 1] + (data_class[i, 3] - data_class[i, 1]) / 2) < data_class[
                j, 3]) or
                     (data_class[i, 1] < (data_class[j, 1] + (data_class[j, 3] - data_class[j, 1]) / 2) < data_class[
                         i, 3]))
                and (data_class[i, 5] == data_class[j, 5] and abs(data_class[j, 2] - data_class[i, 4]) <= 15 and
                     data_class[i, 4] - data_class[i, 2] <= 100 and data_class[j, 4] - data_class[j, 2] <= 100) or
                    (abs(data_class[j, 2] - data_class[i, 4]) <= 15 and data_class[i, 4] - data_class[i, 2] <= 15
                     and data_class[j, 4] - data_class[j, 2] <= 15)):
                data_class[j, 1] = min(data_class[i, 1], data_class[j, 1])
                data_class[j, 2] = data_class[i, 2]
                data_class[j, 3] = max(data_class[i, 3], data_class[j, 3])
                count_pre2.append(i)
    count = 0
    for i in count_pre2:
        data_class = np.delete(data_class, i - count, 0)
        count = count + 1
    # 重置序列
    for i in range(len(data_class)):
        data_class[i, 6] = i
    print(data_class)

    # 预处理数据合并水平阈值内的文本
    # count_pre1 = []
    # for i in range(len(data_class) - 1):
    #     for j in range(i + 1, i + 2):
    #         if ((data_class[i, 4] - data_class[i, 2] < 50) and (data_class[j, 4] - data_class[j, 2] < 50) and
    #                 (data_class[j, 2] < (data_class[i, 2] + (data_class[i, 4] - data_class[i, 2]) / 2) < data_class[
    #                     j, 4] or data_class[i, 2] < (data_class[j, 2] + (data_class[j, 4] - data_class[j, 2]) / 2) <
    #                     data_class[i, 4])):
    #             print("---------", i, j)
    #             data_class[j, 1] = min(data_class[i, 1], data_class[j, 1])
    #             data_class[j, 2] = min(data_class[i, 2], data_class[j, 2])
    #             data_class[j, 4] = max(data_class[i, 4], data_class[j, 4])
    #             count_pre1.append(i)
    #
    # count = 0
    # for i in count_pre1:
    #     data_class = np.delete(data_class, i - count, 0)
    #     count = count + 1
    # # 重置序列
    # for i in range(len(data_class)):
    #     data_class[i, 6] = i
    # print(data_class)
    # img = cv2.imread('H:/graduate-one/vsg/numpy_type/%d.jpg' % (data_i[image_num - 1]))
    # for i in range(len(data_class)):
    #     cv2.imwrite('H:/graduate-one/vsg/mix/%s' % (data_i[image_num - 1]) + '_' + '_'+ '_'+"%d.jpg" % (i + 1),
    #                 img[int(data_class[i, 2]):int(data_class[i, 4]), int(data_class[i, 1]):int(data_class[i, 3])])
    # 存储元素所在行
    i = 0
    j = 0
    count = 0  # 跳过已被判定过行号的循环
    row_num = []  # 存储行号
    m = 0  # 每行只有一个元素时，记录行号
    n = 0  # 记录所有元素数目和行数目之差
    for i in range(0, len(data_class)):
        # 跳过已被判定为行的循环
        if (count > 0):
            count = count - 1
            row_num.append(i - n - 1)
            n = n + 1
            continue
        row_num.append(m)
        m = m + 1
        #  ...,,./
        temp3 = i
        j = 0
        while j < len(data_class):
            # print(temp3, i, j)
            # print("aaaaaaaa", i, j)
            if (i == j):
                j = j + 1
                continue
            temp2 = data_class[i, :]
            # 左包含右
            if (data_class[i, 1] <= data_class[j, 1] and data_class[i, 2] <= data_class[j, 2] and data_class[i, 3] <=
                    data_class[j, 3] and data_class[i, 4] >= data_class[j, 4]):
                column1 = np.row_stack((temp2, data_class[j, :]))
                print("aa", i, column1)
                count = count + 1
                j = j + 1
                continue
            # 右包含左
            if (data_class[i, 1] <= data_class[j, 1] and data_class[i, 2] >= data_class[j, 2] and data_class[i, 3] <=
                    data_class[j, 3] and data_class[i, 4] <= data_class[j, 4]):
                column2 = np.row_stack((temp2, data_class[j, :]))
                print("bb", i, column2)
                count = count + 1
                i = i + 1
                j = 0
                continue
            # 左高右低
            if (data_class[i, 1] <= data_class[j, 1] and data_class[i, 3] <= data_class[j, 3] and
                    ((data_class[j, 2] > data_class[i, 2] and  abs(data_class[j, 4] - data_class[i, 4]) <= 50))
                and data_class[i,4]>data_class[j,2]):
                column3 = np.row_stack((temp2, data_class[j, :]))
                print("cc", i, column3)
                count = count + 1
                j = j + 1
                continue
            # 左低右高
            if (data_class[i, 1] <= data_class[j, 1] and data_class[i, 3] <= data_class[j, 3] and
                    ((abs(data_class[i, 2] - data_class[j, 2]) <= 50 and data_class[i, 4] > data_class[j, 4]))
                and data_class[i,4]>data_class[j,2]):
                # and abs(data[i,2]-data[j,4]>10)
                column4 = np.row_stack((temp2, data_class[j, :]))
                print("dd", i, column4)
                count = count + 1
                j = j + 1
                continue
            j = j + 1
    data_class = np.column_stack((data_class, np.array(row_num)))  # 把一列行序号加入数组中
    print("data_class", data_class)
    img = cv2.imread('H:/graduate-one/vsg/numpy_type/%d.jpg'%(data_i[image_num - 1]))
    for i in range(len(data_class)):
        cv2.imwrite('H:/graduate-one/vsg/mix/%d.jpg' % (i),
                    img[int(data_class[i, 2]):int(data_class[i, 4]), int(data_class[i, 1]):int(data_class[i, 3])])
        # cv2.imwrite('H:/graduate-one/vsg/mix/%s' % (data_i[image_num - 1]) + '_' + "%d.jpg" % (i + 1),
        #         img[int(data_class[i, 2]):int(data_class[i, 4]), int(data_class[i, 1]):int(data_class[i, 3])])
    # 存储每个顶点大小
    element_size = []  # 存储每个顶点大小
    for i in range(0, len(data_class)):
        element_size.append((data_class[i, 3] - data_class[i, 1]) * (data_class[i, 4] - data_class[i, 2]))
        # 把一列元素序号加入数组中
    data_class = np.column_stack((data_class, np.array(element_size)))
    print(data_class)

    # 存储每个顶点中心坐标
    element_core_x = []  # 存储每个顶点中心x值
    element_core_y = []  # 存储每个顶点中心y值
    for i in range(0, len(data_class)):
        element_core_x.append(data_class[i, 1] + (data_class[i, 3] - data_class[i, 1]) / 2)
        element_core_y.append(data_class[i, 2] + (data_class[i, 4] - data_class[i, 2]) / 2)
        # 把一列元素序号加入数组中
    data_class = np.column_stack((data_class, np.array(element_core_x)))
    data_class = np.column_stack((data_class, np.array(element_core_y)))
    data_class = np.trunc(data_class)
    data_class = data_class.astype('int')
    print(data_class)
    return data_class
def element_Rela(data_class):
    data_rela = data_class.copy()
    rela = [[0 for m in range(len(data_rela))] for n in range(len(data_rela))]
    for i in range(len(data_rela)):
        for j in range(len(data_rela)):
            # print(i,j)
            if (i == j):
                rela[i][j] = 0
                continue
            # 上下关系
            if ((data_rela[j, 1] < (data_rela[i, 1] + (data_rela[i, 3] - data_rela[i, 1]) / 2) < data_rela[j, 3]) or
                    (data_rela[i, 1] < (data_rela[j, 1] + (data_rela[j, 3] - data_rela[j, 1]) / 2) < data_rela[i, 3])):
                rela[i][j] = 1
                # print("x",i,j)
                for k in range(len(data_rela)):
                    if (k == i or k == j):
                        continue
                    if (
                            #     data_rela[k, 1]<(min(data_rela[i, 1], data_rela[j, 1]) + (max(data_rela[i, 3],data_rela[j, 3])-min(data_rela[i, 1], data_rela[j, 1]))/2)<data_rela[k, 3]
                            # and data_rela[k, 2]<(min(data_rela[i, 4], data_rela[j, 4]) + (max(data_rela[i, 2],data_rela[j, 2])-min(data_rela[i, 4], data_rela[j, 4]))/2)<data_rela[k, 4])\
                            # or \
                            (min(data_rela[i, 4], data_rela[j, 4]) < data_class[k, 10] < max(data_rela[i, 2],
                                                                                             data_rela[j, 2]))):
                        # and (min(data_rela[i, 1],data_rela[j,1]) < data_class[k,9] < max(data_rela[i,3],data_rela[j, 3]))):
                        # print("x",k,i, j)
                        rela[i][j] = 0
                        break

            # 左右关系
            if ((data_rela[j, 2] < (data_rela[i, 2] + ((data_rela[i, 4] - data_rela[i, 2]) / 2)) < data_rela[j, 4]) or
                    (data_rela[i, 2] < (data_rela[j, 2] + ((data_rela[j, 4] - data_rela[j, 2]) / 2)) < data_rela[
                        i, 4])):
                rela[i][j] = 2
                # print("y", i, j)
                for k in range(len(data_rela)):
                    if (k == i or k == j):
                        continue
                    if (
                            #     (data_rela[k, 1] < (min(data_rela[i, 3], data_rela[j, 3]) + (max(data_rela[i, 1], data_rela[j, 1]) - min(data_rela[i, 3], data_rela[j, 3])) / 2 )<data_rela[k, 3]
                            # and data_rela[k, 2] < (min(data_rela[i, 2], data_rela[j,2]) + (max(data_rela[i, 4], data_rela[j, 4]) - min(data_rela[i, 2], data_rela[j, 2])) / 2 )<data_rela[k, 4])\
                            # or (
                                (min(data_rela[i, 3], data_rela[j, 3]) < data_class[k, 9] < max(data_rela[i, 1],
                                                                                                data_rela[j, 1])) and
                                        min(data_rela[i, 2], data_rela[j, 2]) < data_class[k, 10] < max(data_rela[i, 4],
                                                                                                        data_rela[j, 4])):
                        # print(k,i, j)
                        rela[i][j] = 0
                        break
            if ((data_rela[i, 2] <= data_rela[j, 2] and data_rela[i, 4] >= data_rela[j, 4]) or
                            (data_rela[j, 2] <= data_rela[i, 2] and data_rela[j, 4] >= data_rela[i, 4])):
                        rela[i][j] = 2
    print("data_rela",data_rela)
    rela = np.mat(rela)  # 列表转矩阵
    np.set_printoptions(threshold=np.inf)#消除省略号

    print(rela)
    rela = rela.tolist()
    return rela,data_rela
def element_Dis(data_class):
    # 存储任意两个顶点之间的距离（中心坐标之差）
    data_distance = data_class.copy()
    print(len(data_distance))
    element_distance = []
    distance = [[0 for m in range(len(data_distance))] for n in range(len(data_distance))]
    # print(distance)
    for i in range(len(data_distance)):
        for j in range(len(data_distance)):
            if i == j:
                continue
            else:
                distance[i][j] = math.sqrt(
                    ((data_class[i, 9] - data_class[j, 9]) ** 2) + ((data_class[i, 10] - data_class[j, 10]) ** 2))
    distance = np.array(distance)
    distance = np.trunc(distance)
    distance = distance.astype('int')
    # distance = np.mat(distance)#列表转矩阵
    # print(distance)
    return distance
def one_Group(rela,data_rela,list_all,data_class_number,data_class):
    list_down_numpy = []
    list_count = []
    count_ele = 0
    # 上下关系分组
    temp = []
    for i in range(len(rela)):
        for j in range(i + 1, len(rela)):
            if ((rela[i][j] == 1 and (2 not in rela[i]) and (2 not in rela[j]) and data_rela[i][5] == data_rela[j][5])):
                if (data_class_number[i] in temp and data_class_number[j] in temp):
                    continue
                if (data_class_number[i] in temp and data_class_number[j] not in temp):
                    temp.append(data_class_number[j])
                if (data_class_number[j] in temp and data_class_number[i] not in temp):
                    temp.append(data_class_number[i])
                if (data_class_number[i] not in temp):
                    temp = "list_down_1%d" % i
                    temp = []
                    temp.append(data_class_number[i])
                    temp.append(data_class_number[j])
                    list_all.append(temp)
            else:
                continue
                # if ((i and j) not in list_count):
                #     list_solo.append(data_rela[i].tolist())
    print("上下关系单个分组", list_all)

    new=[]
    list_flatten = list_app(list_all,new)
    # if (len(list_all) != 0):
    #     for i in range(len(list_all)):
    #         if (len((np.array(list_all[i])).shape) - 1 == 0):
    #             list_flatten.append(list_all[i])  # 将多维列表变为一维列表
    #         else:
    #             list_flatten.append(list(itertools.chain.from_iterable(list_all[i])))
    #     list_flatten = list(itertools.chain.from_iterable(list_flatten))
    # 左右关系分组
    temp = []
    list_right_numpy = []
    for i in range(len(rela)):
        if data_class_number[i] in list_flatten:
            continue
        for j in range(i + 1, len(rela)):
            if data_class_number[j] in list_flatten:
                continue
            if ((rela[i][j] == 2) and data_rela[i][5] == data_rela[j][5]):
                if (data_class_number[i] in temp and data_class_number[j] in temp):
                    continue
                if (data_class_number[i] in temp and data_class_number[j] not in temp):
                    temp.append(data_class_number[j])
                if (data_class_number[j] in temp and data_class_number[i] not in temp):
                    temp.append(data_class_number[i])
                if (data_class_number[i] not in temp and data_class_number[j] not in temp):
                    temp = "list_down_2%d" % i
                    temp = []
                    temp.append(data_class_number[i])
                    temp.append(data_class_number[j])
                    list_right_numpy.append(temp)
            else:
                continue
                # if ((i and j) not in list_count):
                #     list_solo.append(data_rela[i].tolist())
    print("++++++++++", list_right_numpy)
    right_len = len(list_right_numpy)
    print(right_len)
    list_right_del = []  # 存储要删除的单个组
    judge_2=0
    for i in range(right_len):
        if (right_len == 1 or right_len == 0):
            break
        if (len(list_right_numpy[i]) == 2):#如果一行中只有两个类型相似，并且此行还有其他元素，删除
            for m in range(len(data_class)):
                if(list_right_numpy[i][0]==data_class[m,7]):
                    judge_2=judge_2+1
            if judge_2>2:
                list_right_del.append(list_right_numpy[i])
        if (list_right_numpy[i] in list_right_del):
            continue
        for j in range(i + 1, right_len):
            if (((len(list_right_numpy[i]) == len(list_right_numpy[j])) and
                     (abs(data_class[list_right_numpy[i][0]][7] - data_class[list_right_numpy[j][0]][7]) == 1))
                or ((len(list_right_numpy[i]) == 2) and (len(list_right_numpy[j]) == 2))):
                print("]]]]]]",list_right_numpy[i], list_right_numpy[j])
                print(len(list_right_numpy[i]), len(list_right_numpy[j]))
                if (list_right_numpy[i] in list_right_del):
                    list_right_del.append(list_right_numpy[j])
                    continue
                list_right_del.append(list_right_numpy[i])
                list_right_del.append(list_right_numpy[j])
    # 删除相同的组
    print("++++++++++", list_right_numpy)
    for i in list_right_del:
        if i in list_right_numpy[::-1]:
            list_right_numpy.remove(i)
    print("++++++++++", list_right_numpy)
    list_all = list_all + list_right_numpy
    print("左右关系单个分组", list_all)
    list_flatten = []
    new=[]
    list_flatten = list_app(list_all,new)

    # 左右上下关系分组
    temp = []
    list_down_right = []
    for i in range(len(rela)):
        if data_class_number[i] in list_flatten:
            continue
        if (data_rela[i][5] != 1):
            continue
        for j in range(i + 1, len(rela)):
            if data_class_number[j] in list_flatten:
                continue
            if (data_rela[j][5] != 1):
                break
            if ((rela[i][j] == 2) and data_rela[i][5] == 1 and data_rela[j][5] == 1):  # 1为图片类型
                if (data_class_number[i] in temp and data_class_number[j] in temp):
                    continue
                if (data_class_number[i] in temp and data_class_number[j] not in temp):
                    temp.append(data_class_number[j])
                if (data_class_number[j] in temp and data_class_number[i] not in temp):
                    temp.append(data_class_number[i])
                if (data_class_number[i] not in temp and data_class_number[j] not in temp):
                    temp = "list_down_3%d" % i
                    temp = []
                    temp.append(data_class_number[i])
                    temp.append(data_class_number[j])
                    list_down_right.append(temp)
            else:
                continue
    print(list_down_right)
    list_down_right_numpy = []
    temp = []
    if (len(list_down_right) == 0 or len(list_down_right) == 1):
        list_down_right.clear()
    else:
        for i in range(len(list_down_right) - 1):
            for j in range(i + 1, i + 2):
                if ((len(list_down_right[i]) == len(list_down_right[j]))
                    and abs(data_class[list_down_right[i][0]][7] - data_class[list_down_right[j][0]][7]) == 1
                    and data_class[list_down_right[i][0]][5] == 1 and data_class[list_down_right[j][0]][5]==1):
                    if (list_down_right[i] in temp and list_down_right[j] in temp):
                        continue
                    if (list_down_right[i] in temp and list_down_right[j] not in temp):
                        temp.append(list_down_right[j])
                    if (list_down_right[j] in temp and list_down_right[i] not in temp):
                        temp.append(list_down_right[i])
                    if list_down_right[i] not in temp:
                        temp = "list_down_right_2%d" % i
                        temp = []
                        temp.append(list_down_right[i])
                        temp.append(list_down_right[j])
        if(len(temp) != 0):
            temp = list(itertools.chain.from_iterable(temp))
            print("temp",temp)
            list_all.append(temp)
    print("左右上下关系单个分组", list_all)

    return list_all

# 语义复合组合按钮
def semantic_RecomButton(data_class,rela,distance,list_all):
    new = []
    new = list_app(list_all,new)
    # print("listAll:\n",list_all)
    # print("new:\n",new)

    data_sema = []
    for i in range(len(data_class)):
        if(i in new):
            continue
        if(data_class[i][5] == 1):

            num = []
            for j in range(len(rela)):
                # if(rela[i][j] == 1 and data_class[j][5] == 4 and ((-30 < (data_class[i][4] - data_class[j][2]) <30) or (-30 < (data_class[j][4] - data_class[i][2]) <30))):
                if(rela[i][j] == 1 and data_class[j][5] == 4 and (distance[i][j] < 140)):
                    num.append(j)
                    # mark = j
                    # for j2 in range(len(rela)):
                    #     # if (rela[mark][j2] == 1 and data_class[j2][5] == 4 and (
                    #     #         (-30 < (data_class[mark][4] - data_class[j2][2]) < 30) or (
                    #     #         -30 < (data_class[j2][4] - data_class[mark][2]) < 30))):
                    #     if (rela[mark][j2] == 1 and data_class[j2][5] == 4 and (distance[mark][j2] < 140)):
                    #         m = -1
                    #         for n in num:
                    #             if (j2 == n):
                    #                 m = j2
                    #                 break
                    #         if(m == -1):
                    #             num.append(j2)
                    #         mark = j2
                    #         j2 = 0
            if(len(num) != 0):
                num.append(i)
                data_sema.append(num)
    dele = []
    # for i in range(len(data_sema)):
    #     if(len(data_sema[i]) > 2):
    #         if (distance[[data_sema[i][2]][data_sema[i][1]]] > distance[[data_sema[i][2]][data_sema[i][0]]]):
    #             term = [data_sema[i][0],data_sema[i][2]]
    #             data_sema[i] = term
    #         else:
    #             term = [data_sema[i][1], data_sema[i][2]]
    #             data_sema[i] = term
    for i in range(len(data_sema)):

        length = len(data_sema[i])
        print("组长度：",length)
        # 可能把图片上下文本都分成一组，选择距离图片较近的
        if (len(data_sema[i]) > 2):
            if (distance[data_sema[i][length-1]][data_sema[i][1]] > distance[data_sema[i][length-1]][data_sema[i][0]]):
                term = [data_sema[i][0], data_sema[i][2]]
                data_sema[i] = term
            else:
                term = [data_sema[i][1], data_sema[i][2]]
                data_sema[i] = term
        # 图片和文本对应为左右关系
        if(i>=0):
            length = len(data_sema[i])
            if (rela[data_sema[i][length-1]][data_sema[i-1][len(data_sema[i - 1])-1]] == 2 and rela[data_sema[i][0]][data_sema[i-1][0]] == 2):
                print("符合")
                continue
            else:
                row = 0
                for j in range(i):
                    row = max(row, len(data_sema[j]))
                if(i != (len(data_sema) - 1)):
                    if(rela[data_sema[i][length-1]][data_sema[i+1][len(data_sema[i + 1])-1]] == 2 and rela[data_sema[i][0]][data_sema[i+1][0]] == 2):#(data_class[data_sema[i][length-1]][7] - data_class[data_sema[i-1][1]][7] == 2):
                        continue
                        print("符合")
                else:
                    dele.append(i)
                    print(i,"不符合")

    if(len(dele) != 0):
        count = 0
        print(data_sema)
        for i in dele:
            print("删除了", data_sema[i - count] ," ")
            data_sema = np.delete(data_sema, i - count, 0)
            count = count + 1

    if (len(data_sema) == 1):
        print("删除了", data_sema[0])
        data_sema = np.delete(data_sema, 0, 0)

    if(len(data_sema) != 0):
        if(list_all == None):
            list_all = []
        list_all.append(data_sema)
    return list_all

# 复合单选按钮
def recom_RadioBox(data_class,list_all):
    new = []
    new = list_app(list_all, new)

    radio = []
    for i in range(len(data_class)):
        if(i in new):
            continue
        if(data_class[i][5] == 3):
            num = []
            for j in range(len(data_class)):
                if(data_class[j][7] == data_class[i][7]):
                    num.append(j)
            radio.append(num)

    if (len(radio) != 0):
        if (list_all == None):
            list_all = []
        list_all.append(radio)
    return list_all

# 复合复选框按钮
def recom_CheckBox(data_class,list_all):
    new = []
    new = list_app(list_all, new)
    check = []
    for i in range(len(data_class)):
        if(i in new):
            # print("已分组：", data_class[i])
            continue
        if (data_class[i][5] == 5):
            num = []
            # lab = 0
            for j in range(len(data_class)):
                if (data_class[j][7] == data_class[i][7]):
                    num.append(j)
                    # lab  = lab + 1
            check.append(num)
            # 可能没分到同一行，选择距离复选框近的一行
            # if(lab == 0):
            #     if(data_class[i-1][5] == 4 and (data_class[i][10] - data_class[i-1][10])<(data_class[i+1][10] - data_class[i][10])):
            #         data_class[i][1] = min(data_class[i][1], data_class[i-1][1])
            #         data_class[i][2] = min(data_class[i][2], data_class[i-1][2])
            #         data_class[i][3] = max(data_class[i][3], data_class[i-1][3])
            #         data_class[i][4] = max(data_class[i][4], data_class[i-1][4])
            #         num.append(i-1)
            #     else:
            #         if ((data_class[i+1][5] == 4 and (data_class[i+1][10] - data_class[i][10])<(data_class[i][10] - data_class[i-1][10]))):
            #             data_class[i][1] = min(data_class[i][1], data_class[i + 1][1])
            #             data_class[i][2] = min(data_class[i][2], data_class[i + 1][2])
            #             data_class[i][3] = max(data_class[i][3], data_class[i + 1][3])
            #             data_class[i][4] = max(data_class[i][4], data_class[i + 1][4])
            #             num.append(i + 1)
    if (len(check) != 0):
        if (list_all == None):
            list_all = []
        list_all.append(check)
    return list_all

# #复合开关按钮
def recom_Switch(data_class,list_all):
    new = []
    new = list_app(list_all, new)
    # print("listAll:\n",list_all)
    # print("new:\n",new)
    switch = []
    for i in range(len(data_class)):
        if (i in new):
            continue
        if (data_class[i][5] == 2):
            # lab = 0
            num = []
            for j in range(len(data_class)):
                if (data_class[j][7] == data_class[i][7]):
                    num.append(j)
            switch.append(num)
            #         lab = lab + 1
            # if (lab == 0):
            #     if (data_class[i - 1][5] == 4 and (data_class[i][10] - data_class[i - 1][10]) < (
            #             data_class[i + 1][10] - data_class[i][10])):
            #         data_class[i][1] = min(data_class[i][1], data_class[i - 1][1])
            #         data_class[i][2] = min(data_class[i][2], data_class[i - 1][2])
            #         data_class[i][3] = max(data_class[i][3], data_class[i - 1][3])
            #         data_class[i][4] = max(data_class[i][4], data_class[i - 1][4])
            #         num.append(i - 1)
            #     else:
            #         if ((data_class[i + 1][5] == 4 and (data_class[i + 1][10] - data_class[i][10]) < (
            #                 data_class[i][10] - data_class[i - 1][10]))):
            #             data_class[i][1] = min(data_class[i][1], data_class[i + 1][1])
            #             data_class[i][2] = min(data_class[i][2], data_class[i + 1][2])
            #             data_class[i][3] = max(data_class[i][3], data_class[i + 1][3])
            #             data_class[i][4] = max(data_class[i][4], data_class[i + 1][4])
            #             num.append(i + 1)
    # count = 0
    # for i in num:
    #     print(i)
    #     data_class = np.delete(data_class, i - count, 0)
    #     count = count + 1
    if (len(switch) != 0):
        if (list_all == None):
            list_all = []
        list_all.append(switch)
    return list_all

def one_RowList(data_class, rela, data_class_number, list_all):
    print("###########横向多次融合###########")
    new = []
    list_flatten = list_app(list_all, new)
    # 两个连接子图比较
    # 左右关系比较相似
    list_right1 = []
    temp = []
    for i in range(len(rela)):
        if data_class_number[i] in list_flatten:
            continue
        for j in range(i + 1, len(rela)):
            if data_class_number[j] in list_flatten:
                break
            if (rela[i][j] == 2):
                if ((data_class_number[i] in temp) and (data_class_number[j] in temp)):
                    continue
                if ((data_class_number[i] in temp) and (data_class_number[j] not in temp)):
                    temp.append(data_class_number[j])
                if ((data_class_number[j] in temp) and (data_class_number[i] not in temp)):
                    temp.append(data_class_number[i])
                if ((data_class_number[i] not in temp) and (data_class_number[j] not in temp)):
                    temp = "list_right_2%d" % i
                    temp = []
                    temp.append(data_class_number[i])
                    temp.append(data_class_number[j])
                    list_right1.append(temp)
    # 比较相似性
    print(list_right1)
    list_notadj = []
    print(len(list_right1))
    if (len(list_right1) == 0 or len(list_right1) == 1):
        list_right1.clear()
    else:
        temp = []
        adjacent = 0  # 判断是否有相邻的相似行
        for i in range(len(list_right1)):
            for j in range(i + 1, len(list_right1)):
                if (len(list_right1[i]) == len(list_right1[j])):
                    count_right1 = 0
                    for k in range(len(list_right1[i])):  # 遍历这两个列表，判断这两个列表中的对应的元素类型是否相同
                        if (data_class[list_right1[i][k]][5] != data_class[list_right1[j][k]][5]):
                            break
                        # edit 把下面的参数从0.5变成0.35
                        if (data_class[list_right1[i][k]][5] == data_class[list_right1[j][k]][5]):
                            # if (data_class[list_right1[i][k]][5] == data_class[list_right1[j][k]][5] and
                            #         (min(data_class[list_right1[i][k]][8], data_class[list_right1[j][k]][8]) / max(
                            #             data_class[list_right1[i][k]][8], data_class[list_right1[j][k]][8])) > 0.35):
                            count_right1 = count_right1 + 1
                            if (abs(data_class[i][7] - data_class[j][7]) == 1):
                                adjacent = adjacent + 1
                    if (count_right1 == len(list_right1[i]) and  # 不存在复选框，按钮和开关按钮且相邻
                                abs(data_class[list_right1[i][0]][7] - data_class[list_right1[j][0]][7]) == 1):
                        if ((list_right1[i] in temp) and (list_right1[j] in temp)):
                            continue
                        if ((list_right1[i] in temp) and (list_right1[j] not in temp)):
                            temp.append(list_right1[j])
                        if ((list_right1[j] in temp) and (list_right1[i] not in temp)):
                            temp.append(list_right1[i])
                        if ((list_right1[i] not in temp) and (list_right1[j] not in temp)):
                            temp = "list_right_4%d" % i
                            temp = []
                            temp.append(list_right1[i])
                            temp.append(list_right1[j])
                            list_all.append(temp)
                    if (adjacent == 0 and count_right1 == len(list_right1[i]) and  # 不存在复选框，按钮和开关按钮且不相邻
                                abs(data_class[list_right1[i][0]][7] - data_class[list_right1[j][0]][7]) > 1):
                        if (list_right1[i] in temp and list_right1[j] in temp):
                            continue
                        if (list_right1[i] in temp and list_right1[j] not in temp):
                            temp.append(list_right1[j])
                        if (list_right1[j] in temp and list_right1[i] not in temp):
                            temp.append(list_right1[i])
                        if (list_right1[i] not in temp and list_right1[j] not in temp):
                            temp = "list_right_5%d" % i
                            temp = []
                            temp.append(list_right1[i])
                            temp.append(list_right1[j])
                            list_notadj.append(temp)
                    else:
                        continue
        print("左右关系融合分组", list_all)
    print("-------------END横向------------")
    return list_all

def one_Double_ColumnList(list_all, rela, data_class_number, data_class):
    print("###########纵向多次融合###########")
    # 上下融合（分两种情况）
    # 上下融合一次的情况
    new = []
    list_flatten = list_app(list_all, new)
    list_down = []
    temp = []
    # print("data_class_number",data_class_number)
    # print("list_all", list_all)
    # print("list_flatten",list_flatten)
    for i in range(len(rela)):
        if data_class_number[i] in list_flatten:
            continue
        for j in range(i, len(rela)):
            # print(i,j)
            if(i == j):
                continue
            if data_class_number[j] in list_flatten:
                continue
            if (rela[i][j] == 1):
                temp = "list_down_2%d" % i
                temp = []
                temp.append(data_class_number[i])
                temp.append(data_class_number[j])
                list_down.append(temp)

    # 1对多融合或多对1融合
    print("上下融合一次", list_down)

    temp = []
    list_down_del = []  # 记录要删除的有多对融合的组
    for i in range(len(list_down) - 1):
        for j in range(i + 1, len(list_down)):
            if (list_down[i][0] == list_down[j][0] and len(list_down[i]) == len(list_down[j])):
                if (list_down[j][0] in temp and list_down[j][1] not in temp):
                    temp.append(list_down[j][1])
                    list_down_del.append(list_down[j])
                if list_down[i][0] not in temp:
                    temp = "list_down_3%d" % i
                    temp = []
                    temp.append(list_down[i][0])
                    temp.append(list_down[i][1])
                    temp.append(list_down[j][1])
                    list_down.append(temp)
                    # print("iiiiii", i, j, temp)
                    list_down_del.append(list_down[i])
                    list_down_del.append(list_down[j])
    temp = []
    for i in range(len(list_down) - 1):
        if len(list_flatten) != 0:
            if data_class_number[i] in list_flatten:
                continue
        for j in range(i + 1, len(list_down)):
            if len(list_flatten) != 0:
                if data_class_number[j] in list_flatten:
                    continue
            if (list_down[i][1] == list_down[j][1] and len(list_down[i]) == len(list_down[j])):
                if (list_down[j][1] in temp and list_down[j][0] not in temp):
                    temp.append(list_down[j][0])
                    list_down_del.append(list_down[j])
                    # print("jjjjjjjjj", i, j, temp)
                if list_down[i][1] not in temp:
                    temp = "list_down_4%d" % i
                    temp = []
                    temp.append(list_down[i][0])
                    temp.append(list_down[j][0])
                    temp.append(list_down[i][1])
                    list_down.append(temp)
                    # print("jjjjjjjjj", i, j, list_down)
                    list_down_del.append(list_down[i])
                    list_down_del.append(list_down[j])
    # print(list_down)
    for i in list_down_del:
        if i in list_down:
            list_down.remove(i)
    # 多对融合排序
    if len(list_down) != 0:
        for i in range(len(list_down)):
            list_down[i] = sorted(list_down[i])
    # print("22222222222222222", list_down)
    # 比较相似性，判断所有同行差是否均为2的倍数和找寻个数最多，数量最多的组
    list_down_temp = []
    temp = []
    if (len(list_down) == 0 or len(list_down) == 1):
        list_down.clear()
    else:
        for i in range(len(list_down)):
            for j in range(i + 1, len(list_down)):
                if (len(list_down[i]) == len(list_down[j])):
                    count_down1 = 0
                    for k in range(len(list_down[i])):  # 遍历这两个列表，判断这两个列表中的对应的元素类型是否相同
                        if (data_class[list_down[i][k]][5] != data_class[list_down[j][k]][5]):
                            break
                        if (data_class[list_down[i][k]][5] == data_class[list_down[j][k]][5]):
                            count_down1 = count_down1 + 1
                    if (count_down1 == len(list_down[i])):
                        if ((list_down[i] and list_down[j]) in temp):
                            continue
                        if (list_down[i] in temp):
                            temp.append(list_down[j])
                        if list_down[i] not in temp:
                            temp = "list_down_5%d" % i
                            temp = []
                            temp.append(list_down[i])
                            temp.append(list_down[j])
                            list_down_temp.append(temp)
    # print(list_down_temp)
    # 判断是否上下只需要融合一次的类型
    if (len(list_down_temp) == 0):
        list_down.clear()
    if (len(list_down_temp) == 1):  # 一行两两融合相似组
        list_all = list_all + list_down_temp
        print("上下关系一行融合一次分组", list_all)
    if (len(list_down_temp) > 1):
        # print("..........", list_down_temp)
        count_0 = 0
        count_2 = 0
        count_n = 0
        for i in range(len(list_down_temp)):
            for j in range(len(list_down_temp[i]) - 1):
                # for k in range(len(list_down_temp[i][j])):
                if (abs(data_class[list_down_temp[i][j][0]][7] - data_class[list_down_temp[i][j + 1][0]][7]) == 0):
                    count_0 = count_0 + 1
                if (abs(data_class[list_down_temp[i][j][0]][7] - data_class[list_down_temp[i][j + 1][0]][7]) == 2):
                    count_2 = count_2 + 1
                if (abs(data_class[list_down_temp[i][j][0]][7] - data_class[list_down_temp[i][j + 1][0]][7]) > 2):
                    count_n = count_n + 1
        # print(count_0, count_2, count_n)
        if (count_0 > 0):  # 多行两两融合相似组
            # 筛选最长列表
            max_list = 0  # 记录最长列表
            list_max = []
            if (len(list_down_temp) == 0):
                list_down_temp.clear()
            if (len(list_down_temp) > 1):
                for i in range(len(list_down_temp)):
                    new=[]
                    s=len(list_app(list_down_temp[i],new))
                    if (max_list < s):
                        max_list = s
                        list_max = list_down_temp[i]
                for i in list_down_temp[::-1]:
                    # print(i)
                    if i != list_max:
                        list_down_temp.remove(i)
            list_all = list_all + list_down_temp
            print("上下关系多行融合一次分组", list_all)

        if (count_n > 0):  # 多行且一对或多对融合相似组
            row_hao1 = []
            row_distance1 = 0
            if (len(list_down_temp) != 0):
                for i in range(len((np.array(list_down_temp)).shape) - 1):
                    if (i == 0):
                        list_n_flatten = list(itertools.chain.from_iterable(list_down_temp))  # 将多维列表变为一维列表
                    else:
                        list_n_flatten = list(itertools.chain.from_iterable(list_n_flatten))
            # print("555555555", list_n_flatten)
            for i in range(len(list_n_flatten)):
                row_hao1.append(data_class[list_n_flatten[i]][7])
            min_row1 = min(row_hao1)
            max_row1 = max(row_hao1)
            # print(max_row1)
            for i in range(len(list_down_temp)):
                for j in range(len(list_down_temp[i])):
                    for k in range(len(list_down_temp[i][j])):
                        if (min_row1 == data_class[list_down_temp[i][j][k]][7]):
                            row_distance1 = data_class[list_down_temp[i][j + 1][k]][7] - \
                                            data_class[list_down_temp[i][j][k]][7] - 2
                            i_record1 = i
                            j_record1 = j
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            t1 = 1  # 记录循环的次数
            # print(row_distance1)
            # print(list_down_temp[i_record1])
            while (row_distance1 > 0):
                for i in range(len(list_down_temp[i_record1])):
                    if data_class_number[i] in list_flatten:
                        continue
                    for j in range(len(data_class)):
                        if data_class_number[j] in list_flatten:
                            continue
                        while (data_class[j][7] == data_class[list_down_temp[i_record1][i][0]][7] + t1 + 1 and
                               data_class[j][6] in list_n_flatten and
                               (rela[j, 1] < (rela[list_down_temp[i_record1][i][0], 1] + (
                                       rela[list_down_temp[i_record1][i][0], 3] - rela[
                                   list_down_temp[i_record1][i][0], 1]) / 2) < rela[j, 3]) or
                               (rela[list_down_temp[i_record1][i][0], 1] < (
                                       rela[j, 1] + (rela[j, 3] - rela[j, 1]) / 2) < rela[
                                    list_down_temp[i_record1][i][0], 3])):
                            if (count_0 > 0):  # 多行且多对融合相似组
                                for k in range(len(list_down_temp[i_record1])):
                                    if (rela[list_down_temp[i_record1][k]][j] == 1):
                                        if data_class_number[j] in list_down_temp[i_record1][i]:
                                            continue
                                        if data_class_number[j] not in list_down_temp[i_record1][i]:
                                            list_down_temp[i_record1][i].append(data_class[j][6])
                                            list_all.append(list_down_temp[i_record1][i])
                                        break
                                    else:
                                        continue
                            if (count_0 == 0):  # 多行且一对融合相似组
                                if data_class_number[j] in list_down_temp[i_record1][i]:
                                    continue
                                if data_class_number[j] not in list_down_temp[i_record1][i]:
                                    list_down_temp[i_record1][i].append(data_class_number[j])
                                    list_all.append(list_down_temp[i_record1][i])
                            row_distance1 = row_distance1 - 1
                            t1 = t1 + 1
    print("上下关系多行融合多次分组", list_all)
    print("-------------END纵向------------")
    return list_all
def Other_List(list_all,rela,data_class_number,data_class):
    new=[]
    list_flatten = list_app(list_all,new)
    list_right1 = []
    temp = []
    for i in range(len(rela)):
        if data_class_number[i] in list_flatten:
            continue
        for j in range(i+1, len(rela)):
            if data_class_number[j] in list_flatten:
                break
            if (rela[i][j] == 2):
                if (data_class_number[i] in temp and data_class_number[j] in temp):
                    continue
                if (data_class_number[i] in temp and data_class_number[j] not in temp):
                    temp.append(data_class_number[j])
                if (data_class_number[j] in temp and data_class_number[i] not in temp):
                    temp.append(data_class_number[i])
                if data_class_number[i] not in temp:
                    temp = "list_right_2%d" % i
                    temp = []
                    temp.append(data_class_number[i])
                    temp.append(data_class_number[j])
                    # numpy_first=np.array(data_class[i,:])
                    # numpy_first=np.row_stack((numpy_first, np.array(data_class[j,:])))
                    list_right1.append(temp)
    temp = []

    list_right2=[]#存储有相似组的合并组
    list_right3=[]#存储有相似组的单个组
    if (len(list_right1) == 0 or len(list_right1) == 1):
        list_right1.clear()
    adjacent = 0  # 判断是否有相邻的相似行
    for i in range(len(list_right1)):
        for j in range(i + 1, len(list_right1)):
            if (len(list_right1[i]) == len(list_right1[j])):
                count_right1 = 0
                for k in range(len(list_right1[i])):  # 遍历这两个列表，判断这两个列表中的对应的元素类型是否相同
                    if (data_class[list_right1[i][k]][5] != data_class[list_right1[j][k]][5]):
                        break
                    if (data_class[list_right1[i][k]][5] == data_class[list_right1[j][k]][5] and
                                (min(data_class[list_right1[i][k]][8], data_class[list_right1[j][k]][8]) / max(
                                    data_class[list_right1[i][k]][8], data_class[list_right1[j][k]][8])) > 0.5):
                        count_right1 = count_right1 + 1
                        if (abs(data_class[list_right1[i][0]][7] - data_class[list_right1[j][0]][7]) == 1):
                            adjacent = adjacent + 1
                if(count_right1==len(list_right1[j])):
                    if (list_right1[i] in list_right3 and list_right1[j] in list_right3):
                        continue
                    if (list_right1[i] in list_right3):
                        list_right3.append(list_right1[j])
                        temp.append(list_right1[j])
                    if (list_right1[i] not in list_right3 and list_right1[j] not in list_right3):
                        temp = "list_right_3%d" % i
                        temp = []
                        temp.append(list_right1[i])
                        temp.append(list_right1[j])
                        list_right3.append(list_right1[i])
                        list_right3.append(list_right1[j])
                        list_right2.append(temp)
    print(len(list_right2))
    list_notadj_flatten = []
    if (adjacent == 0):
        row_hao = []
        new=[]
        list_notadj_flatten = list_app(list_right3,new)
        for i in range(len(list_notadj_flatten)):
            row_hao.append(data_class[list_notadj_flatten[i]][7])
        print("++++++++++++++", list_notadj_flatten)
        if len(row_hao) != 0:
            min_row = min(row_hao)
            max_row = max(row_hao)
            for i in range(len(list_right2)):
                for j in range(len(list_right2[i])):
                    for k in range(len(list_right2[i][j])):
                        if (min_row == data_class[list_right2[i][j][k]][7]):
                            row_distance = abs(data_class[list_right2[i][j + 1][k]][7] - data_class[list_right2[i][j][k]][7])- 1
                            i_record = i
                            j_record = j
                            k_record = k
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            t=row_distance
            # 根据相似组行距，融合其他行
            list_other=[]
            for i in range(len(list_right2[i_record])):
                temp = []
                for k in range(1,row_distance+1):
                    for j in range(len(data_class)):
                         if (data_class[j][7] == data_class[list_right2[i_record][i][0]][7] + k ):
                             if(len(temp)==0):
                                 list_right2[i_record][i].append(data_class[j][6])
                                 temp=list_right2[i_record][i]
                                 print(temp,list_right2[i_record][i],data_class[j][6])
                             else:
                                 temp.append(data_class[j][6])
                list_other.append(temp)
            list_other_end=[]
            for i in range(len(list_other)):
                for j in range(i + 1, len(list_other)):
                    if (len(list_other[i]) == len(list_other[j])):
                        count_list_other = 0
                        for k in range(len(list_other[i])):  # 遍历这两个列表，判断这两个列表中的对应的元素类型是否相同
                            if (data_class[list_other[i][k]][5] != data_class[list_other[j][k]][5]):
                                break
                            if (data_class[list_other[i][k]][5] == data_class[list_other[j][k]][5] and
                                        (min(data_class[list_other[i][k]][8], data_class[list_other[j][k]][8]) / max(
                                            data_class[list_other[i][k]][8], data_class[list_other[j][k]][8])) > 0.5):
                                count_list_other = count_list_other + 1
                        if(count_list_other==len(list_other[j])):
                            if (list_other[i] in list_other_end and list_other[j] in list_other_end):
                                continue
                            if             (list_other[i] in list_other_end):
                                list_other_end.append(list_other[j])
                            if (list_other[i] not in list_other_end and list_other[j] not in list_other_end):
                                list_other_end.append(list_other[i])
                                list_other_end.append(list_other[j])
                                list_all.append(list_other_end)
            print(list_other_end)

    print("其他分组", list_all)
    return list_all
# 存储每个顶点左右关系


# 把维度不规则列表转变为一维列表
def list_app(list_all_other,new):
    for l in list_all_other:
         if isinstance(l, list):
             list_app(l,new) # 调用递归
         else:
             # 如果不是,把l添加进一个新的list
             new.append(l)
    return new
def main():
    # 下载数据
    data_all = np.loadtxt("Image_temp.txt")
    data_i = np.unique(data_all[:, 0])
    print(data_i)
    image_num = 0
    data_i = np.array(data_i)
    data_i = np.trunc(data_i)
    data_i = data_i.astype('int')
    print(len(data_i))
    for i in range(len(data_i)):
        data = []
        for j in range(len(data_all)):
            if (data_i[i] == data_all[j, 0]):
                data.append(data_all[j])
            else:
                continue
        image_num=image_num+1
        data = np.array(data)
        data = np.trunc(data)
        data = data.astype('int')
        # 元素数据（0图片名称，1左上角横，2左上角纵，3右上角横，4右上角纵，5元素类型，6元素序号，7元素行号，8元素面积，9元素中心横，10元素中心纵）
        data_class=element_Data(data,data_i,image_num)
        #元素之间距离
        distance=element_Dis(data_class)
        #元素之间的左右上下关系
        rela,data_rela=element_Rela(data_class)

        data_class_number = []  # 存储所有节点的序号
        for i in data_class:
            data_class_number.append(i[6])
        print(data_class_number)

        list_all = []  # 存储最后的分组后的所有节点
        #单文本/图片分组
        list_all=one_Group(rela,data_rela,list_all,data_class_number,data_class)

        # 语义复合组合按钮
        list_all = semantic_RecomButton(data_class, rela, distance, list_all)
        # # 复合单选按钮
        list_all = recom_RadioBox(data_class, list_all)
        # # 复合复选框按钮
        list_all = recom_CheckBox(data_class, list_all)
        # # 复合开关按钮
        list_all = recom_Switch(data_class, list_all)

        #单行列表项（横向多次融合）
        list_all = one_RowList(data_class, rela, data_class_number, list_all)
        #单双列表项（纵向多次融合）
        list_all = one_Double_ColumnList(list_all, rela, data_class_number, data_class)
        #列表项（横向纵向多次融合）
        list_all=Other_List(list_all,rela,data_class_number,data_class)
        new=[]
        list_flatten=list_app(list_all,new)
        # 查找剩余节点，默认为孤单节点
        for i in data_class_number:
            if (i not in list_flatten):
                list_all.append(i)
            else:
                continue
        print(list_all)
        for i in range(len(list_all)):
            if isinstance(list_all[i], list) is False:
                list_all[i] = data_class[list_all[i]].tolist()
            else:
                for j in range(len(list_all[i])):
                    list_all[i][j] = data_class[list_all[i][j]].tolist()
        print(list_all)
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
if __name__ == '__main__':
    main()
