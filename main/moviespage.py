from database import get_connection

class MoviesPage:

    def add_movie(self, title, genre, theater, show_time, price, seats):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies")
        count = cursor.fetchone()[0]
        movie_id = f"M{count+1:03d}"

        cursor.execute("""
            INSERT INTO movies VALUES (?,?,?,?,?,?,?,?)
        """, (movie_id, title, genre, theater, show_time, price, seats, seats))

        conn.commit()
        conn.close()
        print(f"✅ Movie added (ID: {movie_id})")

    def view_movies(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        conn.close()

        if not movies:
            print("❌ No movies found")
            return

        for m in movies:
            print(f"{m['id']} | {m['title']} | ₹{m['price']} | Seats {m['available_seats']}")

    def update_movie(self, movie_id):
        conn = get_connection()
        cursor = conn.cursor()

        print("1. Update Title")
        print("2. Update Price")
        choice = input("Choice: ")

        if choice == "1":
            title = input("New Title: ")
            cursor.execute("UPDATE movies SET title=? WHERE id=?", (title, movie_id))
        elif choice == "2":
            price = float(input("New Price: "))
            cursor.execute("UPDATE movies SET price=? WHERE id=?", (price, movie_id))
        else:
            print("❌ Invalid option")
            conn.close()
            return

        conn.commit()
        conn.close()
        print("✅ Movie updated")

    def delete_movie(self, movie_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        conn.commit()
        conn.close()
        print("🗑️ Movie deleted")
