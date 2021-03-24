'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/31 11:09 上午
@File: leetCode202012312.py
'''
"""
给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。

示例 1:

输入: "Let's take LeetCode contest"
输出: "s'teL ekat edoCteeL tsetnoc" 
注意：在字符串中，每个单词由单个空格分隔，并且字符串中不会有任何额外的空格。
"""

class Solution:
    def reverse_word(self, word: str):
        # 用空格分隔符将s分成列表
        word_list = word.split(' ')
        print(word_list)
        new_list = []
        for w in word_list:
           new_list.append(w[::-1])
        new_word = ' '.join(new_list)
        return new_word


word = "Let's take LeetCode contest"
s = Solution()
result = s.reverse_word(word)
print(result)




