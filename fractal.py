import pandas as pd
import numpy as np
import datetime as dt
import smtrad, time

# Path for csv file
qt_micex = r'C:\Users\RNCB\Desktop\Python\MICEX\QUOTES\USDRUB_TOM\compiled\b_mdf.csv'

# Read csv file
df = pd.read_csv(qt_micex)
df['DATETIME'] = pd.to_datetime(df['DATETIME'], format='%Y%m%d %H:%M:%S')
df.set_index('DATETIME', inplace=True)

# Resampling to 5-min and 30-min candles
df_30 = smtrad.qt_resample(df, '30MIN')
df_5 = smtrad.qt_resample(df, '5MIN')
df_5.tail()

# Search fractal in 30-min
x_min, x_mid, x_max = 0, 2, 5 # Frame range

def ff():
    global x_min, x_mid, x_max
    while x_max < len(df_30): # Start scrolling
#         print(x_min, x_mid, x_max)
        x_mid_low = df_30.iloc[x_mid]['LOW'] # LOW value in the middle of the frame
        x_mid_high = df_30.iloc[x_mid]['HIGH'] # HIGH value in the middle of the frame
        start_date = dt.datetime.date(df_30.index[x_mid]) # Date which we scroll in
        if x_mid_high == df_30.iloc[x_min:x_max]['HIGH'].max(): # If the high in the middle of the frame
            if x_mid_low == df_30.iloc[x_min:x_max]['LOW'].min(): # If the low in the middle of the frame
                print('Wrong candle')
            else:
                print('UpFractal found at ', df_30.index[x_mid], 'rate is ', df_30.iloc[x_mid]['HIGH'])
                ff_30_bu(x_min, x_mid, x_max, x_mid_high, start_date) # Search break up for 30 min
        elif x_mid_low == df_30.iloc[x_min:x_max]['LOW'].min(): # If the low in the middle of the frame
            print('DownFractal found at ', df_30.index[x_mid], 'rate is ', df_30.iloc[x_mid]['LOW'])   
            ff_30_bd(x_min, x_mid, x_max, x_mid_low, start_date) # Search break down for 30 min
        x_min += 1 # Scrolling
        x_mid += 1 # Scrolling
        x_max += 1 # Scrolling

# Search fractal break down in 30-min
def ff_30_bd(x_min, x_mid, x_max, x_mid_low, start_date):
    x_min += 1 # Scrolling
    x_mid += 1 # Scrolling
    x_max += 1 # Scrolling
    while dt.datetime.date(df_30.index[x_mid]) == start_date: # Inside one date check
        if x_mid_low > df_30.iloc[x_mid]['LOW']: # If it is a break down
            # Check if after plunge into 5 min in 30 min df are any fractals
#                 x_min_loc = x_min + 1 # Only for check if there are any fractals after plunge
#                 x_mid_loc = x_mid + 1
#                 x_max_loc = x_max + 1
#                 while dt.datetime.date(df_30.index[x_mid_loc]) == start_date:
#                     if (df_30.iloc[x_mid_loc]['HIGH'] == df_30.iloc[x_min_loc:x_max_loc]['HIGH'].max() or 
#                         df_30.iloc[x_mid_loc]['LOW'] == df_30.iloc[x_min_loc:x_max_loc]['LOW'].min()):
#                         print('There is a fractal after break down')
#                         break
#                     x_min_loc += 1
#                     x_mid_loc += 1
#                     x_max_loc += 1 
#                 else:
#                     print('Out of date')
#                     time_mid = df_30.index[x_mid] # Time of brake
#                     x_mid_low = df_30.iloc[x_mid]['LOW'] # Value of LOW in break point
#                     print('Broken down at ', time_mid, 'at ', x_mid_low)
#                     to_5_down(time_mid, x_mid_low)
#                     break
#                 break
            time_mid = df_30.index[x_mid] # Time of brake
            to_5_down(time_mid, x_mid_low)
    else:
        print('Out of date')
        break
        x_min += 1 # Scrolling
        x_mid += 1 # Scrolling
        x_max += 1 # Scrolling

# Search fractal break up in 30-min
def ff_30_bu(x_min, x_mid, x_max, x_mid_high, start_date):
    x_min += 1 # Scrolling
    x_mid += 1 # Scrolling
    x_max += 1 # Scrolling
    while x_max < len(df_30):
        if dt.datetime.date(df_30.index[x_mid]) == start_date: # Inside one date check
            if x_mid_high < df_30.iloc[x_mid]['HIGH']: # If it is a break up
                # Check if after plunge into 5 min in 30 min df are any fractals
#                 x_min_loc = x_min + 1 # Only for check if there are any fractals after plunge
#                 x_mid_loc = x_mid + 1
#                 x_max_loc = x_max + 1
#                 while dt.datetime.date(df_30.index[x_mid_loc]) == start_date:
#                     if (df_30.iloc[x_mid_loc]['HIGH'] == df_30.iloc[x_min_loc:x_max_loc]['HIGH'].max() or
#                         df_30.iloc[x_mid_loc]['LOW'] == df_30.iloc[x_min_loc:x_max_loc]['LOW'].min()):    
#                         print('There is a fractal after break up')
#                         break
#                     x_min_loc += 1
#                     x_mid_loc += 1
#                     x_max_loc += 1
#                 else:
#                     print('Out of date')
#                     time_mid = df_30.index[x_mid] # Time of brake
#                     x_mid_high = df_30.iloc[x_mid]['HIGH'] # Value of HIGH in break point
#                     print('Broken up at ', time_mid, 'at ', x_mid_high)
#                     to_5_up(time_mid, x_mid_high)
#                     break
#                 break
                time_mid = df_30.index[x_mid] # Time of brake
                to_5_up(time_mid, x_mid_high)
        else:
            print('Out of date')
            break
        x_min += 1 # Scrolling
        x_mid += 1 # Scrolling
        x_max += 1 # Scrolling
        
def to_5_up(time_mid, x_mid_high):
    if time_mid in df_5.index:
        x_min = df_5.index.get_loc(time_mid)
        x_max = x_min + 5
#         print(x_min, x_max)
        while x_mid_high > df_5.iloc[x_min]['HIGH'] and x_min <= x_max:
            x_min += 1
        print('Found the candle in which we broken down at ', df_5.index[x_min])
        inverse_down(x_min)

def to_5_down(time_mid, x_mid_low):
    if time_mid in df_5.index:
        x_min = df_5.index.get_loc(time_mid)
        x_max = x_min + 5
#         print(x_min, x_max)
        while x_mid_low < df_5.iloc[x_min]['LOW'] and x_min <= x_max:
            x_min += 1
        print('Found the candle in which we broken up at ', df_5.index[x_min])
        inverse_up(x_min)
            
def inverse_down(x_min):
    x_mid = x_min + 2
    x_max = x_min + 5
    start_date = dt.datetime.date(df_5.index[x_mid])
    while dt.datetime.date(df_5.index[x_mid]) == start_date:
        x_mid_high = df_5.iloc[x_mid]['HIGH']
        x_mid_low = df_5.iloc[x_mid]['LOW']
        if x_mid_low == df_5.iloc[x_min:x_max]['LOW'].min():
            if x_mid_high == df_5.iloc[x_min:x_max]['HIGH'].max():
                print('Wrong candle')
            else:
                print('Inverse fractal down found in 5 min')
                inverse_up_bd(x_min, x_mid_low)
        x_min += 1
        x_mid += 1
        x_max += 1

def inverse_up(x_min):
    x_mid = x_min + 2
    x_max = x_min + 5
    start_date = dt.datetime.date(df_5.index[x_mid])
    while dt.datetime.date(df_5.index[x_mid]) == start_date:
        x_mid_high = df_5.iloc[x_mid]['HIGH']
        x_mid_low = df_5.iloc[x_mid]['LOW']
        if x_mid_high == df_5.iloc[x_min:x_max]['HIGH'].max():
            if x_mid_low == df_5.iloc[x_min:x_max]['LOW'].min():
                print('Wrong candle')
            else:
                print('Inverse fractal up found in 5 min')
                inverse_up_bu(x_min, x_mid_high)
        x_min += 1
        x_mid += 1
        x_max += 1
        
def inverse_up_bu(x_min, x_mid_high):
    x_min += 1
    x_mid = x_min + 2
    x_max = x_min + 5
    start_date = dt.datetime.date(df_5.index[x_mid])
    while dt.datetime.date(df_5.index[x_mid]) == start_date:
        if x_mid_high >= df_5.iloc[x_mid]['HIGH']:
            x_min += 1
            x_mid += 1
            x_max += 1
        else:
            print('Broken up in 5 min')
            get_back_down(x_mid)
            break
 
def inverse_up_bd(x_min, x_mid_low):
    x_min += 1
    x_mid = x_min + 2
    x_max = x_min + 5
    start_date = dt.datetime.date(df_5.index[x_mid])
    while dt.datetime.date(df_5.index[x_mid]) == start_date:
        if x_mid_low >= df_5.iloc[x_mid]['LOW']:
            x_min += 1
            x_mid += 1
            x_max += 1
        else:
            print('Broken up in 5 min')
            get_back_down(x_mid)
            break
            
def get_back_down(x_mid):
    x_min = x_mid - 5
    x_mid = x_min + 2
    x_max = x_mid
    
    while 
    
#     list_low = list(df_5['LOW'][x_min:x_max])
#     list_lowest = []
#     for x in list_low:
#         if x == list_low[2]:
#             list_lowest.append(x)

#     while True:
#         while len(list_lowest) < 1:
#             x_min -= 1
#             x_max -= 1
#             list_low = list(df_5['LOW'][x_min:x_max])
#             list_lowest = []
#             for x in list_low:
#                 if x == list_low[2]:
#                     list_lowest.append(x)

#         if df_5['LOW'][x_min:x_max][2] == df_5['LOW'][x_min:x_max].min():
#             x_mid = x_max - 3
#             go_long(x_mid)
#             break

#         x_min -= 1
#         x_mid -= 1
#         x_max -= 1
            
def get_back_up(x_mid):
    x_min = x_mid - 5
    x_max = x_mid
    
    list_high = list(df_5['HIGH'][x_min:x_max])
    list_highest = []
    for x in list_high:
        if x == list_high[2]:
            list_highest.append(x)

    while True:
        while len(list_highest) < 1:
            x_min -= 1
            x_max -= 1
            list_high = list(df_5['HIGH'][x_min:x_max])
            list_highest = []
            for x in list_high:
                if x == list_high[2]:
                    list_highest.append(x)

        if df_5['HIGH'][x_min:x_max][2] == df_5['HIGH'][x_min:x_max].max():
            x_mid = x_max - 3
            go_long(x_mid)
            break

        x_min -= 1
        x_mid -= 1
        x_max -= 1
        
def go_long(x_mid):        
    long_min = x_mid
    long_mid = x_mid + 2
    long_max = x_mid + 5
    while df_5.iloc[x_mid]['HIGH'] >= df_5['HIGH'][long_mid]:
        if long_max < len(df_5):
            long_min += 1
            long_mid += 1
            long_max += 1
        else:
            break
    if dt.datetime.date(df_5.index[x_mid]) == dt.datetime.date(df_5.index[long_mid]): # Проверка на работу внутри одних суток
        print('+++ +++ +++ +++ +++ +++ GO LONG at ' + str(df_5['HIGH'][long_min + 2]) + ' at ' + str(df_5.index[long_min + 2]))
#         pivot = short_min + 2
#         pivots(pivot)

def go_short(x_mid):
    short_min = x_mid
    short_mid = x_mid + 2
    short_max = x_mid + 5
    while df_5.iloc[x_mid]['LOW'] <= df_5['LOW'][short_mid]:
        if short_max > len(df_5):
            short_min += 1
            short_mid += 1
            short_max += 1
        else:
            break
    if dt.datetime.date(df_5.index[x_mid]) == dt.datetime.date(df_5.index[short_mid]): # Проверка на работу внутри одних суток
        print('+++ +++ +++ +++ +++ +++ GO SHORT at ' + str(df_5['LOW'][short_min + 2]) + ' at ' + str(df_5.index[short_min + 2]))