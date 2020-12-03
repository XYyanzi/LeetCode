"""
给定一个整数数组 nums和一个目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。
你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
示例：
给定 nums = [2, 7, 11, 15], target = 9

因为 nums[0] + nums[1] = 2 + 7 = 9
所以返回 [0, 1]
思路：
i=0 j=1 0+1 2+7
    j=2 0+2 2+11
    j=3 0+3 2+15
i=1 j=2 1+2 7+11
    j=3 1+3 7+15
i=2 j=3 2+3 11+15
遇到的问题： for循环中的range 不包括最后的值，range(1,3) 实际范围是1，2
"""


class Solution(object):
    def twoSum(nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        index_list = []
        for i in range(len(nums) - 1):
            print("外层第{}次循环".format(i))
            for j in range((i + 1), len(nums)):
                print("  内层第{}次循环".format(j))
                print("  此时计算的是{} + {}".format(nums[i], nums[j]))
                if nums[i] + nums[j] == target:
                    index_list.append(i)
                    index_list.append(j)
                    return (index_list)


if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    target = 26
    result = Solution.twoSum(nums, target)
    print(result)
