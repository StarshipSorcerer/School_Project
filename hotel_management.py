"""
Hotel Management System
-------------------------------------------
Class 12 Project (Python + MySQL)

Features:
1. Add Room
2. View Rooms
3. Add Customer
4. View Customers
5. Book Room (Check-in)
6. View Bookings
7. Checkout
8. Exit
"""

import mysql.connector
from datetime import date, timedelta

# ---------- Connect to MySQL on localhost ----------
con = mysql.connector.connect(
    host="localhost",
    user="root",          # your MySQL username
    password="root",      # your MySQL password (change if needed)
    database="hotel"
)
cursor = con.cursor()

# ---------- Features ----------

def add_room():
    room_no = int(input("Enter room number: "))
    room_type = input("Enter room type (Single/Double/Deluxe): ")
    price = float(input("Enter price per night: "))
    query = "INSERT INTO rooms VALUES (%s, %s, %s, TRUE)"
    cursor.execute(query, (room_no, room_type, price))
    con.commit()
    print("Room added successfully!\n")

def view_rooms():
    cursor.execute("SELECT * FROM rooms")
    data = cursor.fetchall()
    if not data:
        print("No rooms available.\n")
        return
    print("\nRoom No | Type | Price | Available")
    print("-----------------------------------")
    for row in data:
        status = "Yes" if row[3] else "No"
        print(f"{row[0]:7} | {row[1]:6} | {row[2]:6} | {status}")
    print()

def add_customer():
    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    query = "INSERT INTO customers(name, phone, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, phone, email))
    con.commit()
    print("Customer added successfully!\n")

def view_customers():
    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    if not data:
        print("No customers found.\n")
        return
    print("\nCust ID | Name | Phone | Email")
    print("------------------------------------")
    for row in data:
        print(f"{row[0]:7} | {row[1]:10} | {row[2]:10} | {row[3]}")
    print()

def book_room():
    view_rooms()
    room_no = int(input("Enter room number to book: "))
    cursor.execute("SELECT available, price_per_night FROM rooms WHERE room_no=%s", (room_no,))
    room = cursor.fetchone()
    if not room:
        print("Room not found.\n")
        return
    if not room[0]:
        print("Room is not available.\n")
        return

    view_customers()
    cust_id = int(input("Enter customer ID: "))
    nights = int(input("Enter number of nights: "))
    check_in = date.today()
    check_out = check_in + timedelta(days=nights)
    total = room[1] * nights

    query = "INSERT INTO bookings(cust_id, room_no, check_in, check_out, total_amount) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (cust_id, room_no, check_in, check_out, total))
    cursor.execute("UPDATE rooms SET available=FALSE WHERE room_no=%s", (room_no,))
    con.commit()
    print(f"Room booked successfully! Total Amount = ₹{total}\n")

def checkout():
    booking_id = int(input("Enter booking ID to checkout: "))
    cursor.execute("SELECT room_no, total_amount FROM bookings WHERE booking_id=%s", (booking_id,))
    data = cursor.fetchone()
    if not data:
        print("Booking not found.\n")
        return
    room_no, total = data
    print(f"Total bill: ₹{total}")
    cursor.execute("UPDATE rooms SET available=TRUE WHERE room_no=%s", (room_no,))
    con.commit()
    print("Checkout completed. Room is now available.\n")

def view_bookings():
    cursor.execute("""
        SELECT b.booking_id, c.name, b.room_no, b.check_in, b.check_out, b.total_amount
        FROM bookings b JOIN customers c ON b.cust_id = c.cust_id
    """)
    data = cursor.fetchall()
    if not data:
        print("No bookings found.\n")
        return
    print("\nBooking ID | Customer | Room | Check-In | Check-Out | Total")
    print("---------------------------------------------------------------")
    for row in data:
        print(f"{row[0]:10} | {row[1]:10} | {row[2]:4} | {row[3]} | {row[4]} | ₹{row[5]}")
    print()

# ---------- Main Menu ----------
while True:
    print("""
========= HOTEL MANAGEMENT =========
1. Add Room
2. View Rooms
3. Add Customer
4. View Customers
5. Book Room (Check-in)
6. View Bookings
7. Checkout
8. Exit
""")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_room()
    elif choice == "2":
        view_rooms()
    elif choice == "3":
        add_customer()
    elif choice == "4":
        view_customers()
    elif choice == "5":
        book_room()
    elif choice == "6":
        view_bookings()
    elif choice == "7":
        checkout()
    elif choice == "8":
        print("Goodbye! Data saved in MySQL (localhost).")
        break
    else:
        print("Invalid choice. Try again.\n")

# ---------- Close Connection ----------
cursor.close()
con.close()
