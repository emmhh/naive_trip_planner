import json
import random

# Define cities and their respective countries
cities = {
    "JFK": "USA",
    "LAX": "USA",
    "LHR": "UK",
    "NRT": "Japan",
    "SYD": "Australia"
}

# Define additional stop cities
additional_stops = [
    "ORD", "ATL", "DFW", "DEN", "CDG", "FRA", "HND", "DXB", "SIN", "AMS"
]

# Generate random flights data
flights = []
for from_city in cities.keys():
    for to_city in cities.keys():
        if from_city != to_city:
            for _ in range(5):
                # Combine main cities and additional stops for potential stops
                all_stops = list(cities.keys()) + additional_stops
                flight = {
                    "from":
                    from_city,
                    "to":
                    to_city,
                    "stops":
                    random.sample(all_stops,
                                  random.randint(0, 2)),  # random stops
                    "price":
                    round(random.uniform(100, 1500),
                          2),  # random price between 100 and 1500
                    "departure_time":
                    f"{random.randint(0, 23):02}:{random.randint(0, 59):02}",
                    "arrival_time":
                    f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"
                }
                flights.append(flight)

# Save flights to flights.json
with open('flights.json', 'w') as f:
    json.dump(flights, f, indent=2)

# Generate random hotels data
hotels = []
for city, country in cities.items():
    for _ in range(5):
        hotel = {
            "name":
            f"{random.choice(['Grand', 'Luxury', 'Comfort', 'Economy', 'Royal'])} Hotel {random.randint(1, 100)}",
            "address":
            f"{random.randint(100, 999)} {random.choice(['Main', 'Market', 'High', 'Low'])} Street, {city}, {country}",
            "stars":
            random.randint(1, 5),
            "rating":
            round(random.uniform(1, 10), 1),  # random rating between 1 and 10
            "amenities":
            random.sample([
                "Free Wi-Fi", "Swimming pool", "Fitness center", "Restaurant",
                "Bar", "Room service", "Spa", "Parking", "Airport shuttle",
                "Pet-friendly"
            ], random.randint(2, 6)),
            "price_per_night":
            round(random.uniform(50, 500),
                  2)  # random price per night between 50 and 500
        }
        hotels.append(hotel)

# Save hotels to hotels.json
with open('hotels.json', 'w') as f:
    json.dump(hotels, f, indent=2)

print(
    "Data generation complete. Check flights.json and hotels.json for generated data."
)
