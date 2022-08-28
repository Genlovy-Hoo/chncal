# 中国节假日

判断某年某月某一天是不是工作日/节假日。

修改自chinese_calendar：

github: [chinese-calendar](https://github.com/LKI/chinese-calendar) , pypi: [chinese-calendar](https://pypi.org/project/chinesecalendar/)



**在chinese_calendar的基础上增加了从2001到2003年的数据。**

**增加了A股交易日和公历农历干支转换相关函数（日期参数均可传字符串或整数格式）：**

get_recent_workday：最近的工作日

get_next_nth_workday：往后（前）推n个工作日

get_work_dates：取指定起止日期内的工作日列表

is_tradeday：判断是否为沪深A股交易日

get_recent_tradeday：最近交易日

get_next_nth_tradeday：往后（前）推n个交易日

get_trade_dates：取指定起止日期内的交易日期（周内的工作日）列表

get_xingzuo：获取日期所属星座

get_tgdz_year：计算（农历）年份天干地支

gen2lun：公历日期转农历日期

lun2gen：农历日期转普通日期（日期只能传字符串格式，形如'2023.02.30'）

gen2gz：公历日期转干支纪日法

get_tgdz_hour：公历时间（小时）转干支纪时法

get_bazi：根据公历时间生成八字

get_bazi_lunar：根据农历时间生成八字（时间只能传字符串格式，形如'2023.02.30 19:30:20'分和秒可以不写）

fate_weight：称命，传入公历时间

fate_weight_lunar：称命，传入农历时间（时间只能传字符串格式，形如'2023.02.30 19:30:20'分和秒可以不写）

zodiac_match：生肖合婚信息

get_zodiac_match：根据公历时间获取生肖合婚信息

get_zodiac_match_lunar：根据农历时间获取生肖合婚信息（时间只能传字符串格式，形如'2023.02.30 19:30:20'时分秒可以不写）



安装：

```
pip install chncal --upgrade
```



Github：

[chncal](https://github.com/Genlovy-Hoo/chncal/)

Pypi

[chncal](https://pypi.org/project/chncal/)

感谢使用和支持！
