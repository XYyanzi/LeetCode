'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/30 10:24 下午
@File: leetCode_26.py
'''
"""
给定一个排序数组，你需要在 原地 删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。
示例：
给定数组 nums = [1,1,2], 
函数应该返回新的长度 2, 并且原数组 nums 的前两个元素被修改为 1, 2。 
你不需要考虑数组中超出新长度后面的元素。

"""


class Solution(object):

    def remove_duplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        length = len(nums) - 1
        print(length)
        if length > 0:
            for i in range(length):
                print('第{}次循环, nums[length - i]={}, nums[length - i - 1]={}'.format(i, nums[length - i], nums[length - i - 1]))
                if nums[length - i] == nums[length - i - 1]:
                    del nums[length - i - 1]
        return len(nums)


l = [1, 1, 2, 2, 3, 4]
s = Solution()
print(s.remove_duplicates(l))
