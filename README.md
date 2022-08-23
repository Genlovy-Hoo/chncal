# 中国节假日

判断某年某月某一天是不是工作日/节假日。

修改自chinese_calendar：

github: [chinese-calendar](https://github.com/LKI/chinese-calendar) , pypi: [chinese-calendar](https://pypi.org/project/chinesecalendar/)



**在chinese_calendar的基础上增加了从1990到2003年的数据。**

**增加了A股交易日相关函数（日期参数均可传字符串格式）：**

get_recent_workday：最近的工作日

get_next_nth_workday：往后（前）推n个工作日

get_work_dates：取指定起止日期内的工作日列表

is_tradeday：判断是否为沪深A股交易日

get_recent_tradeday：最近交易日

get_next_nth_tradeday：往后（前）推n个交易日

get_trade_dates：取指定起止日期内的交易日期（周内的工作日）列表



安装：

```
pip install chncal --upgrade
```



Github：

[chncal](https://github.com/Genlovy-Hoo/chncal/)

Pypi

[chncal](https://pypi.org/project/chncal/)

感谢使用和支持！
