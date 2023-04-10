import requests
import pandas as pd
import csv

query = {'stationId':'KNYNEWYO1348', 'format':'json', 'units':'e','apiKey':'329d28aca92149f19d28aca92139f1ea'}
src = "https://api.weather.com/v2/pws/observations/all/1day"
res = requests.get(src, params=query).json()

csvfile = open('rainfall_04_10_2022', 'w', newline='')
rainwriter = csv.writer(csvfile, delimiter=',')
#write the names of the columns to the csv
rainwriter.writerow(['time_local', 'time_utc', 'precip_rate', 'precip_total'])

#df = pd.DataFrame(columns=['time_local', 'time_utc', 'precip_rate', 'precip_total'])
#print(res['observations'][0])

for obs in res['observations']:
    tl = obs['obsTimeLocal']
    tu = obs['obsTimeUtc']
    pr = obs["imperial"]["precipRate"]
    pt = obs['imperial']['precipTotal']
    # write a row of data into the csvfile
    rainwriter.writerow([tl, tu, pr, pt])

    #df.loc[len(df.index)] = [tl, tu, pr, pt]
    #print("precip_rate: {}, precip_total: {}".format(pr, pt))

#print(df.head())