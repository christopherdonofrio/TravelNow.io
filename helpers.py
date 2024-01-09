import requests
from amadeus import Client, ResponseError
from datetime import datetime, timedelta


amadeus = Client(client_id='5tSKDdKe29rqFDdjgs2EOMipQjC8zWmc', client_secret='toVxF0YiT5i4EisN')





def get_coordinates(city):

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": city,
        "key": "AIzaSyCXqmMt03kHM4v_iSiC4pG6cWejjWbVhaA"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    coords = []



    if data['status'] == 'OK':
        results = data['results']
        if results:
            # Extract latitude and longitude from the first result
            location = results[0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            coords.append(latitude)
            coords.append(longitude)
            return coords


    return None




def search_locations(destinationCity):

    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

    querystring = {"name":destinationCity,"locale":"en-us"}

    headers = {
        "X-RapidAPI-Key": "a09a1febc0msh52d994e4a7504e3p1458c9jsnbd5fffa51e82",
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    response_json = response.json()

    if response_json:
        first_dest_id = response_json[0]['dest_id']
        return first_dest_id







def find_hotel(checkInDate, checkOutDate, lo):


    formatted_date = datetime.strptime(checkInDate, "%Y-%m-%d")  # Convert string to datetime object
    checkInDate = formatted_date + timedelta(days=1)  # Add one day to the date

    checkInDate = checkInDate.strftime("%Y-%m-%d")  # Convert datetime object back to string

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    querystring = {"checkin_date":checkInDate,"dest_type":"city","units":"imperial","checkout_date":checkOutDate,"adults_number":"1","order_by":"price","dest_id":lo,"filter_by_currency":"USD","locale":"en-gb","room_number":"1"}

    headers = {
        "X-RapidAPI-Key": "a09a1febc0msh52d994e4a7504e3p1458c9jsnbd5fffa51e82",
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    hotelData = []


    try:

        response_raw = requests.get(url, headers=headers, params=querystring)

        response = response_raw.json()


        days = int(daysBetween(checkInDate, checkOutDate))





        if response:

            total = 0

            i = 0
            x = 0




            while x < 3:


                if response['result'][i]['hotel_name']:
                    hotelData.append(response['result'][i]['hotel_name'])
                    hotelData.append(round((response['result'][i]['min_total_price'] / days), 2))
                    total += (response)['result'][i]['min_total_price']
                    hotelData.append((response)['result'][i]['review_score'])
                    hotelData.append((response)['result'][i]['url'])
                    hotelData.append((response)['result'][i]['max_1440_photo_url'])
                    x = x + 1
                i = i + 1




            average = round(float(total / 3), 2)
            hotelData.append(average)

            return hotelData
    except:
        x = 0
        i = 0

        while x < 3:
            hotelData.append("Name Not Found")
            hotelData.append(0.0)
            hotelData.append(0.0)
            hotelData.append("about:blank")
            hotelData.append("https://placehold.co/600x400/png")
            x = x + 1

        hotelData.append(0.0)
        return hotelData





def airport_iata(lat, long):
    url = "https://airlabs.co/api/v9/nearby"

    querystring = {"api_key": "5116d24e-8cb5-4138-987a-9476e954244f",
                   "lat":lat,
                   "lng":long,
                   "distance": 500
                   }


    response = requests.get(url, params=querystring)
    data = response.json()
    airports = data["response"]["airports"]
    sorted_airports = sorted(airports, key=lambda x: x["popularity"], reverse=True)
    return sorted_airports[0]["iata_code"]






def search_flights(originIata, destIata, departDate, retDate):


    try:
        response = amadeus.shopping.flight_offers_search.get(
        originLocationCode=originIata,
        destinationLocationCode=destIata,
        departureDate=departDate,
        returnDate=retDate,
        adults=1)
        
        
        filter_data = response.data



        if filter_data is not None:


            date_string = filter_data[0]['itineraries'][0]['segments'][0]['departure']['at']
            datetime_obj = datetime.fromisoformat(date_string)
            formatted_date = datetime_obj.strftime("%B %d, %Y")
            formatted_time = datetime_obj.strftime("%I:%M %p")

        

            date_string2 = filter_data[0]['itineraries'][1]['segments'][0]['departure']['at']
            datetime_obj2 = datetime.fromisoformat(date_string2)
            formatted_date2 = datetime_obj2.strftime("%B %d, %Y")
            formatted_time2 = datetime_obj2.strftime("%I:%M %p")

        


            departureOrigin = formatted_time + " on " + formatted_date


            departureDest = formatted_time2 + " on " + formatted_date2





            flightInfo['departureOrigin'] = departureOrigin
            flightInfo['departureDest'] = departureDest
            flightInfo['price'] = filter_data[0]['price']['grandTotal']



        else:

            flightInfo['departureOrigin'] = "skuh"
            flightInfo['departureDest'] = "ERROR"
            flightInfo['price'] = 0.0

        
        return flightInfo
        
    except ResponseError as e:
        print(f"Amadeus API asdkojklasdfalsd: {e}")
        flightInfo = {}

        flightInfo['departureOrigin'] = "ERROR"
        flightInfo['departureDest'] = "ERROR"
        flightInfo['price'] = 0.0

        return flightInfo
 







def daysBetween(firstDate, secondDate):
    date_format = "%Y-%m-%d"

    start_datetime = datetime.strptime(firstDate, date_format)
    end_datetime = datetime.strptime(secondDate, date_format)

    delta = end_datetime - start_datetime

    num_days = delta.days

    return num_days

def food_prices(city, country):

    finalData = []


    try:

        if country == "USA":
            country = "United States"
        elif country == "UK":
            country = "United Kingdom"

        url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"

        querystring = {"city_name":city,"country_name":country}

        headers = {
            "X-RapidAPI-Key": "a09a1febc0msh52d994e4a7504e3p1458c9jsnbd5fffa51e82",
            "X-RapidAPI-Host": "cost-of-living-and-prices.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()

        if not data:
            foodPerDay = 0.0
            transportationPerDay = 0.0
        else:
            foodPerDay = round((float(data['prices'][35]['usd']['avg']) * 3), 2)
            transportationPerDay = round((float(data['prices'][42]['usd']['avg']) * 5), 2)





        finalData.append(foodPerDay)
        finalData.append(transportationPerDay)

    except:

        finalData.append(0.0)
        finalData.append(0.0)


    return finalData


