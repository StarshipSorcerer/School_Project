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

# ---------- Connect to MySQL Server ----------
con = mysql.connector.connect(
    host="localhost",
    user="root",        # change to your MySQL username
    password="root"     # change to your MySQL password
)
cur = con.cursor()

# ---------- Auto-create Database & Tables ----------
cur.execute("CREATE DATABASE IF NOT EXISTS hotel")
cur.execute("USE hotel")

cur.execute("""
CREATE TABLE IF NOT EXISTS rooms(
    room_no INT PRIMARY KEY,
    room_type VARCHAR(20),
    price_per_night FLOAT,
    available BOOLEAN DEFAULT TRUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
    cust_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15),
    email VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_id INT,
    room_no INT,
    check_in DATE,
    check_out DATE,
    total_amount FLOAT,
    FOREIGN KEY (cust_id) REFERENCES customers(cust_id),
    FOREIGN KEY (room_no) REFERENCES rooms(room_no)
)
""")
con.commit()

# ---------- Functions ----------

def add_room():
    room_no = int(input("Enter room number: "))
    room_type = input("Enter room type (Single/Double/Deluxe): ")
    price = float(input("Enter price per night: "))

    cur.execute("INSERT INTO rooms VALUES (%s, %s, %s, TRUE)", (room_no, room_type, price))
    con.commit()
    print("Room added successfully!\n")

def view_rooms():
    cur.execute("SELECT * FROM rooms")
    data = cur.fetchall()
    if not data:
        print("No rooms available.\n")
        return
    print("\nRoom No | Type | Price | Available")
    print("-----------------------------------")
    for r in data:
        status = "Yes" if r[3] else "No"
        print(f"{r[0]:7} | {r[1]:6} | {r[2]:6} | {status}")
    print()

def add_customer():
    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email: ")
    cur.execute("INSERT INTO customers(name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
    con.commit()
    print("Customer added successfully!\n")

def view_customers():
    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()
    if not data:
        print("No customers found.\n")
        return
    print("\nCust ID | Name | Phone | Email")
    print("------------------------------------")
    for c in data:
        print(f"{c[0]:7} | {c[1]:10} | {c[2]:10} | {c[3]}")
    print()

def book_room():
    view_rooms()
    room_no = int(input("Enter room number to book: "))
    cur.execute("SELECT available, price_per_night FROM rooms WHERE room_no=%s", (room_no,))
    room = cur.fetchone()
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

    cur.execute("""
        INSERT INTO bookings(cust_id, room_no, check_in, check_out, total_amount)
        VALUES (%s, %s, %s, %s, %s)
    """, (cust_id, room_no, check_in, check_out, total))
    cur.execute("UPDATE rooms SET available=FALSE WHERE room_no=%s", (room_no,))
    con.commit()
    print(f"Room booked successfully! Total = ₹{total}\n")

def view_bookings():
    cur.execute("""
        SELECT b.booking_id, c.name, b.room_no, b.check_in, b.check_out, b.total_amount
        FROM bookings b
        JOIN customers c ON b.cust_id = c.cust_id
    """)
    data = cur.fetchall()
    if not data:
        print("No bookings found.\n")
        return
    print("\nBooking ID | Customer | Room | Check-In | Check-Out | Total")
    print("---------------------------------------------------------------")
    for b in data:
        print(f"{b[0]:10} | {b[1]:10} | {b[2]:4} | {b[3]} | {b[4]} | ₹{b[5]}")
    print()

def checkout():
    booking_id = int(input("Enter booking ID to checkout: "))
    cur.execute("SELECT room_no, total_amount FROM bookings WHERE booking_id=%s", (booking_id,))
    data = cur.fetchone()
    if not data:
        print("Booking not found.\n")
        return
    room_no, total = data
    print(f"Total bill: ₹{total}")
    cur.execute("UPDATE rooms SET available=TRUE WHERE room_no=%s", (room_no,))
    con.commit()
    print("Checkout complete. Room is now available.\n")

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
    choice = input("\nEnter your choice: ")

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
        print("Goodbye! All data saved in MySQL (localhost).")
        break
    else:
        print("Invalid choice, try again.\n")

cur.close()
con.close()