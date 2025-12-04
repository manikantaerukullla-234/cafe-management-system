import sqlite3
from datetime import datetime

# -------------------------------
# DATABASE SETUP
# -------------------------------

conn = sqlite3.connect("cafe.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    item_name TEXT,
    qty INTEGER,
    price REAL,
    time TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    total REAL,
    timestamp TEXT
)
""")
conn.commit()


# -------------------------------
# MENU MANAGEMENT
# -------------------------------

def add_menu_item():
    name = input("Enter item name: ")
    price = float(input("Enter price: "))
    cur.execute("INSERT INTO menu (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    print("✔ Item added successfully!\n")


def view_menu():
    cur.execute("SELECT * FROM menu")
    menu = cur.fetchall()
    print("\n------ Café Menu ------")
    for item in menu:
        print(f"{item[0]}. {item[1]} - ₹{item[2]}")
    print("-----------------------\n")


def delete_menu_item():
    view_menu()
    item_id = int(input("Enter ID of item to delete: "))
    cur.execute("DELETE FROM menu WHERE id=?", (item_id,))
    conn.commit()
    print("✔ Item deleted.\n")


# -------------------------------
# ORDER MANAGEMENT
# -------------------------------

def take_order():
    order_id = int(datetime.now().timestamp())  # unique ID
    total = 0
    order_items = []

    while True:
        view_menu()
        item_id = int(input("Enter item ID to order (0 to finish): "))
        if item_id == 0:
            break
        
        qty = int(input("Enter quantity: "))
        
        cur.execute("SELECT name, price FROM menu WHERE id=?", (item_id,))
        item = cur.fetchone()

        if item:
            name, price = item
            amount = qty * price
            total += amount

            cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                        (order_id, name, qty, price, str(datetime.now())))
            conn.commit()

            order_items.append((name, qty, price, amount))
            print(f"Added {qty} x {name}\n")
        else:
            print("Invalid item!")

    # Save bill
    cur.execute("INSERT INTO bills (order_id, total, timestamp) VALUES (?, ?, ?)",
                (order_id, total, str(datetime.now())))
    conn.commit()

    print("\n========== BILL ==========")
    for item in order_items:
        print(f"{item[0]}  x{item[1]}  = ₹{item[3]}")
    print("----------------------------")
    print(f"Total Bill Amount: ₹{total}")
    print("===========================\n")


# -------------------------------
# REPORTS
# -------------------------------

def view_all_orders():
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()

    print("\n------ All Orders ------")
    for r in rows:
        print(f"OrderID: {r[0]}, Item: {r[1]}, Qty: {r[2]}, Price: ₹{r[3]}, Time: {r[4]}")
    print("--------------------------\n")


def total_sales_today():
    today = datetime.now().date()
    cur.execute("SELECT total, timestamp FROM bills")
    rows = cur.fetchall()

    total = sum(r[0] for r in rows if str(today) in r[1])
    print(f"\nToday's Total Sales: ₹{total}\n")


# -------------------------------
# MAIN MENU UI
# -------------------------------

def main():
    while True:
        print("""
========= Café Management =========
1. Add Menu Item
2. View Menu
3. Delete Menu Item
4. Take Customer Order
5. View All Orders
6. View Today's Sales
7. Exit
-----------------------------------
""")
        choice = input("Enter choice: ")

        if choice == "1": add_menu_item()
        elif choice == "2": view_menu()
        elif choice == "3": delete_menu_item()
        elif choice == "4": take_order()
        elif choice == "5": view_all_orders()
        elif choice == "6": total_sales_today()
        elif choice == "7":
            print("Exiting system...")
            break
        else:
            print("Invalid choice!")

main()
