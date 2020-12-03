"""
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
示例：
输入: 123
输出: 321
输入: -123
输出: -321
输入: 120
输出: 21
注意：假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2^31,  2^31 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。
思路：将数字转换成字符串，然后翻转字符串，翻转之后判断是否超过整数范围
"""


class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        # 将x转换成str
        str_x = str(x)
        # 将str转换成列表
        list_x = str_x.split("-")
        # 如果列表长度是1，证明是整数，列表长度是2说明是负数
        if len(list_x) > 1:
            reversed_x = int("-" + list_x[1][::-1])
        else:
            reversed_x = int(list_x[0][::-1])
        print("此时x是".format(reversed_x))
        print("判断的区间是({},{})".format((-2) ** 31, (2 ** 31 - 1)))
        if (-2) ** 31 < reversed_x < 2 ** 31 - 1:
            return reversed_x
        else:
            return 0


if __name__ == '__main__':
    s = Solution()
    result = s.reverse(1534236469)
    print(result)
