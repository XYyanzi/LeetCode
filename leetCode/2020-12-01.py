'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/1 12:46 下午
@File: 2020-12-01.py
'''

"""
给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置（第一次出现的位置）和结束位置（第二次出现的位置）。
如果数组中不存在目标值 target，返回 [-1, -1]。
示例1：
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
示例2：
输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
示例3：
输入：nums = [], target = 0
输出：[-1,-1]
"""


class Solution(object):
    def binarySearch(self, search_list, target) -> int:
        """
        二分查找，找到target对应的下标
        :param search_list: 被查找的有序list
        :param target: 目标数字
        :return:
        """
        count = 1  # 循环次数计数
        left = 0
        right = len(search_list) - 1
        if target not in search_list:
            print("该元素不再列表中")
            return -1
        else:
            while left <= right:
                mid = (left + right) // 2  # python整除符号使用//，结果向下取整  /表示除法，返回float
                # mid = left + (right - left)/2  # 这种写法可以防止left + right超出整数范围溢出
                if target > search_list[mid]:
                    left = mid + 1
                    print(
                        "这是循环第{}次，此时mid={}, target{} > search_list[mid]{}, 下次查找区间是：[{},{}]".format(count, mid, target, search_list[mid], left, right))
                    count += 1
                elif target < search_list[mid]:
                    right = mid
                    print(
                        "这是循环第{}次，此时mid={}, target{} < search_list[mid]{},下次查找区间是：[{},{}]".format(count, mid, target, search_list[mid], left, right))
                    count += 1
                elif target == search_list[mid]:
                    print("这是循环第{}次，此时mid={}, target{} = search_list[mid]{}".format(count, mid, target, search_list[mid]))
                    count += 1
                    return mid

    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """


if __name__ == '__main__':
    solution = Solution()
    search_list = [-2, 4, 5, 7, 8, 12, 40, 50, 60, 70]
    index = solution.binarySearch(search_list, 70)
    print(index)
