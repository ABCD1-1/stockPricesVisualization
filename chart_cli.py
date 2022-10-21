import pandas_datareader.data as web
import pandas as pd
import datetime
import sys
import matplotlib.pyplot as plt
from utils import *

# Defaults
pct = False
agg = None
start = datetime.datetime(2022, 1, 1)
end = datetime.datetime.today()

userInputs = sys.argv

if "--help" in userInputs:
    print("""Any command that does not respect these conditions is expected to fail.
- signs (required) : a comma separated list of signs accessible from reader
- col (required) : a comma separated list of column names, available in dataframes
gathered from the reader.
- pct (default = False) : a boolean flag. If set, represent the percentage change of the
value in place of the actual value.
- agg (default = None) : a level of aggregation, authorized values must are (W, M, Y,
all) and are defined as:
- W : aggregate the series on a weekly basis, ending on the last day of
available data;
- M : aggregate the series on a monthly basis, ending on the last day of
available data;
- Y : aggregate the series on a yearly basis, ending on the last day of available
data;
- all : instead of using time series, compute the mean of the series and use
scatter charts as representation:
● X axis : the selected column;
● Y axis : the High column;
● Size of the dot : the log of the Volume.
- start (default = 2022-01-01) the gathered data start date.
- end (default = today’s date) the gathered data start date.""")
    exit()


if "--signs" in userInputs:
    signsIndex = userInputs.index("--signs")
    signs = userInputs[signsIndex + 1]
    if "," in signs:
        signs = signs.split(',')

if "--start" in userInputs:
    startIndex = userInputs.index("--start")
    start = userInputs[startIndex + 1]

if "--end" in userInputs:
    endIndex = userInputs.index("--end")
    end = userInputs[endIndex + 1]


df = web.DataReader(signs, 'yahoo', start=start, end=end)

if not isinstance(signs, list):
    signs = [signs]

if "--col" in userInputs:
    colIndex = userInputs.index("--col")
    col = userInputs[colIndex + 1]
    if "," in col:
        col = col.split(',')
    if not isinstance(col, list):
        col = [col]
    df = df[col]


if "--agg" in userInputs:
    aggIndex = userInputs.index("--agg")
    agg = userInputs[aggIndex + 1]
    assert(agg in ['W', 'M', 'Y', 'all'])
    if agg == 'W':
        df = aggByWeek(df)
    elif agg == 'M':
        df = aggByMonth(df)
    elif agg == 'Y':
        pass
    elif agg == 'all':
        pass


if "--pct" in userInputs:
    pct = True


pctDict = {}

if pct:
    updatePctDict(col, signs, df, pctDict)
    df = getDfFromPctDict(df, pctDict)

# print(pctDict)
# print(df)
# getDfFromPctDict(df, pctDict)

# exit()
ylabel = "Percentage" if pct else "Value"

# df.plot.line()
# df.plot.scatter(x='w',y='h')

plt.figure()
#
for i, columnName in enumerate(col, start=1):
    plt.title(columnName)
    # if pct:
    #     pass
    #     # for sign in pctDict.keys():
    #     #     print(sign)
    #     #     plt.scatter(pctDict[sign])
    #     # plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    # else:
    plt.plot(df[columnName][signs])
    plt.legend(signs)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.show()

