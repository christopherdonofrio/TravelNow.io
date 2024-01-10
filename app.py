from helpers import find_hotel, get_coordinates, search_locations, airport_iata, search_flights, daysBetween, food_prices
from datetime import datetime
from flask import Flask, request, render_template



# Configure application
app = Flask(__name__)


#Declare make and model lists for autocomplete






@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        rawDepartureDate = request.form.get("departure")
        rawReturnDate = request.form.get("return")


        date_obj = datetime.strptime(rawDepartureDate, "%Y-%m-%d")

        date_obj2 = datetime.strptime(rawReturnDate, "%Y-%m-%d")



        #define variables
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        departureDate = date_obj.strftime("%Y-%m-%d")
        returnDate = date_obj2.strftime("%Y-%m-%d")
        budget = float(request.form.get("budget"))
        days = int(daysBetween(departureDate, returnDate))

        originSplit = origin.split(",")
        destinationSplit = destination.split(",")

        originCountry = originSplit[-1].strip()
        destinationCountry = destinationSplit[-1].strip()

        originCity = originSplit[0].strip()
        destinationCity = destinationSplit[0].strip()

        originLat = get_coordinates(originCity)[0]
        originLong = get_coordinates(originCity)[1]

        destinationLat = get_coordinates(destinationCity)[0]
        destinationLong = get_coordinates(destinationCity)[1]

        """
        current Variables

        origin
        destination
        departureDate
        returnDate
        budget
        originCountry
        destinationCountry
        originCity
        destinationCity

        """
        lo = int(search_locations(destinationCity))


        hotelData = find_hotel(departureDate, returnDate, lo)

        originIata = airport_iata(originLat, originLong)
        destinationIata = airport_iata(destinationLat, destinationLong)


        hotelData = find_hotel(departureDate, returnDate, lo)
        flightData = {}
        flightData['departureOrigin'] = "skuh"
        flightData['departureDest'] = "ERROR"
        flightData['price'] = 0.0 
        #flightData = search_flights(originIata, destinationIata, departureDate, returnDate)


        foodAndTransport = food_prices(destinationCity, destinationCountry)
        foodPerDay = round(foodAndTransport[0], 2)
        transportationPerDay = round(foodAndTransport[1], 2)


        #Budget Calculations
        initialBudget = budget
        budget = budget - round(float(flightData['price']), 2)
        budget = budget - hotelData[15]
        budget = budget - round((foodPerDay * days), 2)
        budget = round((budget - round((transportationPerDay * days), 2)), 2)



        expenses = [round(float(flightData['price']), 2), round(hotelData[15], 2), round((foodPerDay * days), 2), (transportationPerDay * days)]

        if budget < 0:
            moneyNeeded = abs(budget)
            congrats = "Sorry."
            message = "Unfortunately, you cannot afford this trip yet. Keep saving and once you have another $" + str(moneyNeeded) + ", you will be able to visit " + destinationCity + "!"
        elif budget < 300:
            congrats = "Congratulations!"
            message = "You can afford to visit " + destinationCity + ", but it's going to be tight. Your entertainment is going to have to be free, or very very cheap because you only have $" + str(budget) + " of flexible spending."
        else:
            congrats = "Congratulations!"

            message = "You can afford to visit " + destinationCity + "! You will have $" + str(budget) + " for entertainment and other flexible spending. Have fun!"








        return render_template("results.html", flightData=flightData, hotelData=hotelData, originIata=originIata, destinationIata=destinationIata, budget=budget, originCity=originCity, destinationCity=destinationCity, message=message, congrats=congrats, foodPerDay=foodPerDay, transportationPerDay=transportationPerDay, initialBudget=initialBudget, expenses=expenses)








    else:
        return render_template("index.html")
