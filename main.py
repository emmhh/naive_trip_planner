from flask import Flask, request, jsonify, send_from_directory
import json
from collections import OrderedDict

app = Flask(__name__)


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value


# Load data from JSON files
with open('flights.json', 'r') as f:
    flights = json.load(f)
with open('hotels.json', 'r') as f:
    hotels = json.load(f)

# LRU Cache for searchBestTrip results
cache = LRUCache(capacity=10)

# Index flights by origin and destination
flight_index = {}
for flight in flights:
    key = (flight['from'], flight['to'])
    if key not in flight_index:
        flight_index[key] = []
    flight_index[key].append(flight)

# Index hotels by city
hotel_index = {}
for hotel in hotels:
    city = hotel['address'].split(', ')[1]
    if city not in hotel_index:
        hotel_index[city] = []
    hotel_index[city].append(hotel)


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


# High Cost/query + time consuming -> minimize call to optimize.
@app.route('/getFlights', methods=['GET'])
def get_flights():
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    if not from_city or not to_city:
        return jsonify({"error": "Missing required parameters"}), 400

    available_flights = [
        flight for flight in flights
        if flight['from'] == from_city and flight['to'] == to_city
    ]
    return jsonify(available_flights)


# time consuming, minimize call
# input: destination
@app.route('/getHotels', methods=['GET'])
def get_hotels():
    destination = request.args.get('destination')
    if not destination:
        return jsonify({"error": "Missing required parameter"}), 400

    available_hotels = [
        hotel for hotel in hotels
        if hotel['address'].split(', ')[1] == destination
    ]
    return jsonify(available_hotels)


@app.route('/searchBestTrip', methods=['GET'])
def search_best_trip():
    origin = request.args.get('origin')
    budget = float(request.args.get('budget'))
    nights = int(request.args.get('nights'))

    if not origin or not budget or not nights:
        return jsonify({"error": "Missing required parameters"}), 400

    cache_key = (origin, budget)
    cached_result = cache.get(cache_key)

    if cached_result:
        # Adjust total cost for extra nights and filter out trips exceeding budget
        adjusted_trips = []
        for trip in cached_result:
            trip['total_cost'] += trip['hotel']['price_per_night'] * (
                nights - trip['nights'])
            trip['nights'] = nights
            if trip['total_cost'] <= budget:
                adjusted_trips.append(trip)
        if adjusted_trips:
            return jsonify(adjusted_trips)

    best_trips = []
    for outbound_flight in flights:
        if outbound_flight['from'] == origin:
            return_flights = flight_index.get((outbound_flight['to'], origin),
                                              [])
            for return_flight in return_flights:
                destination_hotels = hotel_index.get(outbound_flight['to'], [])
                for hotel in destination_hotels:
                    total_cost = (outbound_flight['price'] +
                                  return_flight['price'] +
                                  (hotel['price_per_night'] * nights))
                    if total_cost <= budget:
                        best_trips.append({
                            "total_cost":
                            total_cost,
                            "outbound_flight":
                            outbound_flight,
                            "return_flight":
                            return_flight,
                            "total_stops":
                            len(outbound_flight['stops']) +
                            len(return_flight['stops']),
                            "hotel":
                            hotel,
                            "stars":
                            hotel['stars'],
                            "hotel_rating":
                            hotel['rating'],
                            "nights":
                            nights
                        })

    # Sort trips by total cost, hotel rating, and number of stops
    best_trips = sorted(
        best_trips,
        key=lambda x:
        (-x['hotel_rating'], -x['stars'], x['total_cost'], x['total_stops']))

    if not best_trips:
        return jsonify({"message":
                        "No trips found within the given budget"}), 200

    # Store the result in the cache
    cache.put(cache_key, best_trips)

    return jsonify(best_trips)


if __name__ == '__main__':
    app.run(debug=True)
