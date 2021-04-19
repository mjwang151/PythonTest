tips = ['A. 东京']
xXian = ['A. 东京', 'B. 莫斯科', 'C. 开罗', 'D. 雅尔塔']
for xx in xXian:
    for tip in tips:
        if tip in xx:
            print('答案是:' + xx)


list1 =['A. 东京', 'B. 莫斯科', 'C. 开罗', 'D. 雅尔塔']
list2 =[]

for i in range(len(list1)):
    print(str(i)+':'+str(len(list1)))
    list2.append(list1[i])
print(list2)