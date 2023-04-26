import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil.parser import parse
from locator import PWSLocator

class Scraper(object):
    def __init__(self, name="MyScraper", init_url="https://www.wunderground.com/dashboard/pws/"):
        self.name = name
        self.init_url = init_url
        #locator = PWSLocator()
        #self.pws_set = locator.get_pws()
        self.pws_set = [("_", "KNYNEWYO116"), ("_", "KNYNEWYO628"), ("_", "KNYNEWYO900"), ("_", "KNYNEWYO1196"), ("_", "KNYNEWYO1664")]

    def __repr__(self):
        print("A web-scraper with the name: ", self.name)
    
    def get_daily_data(self, pws_name: str, dt: datetime, features=['Precip. Rate.', 'Precip. Accum.']) -> pd.DataFrame:
        date_str = "-".join([str(dt.year), str(dt.month), str(dt.day)])
        mod_str = (date_str + "/") * 2
        #print("date_str = ", mod_str)
        url = "".join([self.init_url, pws_name, "/table/", mod_str, "daily"])
        #print("init_url=", self.init_url)
        #print("pws_name=", pws_name)
        #print("mod_str=", mod_str)
        #print("url = ", url)
        
        # Send an HTTP request to the URL and get the HTML content
        # url = 'https://www.wunderground.com/dashboard/pws/KNYNEWYO1348/table/2022-10-3/2023-4-23/daily'

        response = requests.get(url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first table element with the specified classes
        table = soup.select_one('table.history-table.desktop-table')
        df = pd.read_html(str(table))[0].dropna()

        rain_data = df[features].dropna()
        print(date_str)
        #print(df['Time'])
        
        rain_data['Datetime'] = pd.to_datetime(date_str + " " + df['Time'], format='%Y-%m-%d %I:%M %p')
        #print(rain_data.head())
        #rain_data.to_csv('rain_data.csv', index=False)
        return rain_data

    def __check_dates(self, start_date: str, end_date: str):
        while (1):
            try:
                start_date_obj = parse(start_date)
                end_date_obj = parse(end_date)
                if (end_date_obj < start_date_obj):
                    raise ValueError("Start date must be before or equal to the end date")
                elif (end_date_obj > datetime.today()):
                    raise ValueError("Cannot access data for future dates")
                break
            except ValueError as ve:
                if str(ve) == "Start date must be before or equal to the end date":
                    print("Error: Start date must be before or equal to the end date")
                elif str(ve) == "Cannot access data for future dates":
                    print("Error: Cannot access data for future dates")
                else:
                    print("Error: The start and/or end date is invalid. Please make sure they are in the format MM/DD/YY or YYYY-MM-DD")
                start_date = input("Start date: ")
                end_date = input("End date: ")
        return start_date_obj, end_date_obj

    def get_data_from_range(self, pws_name: str, start_date: str, end_date: str, step=1, features=['Precip. Rate.', 'Precip. Accum.']):
        
        start_dt, end_dt = self.__check_dates(start_date, end_date)
        delta = timedelta(days=step)
        
        output_df = pd.DataFrame(columns = ["Datetime"] + features)
        
        curr_dt = start_dt
        while curr_dt <= end_dt:
            df = self.get_daily_data(pws_name, curr_dt.date())
            output_df = pd.concat([output_df, df], axis=0)
            #print(df.head())
            curr_dt += delta
        #print(output_df)
        output_df.to_csv('data/wunderground/' + pws_name + '.csv', index=False)

    def get_all_pws_data(self, start_date, end_date):
        for pws in self.pws_set:
            stationName = pws[1]
            self.get_data_from_range(stationName, start_date, end_date)


if __name__ == "__main__":
    s = Scraper()
    #dt = datetime(2022, 3, 1)
    #s.get_daily_data("KNYNEWYO1348", dt)
    #s.get_data_from_range("KNYNEWYO1348", "4/22/2023", "4/24/2023")
    s.get_all_pws_data("09/01/2022", "09/30/2022")
