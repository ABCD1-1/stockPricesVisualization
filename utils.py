import pandas as pd
import datetime
from dateutil import relativedelta

def aggByWeek(df):
    dfIndex= df.index
    dfWeeks = df.iloc[0:5, :].mean(axis=0).to_frame().T
    dfWeeks.set_index(pd.Index([dfIndex[0]]), inplace=True)
    for iWeek in range(1, len(df)//5):
        dfWeek = df.iloc[iWeek*5:(iWeek*5+5), :].mean(axis=0).to_frame().T
        dfWeek.set_index(pd.Index([dfIndex[iWeek*5]]), inplace=True)
        dfWeeks = pd.concat([dfWeeks,dfWeek])
    return dfWeeks

def aggByMonth(df):
    dfIndex= df.index
    # Generate date every complete month
    monthsDate = pd.date_range(str(dfIndex[0])[:10], str(dfIndex[-1])[:10], freq='1M').tolist()
    dfMonths = df.iloc[dfIndex < monthsDate[0], :].mean(axis=0).to_frame().T

    dfMonths.set_index(pd.Index([dfIndex[0]]), inplace=True)
    for iMonth in range(1, len(monthsDate)):
        dfMonth = df.iloc[(dfIndex > monthsDate[iMonth-1]) & (dfIndex < monthsDate[iMonth]),:].mean(axis=0).to_frame().T
        dfMonth.set_index(pd.Index([monthsDate[iMonth]]), inplace=True)
        dfMonths = pd.concat([dfMonths,dfMonth])
    return dfMonths


def updatePctDict(col, signs, df, pctDict):
    dfIndex = df.index
    for i in range(1,len(dfIndex)):
        pctDictTemp = {}
        for column in col:
            dateStart = dfIndex[i-1]
            dateEnd = dfIndex[i]
            if len(signs) > 1:
                for sign in signs:
                    percentage = 100 * (df.loc[[dateEnd]][column][sign].item() - df.loc[[dateStart]][column][sign].item()) / df.loc[[dateStart]][column][sign].item()
                    if column not in pctDictTemp:
                        pctDictTemp[column] = {sign: percentage}
                    else:
                        pctDictTemp[column][sign] = percentage

                    # if sign not in pctDictTemp:
                    #     pctDictTemp[sign] = {column: percentage}
                    # else:
                    #     pctDictTemp[sign][column] = percentage
            else:
                percentage = 100 * (df.loc[[dateEnd]][column].item() - df.loc[[dateStart]][column].item()) / df.loc[[dateStart]][column].item()
                if column not in pctDictTemp:
                    pctDictTemp[column] = {signs[0]: percentage}
                else:
                    pctDictTemp[column][signs[0]] = percentage
                # if signs[0] not in pctDictTemp:
                #     pctDictTemp[signs[0]] = {column: percentage}
                # else:
                #     pctDictTemp[signs[0]][column] = percentage

        pctDict[dateEnd] = pctDictTemp


def getDfFromPctDict(df, pctDict):
    dfIndex = df.index[1:]   # don't take the first item because it is used as reference for comparison
    dfColumns = df.columns
    pctDf = pd.DataFrame(index=dfIndex, columns=dfColumns)
    for index in pctDict.keys():
    # for index in dfIndex:
        if isinstance(dfColumns, pd.MultiIndex):
            for columnIndex in dfColumns:
                pctDf.loc[index, [columnIndex]] = pctDict[index][columnIndex[0]][columnIndex[1]]

    return pctDf




