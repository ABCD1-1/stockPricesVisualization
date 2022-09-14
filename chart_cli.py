import pandas_datareader.data as web
import pandas as pd
import datetime
import sys
import matplotlib.pyplot as plt

# Defaults
pct = False
agg = None
start = datetime.datetime(2022, 1, 1)
end = datetime.datetime.today()

user_inputs = sys.argv
if "--signs" in user_inputs:
    signsIndex = user_inputs.index("--signs")
    signs = user_inputs[signsIndex+1]
    if "," in signs:
        signs = signs.split(',')

df = web.DataReader(signs, 'yahoo', start=start, end=end)

if not isinstance(signs, list):
    signs = [signs]

if "--col" in user_inputs:
    colIndex = user_inputs.index("--col")
    col = user_inputs[colIndex + 1]
    if "," in col:
        col = col.split(',')
    if not isinstance(col, list):
        col = [col]
    df = df[col]

if "--pct" in user_inputs:
    pct = True


if "--agg" in user_inputs:
    aggIndex = user_inputs.index("--agg")
    agg = user_inputs[aggIndex + 1]
    assert(agg in ['W', 'M', 'Y', 'all'])

if "--start" in user_inputs:
    startIndex = user_inputs.index("--start")
    start = user_inputs[startIndex + 1]

if "--end" in user_inputs:
    endIndex = user_inputs.index("--end")
    end = user_inputs[endIndex + 1]

if "--help" in user_inputs:
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
- W : aggregate the series on a yearly basis, ending on the last day of available
data;
- all : instead of using time series, compute the mean of the series and use
scatter charts as representation:
● X axis : the selected column;
● Y axis : the High column;
● Size of the dot : the log of the Volume.
- start (default = 2022-01-01) the gathered data start date.
- end (default = today’s date) the gathered data start date.""")

pctDict = {}
def pct(df):
    for column in col:
        dateTimeYesterday = datetime.date.today() - datetime.timedelta(days=1)  # because data of today is not yet in the API
        dateTimeYesterday_1 = dateTimeYesterday - datetime.timedelta(days=1)  # because data of today is not yet in the API

        # Doesn't work well

        if len(signs) > 1:
            for sign in signs:
                percentage = (df.loc[[dateTimeYesterday]][column][sign] - df.loc[[dateTimeYesterday_1]][column][sign]) / df.loc[[dateTimeYesterday]][column][sign]
                print("ici", df.loc[[dateTimeYesterday]][column][sign])

                print(percentage)
                pctDict[column] = [sign, percentage]
        else:
            percentage = (df.loc[[dateTimeYesterday]][column] - df.loc[[dateTimeYesterday_1]][column]) / \
                         df.loc[[dateTimeYesterday]][column]
            print("ici", df.loc[[dateTimeYesterday]][column])

            print(percentage)
            pctDict[column] = [sign, percentage]

# pct(df)
# print(pctDict)

def aggByWeek(df):
    # doesn't work well
    df_weeks = df.iloc[0:5, :].mean(axis=0)
    for iWeek in range(1, len(df)//5):
        df_week = df.iloc[iWeek*5:(iWeek*5+5), :].mean(axis=0)
        df_weeks = pd.concat([df_weeks,df_week])

    return df_weeks

# df = aggByWeek(df)
# print(df)
# exit()


plt.figure()

for i, columnName in enumerate(col, start=1):
    plt.title(columnName)
    plt.plot(df[columnName][signs])
    plt.legend(signs)
    plt.xlabel("Date")

    plt.show()

