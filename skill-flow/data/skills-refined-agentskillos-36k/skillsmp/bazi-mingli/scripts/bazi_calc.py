#!/usr/bin/env python3
"""
八字命理排盤計算工具
Bazi (Four Pillars of Destiny) Calculator

內建農曆轉換與節氣計算功能，無需外部依賴。
"""

from datetime import datetime, date, timedelta
from typing import Tuple, Dict, List, Optional

# ============================================================
# 基礎數據
# ============================================================

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
TIANGAN_WUXING = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
TIANGAN_YINYANG = ["陽", "陰", "陽", "陰", "陽", "陰", "陽", "陰", "陽", "陰"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
DIZHI_WUXING = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]
DIZHI_SHENGXIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"]

# 地支藏干
DIZHI_CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "戊", "庚"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 時辰對照
SHICHEN = {
    23: 0, 0: 0,   # 子時 23:00-00:59
    1: 1, 2: 1,    # 丑時 01:00-02:59
    3: 2, 4: 2,    # 寅時 03:00-04:59
    5: 3, 6: 3,    # 卯時 05:00-06:59
    7: 4, 8: 4,    # 辰時 07:00-08:59
    9: 5, 10: 5,   # 巳時 09:00-10:59
    11: 6, 12: 6,  # 午時 11:00-12:59
    13: 7, 14: 7,  # 未時 13:00-14:59
    15: 8, 16: 8,  # 申時 15:00-16:59
    17: 9, 18: 9,  # 酉時 17:00-18:59
    19: 10, 20: 10, # 戌時 19:00-20:59
    21: 11, 22: 11, # 亥時 21:00-22:59
}

# 十神名稱
SHISHEN_NAMES = {
    (0, 0): "比肩", (0, 1): "劫財",  # 同我（比劫）
    (1, 0): "食神", (1, 1): "傷官",  # 我生（食傷）
    (2, 0): "偏財", (2, 1): "正財",  # 我剋（財星）
    (3, 0): "七殺", (3, 1): "正官",  # 剋我（官殺）
    (4, 0): "偏印", (4, 1): "正印",  # 生我（印星）
}

# ============================================================
# 農曆數據 (1900-2099)
# ============================================================

YEAR_INFOS = [
    # 1900-1909
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
    # 1910-1919
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
    # 1920-1929
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
    # 1930-1939
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
    # 1940-1949
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
    # 1950-1959
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
    # 1960-1969
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
    # 1970-1979
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
    # 1980-1989
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
    # 1990-1999
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0,
    # 2000-2009
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
    # 2010-2019
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
    # 2020-2029
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
    # 2030-2039
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
    # 2040-2049
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
    # 2050-2059
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0,
    # 2060-2069
    0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    # 2070-2079
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    # 2080-2089
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    # 2090-2099
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
]

LUNAR_START_DATE = date(1900, 1, 31)

# ============================================================
# 節氣數據
# ============================================================

# 節氣名稱（24節氣，每月兩個，第一個是「節」，第二個是「中氣」）
JIEQI_NAMES = [
    "小寒", "大寒", "立春", "雨水", "驚蟄", "春分",
    "清明", "穀雨", "立夏", "小滿", "芒種", "夏至",
    "小暑", "大暑", "立秋", "處暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

# 節氣（月份起始）的索引：立春、驚蟄、清明、立夏、芒種、小暑、立秋、白露、寒露、立冬、大雪、小寒
JIE_INDICES = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 0]

# 節氣大約日期（簡化版，實際需要精確計算）
# 格式：月份 -> [(節名, 大約日期), ...]
JIEQI_DATES = {
    1: [("小寒", 6), ("大寒", 20)],
    2: [("立春", 4), ("雨水", 19)],
    3: [("驚蟄", 6), ("春分", 21)],
    4: [("清明", 5), ("穀雨", 20)],
    5: [("立夏", 6), ("小滿", 21)],
    6: [("芒種", 6), ("夏至", 21)],
    7: [("小暑", 7), ("大暑", 23)],
    8: [("立秋", 8), ("處暑", 23)],
    9: [("白露", 8), ("秋分", 23)],
    10: [("寒露", 8), ("霜降", 24)],
    11: [("立冬", 8), ("小雪", 22)],
    12: [("大雪", 7), ("冬至", 22)],
}

# ============================================================
# 輔助函數
# ============================================================

def _year_days(year_info: int) -> int:
    """計算農曆年的總天數"""
    days = 29 * 12
    leap_month = year_info & 0xF
    if leap_month:
        days += 29
        if (year_info >> 16) & 1:
            days += 1
    for month in range(1, 13):
        if (year_info >> (16 - month)) & 1:
            days += 1
    return days


def _month_days(year_info: int, month: int, is_leap: bool = False) -> int:
    """計算農曆某月的天數"""
    if is_leap:
        return 30 if (year_info >> 16) & 1 else 29
    return 30 if (year_info >> (16 - month)) & 1 else 29


def gregorian_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int, bool]:
    """西曆轉農曆"""
    if year < 1900 or year > 2099:
        raise ValueError(f"年份 {year} 超出支援範圍 (1900-2099)")
    
    target_date = date(year, month, day)
    offset = (target_date - LUNAR_START_DATE).days
    
    if offset < 0:
        raise ValueError("日期早於1900年1月31日")
    
    lunar_year = 1900
    year_index = 0
    
    while year_index < len(YEAR_INFOS):
        year_info = YEAR_INFOS[year_index]
        year_days = _year_days(year_info)
        if offset < year_days:
            break
        offset -= year_days
        lunar_year += 1
        year_index += 1
    
    if year_index >= len(YEAR_INFOS):
        raise ValueError("日期超出支援範圍")
    
    year_info = YEAR_INFOS[year_index]
    leap_month = year_info & 0xF
    
    for m in range(1, 13):
        days = _month_days(year_info, m, False)
        if offset < days:
            return (lunar_year, m, offset + 1, False)
        offset -= days
        
        if m == leap_month:
            days = _month_days(year_info, m, True)
            if offset < days:
                return (lunar_year, m, offset + 1, True)
            offset -= days
    
    raise ValueError("日期計算錯誤")


def get_jieqi_month(year: int, month: int, day: int) -> int:
    """
    根據節氣確定月柱的月份
    返回 1-12，對應寅月-丑月
    """
    # 簡化版：根據節氣表判斷
    jieqi = JIEQI_DATES.get(month, [])
    
    # 月柱月份映射（以節氣為準）
    # 立春(2月)=寅月(1), 驚蟄(3月)=卯月(2), ...
    month_map = {
        2: 1,   # 立春後為寅月
        3: 2,   # 驚蟄後為卯月
        4: 3,   # 清明後為辰月
        5: 4,   # 立夏後為巳月
        6: 5,   # 芒種後為午月
        7: 6,   # 小暑後為未月
        8: 7,   # 立秋後為申月
        9: 8,   # 白露後為酉月
        10: 9,  # 寒露後為戌月
        11: 10, # 立冬後為亥月
        12: 11, # 大雪後為子月
        1: 12,  # 小寒後為丑月
    }
    
    jie_day = jieqi[0][1] if jieqi else 6  # 節氣（第一個）的大約日期
    
    if day >= jie_day:
        return month_map.get(month, month)
    else:
        # 未過節，屬於上一個月
        prev_month = month - 1 if month > 1 else 12
        return month_map.get(prev_month, prev_month)


def get_year_ganzhi(year: int, month: int, day: int) -> Tuple[int, int]:
    """
    計算年柱干支（以立春為界）
    返回 (天干索引, 地支索引)
    """
    # 判斷是否過了立春
    lichun_day = JIEQI_DATES[2][0][1]  # 立春大約日期
    
    if month < 2 or (month == 2 and day < lichun_day):
        year -= 1  # 未過立春，屬於前一年
    
    # 計算干支
    # 1984年為甲子年
    offset = year - 1984
    gan = offset % 10
    zhi = offset % 12
    
    return (gan, zhi)


def get_month_ganzhi(year_gan: int, jieqi_month: int) -> Tuple[int, int]:
    """
    計算月柱干支
    year_gan: 年干索引
    jieqi_month: 節氣月份 (1=寅月, 12=丑月)
    返回 (天干索引, 地支索引)
    """
    # 月支：寅月(1)=寅(2), 卯月(2)=卯(3), ...
    month_zhi = (jieqi_month + 1) % 12
    
    # 月干推算（五虎遁）
    # 甲己年丙寅, 乙庚年戊寅, 丙辛年庚寅, 丁壬年壬寅, 戊癸年甲寅
    month_gan_start = {
        0: 2,  # 甲年 -> 丙
        1: 4,  # 乙年 -> 戊
        2: 6,  # 丙年 -> 庚
        3: 8,  # 丁年 -> 壬
        4: 0,  # 戊年 -> 甲
        5: 2,  # 己年 -> 丙
        6: 4,  # 庚年 -> 戊
        7: 6,  # 辛年 -> 庚
        8: 8,  # 壬年 -> 壬
        9: 0,  # 癸年 -> 甲
    }
    
    start_gan = month_gan_start[year_gan]
    month_gan = (start_gan + jieqi_month - 1) % 10
    
    return (month_gan, month_zhi)


def get_day_ganzhi(year: int, month: int, day: int) -> Tuple[int, int]:
    """
    計算日柱干支
    使用儒略日計算法
    """
    # 計算儒略日
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    
    jd = day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    
    # 1984年1月1日是甲子日，JD = 2445701
    offset = jd - 2445701
    
    gan = offset % 10
    zhi = offset % 12
    
    return (gan, zhi)


def get_hour_ganzhi(day_gan: int, hour: int) -> Tuple[int, int]:
    """
    計算時柱干支
    day_gan: 日干索引
    hour: 小時 (0-23)
    """
    # 時支
    hour_zhi = SHICHEN.get(hour, 0)
    
    # 時干推算（五鼠遁）
    # 甲己日甲子, 乙庚日丙子, 丙辛日戊子, 丁壬日庚子, 戊癸日壬子
    hour_gan_start = {
        0: 0,  # 甲日 -> 甲
        1: 2,  # 乙日 -> 丙
        2: 4,  # 丙日 -> 戊
        3: 6,  # 丁日 -> 庚
        4: 8,  # 戊日 -> 壬
        5: 0,  # 己日 -> 甲
        6: 2,  # 庚日 -> 丙
        7: 4,  # 辛日 -> 戊
        8: 6,  # 壬日 -> 庚
        9: 8,  # 癸日 -> 壬
    }
    
    start_gan = hour_gan_start[day_gan]
    hour_gan = (start_gan + hour_zhi) % 10
    
    return (hour_gan, hour_zhi)


def get_shishen(day_gan: int, target_gan: int) -> str:
    """計算十神"""
    day_wuxing = TIANGAN.index(TIANGAN[day_gan]) // 2
    target_wuxing = TIANGAN.index(TIANGAN[target_gan]) // 2
    
    day_yy = TIANGAN.index(TIANGAN[day_gan]) % 2
    target_yy = TIANGAN.index(TIANGAN[target_gan]) % 2
    
    # 計算五行關係
    relation = (target_wuxing - day_wuxing) % 5
    same_yy = 0 if day_yy == target_yy else 1
    
    return SHISHEN_NAMES.get((relation, same_yy), "")


def count_wuxing(pillars: List[Tuple[int, int]]) -> Dict[str, int]:
    """統計五行數量"""
    count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for gan, zhi in pillars:
        # 天干五行
        count[TIANGAN_WUXING[gan]] += 1
        # 地支五行
        count[DIZHI_WUXING[zhi]] += 1
        # 藏干五行
        for cg in DIZHI_CANGGAN[DIZHI[zhi]]:
            cg_idx = TIANGAN.index(cg)
            count[TIANGAN_WUXING[cg_idx]] += 0.5  # 藏干權重較低
    
    return count


def analyze_rizhu_strength(day_gan: int, month_zhi: int, pillars: List[Tuple[int, int]]) -> Dict:
    """分析日主強弱"""
    day_wuxing = TIANGAN_WUXING[day_gan]
    month_wuxing = DIZHI_WUXING[month_zhi]
    
    # 月令旺衰
    wuxing_order = ["木", "火", "土", "金", "水"]
    day_idx = wuxing_order.index(day_wuxing)
    month_idx = wuxing_order.index(month_wuxing)
    
    # 判斷月令
    if day_wuxing == month_wuxing:
        month_strength = "旺"
    elif wuxing_order[(day_idx + 1) % 5] == month_wuxing:
        month_strength = "相"
    elif wuxing_order[(day_idx + 4) % 5] == month_wuxing:
        month_strength = "休"
    elif wuxing_order[(day_idx + 3) % 5] == month_wuxing:
        month_strength = "囚"
    else:
        month_strength = "死"
    
    # 統計通根
    root_count = 0
    for gan, zhi in pillars:
        for cg in DIZHI_CANGGAN[DIZHI[zhi]]:
            if TIANGAN_WUXING[TIANGAN.index(cg)] == day_wuxing:
                root_count += 1
    
    # 統計比劫印星
    help_count = 0
    for gan, zhi in pillars:
        gan_wuxing = TIANGAN_WUXING[gan]
        if gan_wuxing == day_wuxing:  # 比劫
            help_count += 1
        elif wuxing_order[(day_idx + 4) % 5] == gan_wuxing:  # 印星
            help_count += 1
    
    # 綜合判斷
    strength_score = 0
    if month_strength in ["旺", "相"]:
        strength_score += 2
    if root_count >= 2:
        strength_score += 2
    if help_count >= 2:
        strength_score += 1
    
    if strength_score >= 4:
        overall = "身強"
    elif strength_score >= 2:
        overall = "中和"
    else:
        overall = "身弱"
    
    return {
        "日主": f"{TIANGAN[day_gan]}（{day_wuxing}）",
        "月令": f"{DIZHI[month_zhi]}（{month_wuxing}）",
        "月令旺衰": month_strength,
        "通根數": root_count,
        "比劫印星": help_count,
        "綜合判斷": overall,
    }


def get_yongshen(day_gan: int, strength: str) -> Dict:
    """推斷用神喜忌"""
    day_wuxing = TIANGAN_WUXING[day_gan]
    wuxing_order = ["木", "火", "土", "金", "水"]
    day_idx = wuxing_order.index(day_wuxing)
    
    if strength == "身強":
        # 身強宜洩、宜剋、宜耗
        xiyong = [
            wuxing_order[(day_idx + 1) % 5],  # 食傷（我生）
            wuxing_order[(day_idx + 2) % 5],  # 財星（我剋）
            wuxing_order[(day_idx + 3) % 5],  # 官殺（剋我）
        ]
        jishen = [
            wuxing_order[(day_idx + 4) % 5],  # 印星（生我）
            day_wuxing,  # 比劫（同我）
        ]
    else:
        # 身弱宜生、宜助
        xiyong = [
            wuxing_order[(day_idx + 4) % 5],  # 印星（生我）
            day_wuxing,  # 比劫（同我）
        ]
        jishen = [
            wuxing_order[(day_idx + 1) % 5],  # 食傷（我生）
            wuxing_order[(day_idx + 2) % 5],  # 財星（我剋）
            wuxing_order[(day_idx + 3) % 5],  # 官殺（剋我）
        ]
    
    return {
        "喜用神": "、".join(xiyong),
        "忌神": "、".join(jishen),
    }


def calculate_dayun(year_gan: int, year_zhi: int, gender: str, 
                    birth_year: int, birth_month: int, birth_day: int) -> List[Dict]:
    """計算大運"""
    # 判斷順逆
    # 陽年男、陰年女為順排；陰年男、陽年女為逆排
    year_yinyang = TIANGAN_YINYANG[year_gan]
    
    if (year_yinyang == "陽" and gender == "男") or (year_yinyang == "陰" and gender == "女"):
        direction = 1  # 順排
    else:
        direction = -1  # 逆排
    
    # 計算起運歲數（簡化版：以3年為1歲計算）
    # 實際應計算到下一個節氣的天數
    start_age = 3 if birth_day <= 15 else 6
    
    # 獲取月柱
    jieqi_month = get_jieqi_month(birth_year, birth_month, birth_day)
    month_gan, month_zhi = get_month_ganzhi(year_gan, jieqi_month)
    
    dayun_list = []
    for i in range(8):  # 排8運
        age_start = start_age + i * 10
        age_end = age_start + 9
        
        # 計算該運的干支
        gan = (month_gan + (i + 1) * direction) % 10
        zhi = (month_zhi + (i + 1) * direction) % 12
        
        dayun_list.append({
            "年齡": f"{age_start}-{age_end}歲",
            "干支": f"{TIANGAN[gan]}{DIZHI[zhi]}",
            "五行": f"{TIANGAN_WUXING[gan]}{DIZHI_WUXING[zhi]}",
        })
    
    return dayun_list


def paipan(year: int, month: int, day: int, hour: int, gender: str = "男") -> Dict:
    """
    八字排盤主函數
    
    Args:
        year: 西曆年份
        month: 西曆月份
        day: 西曆日期
        hour: 小時 (0-23)
        gender: "男" 或 "女"
    
    Returns:
        完整的八字命盤資訊
    """
    # 1. 計算四柱
    year_gan, year_zhi = get_year_ganzhi(year, month, day)
    
    jieqi_month = get_jieqi_month(year, month, day)
    month_gan, month_zhi = get_month_ganzhi(year_gan, jieqi_month)
    
    day_gan, day_zhi = get_day_ganzhi(year, month, day)
    
    hour_gan, hour_zhi = get_hour_ganzhi(day_gan, hour)
    
    pillars = [
        (year_gan, year_zhi),
        (month_gan, month_zhi),
        (day_gan, day_zhi),
        (hour_gan, hour_zhi),
    ]
    
    # 2. 轉農曆
    try:
        lunar_year, lunar_month, lunar_day, is_leap = gregorian_to_lunar(year, month, day)
        lunar_str = f"{lunar_year}年{'閏' if is_leap else ''}{lunar_month}月{lunar_day}日"
    except:
        lunar_str = "無法轉換"
    
    # 3. 計算十神
    shishen_list = []
    for i, (gan, zhi) in enumerate(pillars):
        if i == 2:  # 日柱
            shishen_list.append("日主")
        else:
            shishen_list.append(get_shishen(day_gan, gan))
    
    # 4. 統計五行
    wuxing_count = count_wuxing(pillars)
    
    # 5. 分析日主強弱
    strength_analysis = analyze_rizhu_strength(day_gan, month_zhi, pillars)
    
    # 6. 推斷用神
    yongshen = get_yongshen(day_gan, strength_analysis["綜合判斷"])
    
    # 7. 計算大運
    dayun = calculate_dayun(year_gan, year_zhi, gender, year, month, day)
    
    # 8. 組裝結果
    result = {
        "基本資訊": {
            "西曆": f"{year}年{month}月{day}日 {hour}時",
            "農曆": lunar_str,
            "性別": gender,
            "生肖": DIZHI_SHENGXIAO[year_zhi],
        },
        "四柱八字": {
            "年柱": {
                "干支": f"{TIANGAN[year_gan]}{DIZHI[year_zhi]}",
                "天干": f"{TIANGAN[year_gan]}（{TIANGAN_WUXING[year_gan]}）",
                "地支": f"{DIZHI[year_zhi]}（{DIZHI_WUXING[year_zhi]}）",
                "藏干": "、".join(DIZHI_CANGGAN[DIZHI[year_zhi]]),
                "十神": shishen_list[0],
            },
            "月柱": {
                "干支": f"{TIANGAN[month_gan]}{DIZHI[month_zhi]}",
                "天干": f"{TIANGAN[month_gan]}（{TIANGAN_WUXING[month_gan]}）",
                "地支": f"{DIZHI[month_zhi]}（{DIZHI_WUXING[month_zhi]}）",
                "藏干": "、".join(DIZHI_CANGGAN[DIZHI[month_zhi]]),
                "十神": shishen_list[1],
            },
            "日柱": {
                "干支": f"{TIANGAN[day_gan]}{DIZHI[day_zhi]}",
                "天干": f"{TIANGAN[day_gan]}（{TIANGAN_WUXING[day_gan]}）【日主】",
                "地支": f"{DIZHI[day_zhi]}（{DIZHI_WUXING[day_zhi]}）",
                "藏干": "、".join(DIZHI_CANGGAN[DIZHI[day_zhi]]),
                "十神": "日主",
            },
            "時柱": {
                "干支": f"{TIANGAN[hour_gan]}{DIZHI[hour_zhi]}",
                "天干": f"{TIANGAN[hour_gan]}（{TIANGAN_WUXING[hour_gan]}）",
                "地支": f"{DIZHI[hour_zhi]}（{DIZHI_WUXING[hour_zhi]}）",
                "藏干": "、".join(DIZHI_CANGGAN[DIZHI[hour_zhi]]),
                "十神": shishen_list[3],
            },
        },
        "五行統計": wuxing_count,
        "日主分析": strength_analysis,
        "用神喜忌": yongshen,
        "大運排列": dayun,
    }
    
    return result


def print_result(result: Dict):
    """格式化輸出結果"""
    print("\n" + "=" * 60)
    print("🎋 八字命理排盤結果")
    print("=" * 60)
    
    print("\n【基本資訊】")
    for key, value in result["基本資訊"].items():
        print(f"  {key}：{value}")
    
    print("\n【四柱八字】")
    print("  " + "-" * 50)
    print(f"  {'':6} | 年柱 | 月柱 | 日柱 | 時柱 |")
    print("  " + "-" * 50)
    
    pillars = result["四柱八字"]
    print(f"  {'干支':6} | {pillars['年柱']['干支']:^4} | {pillars['月柱']['干支']:^4} | {pillars['日柱']['干支']:^4} | {pillars['時柱']['干支']:^4} |")
    print(f"  {'十神':6} | {pillars['年柱']['十神']:^4} | {pillars['月柱']['十神']:^4} | {pillars['日柱']['十神']:^4} | {pillars['時柱']['十神']:^4} |")
    print("  " + "-" * 50)
    
    print("\n【五行統計】")
    wuxing = result["五行統計"]
    print(f"  金:{wuxing['金']:.1f}  木:{wuxing['木']:.1f}  水:{wuxing['水']:.1f}  火:{wuxing['火']:.1f}  土:{wuxing['土']:.1f}")
    
    print("\n【日主分析】")
    for key, value in result["日主分析"].items():
        print(f"  {key}：{value}")
    
    print("\n【用神喜忌】")
    for key, value in result["用神喜忌"].items():
        print(f"  {key}：{value}")
    
    print("\n【大運排列】")
    for dayun in result["大運排列"]:
        print(f"  {dayun['年齡']:12} | {dayun['干支']} ({dayun['五行']})")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) >= 5:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4])
        gender = sys.argv[5] if len(sys.argv) > 5 else "男"
        
        result = paipan(year, month, day, hour, gender)
        print_result(result)
    else:
        print("用法：")
        print("  python bazi_calc.py 年 月 日 時 [性別]")
        print("  例：python bazi_calc.py 1990 8 15 14 男")
        print()
        print("使用當前時間示例：")
        now = datetime.now()
        result = paipan(now.year, now.month, now.day, now.hour, "男")
        print_result(result)
