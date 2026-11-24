"""
clear_treks.py

One-time helper script to wipe ALL treks and bookings from the database.
Useful during development/testing when you want a clean slate.

Does NOT touch Users (Admin, Staff, Trekkers) -- only clears Trek and Booking data.

Run from your project folder (venv activated):

    python clear_treks.py

You will be asked to confirm before anything is deleted.
"""

from app import app, db, Trek, Booking


def clear_treks_and_bookings():
    with app.app_context():
        booking_count = Booking.query.count()
        trek_count = Trek.query.count()

        print(f"This will permanently delete {trek_count} trek(s) and {booking_count} booking(s).")
        confirm = input("Type YES to confirm: ")

        if confirm.strip() != 'YES':
            print("Cancelled. Nothing was deleted.")
            return

        Booking.query.delete()
        Trek.query.delete()
        db.session.commit()

        print(f"Done. Deleted {trek_count} trek(s) and {booking_count} booking(s).")


if __name__ == '__main__':
    clear_treks_and_bookings()
