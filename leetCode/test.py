import pytest
from leetCode.leetCode20201201 import Solution

solution = Solution()


class TestSearchRange:

    def test_empty_list(self):
        nums = []
        target = 0
        result = solution.searchRange(nums, target)
        assert result == [-1, -1]

    def test_target_not_in_list(self):
        nums = [5, 7, 7, 8, 8, 10]
        target = 6
        result = solution.searchRange(nums, target)
        assert result == [-1, -1]

    def test_target_only_one(self):
        nums = [5, 7, 7, 8, 9, 10]
        target = 8
        result = solution.searchRange(nums, target)
        assert result == [-1, -1]

    def test_correct(self):
        nums = [5, 7, 7, 8, 8, 10]
        target = 8
        result = solution.searchRange(nums, target)
        assert result == [3, 4]

    def test_correct_target_more_than_two(self):
        nums = [5, 7, 7, 7, 8, 8, 8, 8, 10]
        target = 8
        result = solution.searchRange(nums, target)
        assert result == [4, 7]
