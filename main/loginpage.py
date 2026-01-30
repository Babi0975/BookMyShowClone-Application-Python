from database import get_connection

class LoginPage:
    def __init__(self):
        self.current_customer = None

    def register_user(self, cid, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (cid,))
        if cursor.fetchone():
            print(f"✅ Welcome back {name}!")
        else:
            cursor.execute('INSERT INTO customers VALUES (?,?)', (cid, name))
            conn.commit()
            print(f"✅ User '{name}' registered!")
        self.current_customer = cid
        conn.close()

    def view_movies(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movies WHERE available_seats > 0')
        movies = cursor.fetchall()
        conn.close()
        print("\n--- Available Movies ---")
        if not movies:
            print("❌ No movies available!")
            return
        for m in movies:
            print(f"ID: {m['id']} | {m['title']} | ₹{m['price']} | Seats: {m['available_seats']}")

    def book_ticket(self):
        if not self.current_customer:
            print("❌ Please register first!")
            return
        self.view_movies()
        try:
            movie_id = input("Movie ID: ")
            seats = int(input("Seats: "))
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
            movie = cursor.fetchone()
            if movie and movie['available_seats'] >= seats:
                cursor.execute('UPDATE movies SET available_seats = available_seats - ? WHERE id = ?', (seats, movie_id))
                total = seats * movie['price']
                cursor.execute('INSERT INTO bookings (customer_id, movie_id, seats, total_amount) VALUES (?,?,?,?)', 
                              (self.current_customer, movie_id, seats, total))
                conn.commit()
                print(f"✅ Booked {seats} seats for ₹{total}!")
            else:
                print("❌ Not available!")
            conn.close()
        except ValueError:
            print("❌ Enter valid numbers!")

    def cancel_booking(self):
        if not self.current_customer:
            print("❌ Please register first!")
            return
        self.view_my_bookings(self.current_customer)
        try:
            booking_id = int(input("Booking ID to cancel: "))
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT seats, movie_id FROM bookings WHERE id = ? AND customer_id = ?', 
                          (booking_id, self.current_customer))
            booking = cursor.fetchone()
            if booking:
                cursor.execute('UPDATE movies SET available_seats = available_seats + ? WHERE id = ?', 
                              (booking['seats'], booking['movie_id']))
                cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
                conn.commit()
                print("✅ Booking cancelled!")
            else:
                print("❌ Booking not found!")
            conn.close()
        except ValueError:
            print("❌ Invalid booking ID!")

    def view_my_bookings(self, customer_id): 
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT b.*, m.title FROM bookings b 
            JOIN movies m ON b.movie_id = m.id 
            WHERE b.customer_id = ? ORDER BY b.id DESC
        ''', (customer_id,))
        bookings = cursor.fetchall()
        conn.close()
        print(f"\n--- {customer_id}'s Bookings ---")
        if not bookings:
            print("❌ No bookings found.")
            return
        for b in bookings:
            print(f"ID: {b['id']} | Movie: {b['title']} | Seats: {b['seats']} | ₹{b['total_amount']}")
