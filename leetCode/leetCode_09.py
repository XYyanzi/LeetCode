'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/3 1:02 下午
@File: leetCode_09.py
'''
"""
判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
示例：
输入: 121
输出: true

输入: -121
输出: false
解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。

输入: 10
输出: false
解释: 从右向左读, 为 01 。因此它不是一个回文数。

进阶：你能不将整数转为字符串来解决这个问题吗？
思路1：将数字转换成字符串，反转字符串，判断反转后字符串是否相等
思路2：将数字整个取反
小于0  return false
大于等于0小于10 return true
大于10 循环 获得倒序的list [3,2,1]
    将[3,2,1]转换成321
    笨方法循环遍历
"""


class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if type(x) != int:
            # x不是数字的话 直接返回false
            return False
        if x < 0:
            # 负数的情况 直接返回false
            return False
        if len(str(x)) == 1:
            # 如果反转之后长度是1 一定是回文数
            return True
        else:
            reverse_x = str(x)[::-1]
            print("反转之后结果是{}".format(reverse_x))
            if int(reverse_x) == x:
                return True
            else:
                return False

    def isPalindrome2(self, x):
        """
        :type x: int
        :rtype: bool
        """
        x_list = []
        if type(x) != int:
            # x不是数字的话 直接返回false
            return False
        if x < 0:
            # 负数的情况 直接返回false
            return False
        if 0 <= x < 10:
            return True
        else:
            temp = x
            while temp >= 10:
                x_list.append(temp % 10)
                print("此时x_list是{}".format(x_list))
                temp = int(temp / 10)
                if temp < 10:
                    x_list.append(temp)
        print("循环结束后获得的list是{}".format(x_list))
        reverse_x = 0
        for i in range(len(x_list)):
            reverse_x += x_list[i] * (10 ** (len(x_list) - i - 1))
            print(reverse_x)

        if reverse_x == x:
            return True
        else:
            return False


if __name__ == '__main__':
    s = Solution()
    print(s.isPalindrome2(121))
