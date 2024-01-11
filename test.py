from helpers import find_hotel, get_coordinates, search_locations, airport_iata, search_flights, daysBetween, food_prices
from datetime import datetime
from amadeus import Client, ResponseError



#functions to TEST
#get_coordinates(city):
#search_locations(destinationCity):
#find_hotel(checkInDate, checkOutDate, lo):
#airport_iata(lat, long):
#search_flights(originIata, destIata, departDate, retDate):
#daysBetween(firstDate, secondDate):
#food_prices(city, country):


print(get_coordinates("Athens"))
print(find_hotel("2024-04-04", "2024-04-09", search_locations("Athens")))
print(airport_iata(32, 34))
print(food_prices("Athens", "Greece"))


"""
amadeus = Client(client_id='5tSKDdKe29rqFDdjgs2EOMipQjC8zWmc', client_secret='toVxF0YiT5i4EisN')

try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-11-01',
        adults=1)
    print(response.data)
except ResponseError as error:
    print(error)
"""
