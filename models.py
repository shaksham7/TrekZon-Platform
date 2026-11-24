from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'admin', 'staff', or 'user'
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active' or 'blacklisted'
    is_approved = db.Column(db.Boolean, default=False)  # For admin approval, if needed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A user (trekker) can have many bookings
    bookings = db.relationship(
        'Booking',
        backref='user',
        lazy=True,
        foreign_keys='Booking.user_id'
    )

    # A staff member (role='staff') can be assigned to many treks
    assigned_treks = db.relationship(
        'Trek',
        backref='assigned_staff',
        lazy=True,
        foreign_keys='Trek.assigned_staff_id'
    )

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Trek(db.Model):
    __tablename__ = 'treks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # 'Easy', 'Moderate', 'Hard'
    duration_days = db.Column(db.Integer, nullable=False)  # Duration in days
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(
        db.String(20), nullable=False, default='Pending'
    )  # 'Pending', 'Approved', 'Open', 'Closed', 'Completed'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(300), nullable=True)  # optional; Admin can paste a link or static filename
    itinerary = db.Column(db.Text, nullable=True)  # full day-wise plan, pickup/drop, travel, and hotel details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A trek can have many bookings
    bookings = db.relationship('Booking', backref='trek', lazy=True)

    def __repr__(self):
        return f'<Trek {self.name} ({self.status})>'


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.String(20), nullable=False, default='Booked'
    )  # 'Booked', 'Cancelled', 'Completed'

    # Prevents the same user from booking the same trek more than once
    __table_args__ = (
        db.UniqueConstraint('user_id', 'trek_id', name='unique_user_trek_booking'),
    )

    def __repr__(self):
        return f'<Booking user={self.user_id} trek={self.trek_id} status={self.status}>'
