from flask import jsonify
from app.extensions import db
from app.models.bus import Bus
from app.models.route import Route  # Assuming you have a Route model

class CustomerService:
    @staticmethod
    def book_seat(data):
        try:
            bus = Bus.query.get(data['bus_id'])
            if not bus:
                return jsonify({"error": "Bus not found"}), 404

            seat = data['seat_number']
            if seat in bus.available_seats:
                bus.available_seats.remove(seat)
                db.session.commit()
                return jsonify({"message": f"Seat {seat} booked successfully."}), 200
            return jsonify({"error": "Seat not available"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def cancel_booking(booking_id):
        try:
            return jsonify({"message": f"Booking {booking_id} canceled successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def view_available_seats(bus_id):
        try:
            bus = Bus.query.get(bus_id)
            if not bus:
                return jsonify({"error": "Bus not found"}), 404
            return jsonify({"available_seats": bus.available_seats}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def send_message(data):
        try:
            return jsonify({"message": "Message sent successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # New Method to Fetch All Buses Posted by Drivers
    @staticmethod
    def view_buses():
        try:
            buses = Bus.query.all()  # Fetch all buses from the database
            if not buses:
                return jsonify({"message": "No buses available"}), 404
            bus_list = [{"bus_number": bus.bus_number, "capacity": bus.capacity, "available_seats": bus.available_seats} for bus in buses]
            return jsonify({"buses": bus_list}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # New Method to Fetch All Routes Posted by Drivers
    @staticmethod
    def view_routes():
        try:
            routes = Route.query.all()  # Fetch all routes from the database
            if not routes:
                return jsonify({"message": "No routes available"}), 404
            route_list = [{"start_location": route.start_location, "destination": route.destination, "departure_time": route.departure_time} for route in routes]
            return jsonify({"routes": route_list}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
