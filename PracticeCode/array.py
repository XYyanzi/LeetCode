'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2021/3/23 4:26 下午
@File: array.py
'''


class PracticeArray:

    @staticmethod
    def basic():
        # 创建数组
        a = []
        # 添加元素 append方式  时间复杂度可能是O(1)或O(N)
        a.append(1)
        a.append(3)
        a.append(4)
        print(a)
        print(type(a))
        # 添加元素 insert方式 时间复杂度是O(N)
        a.insert(2, 99)
        print(a)
        # 访问元素
        print(a[2])
        # 更新元素
        a[2] = 88
        # 删除元素 remove  O(1)
        a.remove(88)  # 这里传入的是元素值
        # 删除元素 pop  O(N)
        a.pop(1)  # 这里传入的是索引
        # 删除元素 pop()  O(1)
        a.pop()  # 删除最后一个元素
        # 获取数组长度
        len(a)
        # 遍历数组
        for i in a:
            print(a[i])
        for index, element in enumerate(a):
            print(index, element)
        for i in range(0, len(a)):
            print(a[i])
        # 查找某个元素
        index = a.index(2)  # 查找元素2的索引
        print(index)
        # 数组排序  O(NlogN)
        a.sort()
        a.sort(reverse=True)



if __name__ == '__main__':
    o = PracticeArray()
    o.basic()
