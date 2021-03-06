import json
from datetime import datetime, time, timedelta

import pytest
from leetCode.leetCode_00 import Solution
import locale

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

    def test_list(self):
        # 列表翻转
        l = [1, 2, 3]
        l2 = l[::-1]
        l3 = str(l)

    def test_type(self):
        x = "3"
        if type(x) != int:
            print("x不是数字")
        else:
            print("x是数字")

    def test_sum(self):
        print(121 % 10)
        print(123 / 10)
        # 遍历列表
        l = [1, 3, 4, 5]
        for i in l:
            print(i)

    def test_list2(self):
        l = [{"a": 1}, {"b": 2}]
        for i in l:
            print(i)

    def test_dict(self):
        aa = "interest"
        extra = {
            "data": {
                "interest": 97600.00,
                "overdueFee": 0,
                "overdueInterest": 0,
                "principal": 600000.00
            }
        }
        # print(aa in extra.keys())

        # print(sum(extra.values()))
        if 'interest' in extra['data'].keys():
            print("在key中")

    def test_time(self):
        # valid_day = datetime.now() + timedelta(days=10)
        # apply_expiration_timestamp = datetime.combine(valid_day, time.max).timestamp()
        # print(apply_expiration_timestamp)
        # print(int(apply_expiration_timestamp * 1000))
        due_date = '2021-01-12' + '23:59:59'
        f = datetime.strptime(due_date, "%Y-%m-%d%H:%M:%S")
        f_time = int(datetime.combine(f, time.max).timestamp() * 1000)
        print(f_time)

    def test_money_format(self):

        print(locale.setlocale(locale.LC_ALL, 'en_US.UTF-8'))
        num = 500000
        r = locale.format_string('%.0f', num, 1)
        print(r)

    def test_split_str(self):

        s = "OKP_U16076793501148233_2021-01-12"
        user_id = s.split('_')[1]
        due_date = s.split('_')[2]
        print(user_id)
        print(due_date)

    def test_str_dict(self):
        s = '{"fee":37124,"interest":400418.00,"overdueFee":55096,"overdueInterest":7362,"principal":0}'
        d = {'overdueFee': 55096, 'overdueInterest': 7362, 'fee': 37124, 'interest': 400418, 'principal': 0}
        ss = json.loads(s)
        print(ss == d)

    @pytest.mark.parametrize('m, n, expect', [
        (0, 100, 0),
        (1, 100, 100),
        (0, 100, 0)
    ])
    def test_multiplication(self, m, n, expect):
        s = m * n
        print("{} * {} = {}".format(m, n, s))
        assert s == expect

    def test_dict_2(self):
        max_amount = 25000
        deduction_map = {
            "platformCouponAmount": 30000
        }
        deduction_sum = sum(deduction_map.values())
        gap = deduction_sum - max_amount
        c = 0
        for i in deduction_map.keys():
            if i != list(deduction_map.keys())[-1]:
                print("此时i不是最后一个key，计算第1个key调整后的值")
                c = deduction_map[i] - round((gap * deduction_map[i] / deduction_sum))
                deduction_map[i] = c
            else:
                deduction_map[i] = max_amount - c
        print(deduction_map)

    def test_li(self):
        rule_list = [{'id': 227, 'template_id': 'T5FE968097509A50001B66934', 'fact': 'platformCoupon', 'out_name': 'platformCouponAmount', 'calculate_on': 'orderAmount', 'discount_amount': None, 'discount_percentage': float('35.00'), 'max_discount_amount': float('300000.00'), 'sequence': 1, 'deleted': 0, 'create_timestamp': 1609132041655, 'update_timestamp': 1609132041655}, {'id': 228, 'template_id': 'T5FE968097509A50001B66934', 'fact': 'merchantCoupon', 'out_name': 'merchantCouponAmount', 'calculate_on': 'orderAmount', 'discount_amount': None, 'discount_percentage': float('25.00'), 'max_discount_amount': float('300000.00'), 'sequence': 2, 'deleted': 0, 'create_timestamp': 1609132041655, 'update_timestamp': 1609132041655}]
        a = [int(i['discount_percentage']) for i in rule_list]
        print(sum(a))


