# TravelNow
#### Video Demo:  <https://youtu.be/UmuyEDhqdzE>
#### Description:
A web based application that takes a users origin location, destination location, departure date,
return date, and budget to estimate the price of a vacation to the destination.

####Tips for avoiding errors
I am using free API subscriptions, so there are request limits that may prevent results from appearing. The maximum usage of the website is 10 times per hour
When answering the form, try to choose known cities in populated countries, smaller ones don't always have the necessary data
In the autofill section of the form, leave the location as is (don't alter the auto-filled text)
I haven't optimized the site for mobile devices, so it looks better on a computer


##### helpers.py


First, the html form takes the users origin and destination, and uses a google API to convert the cities into latititude
and longitude. This is done under the method get_coordinates. These values are used to input into another method called
airport_icao, which find the icao code (airport identifier value) of the airport closest to origin, and another for airport
closest to destination. For some reason, all the real time flight APIs only took iata codes as a parameter, which is a
different form of identification than icao. I tried to find an api where I could input a latitude and longitude and return
an iata code, but I couldn't, so I had to make another method called icao_to_iata which contacts an airport database and finds
the corresponding iata to icao. The search_flights method takes these converted iata codes, finds a connecting flight, and
returns the price and time(s) of flights. This is through the Amadeus API, which has real time flight data. For the hotel data
I used an API which searched through booking.com to find the cheapest hotels in an area. To do this, I first wrote the
search_locations method. This method takes a city and returns the corresponding id for that city, as per booking.com's data.
Then the find_hotel method used that location id to find hotels, storing the hotel name, price, picture url, url, etc.
Lastly, the food_prices method uses an API to contact a database that stores info on the price of living in certain areas.
I found the price of an inexpensive meal and multiplied it by 3 to find food per day price. For transportation, I found train
tickets and assumed someone would be taking at most 5 one way rides a day, to be on the safer side.

##### app.py
This is the main logic of the website. It uses flask to create the server, and takes the data inputted into the form on the homepage, then runs
all the previously described methods to find all the necessary data for the "results" page. If the method of the form is
"POST", it will send the form and present the results page, and if the method is "GET" it returns the index page.

##### index.html
This page has the main heading as well as the form for all the user input of the website. I went with a minimalistic theme
and a type writer style font. I like this font because it has a techy style that fit this project and this course

##### results.html
This page displays all the data that is returned in app.py. It uses jinja to present the variables which are formatted
and spread out by categories flight, hotel, food and transportation, budget, and conclusion. One error I was having
was that if the user inputs a destination with no information on booking.com, the flight database, or anything else,
the page would crash. To fix this, in one of my methods I set a variable that would store a value if there was an error.
Then, on results.html, I used a jinja if statement to determine the value of this variable, and if there was an error,
it would present a blank page with a message indicating the error. This is much friendlier to work with than an
"internal server error" message.


##### design flaws and decisions
One of the main things I debated was whether to use real time data or just find current data. For example, finding
a csv of flights and then referencing those numbers. I quickly realized this would make the site unusable in the
future, and I wanted to create an tool that was actually helpful. I also debated whether I should write the algorithms
to stretch the budget of the user, for example a higher budget equals more expensive flight, hotel, etc. I decided
against it because I realized people have different priorities. Some may want a nicer hotel, while others want
to indulge on food. Because of this, I thought the cheapest option was the best, as you can always decide to spend
more, but is harder to spend less (especially for those on an already tight budget).


