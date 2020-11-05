import numpy as np
import cv2
import pandas as pd
import dataframe

#下载数据
data_all=np.loadtxt("Image_all_all.txt")
data_i=np.unique(data_all[:,0])
print(data_i)
k = 0
data_i = np.array(data_i)
data_i = np.trunc(data_i)
data_i = data_i.astype('int')
print(len(data_i))
for i in range(len(data_i)):
 data=[]
 for i in range(len(data_all)):
     if(data_i[k]==data_all[i,0]):
         data.append(data_all[i])
     else:
         continue
 k=k+1
 data=np.array(data)
 data=np.trunc(data)
 data=data.astype('int')
 data3=data.copy()
 #找多个元素是否同行的循环次数
 # s=0

 # 按第3列X0进行排序，按高度排列
 data = data[data[:, 2].argsort()]
 print(data)
 #根据元素横坐标结合高度筛选出从左到右，从上到下的排列序号
 for i in range(1,len(data)):
     for j in range(0,len(data)):
         if (data[j - 1, 4] < data[j, 2] and data[i, 1] < data[j, 1] and 0 < data[i, 2] - data[j, 2] < 50 and
            data[i, 3] < data[j, 3] and 0 < data[i, 4] - data[j, 4] < 50):
             temp = np.copy(data[i])
             data[i]=data[j]
             data[j]=temp
             print("1",i,j)

         if (data[i, 1] < data[j, 1] and data[i, 2] > data[j, 2] and data[i, 3] < data[j, 3] and data[i, 4] < data[j, 4]):
             temp1 = np.copy(data[i])
             data[i] = data[j]
             data[j] = temp1
             print("2",i,j)

         if (data[i, 1] < data[j, 1] and data[i, 2] < data[j, 2] and data[i, 3] < data[j, 3] and data[i, 4] > data[j, 4]):
             temp1 = np.copy(data[i])
             data[i] = data[j]
             data[j] = temp1
             print("3",i,j)

 element_num=[]#存储每个元素序号
 for i in range(len(data)):
     element_num.append(i)
 #把一列元素序号加入数组中
 data = np.column_stack((data,np.array(element_num)))
 print(data)



 i=0
 j=0
 count=0#跳过已被判定过行号的循环
 row_num=[]#存储行号
 m=0#每行只有一个元素时，记录行号
 n=0#记录所有元素数目和行数目之差
 for i in range(0,len(data)):
     #跳过已被判定为行的循环
     if(count>0):
         count=count-1
         row_num.append( i - n - 1)
         n=n+1
         continue
     row_num.append(m)
     m = m + 1
     for j in range(i+1,len(data)):
         temp=data[i,:]
         # 左包含右
         if(data[i,1] <= data[j,1]and data[i,2] <= data[j,2]and data[i,3] <= data[j,3]and data[i,4] >= data[j,4]):
             column1=np.row_stack((temp, data[j,:]))
             print("aa",i,column1)
             count=count + 1
             continue
         # 右包含左
         if(data[i,1] <= data[j ,1]and data[i,2] >= data[j,2]and data[i,3] <= data[j,3]and data[i,4] <= data[j,4]):
             column2=np.row_stack((temp, data[j,:]))
             print("bb",i,column2)
             count=count + 1
             i=i+1
             continue
         #左高右低
         if (data[i, 1] <= data[j, 1] and data[i, 3] <= data[j, 3] and ((data[j, 2]>data[i, 2] and 0<=data[j, 4] - data[i, 4]<=50))):#
             #    )and abs(data[j,2]-data[i,4])>10
             column3 = np.row_stack((temp, data[j,:]))
             print("cc",i,column3)
             count= count + 1
             continue
         #左低右高
         if (data[i, 1] <= data[j, 1] and  data[i, 3] <= data[j, 3] and((0<=data[i, 2] - data[j, 2]<=50 and data[i, 4]>data[j, 4]))):
             # and abs(data[i,2]-data[j,4]>10)
             column4 = np.row_stack((temp, data[j,:]))
             print("dd",i,column4)
             count= count + 1
             continue
         # 左低右高(右序号在前）
         if (data[i, 1] > data[j, 1] and 0<=data[j, 2] - data[i, 2]<=50 and  data[i, 3] > data[j, 3] and 0<=data[j, 4]-data[i, 4]<=50):
             column5 = np.row_stack((temp, data[j,:]))
             print("ee",i,column5)
             count= count + 1
             continue

         # s=s+1
 print("******************************************")
 data=np.column_stack((data,np.array(row_num)))#把一列行序号加入数组中
 print("data",data)



 #行内第一次融合
 data3=data.copy()
 count3=0
 data4=[]
 for i in range(len(data3)):
     if (count3 > 0):
         count3 = count3 - 1
         continue
     for j in range(i+1,len(data)):
         if(data3[i,7]==data3[j,7] and data3[i,5] != data3[j,5]):
             count3 = count3 + 1
             data4.append(j)
             data3[i,5]= 6
             print(i, j)
             # i在后面的情况
             if (data3[i, 1] > data3[j, 1]):
                 data3[i, 1] = data3[j, 1]
                 data3[i, 4] = data3[j, 4]
                 print(i,j,"1")
                 break
             if (data3[i, 2] > data3[j, 2] and data3[i, 4] < data3[j, 4]):
                 data3[i, 2] = data3[j, 2]
                 data3[i, 3] = data3[j, 3]
                 data3[i, 4] = data3[j, 4]
                 # data1=np.delete(data1,i,0)
                 print(i, j,"2")
                 break
             if (data3[i, 2] > data3[j, 2]):
                 data3[i, 2] = data3[j, 2]
                 data3[i, 3] = data3[j, 3]
                 print(i, j,"3")
                 break
             if (data3[i, 4] < data3[j, 4]):
                 data3[i, 3] = data3[j, 3]
                 data3[i, 4] = data3[j, 4]
                 print(i, j,"4")
                 break
             data3[i, 3] = data3[j, 3]
         break
 print(data3)
 count4_2=0
 for i in data4:
     data3=np.delete(data3, i - count4_2, 0)
     count4_2= count4_2 + 1
 i=0
 for i in range(len(data3)):
     data3[i,6]=i
 print("data3",data3)

 #行内第二次融合
 data3_1=data3.copy()
 count3_1=0
 data4_1=[]
 for i in range(len(data3_1)):
     if (count3_1 > 0):
         count3_1 = count3_1 - 1
         continue
     for j in range(i+1,len(data3)):
         if(data3_1[i,7]==data3_1[j,7] and data3_1[i,5] != data3_1[j,5]):
             count3_1 = count3_1  + 1
             data4_1.append(j)
             data3_1[i,5]= 6
             print(i, j)
             # i在后面的情况
             if (data3_1[i, 1] > data3_1[j, 1]):
                 data3_1[i, 1] = data3_1[j, 1]
                 data3_1[i, 4] = data3_1[j, 4]
                 print(i,j,"1")
                 break
             # 右包含左
             if (data3_1[i, 2] > data3_1[j, 2] and data3_1[i, 3] < data3_1[j, 3] and data3_1[i, 4] < data3_1[j, 4]):
                 data3_1[i, 2] = data3_1[j, 2]
                 data3_1[i, 3] = data3_1[j, 3]
                 data3_1[i, 4] = data3_1[j, 4]
                 # data1=np.delete(data1,i,0)
                 print(i, j,"2")
                 break
             # 左上右下
             if (data3_1[i, 3] < data3_1[j, 3] and data3_1[i, 4] < data3_1[j, 4]):
                 data3_1[i, 3] = data3_1[j, 3]
                 data3_1[i, 4] = data3_1[j, 4]
                 print(i, j, "3")
                 break
             # 左下右上
             if (data3_1[i, 2] > data3_1[j, 2] and data3_1[i, 3] < data3_1[j, 3]):
                 data3_1[i, 2] = data3_1[j, 2]
                 data3_1[i, 3] = data3_1[j, 3]
                 print(i, j, "4")
                 break
             # 左包含右
             if (data3_1[i, 3] < data3_1[j, 3]):
                 data3_1[i, 3] = data3_1[j, 3]
                 print(i, j,"5")
                 break
         break
 print(data3_1)
 count4_1=0
 for i in data4_1:
     data3_1=np.delete(data3_1,i-count4_1,0)
     count4_1= count4_1+1
 i=0
 for i in range(len(data3_1)):
     data3_1[i,6]=i
 print("data3_1",data3_1)


 # 行间距之和
 data8=data[0,:]
 for i in range(1,len(data)):
     if(data[i,7]==data[i-1,7]):
         continue
     else:
         data8=np.row_stack((data8, data[i, :]))
 print("data8",data8)
 num=0
 for i in range(1,len(data8)):
     num=num+data8[i,2]-data8[i-1,4]
 print("num",num)
 num=num/(len(data8)-1)



 # 行外第一次融合
 data5_1 = data3_1.copy()
 data6_1 = []
 data7_1 = data3_1[:, 7]
 data7_1 = data7_1.tolist()
 print(data7_1)
 print("................................")
 for i in range(len(data5_1)):
     if (i in data6_1):
         continue
     for j in range(i + 1, len(data5_1)):
         i_num = data5_1[i, 7]
         j_num = data5_1[j, 7]
         if (data5_1[j, 7] - data5_1[i, 7] == 1 and (data5_1[i, 5] != data5_1[j, 5] and data7_1.count(i_num) == data7_1.count(j_num)
                                                     and (abs(data5_1[i, 1] - data5_1[j, 1]) <= 50 or abs(data5_1[i, 3] - data5_1[j, 3]) <= 50) and abs(data5_1[j, 2] - data5_1[i, 4]) < num)
            or abs(data5_1[j, 2] - data5_1[i, 4]) <= 10):
             data5_1[i, 4] = data5_1[j, 4]
             data6_1.append(j)
             print(i, j)
             if (data5_1[i, 1] > data5_1[j, 1] and data5_1[i, 3] < data5_1[j, 3]):
                 data5_1[i, 1] = data5_1[j, 1]
                 data5_1[i, 3] = data5_1[j, 3]
                 # data1=np.delete(data1,i,0)
                 break
             if (data5_1[i, 1] > data5_1[j, 1]):
                 data5_1[i, 1] = data5_1[j, 1]
                 break
             if (data5_1[i, 3] < data5_1[j, 3]):
                 data5_1[i, 3] = data5_1[j, 3]
                 break
 print("data5_1", data5_1)

 count4_2 = 0
 for i in data6_1:
     data5_1 = np.delete(data5_1, i - count4_2, 0)
     count4_2 = count4_2 + 1
 # 重置序列
 for i in range(len(data5_1)):
     data5_1[i, 6] = i
 j = 0
 for i in range(1, len(data5_1)):
     if (data5_1[i, 7] == data5_1[i - 1, 7]):
         data5_1[i, 7] = j
         data5_1[i - 1, 7] = j
     else:
         j = j + 1
 print("last_data5", data5_1)
 print("******************************************")

 # 行外第二次融合
 data5 = data5_1.copy()
 data6 = []
 data7 = data5_1[:, 7]
 data7 = data7.tolist()
 print(data7)
 print("................................")
 for i in range(len(data5)):
     if (i in data6):
         continue
     for j in range(i + 1, len(data5)):
         i_num = data5[i, 7]
         j_num = data5[j, 7]
         if (data5[j, 7] - data5[i, 7] == 1 and (data5[i, 5] != data5[j, 5] and data7.count(i_num) == data7.count(j_num)
                                                 and (abs(data5[i, 1] - data5[j, 1]) <= 50 or abs(
                     data5[i, 3] - data5[j, 3]) <= 50) and abs(data5[j, 2] - data5[i, 4]) < num)
                 or abs(data5[j, 2] - data5[i, 4]) <= 10):
             data5[i, 4] = data5[j, 4]
             data6.append(j)
             print(i, j)
             if (data5[i, 1] > data5[j, 1] and data5[i, 3] < data5[j, 3]):
                 data5[i, 1] = data5[j, 1]
                 data5[i, 3] = data5[j, 3]
                 # data1=np.delete(data1,i,0)
                 break
             if (data5[i, 1] > data5[j, 1]):
                 data5[i, 1] = data5[j, 1]
                 break
             if (data5[i, 3] < data5[j, 3]):
                 data5[i, 3] = data5[j, 3]
                 break
 print("data5", data5)

 count4 = 0
 for i in data6:
     data5 = np.delete(data5, i - count4, 0)
     count4 = count4 + 1
 # 重置序列
 for i in range(len(data5)):
     data5[i, 6] = i
 j = 0
 for i in range(1, len(data5)):
     if (data5[i, 7] == data5[i - 1, 7]):
         data5[i, 7] = j
         data5[i - 1, 7] = j
     else:
         j = j + 1
 print("last_data5", data5)
 print("******************************************")

 #判定一行中元素最高和最低坐标
 data1=data5.copy()
 # data1=data1.tolist()
 # for i in range(len(data1)):
 #     for j in range(i, len(data1)):
 #         if(data1[i, 6] == data1[j, 6]):
 #             data1
 # data1=np.unique(data1[:,6],axis=0)
 print(data1)
 data2=[]
 # num=0
 # i=0
 count2=0
 for i in range(0,len(data1)):
     if (count2 > 0):
         count2 = count2 - 1
         continue
     for j in range(i+1, len(data1)):
         if (data1[i, 7] == data1[j, 7]):
             count2=count2+1

             data2.append(j)
             # 下包含上
             if (data1[i, 1] > data1[j, 1] and data1[i, 3] < data1[j, 3] and data1[i, 4] < data1[j, 4]):
                 data1[i, 1] = data1[j, 1]
                 data1[i, 3] = data1[j, 3]
                 data1[i, 4] = data1[j, 4]
                 # data1=np.delete(data1,i,0)
                 continue
                 #右包含左
             if (data1[i, 2] > data1[j, 2] and data1[i, 4] < data1[j, 4]):
                 data1[i, 2] = data1[j, 2]
                 data1[i, 3] = data1[j, 3]
                 data1[i, 4] = data1[j, 4]
                 # data1=np.delete(data1,i,0)
                 continue
             # 左低右高# 左下右上
             if (data1[i, 2] > data1[j, 2] and data1[i, 3] < data1[j, 3]):
                 data1[i, 2] = data1[j, 2]
                 data1[i, 3] = data1[j, 3]
                 continue
             # 左高右低 # 左上右下
             if (data1[i, 4] < data1[j, 4]and data1[i, 3] < data1[j, 3]):
                 data1[i, 3] = data1[j, 3]
                 data1[i, 4] = data1[j, 4]
                 continue
             # 元素序号在右，左包含右
             if (data1[i, 1] > data1[j, 1] and data1[i, 4] < data1[j, 4]):
                 data1[i, 1] = data1[j, 1]
                 data1[i, 4] = data1[j, 4]
                 # data1=np.delete(data1,i,0)
                 continue
             # 上包含下
             if (data1[i, 4] < data1[j, 4]):
                 data1[i, 4] = data1[j, 4]
                 # data1=np.delete(data1,i,0)
                 continue
             # 左包含右
             if (data1[i, 3] < data1[j, 3]):
                 data1[i, 3] = data1[j, 3]
                 # data1=np.delete(data1,i,0)
                 continue

         continue
 count1=0
 print(data2)
 for i in data2:
     data1=np.delete(data1,i-count1,0)
     count1=count1+1
 print(data1)




 # # 切割行
 # img = cv2.imread('007332.jpg')
 print(data_i[k-1],"/////////////////////////////////////////")
 img = cv2.imread('D:/118/%d.jpg'%(data_i[k-1]))
 # img = cv2.imread('004759.jpg')
 # cv2.imshow('45',img)
 # cv2.waitKey(0)
 for i in range(len(data1)):
    cv2.imwrite('D:/graduate-one/vsg/mix/%s'% (data_i[k-1])+'0'+"%d.jpg" % (i+1),
                img[int(data1[i, 2]):int(data1[i, 4]), int(data1[i, 1]):int(data1[i, 3])])

# # cv2.imwrite('%d.jpg'%i,temp)
# #     cv2.imwrite("%d.jpg"%i,img[int(data1[i,2]):int(data1[i,4]),int(data1[i,1]):int(data1[i,3])])
# # cropped1 =
# # 裁剪坐标为[y0:y1, x0:x1]
# # cropped2 = img[387:450,922: 990] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped3 = img[251:299,75: 288] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped4 = img[347:397,88: 469] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped5 = img[582:636,88: 388] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped6 = img[103:165,158: 402] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped7 = img[408:492,102: 874] # 裁剪坐标为[y0:y1, x0:x1]
# # cv2.imwrite("0.jpg", cropped1)
# # cv2.imwrite("1.jpg", cropped2)
# # cv2.imwrite("2.jpg", cropped3)
# # cv2.imwrite("3.jpg", cropped4)
# # cv2.imwrite("4.jpg", cropped5)
# # cv2.imwrite("5.jpg", cropped6)
# # cv2.imwrite("6.jpg", cropped7)
# #print(data.size)
