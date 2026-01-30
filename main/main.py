from moviespage import MoviesPage
from loginpage import LoginPage
from database import init_db

def main():
    init_db()

    while True:
        print("\n🎬 BookMyShow Terminal")
        print("1. Movies Page (Admin)")
        print("2. Login Page (User)")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            movies = MoviesPage()
            while True:
                print("\n--- Movies Page ---")
                print("1. Add Movie")
                print("2. View Movies")
                print("3. Update Movie")
                print("4. Delete Movie")
                print("5. Back")

                ch = input("Choice: ")

                if ch == "1":
                    movies.add_movie(
                        input("Title: "),
                        input("Genre: "),
                        input("Theater: "),
                        input("Show Time: "),
                        float(input("Price: ")),
                        int(input("Total Seats: "))
                    )

                elif ch == "2":
                    movies.view_movies()

                elif ch == "3":
                    movies.view_movies()
                    mid = input("Movie ID to update: ")
                    movies.update_movie(mid)

                elif ch == "4":
                    movies.view_movies()
                    mid = input("Movie ID to delete: ")
                    movies.delete_movie(mid)

                elif ch == "5":
                    break

        elif choice == "2":
            login = LoginPage()
            while True:
                print("\n--- Login Page ---")
                print("1. Register")
                print("2. View Movies")
                print("3. Book Ticket")
                print("4. Cancel Booking")
                print("5. View My Bookings")
                print("6. Back")

                ch = input("Choice: ")

                if ch == "1":
                    login.register_user(input("ID: "), input("Name: "))
                elif ch == "2":
                    login.view_movies()
                elif ch == "3":
                    login.book_ticket()
                elif ch == "4":
                    login.cancel_booking()
                elif ch == "5":
                    login.view_my_bookings(input("Customer ID: "))
                elif ch == "6":
                    break

        elif choice == "3":
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
