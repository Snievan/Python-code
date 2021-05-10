
- [0. Install](#0-install)
  - [PIP install with image site](#pip-install-with-image-site)
- [1. System](#1-system)
  - [OS, SYS](#os-sys)
    - [Mute Warnings](#mute-warnings)
    - [get_path_for_file](#get_path_for_file)
    - [Unzip Files](#unzip-files)
    - [os.walk](#oswalk)
  - [MS Office](#ms-office)
    - [pywin32](#pywin32)
  - [String](#string)
    - [decoding](#decoding)
    - [ord,chr](#ordchr)
- [2. Web Scraping](#2-web-scraping)
- [3. Date & Time](#3-date--time)
  - [Get Timestamp](#get-timestamp)
  - [Conver Time Zone in pd](#conver-time-zone-in-pd)
  - [time, datetime module](#time-datetime-module)
  - [Date Formatting](#date-formatting)
- [4. Visualization](#4-visualization)
  - [Echarts](#echarts)
  - [matplotlib](#matplotlib)
    - [initailizing](#initailizing)
    - [Chinese enable](#chinese-enable)
    - [Basic use case: style](#basic-use-case-style)
    - [Multiplots](#multiplots)
    - [line plot](#line-plot)
    - [Scatter plot](#scatter-plot)
    - [Pie chart](#pie-chart)
    - [Tricks](#tricks)
  - [seaborn](#seaborn)
    - [Save Image](#save-image)
- [5. Binary Operator](#5-binary-operator)
- [6. Data Wrangling](#6-data-wrangling)
  - [Pandas](#pandas)
    - [read data](#read-data)
    - [Basic Use Case](#basic-use-case)
    - [Series'](#series)
    - [Multiindex](#multiindex)
    - [Fitering](#fitering)
    - [DF grouby()](#df-grouby)
    - [df.sort_values()](#dfsort_values)
    - [Observation Padding](#observation-padding)
    - [Pandas Profiling](#pandas-profiling)
    - [Miscs](#miscs)
      - [to_markdown](#to_markdown)
  - [Numpy](#numpy)
  - [Tensor flow](#tensor-flow)
    - [Basics](#basics)
- [7. Regular Expression](#7-regular-expression)
  - [re.comple()](#recomple)
  - [Latex](#latex)
- [8. Formatted output](#8-formatted-output)
- [sql](#sql)
  - [impala](#impala)
  - [HIVE sql](#hive-sql)
    - [One row to many](#one-row-to-many)
    - [grouping sets](#grouping-sets)
    - [Use py code to generate sql](#use-py-code-to-generate-sql)
    - [array, key relevant](#array-key-relevant)
  - [mysql](#mysql)

last update on 2021/5/10

# 0. Install
## PIP install with image site
in cmd mode
```
pip install impala -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

# 1. System

## OS, SYS
### Mute Warnings
```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
```

### get_path_for_file
```
os.path.join (a,b,c)
```

### Unzip Files
```PYTHON
import zipfile
path_to_zip_file = r'../PHM原型系统.rar'
directory_to_extract_to = r'../'
with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)
```

### os.walk 
```PYTHON
import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
```

## MS Office

### pywin32 

1. Open excel, get cell value
```python
from win32com import client
excel = client.Dispatch("Excel.Application")
excel.Visible = True
excel.DisplayAlerts = False

wb = excel.Workbooks.Open(filename) 
for ws in  wb.Worksheets:
    print(ws.name)

row = ws.usedrange.rows.count
col = ws.usedrange.columns.count
data = ws.Range(ws.Cells(1,1),ws.Cells(row,col)).value
```

2. Add hyper link 

```PYTHON
import os

from win32com import client
excel = client.Dispatch("Excel.Application")
excel.Visible = True
excel.DisplayAlerts = False

file_path_abs =  r'file_absoulte_path.xlsx'

wb = excel.Workbooks.Open(file_path_abs) 
for ws in  wb.Worksheets:
    print(ws.name)
cells_left = [wb.Worksheets("数据源").Cells(i+3,4) for i in range(61)]
len(cells_left)

cells_right = [wb.Worksheets("ODS字段").Cells(i+2,1) for i in range(1500) if wb.Worksheets("ODS字段").Cells(i+2,1).value]
len(cells_right)
for i,(l,r) in enumerate(zip(cells_left,cells_right)):
    print(i, l.value, r.value,l.value == r.value, r.row)
for i,(l,r) in enumerate(zip(cells_left,cells_right)):
    wb.Worksheets("数据源").Hyperlinks.Add(Anchor = l,
                                    Address = "",
                                     SubAddress = "ODS字段!A"+str(r.row) ,
                                    TextToDisplay = "")
    
    wb.Worksheets("ODS字段").Hyperlinks.Add(Anchor = r,
                                    Address = "",
                                     SubAddress = "数据源!D"+str(l.row) ,
                                    TextToDisplay = "")
```




## String
### decoding 

```python
s = b"\u8d22\u52a1\u4e2d\u5fc3"
t = s.decode("unicode_escape")
```

### ord,chr
in ascii code int -> char is chr dict, ord for contrast


#  2. Web Scraping
Here introduce `Taland`, a powerful extension of Chorm. You can use `Taland` to test API and params before your coding work get started.

# 3. Date & Time

## Get Timestamp
```python
import datetime 
import time 

# get time stamp
dt = datetime.date(2020,1,1)
dt_tuple = dt.timetuple()
dt_unix = time.mktime(dt_tuple)
```

## Conver Time Zone in pd 
```python
pd.to_datetime(crm_time).tz_convert('Asia/Shanghai')
```
## time, datetime module
generate end of day for each month
```python
import datetime

months = []
for year in (2019,2020):
    for month in range(1,13):
        first_day = datetime.date(year,month,1)
        end_day_str = str(first_day + datetime.timedelta(days=-1))
        months.append(end_day_str)
    
print(months)
```

## Date Formatting
"2020-5-6", such format conver to a regular date format
```python
from dateutil import parser
def date_parse(s):
    ''' Converts a string to a date '''
    try:
        t = parser.parse(s, parser.parserinfo())
        return t.strftime('%Y-%m-%d')
    except:
        return None
df_data["上课日期"] = df_data["上课日期"].apply(date_parse)
```

# 4. Visualization

## Echarts
```python
from pyecharts.charts import Bar
from pyecharts import options as opts
#from pyecharts.render import make_snapshot
bar = (
    Bar({"width": "800", "height": "320px"})
    .add_xaxis(list(dau["mm"].values) )
    .add_yaxis("MAU", mau_arr )
    .add_yaxis("DAU", dau_arr )
    .set_global_opts(title_opts=opts.TitleOpts(title="",subtitle="单位: 万"))
)
bar.render_notebook()#在Notebook中进行渲染图像
```
## matplotlib

### initailizing

```python

import seaborn as sns
import matplotlib.pyplot as plt
my_rcParams = {'font.sans-serif':'Microsoft YaHei','axes.unicode_minus':False,'savefig.dpi':160,'figure.dpi':160}
plt.rcParams.update(my_rcParams)
```

### Chinese enable 
```
import matplotlib.pyplot as plt
## method 1
my_rcParams = {'font.sans-serif':'Microsoft YaHei','axes.unicode_minus':False,'savefig.dpi':160,'figure.dpi':160}
plt.rcParams.update(my_rcParams)
## method 2

from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc', size=16)
# font = FontProperties(family="YouYuan", size=16)
ax[0].set_yticklabels(labels=["美团","滴滴"],rotation = 0,fontproperties=font)

```
### Basic use case: style
```python
plt.style.use("fivethirtyeight") ## 风格
plt.xkcd() ## 风格
plt.figure(3) 

x_index = np.arange(5)   #柱的索引
x_data = ('A', 'B', 'C', 'D', 'E')
y1_data = (20, 35, 30, 35, 27)
y2_data = (25, 32, 34, 20, 25)
bar_width = 0.35   #定义一个数字代表每个独立柱的宽度

rects1 = plt.bar(x_index, y1_data, width=bar_width,alpha=0.4, color='b',label='legend1')            #参数：左偏移、高度、柱宽、透明度、颜色、图例
rects2 = plt.bar(x_index + bar_width, y2_data, width=bar_width,alpha=0.5,color='r',label='legend2') #参数：左偏移、高度、柱宽、透明度、颜色、图例
#关于左偏移，不用关心每根柱的中心不中心，因为只要把刻度线设置在柱的中间就可以了
plt.xticks(x_index + bar_width/2, x_data)   #x轴刻度线
plt.legend()    #显示图例
plt.tight_layout()  #自动控制图像外部边缘，此方法不能够很好的控制图像间的间隔
plt.show()
```
### Multiplots
```python
import pandas as pd
from matplotlib import pyplot as plt
tips = pd.read_csv(r".\seaborn-data-master\tips.csv")

fig,(ax1,ax2) = plt.subplots(nrows=1,ncols=2,sharey=True)
ax1.hist("day",data = tips.query(""" sex=="Male" """))
ax1.set_xlabel("Male counts")
ax2.hist("day",data = tips.query(""" sex=="Female" """))
ax2.set_xlabel("Female counts")
```
### line plot

### Scatter plot


### Pie chart
```python
plt.style.use("fivethirtyeight")

slices = [10,20,30,40,50]
labels = ["Java","HTML","SQL","Python","Java"]
explode = [0,0,0,0.1,0]

plt.pie(slices, labels = labels, explode=explode, shadow=True, startangle = 90,
    autopct= '%1.1f%%',
    wedgeprops={"edgecolor":"black"},
    )

plt.title("My Pie Chart")
plt.tight_layout()
plt.show()
```


### Tricks
```
plt.tight_layout()
plt.figure(figsize=(9, 3)) # size set
ax.legend()                # show legend
plt.xticks(rotation=75)    # rotation
```


## seaborn
```
g.set_yscale("log")
g.fig.get_axes()[0].set_yscale('log')
```

```
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)
```
labeL rename\log
```
ax = sns.countplot(y="school_dept", data = df_week.query(query_expr), color="b")
ax.set(xlabel = "xxx",ylabel = "yyy")
ax.set_yscale('log',nonposy='mask',subsy=[0])
plt.show()
```



### Save Image
```python
img.savefig("test.png")
``` 

# 5. Binary Operator
`<<`denoete's add 0's to right side, `>>` means ignore some number's on the right most side
```python
## 190. Reverse Bits
ret, power = 0, 31
while n:
    ret += (n & 1) << power
    n = n >> 1  
    power -= 1
print (ret)
```
# 6. Data Wrangling

## Pandas

### read data
Convert date featrue with timezone
```python
date_parser = lambda x: pd.to_datetime(x).tz_convert('Asia/Shanghai').date()
class_info = pd.read_csv("ClassInformation__c_20201021.csv",parse_dates = ["CreatedDate"],date_parser = date_parser)
```

### Basic Use Case
```
col1 = pd.Series( {1:10,3:10,5:10} )
col2 = pd.Series( {2:20,4:30,5:40,6:50} )

fig, ax = plt.subplots()
ax.plot(col1, label="dog")
ax.plot(col2, label="cat")
ax.legend()

plt.show()
```


### Series'
```
df_week["school_industy"].value_counts()
data['Title'] = data['Title'].replace(['Mme'], 'Miss')
```
### Multiindex

```
vals = [sr_industry_cnt.loc[industry,i] if (industry,i) in sr_industry_cnt.index else 0 for industry in industry_arr]
```

### Fitering
Dataframe.query() function
```
import pandas as pd
df = pd.DataFrame({'a':[1, 2, 3, 4, 5, 6],
                   'b':[1, 2, 3, 4, 5, 6],
                   'c':[1, 2, 3, 4, 5, 6]})

query_list = [1, 2]
df_2 = df.query('c not in @query_list')[['a', 'b']]

```
```
df[(df.A==100)&(df.B=='a')]
```

### DF grouby()
```
grouped = df.groupby('Gender')
grouped_muti = df.groupby(['Gender', 'Age'])

print(grouped.size())
print(grouped_muti.size())

print(grouped.get_group('Female'))
print(grouped_muti.get_group(('Female', 17)))

print(grouped.count())
print(grouped.max()[['Age', 'Score']])
print(grouped.mean()[['Age', 'Score']])


```
### df.sort_values()

```
DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last')
```

###  Observation Padding
```
mport pandas as pd

df = pd.DataFrame([['a','x','1'],['a','y','2'],['b','x','3']])
df.columns = ['cat1','cat2','val1']
df.head()


df['join_key'] = 0
df_new = pd.merge(df[['cat1','join_key']].drop_duplicates(),df[['cat2','join_key']].drop_duplicates(),how='outer',on='join_key')
df_new.drop(columns=['join_key'],inplace=True)

df = pd.merge(df_new,df,on = ['cat1','cat2'],how = 'left')
df.drop(columns=['join_key'],inplace=True)
df_new.head()
```

### Pandas Profiling
```python
import  pandas as pd
import pandas_profiling 
# read data
titanic = pd.read_csv('https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/titanic_train.csv')

profile = pandas_profiling.ProfileReport(titanic)
profile.to_file(outputfile = "output_file.html")
```

### Miscs
#### to_markdown
df.to_markdown
```sql
file_name = r"class_header.csv"
import pandas as pd 
def df_to_md(df):
    md = ""
    header ="|"+  "|".join(str(c) for c in df.columns) + "|"
    line =  "|" + "|".join("-:"for c in df.columns) + "|"
    md += header +"\n"
    md += line +"\n"
    for i, row in df.iterrows():
        md += "|"+ "|".join(str(s) for s in row) + "|" + "\n"
    print(md)
    return md

df =  pd.read_csv(file_name, encoding = 'utf-8')
with open(r"mk_table.txt","w") as f:
    f.write(df_to_md(df))

```
## Numpy

## Tensor flow

### Basics
```python
import tensorflow as tf
msg = tf.constant("Hello world")
with tf.Session() as sess:
    print(sess.run(msg).decode())

sess = tf.InteractiveSession()
A = tf.Variable(tf.random_normal([5,10]))
A.initializer.run()
```


# 7. Regular Expression
## re.comple()
```
import re 
s = "a good   example"
regex  = re.compile('\s+')
res = regex.split(s)
print(res)
```

## Latex
$y = x^2 + 5$


# 8. Formatted output
```
train_stop_threshold = 0.8
print("\nreached accuracy of {:0.1f}%".format(0.952*100))
```
```python
print("Worksheet Count: \t",wb.Worksheets.count)
print("Sheetname\t\t\trows\tcols")
print("-"*48)
for ws in  wb.Worksheets:
    ws_info = {"name" : ws.name,
          "rows":ws.usedrange.rows.count,
          "cols":ws.usedrange.columns.count}
    print("{name:<30s}\t {rows:>6,d}\t{cols:>6,d}".format(**ws_info) )
```

# sql
## impala 
use python to access
```python
from impala.dbapi import connect
from impala.util import as_pandas

# 需要注意的是这里的auth_mechanism必须有，默认是NOSASL，但database不必须，user也不必须
conn = connect(host='172.16.250.1', port=61102, database='default', auth_mechanism='PLAIN', user='hive')
cur = conn.cursor()

sql = """SELECT * FROM liwenhe.class_student_daily limit 10 """

cur.execute(sql)
data = as_pandas(cur)
```

## HIVE sql
### One row to many
```sql
SELECT lv.* 
FROM   ( SELECT 0) t 
lateral VIEW explode(array(1234567890,9876543210)) lv AS phone;

SELECT lv.* 
FROM   (SELECT 0) t 
lateral VIEW inline(array(struct('A',10,'AAA'),struct('B',20, 'BBB'),struct('B',300, 'CCC') )) lv AS col1, col2, col3;

time generator
```sql
select tf.*,t.*, date_add(start_date,pos) 
from (
  select 'a' as a, '2018-11-01' as start_date, '2018-12-01' as end_date 
) t 
lateral view posexplode(split(space(datediff(end_date,start_date)),' ')) tf as pos,val limit 5000
```
### grouping sets 
```sql
with data as (
SELECT "beijing" as city, "1" as mon, "10" as val union all
SELECT "beijing" as city, "2" as mon, "15" as val union all
SELECT "beijing" as city, "3" as mon, "20" as val union all
SELECT "shanghai" as city, "1" as mon, "30" as val union all
SELECT "shanghai" as city, "2" as mon, "40" as val union all
SELECT "shanghai" as city, "3" as mon, "50" as val)

select 
GROUPING__ID, --1city,2mon,3city&mon
city,mon,sum(val) as val
from data 
group by city,mon
grouping sets (city,mon,(city,mon))
order by GROUPING__ID,city,mon
```

###  Use py code to generate sql

```python
import datetime 

sql_template = """ 
select
'{}' as mon,
school_uid,
count(distinct member_uid) as mau,
count(1) as rk_cnt
from  class_student_daily
where time_dd between '{}' and '{}'
group by school_uid
union all 
"""
# struct st/ed date 
months = []
for year in (2019,2020):
    for month in range(1,13):
        ed_date = datetime.date(year,month,1) + datetime.timedelta(days = -1)
        st_date = datetime.date(year,month,1) + datetime.timedelta(days = -30)
        months.append((str(st_date),str(ed_date)))

# sql strucnt 
sql = ""
for st_date,ed_date in months[1:19]:
    sql += sql_template.format(ed_date[:7],st_date,ed_date)
print(sql[:100])

filename = r'sc_per_mon.sql' 

with open(filename,"w") as f :
    f.write(sql)
print(filename, "has saved! ")
```
### array, key relevant

```sql
 select map_keys( map('key1','value1','key2','value2','key3','value3')) as keys;
```
+-------------------------+--+
|          keys           |
+-------------------------+--+
| ["key1","key2","key3"]  |
+-------------------------+--+

```sql
select sort_array(array(1,3,5,2,5));
```
+--------------+--+
|     _c0      |
+--------------+--+
| [1,2,3,5,5]  |
+--------------+--+

```sql
select size(array(1,3,5,2,5));
```
+------+--+
| _c0  |
+------+--+
| 5    |
+------+--+
```
select sentences('Hello there! How are you?');
```
+------------------------------------------+--+
|                   _c0                    |
+------------------------------------------+--+
| [["Hello","there"],["How","are","you"]]  |
+------------------------------------------+--+
1 row selected (0.339 seconds)


## mysql 
查看表注释
```sql
SELECT
table_name 表名,
table_comment 表说明
FROM
information_schema.TABLES
WHERE
table_schema = ‘数据库名’
ORDER BY
table_name
```
查看字段注释
```sql
SELECT 
table_name,
column_name,
column_comment
FROM 
information_schema.COLUMNS WHERE  
TABLE_SCHEMA='eo_oshw'
and TABLE_NAME = 'eeo_course_homework'

```
