# -*- coding: utf-8 -*-
# 程序清单 3-1
print("--------- 程序清单 3-1----------")
import os
import sys

os.chdir(os.path.expanduser("~") + "/Desktop/白帽教程整理/安全数据分析/数据驱动安全/Code For Data-driven Security/book/ch03")

# 程序清单 3-3
print("--------# 程序清单 3-3--------")
# URL for the AlienVault IP Reputation Database (OSSIM format)
# storing the URL in a variable makes it easier to modify later将URL存入一个变量中，让它在之后更好被修改
# if it changes. NOTE: we are using a specific version of the data in these examples, 如果被修改了，就提示：我们在例子中使用一个这个数据的特殊版本
# so we are pulling it from an alternate book-specific location.

import urllib
import os.path

avURL = "http://datadrivensecurity.info/book/ch03/data/reputation.data"

# 下载数据的相对路径
avRep = "data/reputation.data"

# using an if-wrapped test with urllib.urlretrieve() vs direct read
# 通过pandas来避免每次我们跑这个脚本都要重新下载一个16MB的文件
if not os.path.isfile(avRep):
    urllib.urlretrieve(avURL, filename=avRep)

# 程序清单 3-5
print("--------  # 程序清单 3-5   读入数据  --------")

import pandas as pd

# 将数据读入一个 pandas data frame
av = pd.read_csv(avRep, sep="#", header=None)

# 换上一个更棒的列表名
av.columns = ["IP", "Reliability", "Risk", "Type", "Country",
              "Locale", "Coords", "x"]

# print(av)  # 查看一下数据结构

## <class 'pandas.core.frame.DataFrame'>
## Int64Index: 258626 entries, 0 to 258625
## Data columns (total 8 columns):
## IP             258626  non-null values
## Reliability    258626  non-null values
## Risk           258626  non-null values
## Type           258626  non-null values
## Country        248571  non-null values
## Locale         184556  non-null values
## Coords         258626  non-null values
## x              258626  non-null values
## dtypes: int64(2), object(6)

# 查看一下前五行
av.head().to_csv(sys.stdout)
## ,IP,Reliability,Risk,Type,Country,Locale,Coords,x
## 0,222.76.212.189,4,2,Scanning Host,CN,Xiamen,"24.4797992706,
## 118.08190155",11
## 1,222.76.212.185,4,2,Scanning Host,CN,Xiamen,"24.4797992706,
## 118.08190155",11
## 2,222.76.212.186,4,2,Scanning Host,CN,Xiamen,"24.4797992706,
## 118.08190155",11
## 3,5.34.246.67,6,3,Spamming,US,,"38.0,-97.0",12
## 4,178.94.97.176,4,5,Scanning Host,UA,Merefa,"49.8230018616,
## 36.0507011414",11

# Listing 3-6
print("\n--------# 程序清单 3-6  用HTML的格式显示数据 --------")
# 要求3-5中的 av
# See corresponding output in Figure 3-1
# import the capability to display Python objects as formatted HTML
from IPython.display import HTML, display

# 显示数据框架中的前10行 display the first 10 lines of the dataframe as formatted HTML
# 使用HTML一直打印出来的都是 <IPython.core.display.HTML object>
# HTML(av.head(10).to_html())
print(av.head(10))

# Listing 3-8
print("\n--------# 程序清单 3-8 用describe()统计数据--------")

# require object: av (3-5)
av['Reliability'].describe()
## count    258626.000000
## mean          2.798040
## std           1.130419
## min           1.000000
## 25%           2.000000
## 50%           2.000000
## 75%           4.000000
## max          10.000000
## Length: 8, dtype: float64
av['Risk'].describe()
## count    258626.000000
## mean          2.221362
## std           0.531571
## min           1.000000
## 25%           2.000000
## 50%           2.000000
## 75%           2.000000
## max           7.000000
## Length: 8, dtype: float64
print(av.describe())

# Listing 3-10
print("--------# 程序清单 3-10   分类数据--------")

# require object: av (3-5)
# factor_col(col)
# 
# helper function to mimic R's "summary()" function
# for pandas "columns" (which are really just Python
# arrays)
# 利用pandas将数据帧的列转换成一个命名恰当的categorical对象
def factor_col(col):
    factor = pd.Categorical(col)
    # value_counts 计算一个非空值的数的柱状图, sort=False不按照值大小排序展示
    return pd.value_counts(factor, sort=False)

rel_ct = pd.value_counts(av['Reliability'])
risk_ct = pd.value_counts(av['Risk'])
type_ct = pd.value_counts(av['Type'])
country_ct = pd.value_counts(av['Country'])

# print("\n---av['Reliability']---")
# print(factor_col(av['Reliability']))
## 1       5612
## 2     149117
## 3      10892
## 4      87040
## 5          7
## 6       4758
## 7        297
## 8         21
## 9        686
## 10       196
## Length: 10, dtype: int64

# print("\n---av['Risk']---")
# print(factor_col(av['Risk']))
## 1        39
## 2    213852
## 3     33719
## 4      9588
## 5      1328
## 6        90
## 7        10
## Length: 7, dtype: int64

# print("\n----av['Type']前十个---")
# print(factor_col(av['Type']).head(n=10))
## APT;Malware Domain                  1
## C&C                               610
## C&C;Malware Domain                 31
## C&C;Malware IP                     20
## C&C;Scanning Host                   7
## Malicious Host                   3770
## Malicious Host;Malware Domain       4
## Malicious Host;Malware IP           2
## Malicious Host;Scanning Host      163
## Malware Domain                   9274
## Length: 10, dtype: int64

# print("\n----av['Country']前十个-----")
# print(factor_col(av['Country']).head(n=10))
## A1     267
## A2       2
## AE    1827
## AL       4
## AM       6
## AN       3
## AO     256
## AR    3046
## AT      51
## AU     155
## Length: 10, dtype: int64


print("------------------3-14~3-16为以上数据的可视化显示---------------")
# Listing 3-14
print("--------# 程序清单 3-14   为 3-5 的可视化展示(需要单独在命令行跑代码)--------")
# require object: av (3-5)
# See corresponding output in Figure 3-5
# NOTE: Notice the significant differnce in the Python graph in that the 
#       blank/empty country code entries are not in the graph
# need some functions from matplotlib to help reduce 'chart junk'
import matplotlib.pyplot as plt

# sort by country
country_ct = pd.value_counts(av['Country'])

# plot the data
plt.axes(frameon=0)  # reduce chart junk
country_ct[:20].plot(kind='bar',
                     rot=0, title="Summary By Country", figsize=(8, 5)).grid(False)

# Listing 3-15
print("--------# 程序清单 3-15  图3-6的相应输出--------")

# requires packages: matplotlib
# require object: av (3-5), factor_col (3-10)
# 查看 Figure 3-6的相应输出
plt.axes(frameon=0)  # 减少图标垃圾
factor_col(av['Reliability']).plot(kind='bar', rot=0,
                                   title="Summary By 'Reliability'", figsize=(8, 5)).grid(False)

# Listing 3-16
print("--------# 程序清单 3-16   图3-7 的相应输出--------")

# requires packages: matplotlib
# require object: av (3-5), factor_col (3-10)
# See corresponding output in Figure 3-7
plt.axes(frameon=0)  # reduce chart junk
factor_col(av['Risk']).plot(kind='bar', rot=0,
                            title="Summary By 'Risk'", figsize=(8, 5)).grid(False)

# Listing 3-18
print("\n--------# 程序清单 3-18  提取10个最流行的国家--------")

# require object: av (3-5)
# extract the top 10 most prevalent countries
top10 = pd.value_counts(av['Country'])[0:9]
# calculate the % for each of the top 10为前十名中的每一个计算比例
print(top10.astype(float) / len(av['Country']))
## CN    0.265182
## US    0.194826
## TR    0.053970
## DE    0.038484
## NL    0.030666
## RU    0.024537
## GB    0.024332
## IN    0.021189
## FR    0.021069
## Length: 9, dtype: float64


# Listing 3-20
print("\n--------# 程序清单 3-20--------")

# require object: av (3-5)
# compute contingency table for Risk/Reliability factors which 
# produces a matrix of counts of rows that have attributes at
# each (x, y) location
# need cm for basic colors
# need arange to modify axes display
from matplotlib import cm
from numpy import arange

print(pd.crosstab(av['Risk'], av['Reliability']).to_string())
## Reliability    1       2     3      4   5     6    7   8    9   10
## Risk                                                              
## 1               0       0    16      7   0     8    8   0    0   0
## 2             804  149114  3670  57653   4  2084   85  11  345  82
## 3            2225       3  6668  22168   2  2151  156   7  260  79
## 4            2129       0   481   6447   0   404   43   2   58  24
## 5             432       0    55    700   1   103    5   1   20  11
## 6              19       0     2     60   0     8    0   0    1   0
## 7               3       0     0      5   0     0    0   0    2   0


# graphical view of contingency table (swapping risk/reliability)
xtab = pd.crosstab(av['Reliability'], av['Risk'])
plt.pcolor(xtab, cmap=cm.Greens)
plt.yticks(arange(0.5, len(xtab.index), 1), xtab.index)
plt.xticks(arange(0.5, len(xtab.columns), 1), xtab.columns)
plt.colorbar()
plt.title("Risk ~ Reliability")

# Listing 3-23
print("--------# 程序清单 3-23 显示整个Risk和Reliabilty的关系--------")

# require object: av (3-5)
# See corresponding output in Figure 3-9
# compute contingency table for Risk/Reliability factors which 
# produces a matrix of counts of rows that have attributes at

# create new column as a copy of Type column
av['newtype'] = av['Type']

# replace multi-Type entries with “Multiples”
av[av['newtype'].str.contains(";")] = "Multiples"

# setup new crosstab structures
typ = av['newtype']
rel = av['Reliability']
rsk = av['Risk']

# compute crosstab making it split on the
# new “type” column
xtab = pd.crosstab(typ, [rel, rsk],
                   rownames=['typ'], colnames=['rel', 'rsk'])

# the following print statement will show a huge text
# representation of the contingency table. The output
# is too large for the book, but is worth looking at 
# as you run through the exercise to see how useful 
# visualizations can be over raw text/numeric output

# print(xtab.to_string())  # output not shown

xtab.plot(kind='bar', legend=False,
          title="Risk ~ Reliabilty | Type").grid(False)

# Listing 3-25
print("--------# 程序清单 3-25 去掉显示最多的Scanning Host，避免他遮盖了其他数据（比例占得太大）--------")

# require object: av (3-5)
# See corresponding output in Figure 3-14
# filter out all "Scanning Hosts"
rrt_df = av[av['newtype'] != "Scanning Host"]
typ = rrt_df['newtype']
rel = rrt_df['Reliability']
rsk = rrt_df['Risk']
xtab = pd.crosstab(typ, [rel, rsk],
                   rownames=['type cv'], colnames=['rel', 'rsk'])
xtab.plot(kind='bar', legend=False,
          title="Risk ~ Reliabilty | Type").grid(False)

print("""根据这张图可以看出，Malware Doamin类的风险评级在2-3之间，
可靠性集以2为中心向外蔓延。
另外Malware distribution没有产生任何的风险，在程序清单3-27中我们可以移除它
""")
# Listing 3-27
print("--------# 程序清单 3-27 移除Malware distribution和Malware Domain--------")

# require object: av (3-5), rrt_df (3-25)
# See corresponding output in Figure 3-16
rrt_df = rrt_df[rrt_df['newtype'] != "Malware distribution"]
rrt_df = rrt_df[rrt_df['newtype'] != "Malware Domain"]
typ = rrt_df['newtype']
rel = rrt_df['Reliability']
rsk = rrt_df['Risk']
xtab = pd.crosstab(typ, [rel, rsk],
                   rownames=['typ'], colnames=['rel', 'rsk'])

print("Count: %d; Percent: %2.1f%%" % (len(rrt_df), (float(len(rrt_df))
                                                     / len(av)) * 100))
## Count: 15171; Percent: 5.9%

xtab.plot(kind='bar', legend=False,
          title="Risk ~ Reliabilty | Type").grid(False)

## END OF CHAPTER 3 PYTHON CODE
