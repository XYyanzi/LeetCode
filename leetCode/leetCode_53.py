'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/30 10:04 下午
@File: leetCode_53.py
'''
"""
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
输入: [-2,1,-3,4,-1,2,1,-5,4]
输出: 6
解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。
"""


class Solution(object):

    def max_sub_array(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        for i in range(1, len(nums)):
            print("第{}次循环, num[i]={}".format(i, nums[i]))
            nums[i] = nums[i] + max(nums[i - 1], 0)
            print(" num[i]={}, max(num[i-1],0)={})".format(nums[i], max(nums[i - 1], 0)))
            print(nums)
        return max(nums)


l = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
s = Solution()
result = s.max_sub_array(l)
print(result)
