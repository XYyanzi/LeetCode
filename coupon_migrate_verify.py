'''
#-*- coding: utf-8 -*-
@Author: xunyan
@Time: 2020/12/12 5:09 下午
@File: coupon_migrate_verify.py
'''
from datetime import datetime, time, timedelta

import pymysql
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class CouponDBConnect:
    def __init__(self, db_data):
        self.connection = pymysql.Connect(host=db_data['host'], user=db_data['username'], password=db_data['password'],
                                          database=db_data['database'], port=db_data['port'], autocommit=True)
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def select(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def __aexit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


def old_coupon_db_connect():
    old_coupon_db_data = {
        'host': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'advance.ai2016',
        'database': 'coupon_system'
    }
    connection = CouponDBConnect(old_coupon_db_data)
    return connection


def new_coupon_db_connect():
    new_coupon_db_data = {
        'host': '127.0.0.1',
        'port': 13306,
        'username': 'root',
        'password': '123456',
        'database': 'atome_ops'
    }
    connection = CouponDBConnect(new_coupon_db_data)
    return connection


def atome_user_db_connect():
    old_coupon_db_data = {
        'host': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'advance.ai2016',
        'database': 'atome_id'
    }
    connection = CouponDBConnect(old_coupon_db_data)
    return connection


def okp_bill_db_connect():
    old_coupon_db_data = {
        'host': '127.0.0.1',
        'port': 3306,
        'username': 'root',
        'password': 'advance.ai2016',
        'database': 'danakilat'
    }
    connection = CouponDBConnect(old_coupon_db_data)
    return connection


old_db_connect = old_coupon_db_connect()
new_db_connect = new_coupon_db_connect()
atome_user_connect = atome_user_db_connect()
okp_bill_connect = okp_bill_db_connect()


def verify_template():
    """
    1、根据sql查询出需要创建的template，只创建运营coupon，催收coupon template
    2、验证数量是否一致
    3、根据查询出结果依次进行各个字段的对比
    :return:
    """
    # 排除逾期coupon后剩余需要洗的reduction coupon
    # TODO 是否筛选template的时候需要过滤掉加速到期的coupon, 目前没有去掉加速到期的coupon
    print("++++++++++++开始验证迁移后template数据准确性+++++++++++")
    batch_sql = "SELECT * FROM coupon_batch WHERE id IN (SELECT DISTINCT b.id FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and consumed=0 and b.usable_for_overdue=FALSE)"
    old_batch_list = old_db_connect.select(batch_sql)
    print("需要进行迁移的非逾期的coupon batch的数量是: {}".format(len(old_batch_list)))
    # 根据旧coupon batch id查询新数据库中对应的template
    template_sql = "select * from coupon_template where template_id like 'TB%' "
    new_template_list = new_db_connect.select(template_sql)
    print("迁移之后创建的新的template的数量是: {}".format(len(new_template_list)))
    assert len(old_batch_list) == len(new_template_list), "迁移后template数量应相等"

    # 开始循环校验
    for old_batch in old_batch_list:
        new_template_id = 'T' + old_batch['id']
        # # 根据新template id去新数据库中查找
        # new_template_sql = "select * from coupon_template where template_id={}".format(new_template_id)
        # new_template = new_sql_connection.select(new_template_sql)[0]
        for new_template in new_template_list:
            print("开始验证new_template: {}".format(new_template['template_id']))
            if new_template['template_id'] == new_template_id:
                assert new_template['template_name'] == old_batch[
                    'name'], "old batch name: {} 和 new template_name: {} 不相等,验证失败×"
                # print("old batch name: {} == new template_name: {},验证通过 ✔️".format(old_batch['name'], new_template['template_name']))
                assert new_template['currency'] == 'IDR'
                assert new_template['project_id'] == 'PJ5ECB98909E4DD37678093402'
                assert new_template['coupon_amount'] == old_batch[
                    'face_value'], "old batch face_value: {} == new coupon_amount: {} 不相等,验证失败×"
                assert new_template['department_id'] == 2
                assert new_template['coupon_headline'] == 'Rp.' + locale.format_string('%.0f',
                                                                                       int(old_batch['face_value']),
                                                                                       1).replace(',', '.')
                assert new_template['coupon_subtitle'] == 'Pengurangan bunga'
                assert new_template[
                           'description'] == 'Voucher bisa digunakan untuk mengurangi bunga cicilan hingga Rp.' + locale.format_string(
                    '%.0f', int(old_batch['face_value']), 1).replace(',', '.')
                assert new_template[
                           'how_to_use'] == "1. Masuk ke halaman 'Tagihan'\n2. Pilih tab 'Saat ini' dan klik 'Bayar'\n3. Pada halaman 'Metode Pembayaran' klik 'Gunakan' dan pilih voucher yang Anda inginkan\n4. Voucher akan otomatis digunakan untuk tagihan Anda\n5. Gunakan voucher sebelum tanggal kadaluwarsa"
                assert new_template[
                           'how_to_use'] == "1. Masuk ke halaman 'Tagihan'\n2. Pilih tab 'Saat ini' dan klik 'Bayar'\n3. Pada halaman 'Metode Pembayaran' klik 'Gunakan' dan pilih voucher yang Anda inginkan\n4. Voucher akan otomatis digunakan untuk tagihan Anda\n5. Gunakan voucher sebelum tanggal kadaluwarsa"
                if old_batch['validity_type'] == 'COUNTDOWN_DAYS':
                    assert new_template['apply_valid_type'] == 'NUMBER_OF_DAYS'
                    assert new_template['apply_extend_days'] == old_batch['countdown_days']
                elif old_batch['validity_type'] == 'VALIDITY_DATE':
                    assert new_template['apply_valid_type'] == 'DATE_RANGE'
                    assert new_template['apply_expiration_timestamp'] == int(
                        old_batch['validity_date'].timestamp() * 1000)
                assert new_template['discount_type'] == 'AMOUNT'
                assert new_template['status'] == 'ACTIVE'
                assert new_template['coupon_type'] == 'COUPON'
                assert new_template['tenor_apply_rule'] == 'SPECIFIED_BILL'
                assert new_template['stackable'] == 0
                assert new_template['creator'] == old_batch['applicant']
                assert new_template['remarks'] == 'auto imported'
                assert new_template['create_timestamp'] == int(old_batch['create_time'].timestamp() * 1000)

                # 检查每个new_template的apply rule
                apply_rule_list = new_db_connect.select(
                    "select * from coupon_template_apply_rule where template_id='{}' and deleted=0".format(
                        new_template_id))
                assert len(apply_rule_list) == 3, "存在了不应该存在的apply rule"  # 目前只会有3个apply rule
                for apply_rule in apply_rule_list:
                    if apply_rule['fact'] == 'usableForOverdue':
                        assert apply_rule['calculate_on'] == 'overdue'
                        assert apply_rule['operator'] == '='
                        assert apply_rule['value'] == 'NO'
                    elif apply_rule['fact'] == 'usableForCurrentBill':
                        assert apply_rule['calculate_on'] == 'currentBill'
                        assert apply_rule['operator'] == '='
                        assert apply_rule['value'] == 'YES'
                    elif apply_rule['fact'] == 'usableForAcceleratedBill':
                        assert apply_rule['calculate_on'] == 'accelerated'
                        assert apply_rule['operator'] == '='
                        assert apply_rule['value'] == 'NO'
                    else:
                        print("存在了不应该存在的apply rule")
                # 检查每个new_template的consume rule
                consume_rule_list = new_db_connect.select(
                    "select * from coupon_template_consume_rule where template_id='{}' and deleted=0".format(
                        new_template_id))
                assert len(consume_rule_list) == 1, "存在了不应该存在的consume rule"  # 目前只会有1个consume rule
                assert consume_rule_list[0]['fact'] == 'interest' and consume_rule_list[0][
                    'calculate_on'] == 'interest' and int(consume_rule_list[0]['discount_percentage']) == 100
            print("迁移后的coupon template {} 验证通过".format(new_template['template_id']))


def verify_user_coupon_for_only_issue(mobile_hashed):
    # 抽取50条验证
    batch_sql = "SELECT * FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=false and b.usable_for_principal=false and c.external_ref_id is null and c.mobile_hashed='{}'".format(
        mobile_hashed)
    old_user_batch_list = old_db_connect.select(batch_sql)
    print(old_user_batch_list)
    if len(old_user_batch_list) == 0:
        print("该用户不存在已发送未绑定的数据")
    else:
        batch_id = old_user_batch_list[0]['batch_id']
        user_id = atome_user_connect.select("select * from user where mobile_number_hashed='{}'".format(mobile_hashed))[0]['id']
        if user_id:
            new_user_coupon_list = new_db_connect.select(
                "select * from user_coupon where user_id='{}' and template_id='{}' and ref_id is null".format(user_id,
                                                                                                              'T' + batch_id))
            old_user_coupon_list = old_db_connect.select(
                "SELECT * FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=false and b.usable_for_principal=false and c.external_ref_id is null and c.mobile_hashed='{}' and c.batch_id='{}'".format(
                    mobile_hashed, batch_id))
            print("new_user_coupon_list 有 {}个，old_user_coupon_list 有{}个".format(len(new_user_coupon_list),
                                                                                len(old_user_coupon_list)))
            assert len(new_user_coupon_list) == len(old_user_coupon_list)
            old_coupon_sum = 0
            new_coupon_sum = 0
            for old in old_user_coupon_list:
                old_coupon_sum += old['face_value']
            for new in new_user_coupon_list:
                new_coupon_sum += new['coupon_amount']
            print("new_user_coupon_amount 是：{}，old_user_coupon_amount 是：{}".format(new_coupon_sum, old_coupon_sum))
            assert old_coupon_sum == new_coupon_sum


def verify_user_coupon_for_issue_and_apply():
    print("++++++++++++开始验证迁移后已发送已绑定的e数据准确性+++++++++++")
    # 抽取50条验证
    batch_sql = "SELECT * FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=false and b.usable_for_principal=false and c.external_ref_id is not null limit 50"
    old_user_coupon_list = old_db_connect.select(batch_sql)
    print(old_user_coupon_list)
    if len(old_user_coupon_list) == 0:
        print("不存在过期时间类型是VALIDITY_DATE且已发送已绑定的数据")
    else:
        for old_user_coupon in old_user_coupon_list:
            # 根据mobile查询atome_user_id
            atome_user_id = atome_user_connect.select("select * from user where mobile_number_hashed='{}'".format(old_user_coupon['mobile_hashed']))[0]['id']
            print("开始验证user: {}, 对应的是template: {}".format(atome_user_id, ('T' + old_user_coupon['batch_id'])))
            if atome_user_id:
                coupon_template_id = 'T' + old_user_coupon['batch_id']
                coupon_template = \
                new_db_connect.select("select * from coupon_template where template_id='{}'".format(coupon_template_id))[0]
                # 解析ref_id,然后查询到billId
                okp_user_id = old_user_coupon['external_ref_id'].split('_')[1]
                okp_due_date = old_user_coupon['external_ref_id'].split('_')[2]
                okp_bill_id = okp_bill_connect.select(
                    "select id from installment_bill where user_id='{}' and due_date='{}'".format(okp_user_id,
                                                                                                  okp_due_date))[0]['id']
                # 查询在新系统中的user_coupon
                if okp_bill_id:
                    sql = "select * from user_coupon where user_id='{}' and template_id='{}' and ref_id='{}'".format(
                        atome_user_id, coupon_template_id, okp_bill_id)
                    print(sql)
                    new_user_coupon = new_db_connect.select(sql)
                    assert len(new_user_coupon) == 1, '一个refId只能有1个已绑定的coupon'
                    assert new_user_coupon[0]['project_id'] == coupon_template['project_id']
                    assert new_user_coupon[0]['coupon_headline'] == coupon_template['coupon_headline']
                    assert new_user_coupon[0]['coupon_subtitle'] == coupon_template['coupon_subtitle']
                    assert new_user_coupon[0]['coupon_type'] == coupon_template['coupon_type']
                    assert new_user_coupon[0]['tenor_apply_rule'] == coupon_template['tenor_apply_rule']
                    assert new_user_coupon[0]['discount_type'] == coupon_template['discount_type']
                    assert new_user_coupon[0]['coupon_amount'] == coupon_template['coupon_amount']
                    assert new_user_coupon[0]['real_deducted_amount'] is None
                    assert new_user_coupon[0]['status'] == 'APPLIED'
                    assert new_user_coupon[0]['stackable'] == 0
                    assert new_user_coupon[0]['ref_id'] == okp_bill_id
                    if coupon_template['apply_valid_type'] == 'DATE_RANGE':
                        assert new_user_coupon[0]['apply_expiration_timestamp'] == coupon_template['apply_expiration_timestamp']
                    else:
                        valid_day = datetime.now() + timedelta(days=int(coupon_template['apply_extend_days']))
                        apply_expiration_timestamp = datetime.combine(valid_day, time.max).timestamp()
                        assert new_user_coupon[0]['apply_expiration_timestamp'] == int(apply_expiration_timestamp * 1000)
                    assert new_user_coupon[0]['consume_expiration_timestamp'] == int(
                        datetime.combine(datetime.strptime(okp_due_date + '23:59:59', "%Y-%m-%d%H:%M:%S"),
                                         time.max).timestamp() * 1000), \
                        '库里时间是：{}, due_date是：{} 根据due-date计算出时间是：{}'.format(new_user_coupon[0]['consume_expiration_timestamp'],
                                                                            okp_due_date, int(
                                datetime.combine(datetime.strptime(okp_due_date + '23:59:59', "%Y-%m-%d%H:%M:%S"),
                                                 time.max).timestamp() * 1000))
                    assert new_user_coupon[0]['apply_timestamp'] is not None
                    assert new_user_coupon[0]['consume_timestamp'] is None
                    assert new_user_coupon[0]['read'] == 0
                    print("user: {}, 迁移后的user_coupon：{}，验证通过".format(atome_user_id, new_user_coupon[0]['coupon_id']))


def verify_user_coupon_for_overdue():
    print("++++++++++++开始验证迁移后已发送已绑定的逾期coupon的数据准确性+++++++++++")
    template_id = 'T5FD6F90FA184ED00018FA4F1'
    coupon_template = new_db_connect.select("select * from coupon_template where template_id='{}'".format(template_id))[0]
    overdue_sql = "SELECT c.* FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=True and b.usable_for_principal=True limit 50"
    old_overdue_coupon_list = old_db_connect.select(overdue_sql)
    print(old_overdue_coupon_list)
    for old_overdue_coupon in old_overdue_coupon_list:
        okp_user_id = old_overdue_coupon['external_ref_id'].split('_')[1]
        okp_due_date = old_overdue_coupon['external_ref_id'].split('_')[2]
        okp_bill_id = okp_bill_connect.select(
            "select id from installment_bill where user_id='{}' and due_date='{}'".format(okp_user_id, okp_due_date))[
            0]['id']
        user_id = atome_user_connect.select("select * from user where okp_user_id='{}'".format(okp_user_id))[0]['id']
        sql = "select * from user_coupon where user_id='{}' and template_id='{}' and ref_id='{}'".format(user_id,
                                                                                                         coupon_template[
                                                                                                             'template_id'],
                                                                                                         okp_bill_id)
        print(sql)
        if okp_bill_id and user_id:
            new_user_coupon = new_db_connect.select(sql)
            old_coupon_batch = \
            old_db_connect.select("select * from coupon_batch where id='{}'".format(old_overdue_coupon['batch_id']))[0]
            assert len(new_user_coupon) == 1, '一个refId只能有1个已绑定的coupon,refId={}'.format(
                old_overdue_coupon['external_ref_id'])
            assert new_user_coupon[0]['template_id'] == coupon_template['template_id']
            assert new_user_coupon[0]['project_id'] == coupon_template['project_id']
            assert new_user_coupon[0]['coupon_headline'] == 'Rp ' + locale.format_string('%.0f', int(
                old_coupon_batch['face_value']), 1).replace(',', '.')
            assert new_user_coupon[0]['coupon_subtitle'] == 'kupon diskon pembayaran'
            assert new_user_coupon[0]['coupon_type'] == coupon_template['coupon_type']
            assert new_user_coupon[0]['tenor_apply_rule'] == coupon_template['tenor_apply_rule']
            assert new_user_coupon[0]['discount_type'] == coupon_template['discount_type']
            assert new_user_coupon[0]['coupon_amount'] == old_coupon_batch['face_value'], "{}, {}".format(
                new_user_coupon[0]['coupon_amount'], old_coupon_batch['face_value'])
            assert new_user_coupon[0]['real_deducted_amount'] is None
            assert new_user_coupon[0]['status'] == 'APPLIED'
            assert new_user_coupon[0]['stackable'] == 0
            assert new_user_coupon[0]['ref_id'] == okp_bill_id
            if coupon_template['apply_valid_type'] == 'DATE_RANGE':
                assert new_user_coupon[0]['apply_expiration_timestamp'] == coupon_template['apply_expiration_timestamp']
            else:
                valid_day = datetime.now() + timedelta(days=int(coupon_template['apply_extend_days']))
                apply_expiration_timestamp = datetime.combine(valid_day, time.max).timestamp()
                assert new_user_coupon[0]['apply_expiration_timestamp'] == int(apply_expiration_timestamp * 1000)
            assert new_user_coupon[0]['consume_expiration_timestamp'] == int(
                datetime.combine(datetime.now() + timedelta(days=2), time.max).timestamp() * 1000), \
                '库里时间是：{}, due_date是：{} 根据due-date计算出时间是：{}'.format(new_user_coupon[0]['consume_expiration_timestamp'],
                                                                    okp_due_date, int(
                        datetime.combine(datetime.now() + timedelta(days=2), time.max).timestamp() * 1000))
            assert new_user_coupon[0]['apply_timestamp'] is not None
            assert new_user_coupon[0]['consume_timestamp'] is None
            assert new_user_coupon[0]['read'] == 0
            print("user: {}, 迁移后的user_coupon：{}，验证通过".format(user_id, new_user_coupon[0]['coupon_id']))


def verify_issue_and_apply_number():
    # 查询清洗后的template issue和apply的数量
    print("++++++++++++开始验证迁移后总数量+++++++++++")
    coupon_template = new_db_connect.select("select * from atome_ops.coupon_template where template_id like 'TB%'")
    for t in coupon_template:
        # 查询每个template的count_issued数量
        issue_num = new_db_connect.select(
            "select count(*) as num from user_coupon where template_id='{}' and issue_timestamp is not null".format(
                t['template_id']))[0]['num']
        apply_num = new_db_connect.select(
            "select count(*) as num from user_coupon where template_id='{}' and status='APPLIED'".format(
                t['template_id']))[0]['num']
        print("template： {}， 库里记录issue个数是：{}, 库里记录applied个数是：{}, 实际应该是: {}, {}".format(t['template_id'],
                                                                                       t['count_issued'],
                                                                                       t['count_applied'], issue_num,
                                                                                       apply_num))
        assert issue_num == t['count_issued'], apply_num == t['count_applied']


def verify_number():
    # 查询历史只发放未绑定的用户 先验证总数
    before1 = old_db_connect.select(
        "SELECT * FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=false and b.usable_for_principal=false and c.external_ref_id is null")
    after1 = new_db_connect.select(
        "select * from atome_ops.user_coupon where template_id like 'TB%' and ref_id is null")
    print("要迁移的发送未绑定的coupon数量是：{}, 成功迁移后的数量是: {}".format(len(before1), len(after1)))
    assert len(before1) == len(after1)
    # 查询历史已绑定的用户 先验证总数
    before2 = old_db_connect.select(
        "SELECT * FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=false and b.usable_for_principal=false and c.external_ref_id is not null")
    after2 = new_db_connect.select(
        "select * from atome_ops.user_coupon where template_id like 'TB%' and ref_id is not null")
    print("要迁移的发送已绑定的coupon数量是：{}, 成功迁移后的数量是: {}".format(len(before2), len(after2)))
    assert len(before2) == len(after2)
    before = old_db_connect.select(
        "SELECT c.* FROM coupon_binding c,coupon_batch b WHERE c.batch_id=b.id AND c.expiration_time>now() AND b.system='ATOME' and c.consumed=0 AND b.usable_for_overdue=True and b.usable_for_principal=True")
    after = new_db_connect.select("select * from atome_ops.user_coupon where template_id='T5FD6F90FA184ED00018FA4F1'")
    print("要迁移的发送逾期已绑定的coupon数量是：{}, 成功迁移后的数量是: {}".format(len(before), len(after)))
    assert len(before) == len(after)


if __name__ == '__main__':
    verify_template()
    # verify_number()
    verify_user_coupon_for_issue_and_apply()
    # verify_user_coupon_for_overdue()
    # verify_user_coupon_for_only_issue('*H0:8f5815815015b8fa03093d83d8f73636f384cd75')
    # verify_issue_and_apply_number()
