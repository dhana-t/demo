import requests
from datetime import datetime, timedelta
from datetime import date

testUrl = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"

def getResponse(url):
    try:
        response = requests.get(url)
        data = response.json()
        return data["list"]
    except Exception as e:
        return e

def getDate(url):
    try:
        timeData = getResponse(url)
        actDate = [timeData[i]['dt'] for i in range(0,len(timeData))]
        return actDate
    except Exception as e:
        print(e)

def generateDate(start_date,end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        date_array = [start + timedelta(days=x) for x in range(0, (end-start).days)]
        expdate = []
        for date_object in date_array:
            expdate.append((date_object.strftime("%Y-%m-%d")))
        return expdate
    except Exception as e:
        print(e)

def test_4daysData(url):
    try:
        date_data = getDate(url)
        expDate = generateDate('2019-03-27','2019-04-01')
        result = ""
        for i in date_data:
            timestamp = date.fromtimestamp(i)
            if str(timestamp) in expDate:
                result = "PASS: Contains 4 days of data"
            else:
                result = "FAIL: Doesn't contain 4 days of data"
        return result
    except Exception as e:
        print(e)

def test_description(url,wid,wdes):
    try:
        testData = getResponse(url)
        for i in range(0,len(testData)):
            if ((testData[i]['weather'][0]['id'] == wid) and (testData[i]['weather'][0]['description']==wdes)):
                result = "PASS: For weather id {} description is {}".format(wid,wdes)
        print(result)
    except Exception as e:
        print(e)

def strToDateTime(daeteInput):
    try:
        result = datetime.strptime(daeteInput, '%Y-%m-%d %H:%M:%S')
        return result
    except Exception as e:
        print(e)

def test_hourlyInterval(url):
    try:
        testData = getResponse(url)
        fail_time = []
        for i in range(0,len(testData)+1):
            if i != len(testData) and i != 95:
                time_diff = strToDateTime(testData[i]['dt_txt']) - strToDateTime(testData[i+1]['dt_txt'])
                time_mins= int(divmod(time_diff.total_seconds(),60)[0])
                if time_mins != -60:
                    fail_time.append(testData[i]['dt_txt'])
                    result = "FAIL"
                else:
                    result = "PASS"
            else:
                pass
        if result == "PASS":
            return "PASS: All Forecasts Are In Hourly Interval"
        else:
            return "FAIL: Forecasts Are Not In Hourly Interval And Dates Are {}".format(fail_time)
    except Exception as e:
        print(e)

def test_tempminmax(url):
    try:
        testData = getResponse(url)
        for i in range(0,len(testData)):
            actual_temp = testData[i]['main']['temp']
            temp_min = testData[i]['main']['temp_min']
            temp_max = testData[i]['main']['temp_max']
            if actual_temp < temp_min or actual_temp > temp_max:
                result = "FAIL: Temp {0} is less than min {1} or greater than max {2}".format(actual_temp,temp_min,temp_max)
            else:
                result = "PASS: Temp is not less than min or greater than max"
        print(result)
    except Exception as e:
        print(e)

if __name__=='__main__':
   print(test_4daysData(testUrl))
   test_description(testUrl,500,'light rain')
   test_description(testUrl,800,'clear sky')
   print(test_hourlyInterval(testUrl))
   test_tempminmax(testUrl)
