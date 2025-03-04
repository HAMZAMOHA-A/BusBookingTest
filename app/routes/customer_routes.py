from flask import Blueprint, request, jsonify
from app.services.customer_service import CustomerService

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/book_seat', methods=['POST'])
def book_seat():
    data = request.get_json()
    if not data or 'bus_id' not in data or 'seat_number' not in data:
        return jsonify({"error": "Invalid input. Bus ID and Seat Number are required."}), 400
    return CustomerService.book_seat(data)

@customer_bp.route('/cancel_booking/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    if not booking_id:
        return jsonify({"error": "Booking ID is required."}), 400
    return CustomerService.cancel_booking(booking_id)

@customer_bp.route('/view_available_seats/<int:bus_id>', methods=['GET'])
def view_available_seats(bus_id):
    return CustomerService.view_available_seats(bus_id)

@customer_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message content is required."}), 400
    return CustomerService.send_message(data)

# New Route to View All Buses Posted by Drivers
@customer_bp.route('/view_buses', methods=['GET'])
def view_buses():
    return CustomerService.view_buses()

# New Route to View All Routes Posted by Drivers
@customer_bp.route('/view_routes', methods=['GET'])
def view_routes():
    return CustomerService.view_routes()
