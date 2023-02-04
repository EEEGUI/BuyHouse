import logging

# -------------   设置区   --------------
KEY = "5a77c*********************43ec"  # 调用高德api所用的密钥。注册：https://lbs.amap.com/
TOPN = 3  # 周边信息显示个数
THRESHOLD = 2000  # 交通工具切换距离阈值，单位米。小于阈值：步行/骑车；大于阈值：开车、公共交通
TARGET_COMPANY = ('拼多多', '美团', '字节', '小红书')  # 公司地， 用于计算通勤。具体地址填入下方COMPANY_ADDRESS字典中。

# -------------  常量区  --------------
DRIVING = 'driving'
PUBLIC_TRANSPORT = 'public_transport'
NAME = 'name'
DISTANCE = 'distance'
LOCATION = 'location'
WALKING = 'walking'
BICYCLING = 'bicycling'
PROJECT_NAME = "项目名称"
PROJECT_ADDRESS = "项目地址"
PROJECT_LOCATION = "经纬坐标"

COMPANY_ADDRESS = {
    "阿里": "上海市浦东新区纳贤路800号",
    "腾讯": "上海市徐汇区漕河泾新兴技术开发区虹梅路1801号",
    "字节": "上海市闵行区宜山路1999号",
    "蚂蚁": "浦东新区南泉北路447号",
    "美团": "蒲松北路60号",
    "拼多多": "娄山关路533号",
    "b站": "杨浦区政立路485号",
    "滴滴": "嘉定区高潮路318号",
    "携程": "浦东新区金海路2505宝龙商场1号",
    "阅文": "碧波路690号",
    "哈啰": "闵行区秀文路898弄",
    "百度": "浦东新区纳贤路701号",
    "京东": "嘉定区叶城路1118号",
    "网易": "青浦区诸光路1588弄",
    "得物": "杨浦区大桥街道互联宝地c3号楼",
    "唯品会": "浦东新区启帆路6288号",
    "叮咚": "浦东新区创运路256号",
    "小红书": "黄浦区马当路388号",
    "米哈游": "徐汇区宜山路700号",
    "莉莉丝": "徐汇区宜州路188号"
}


# ------------- 函数  ---------------------

def WARM(message):
    logging.debug(message)


def ERROR(message):
    logging.error(message)


def calc_epp(P, R, N, n):
    """
    计算等额本金下，第 n+1 月的还款额。此时，已有 n 个月完成还款。
    EPP：Equal Principal Payment 等额本金

    计算公式：每月还款金额 = (贷款本金 / 还款月数) + (本金 — 已归还本金累计额) × 每月利率

    输入：
    P：贷款本金总额
    R：年利率 %
    N：还款月数
    n：第 n 个月

    输出：
    返回 monthly_payment：第 n+1 月的还款额，保留 2 位小数
    """
    R = R / (100 * 12)
    monthly_payment = int(round((P/N)+(P-((P/N)*n))*R, 0))

    return monthly_payment


def calc_elp(P, R, N):
    """
    ELP：Equal Loan Payment 等额本息
    计算公式：每月还款额 = [贷款本金 × 月利率 × (1+月利率) ^ 还款月数] ÷ [(1+月利率) ^ 还款月数－1]
    输入：
    P：贷款本金总额
    R：年利率 %
    N：还款月数
    """
    R = R / (12 * 100)
    monthly_payment = int(round((P*R*(1+R)**N)/((1+R)**N-1), 0))
    return monthly_payment


