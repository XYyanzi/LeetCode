'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/1 12:46 下午
@File: leetCode20201201.py
'''
"""
给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置（第一次出现的位置）和结束位置（第二次出现的位置）。
如果数组中不存在目标值 target，返回[-1, -1]。
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
            print("该元素不在列表中")
            return -1
        else:
            while left <= right:
                mid = (left + right) // 2  # python整除符号使用//，结果向下取整  /表示除法，返回float
                # mid = left + (right - left)/2  # 这种写法可以防止left + right超出整数范围溢出
                if target > search_list[mid]:
                    left = mid + 1
                    print(
                        "这是循环第{}次，此时mid={}, target{} > search_list[mid]{}, 下次查找区间是：{}".format(count, mid, target,
                                                                                              search_list[mid],
                                                                                              search_list[
                                                                                              left: right + 1]))
                    count += 1
                elif target < search_list[mid]:
                    right = mid
                    print(
                        "这是循环第{}次，此时mid={}, target{} < search_list[mid]{},下次查找区间是：{}".format(count, mid, target,
                                                                                             search_list[mid],
                                                                                             search_list[
                                                                                             left: right + 1]))
                    count += 1
                elif target == search_list[mid]:
                    print(
                        "这是循环第{}次，此时mid={}, target{} = search_list[mid]{}".format(count, mid, target, search_list[mid]))
                    count += 1
                    return mid

    def searchRange(self, nums, target):
        """
        思路：先通过二分查找法找到元素所在的坐标，然后判断元素左边和右边的元素和target是否相等，
        如果左边元素和target相等就从左边开始依次往前查找，找到最小的坐标，
        如果右边元素和target相等就继续从右边区域开始依次往后查找，找到最大的坐标
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if len(nums) == 0:
            return [-1, -1]
        if target not in nums:
            return [-1, -1]
        else:
            mid_index = self.binarySearch(nums, target)
            if nums[mid_index - 1] == target and nums[mid_index + 1] != target:
                print("此时target左边的元素是{},需要重新从左边的列表{}中继续查找".format(nums[mid_index - 1], nums[0:mid_index]))
                left_index = mid_index - 1
                while left_index > 0:
                    if nums[left_index - 1] == target:
                        left_index -= 1
                    else:
                        break
                return [left_index, mid_index]
            elif nums[mid_index + 1] == target and nums[mid_index - 1] != target:
                print("此时target右边的元素是{},需要重新从右边的列表{}中继续查找".format(nums[mid_index + 1], nums[mid_index + 1:len(nums)]))
                right_index = mid_index + 1
                while right_index < len(nums):
                    if nums[right_index + 1] == target:
                        right_index += 1
                        continue
                    else:
                        break
                return [mid_index, right_index]
            elif nums[mid_index - 1] == target and nums[mid_index + 1] == target:
                # TODO 当左右两边都相等时，需要两边同时查找
                return [-1, -1]
            else:
                return [-1, -1]


if __name__ == '__main__':
    nums = [5, 7, 7, 8, 8, 8, 8, 8, 10]
    target = 8
    s = Solution()
    result = s.searchRange(nums, target)
    print(result)
