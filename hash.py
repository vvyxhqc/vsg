import numpy as np
import cv2
import pandas as pd
import dataframe

#下载数据
data_all=np.loadtxt("Image_all.txt")
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



 # # 切割行



 # img = cv2.imread('7332.jpg')
 # print(data_i[k-1],"/////////////////////////////////////////")
 img = cv2.imread('%d.jpg'%(data_i[k-1]))
 # img = cv2.imread('004759.jpg')
 # cv2.imshow('45',img)
 # cv2.waitKey(0)
 for i in range(len(data)):
    cv2.imwrite('D:/graduate-one/vsg/mix/%s'% (data_i[k-1])+'_'+"%d.jpg" % (i+1),
                img[int(data[i, 2]):int(data[i, 4]), int(data[i, 1]):int(data[i, 3])])

# # cv2.imwrite('%d.jpg'%i,temp)
# #     cv2.imwrite("%d.jpg"%i,img[int(data1[i,2]):int(data1[i,4]),int(data1[i,1]):int(data1[i,3])])
# # cropped1 =
# # 裁剪坐标为[y0:y1, x0:x1]
# cropped2 = img[0:100,0:100] # 裁剪坐标为[y0:y1, x0:x1]
# cropped3 = img[347:397,88: 360] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped4 = img[347:397,88: 469] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped5 = img[347:397,88: 469] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped6 = img[103:165,158: 402] # 裁剪坐标为[y0:y1, x0:x1]
# # cropped7 = img[408:492,102: 874] # 裁剪坐标为[y0:y1, x0:x1]
# # cv2.imwrite("0.jpg", cropped1)
# cv2.imwrite("1.jpg", cropped2)
# cv2.imwrite("2.jpg", cropped3)
# # cv2.imwrite("3.jpg", cropped4)
# # cv2.imwrite("4.jpg", cropped5)
# # cv2.imwrite("5.jpg", cropped6)
# # cv2.imwrite("6.jpg", cropped7)
# #print(data.size)
