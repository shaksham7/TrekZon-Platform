import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Trek, Booking
from datetime import datetime, timedelta
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

def create_app():
    app = Flask(__name__)

    # --- Configuration ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-fallback-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///trekzon.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Initialize extensions ---
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'  # route name for login page, once created
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # --- Create tables + seed default Admin (runs once on startup) ---
    with app.app_context():
        db.create_all()
        seed_default_admin()

    return app


def seed_default_admin():
    """Creates a default Admin account if one doesn't already exist."""
    existing_admin = User.query.filter_by(role='admin').first()

    if not existing_admin:
        admin = User(
            username='admin',
            email='admin@trekzon.com',
            password=generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'change-me-now')),
            full_name='Default Admin',
            role='admin',
            status='active',
            is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Default Admin created -> username: admin | password: [set via ADMIN_PASSWORD env var]")
    else:
        print("Admin account already exists. Skipping seed.")


app = create_app()


# Booking timestamps are stored in UTC (good practice), but this app is India-only,
# so we convert to IST (UTC + 5:30) whenever a timestamp is shown to a user.
def to_ist(utc_dt):
    if utc_dt is None:
        return ''
    ist_dt = utc_dt + timedelta(hours=5, minutes=30)
    return ist_dt.strftime('%Y-%m-%d %H:%M') + ' IST'


app.jinja_env.filters['to_ist'] = to_ist


# --- Home route (public landing page, no login required) ---
@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/terms-conditions')
def terms_conditions():
    return render_template('terms_conditions.html')


@app.route('/')
def home():
    # Show a small preview of open treks with slots available, for anyone to see
    featured_treks = Trek.query.filter(
        Trek.status == 'Open', Trek.available_slots > 0
    ).limit(6).all()
    return render_template('home.html', treks=featured_treks, show_hero=True)


# --- Signup route (only for Trekkers/Users; Admin is pre-seeded, Staff added by Admin later) ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')

        # Check if username or email is already taken
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash('Username or email already exists. Please try a different one.', 'error')
            return redirect(url_for('signup'))

        new_user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=generate_password_hash(password),
            role='user',       # signup always creates a Trekker account
            status='active',
            is_approved=True
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# --- Login route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        next_page = request.form.get('next')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password.', 'error')
            return redirect(url_for('login'))

        if user.status == 'blacklisted':
            flash('Your account has been blocked. Contact the Admin.', 'error')
            return redirect(url_for('login'))

        login_user(user)

        # Admin and Staff always go straight to their own dashboard.
        # Trekkers get sent back to whatever page they came from (e.g. a trek they wanted to book),
        # if that page was passed in safely -- otherwise they go to their normal dashboard.
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'staff':
            return redirect(url_for('staff_dashboard'))
        else:
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('user_dashboard'))

    next_page = request.args.get('next', '')
    return render_template('login.html', next=next_page)


# --- Logout route ---
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


# --- Role-based dashboard routes ---
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    stats = {
        'total_treks': Trek.query.count(),
        'total_staff': User.query.filter_by(role='staff').count(),
        'total_trekkers': User.query.filter_by(role='user').count(),
        'total_bookings': Booking.query.count(),
    }
    return render_template('admin_dashboard.html', stats=stats)


# --- Admin: view and manage all users (Staff + Trekkers) ---
@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    search = request.args.get('search', '')
    query = User.query.filter(User.role != 'admin')  # Admin doesn't manage other admins here

    if search:
        query = query.filter(
            (User.username.contains(search)) | (User.full_name.contains(search))
        )

    users = query.all()
    return render_template('admin_users.html', users=users, search=search)


# --- Admin: activate / blacklist a user ---
@app.route('/admin/users/<int:user_id>/status', methods=['POST'])
@login_required
def admin_toggle_user_status(user_id):
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    user.status = 'blacklisted' if user.status == 'active' else 'active'
    db.session.commit()

    flash(f'{user.full_name} is now {user.status}.', 'success')
    return redirect(url_for('admin_users'))


# --- Admin: add a new Staff account (auto-generated password) ---
@app.route('/admin/staff/add', methods=['GET', 'POST'])
@login_required
def admin_add_staff():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        password = request.form.get('password', '').strip()

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash('Username or email already exists.', 'error')
            return redirect(url_for('admin_add_staff'))

        if len(password) < 6:
            flash('Temporary password must be at least 6 characters long.', 'error')
            return redirect(url_for('admin_add_staff'))

        new_staff = User(
            full_name=full_name,
            username=username,
            email=email,
            phone_number=phone_number,
            password=generate_password_hash(password),
            role='staff',
            status='active',
            is_approved=True
        )
        db.session.add(new_staff)
        db.session.commit()

        flash(f'Staff account created! Username: {username}. Share the temporary password you set with them directly.', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin_add_staff.html')


# --- Admin: view all treks ---
@app.route('/admin/treks')
@login_required
def admin_treks():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    treks = Trek.query.all()
    return render_template('admin_treks.html', treks=treks)


# --- Admin: add a new trek ---
@app.route('/admin/treks/add', methods=['GET', 'POST'])
@login_required
def admin_add_trek():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    staff_list = User.query.filter_by(role='staff').all()

    if request.method == 'POST':
        total_slots = int(request.form.get('total_slots'))
        assigned_staff_id = request.form.get('assigned_staff_id') or None

        new_trek = Trek(
            name=request.form.get('name'),
            location=request.form.get('location'),
            difficulty=request.form.get('difficulty'),
            duration_days=int(request.form.get('duration_days')),
            total_slots=total_slots,
            available_slots=total_slots,  # fully open when first created
            assigned_staff_id=assigned_staff_id,
            status='Pending',  # new treks start as Pending until Admin approves
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date(),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            altitude=request.form.get('altitude') or None,
            image_url=request.form.get('image_url') or None,
            itinerary=request.form.get('itinerary') or None
        )
        db.session.add(new_trek)
        db.session.commit()

        flash('Trek created successfully (status: Pending).', 'success')
        return redirect(url_for('admin_treks'))

    return render_template('admin_add_trek.html', staff_list=staff_list)


# --- Admin: edit an existing trek (including status changes) ---
@app.route('/admin/treks/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_trek(trek_id):
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    trek = Trek.query.get_or_404(trek_id)
    staff_list = User.query.filter_by(role='staff').all()

    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration_days = int(request.form.get('duration_days'))
        trek.status = request.form.get('status')
        trek.assigned_staff_id = request.form.get('assigned_staff_id') or None
        trek.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        trek.description = request.form.get('description')
        trek.price = float(request.form.get('price'))
        trek.altitude = request.form.get('altitude') or None
        trek.image_url = request.form.get('image_url') or None
        trek.itinerary = request.form.get('itinerary') or None

        # If total_slots changes, recalculate available_slots based on active bookings
        new_total = int(request.form.get('total_slots'))
        active_bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').count()
        trek.total_slots = new_total
        trek.available_slots = new_total - active_bookings

        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('admin_treks'))

    return render_template('admin_edit_trek.html', trek=trek, staff_list=staff_list)


# --- Admin: delete a trek (only allowed if it has no booking history) ---
@app.route('/admin/treks/<int:trek_id>/delete', methods=['POST'])
@login_required
def admin_delete_trek(trek_id):
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    trek = Trek.query.get_or_404(trek_id)

    # A trek that already has bookings (even cancelled ones) carries real history.
    # Deleting it would either crash (Booking.trek_id can't be NULL) or destroy
    # that history -- so we block it and guide the Admin to close/complete it instead.
    booking_count = Booking.query.filter_by(trek_id=trek.id).count()
    if booking_count > 0:
        flash(
            f'Cannot delete "{trek.name}" — it has {booking_count} booking(s) on record. '
            f'Set its status to Closed or Completed instead of deleting it.',
            'error'
        )
        return redirect(url_for('admin_treks'))

    db.session.delete(trek)
    db.session.commit()

    flash('Trek deleted.', 'success')
    return redirect(url_for('admin_treks'))


# --- Admin: view all bookings system-wide ---
@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if current_user.role != 'admin':
        flash('Access denied: Admins only.', 'error')
        return redirect(url_for('login'))

    bookings = Booking.query.all()
    return render_template('admin_bookings.html', bookings=bookings)


@app.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        flash('Access denied: Staff only.', 'error')
        return redirect(url_for('login'))

    assigned_treks = Trek.query.filter_by(assigned_staff_id=current_user.id).all()
    return render_template('staff_dashboard.html', treks=assigned_treks)


# --- Staff: change their own password ---
@app.route('/staff/change-password', methods=['GET', 'POST'])
@login_required
def staff_change_password():
    if current_user.role != 'staff':
        flash('Access denied: Staff only.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('staff_change_password'))

        if new_password != confirm_password:
            flash('New password and confirmation do not match.', 'error')
            return redirect(url_for('staff_change_password'))

        if len(new_password) < 6:
            flash('New password must be at least 6 characters long.', 'error')
            return redirect(url_for('staff_change_password'))

        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('Password changed successfully.', 'success')
        return redirect(url_for('staff_dashboard'))

    return render_template('staff_change_password.html')


# --- Staff: update the status of one of their assigned treks ---
# Staff can only move a trek forward: Open -> Closed (trek started) -> Completed
# Staff cannot set Pending/Approved -- those are Admin-only stages
@app.route('/staff/treks/<int:trek_id>/update-status', methods=['POST'])
@login_required
def staff_update_trek_status(trek_id):
    if current_user.role != 'staff':
        flash('Access denied: Staff only.', 'error')
        return redirect(url_for('login'))

    trek = Trek.query.get_or_404(trek_id)

    # Security check: staff can only modify treks assigned to them
    if trek.assigned_staff_id != current_user.id:
        flash('You are not assigned to this trek.', 'error')
        return redirect(url_for('staff_dashboard'))

    new_status = request.form.get('status')

    allowed_transitions = {
        'Open': ['Closed'],
        'Closed': ['Completed']
    }

    if trek.status not in allowed_transitions or new_status not in allowed_transitions.get(trek.status, []):
        flash(f'Cannot change status from {trek.status} to {new_status}.', 'error')
        return redirect(url_for('staff_dashboard'))

    trek.status = new_status
    db.session.commit()

    flash(f'Trek "{trek.name}" status updated to {new_status}.', 'success')
    return redirect(url_for('staff_dashboard'))


# --- Staff: view the roster of trekkers booked on one of their assigned treks ---
@app.route('/staff/treks/<int:trek_id>/bookings')
@login_required
def staff_trek_bookings(trek_id):
    if current_user.role != 'staff':
        flash('Access denied: Staff only.', 'error')
        return redirect(url_for('login'))

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != current_user.id:
        flash('You are not assigned to this trek.', 'error')
        return redirect(url_for('staff_dashboard'))

    bookings = Booking.query.filter_by(trek_id=trek.id, status='Booked').all()
    return render_template('staff_trek_bookings.html', trek=trek, bookings=bookings)


# --- PUBLIC: browse/search/filter treks without needing to log in ---
@app.route('/explore')
def explore_treks():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    difficulty = request.args.get('difficulty', '')

    query = Trek.query.filter(Trek.status == 'Open', Trek.available_slots > 0)

    if search:
        query = query.filter(Trek.name.contains(search))
    if location:
        query = query.filter(Trek.location == location)
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()

    all_locations = [row[0] for row in db.session.query(Trek.location).distinct().all()]
    all_difficulties = [row[0] for row in db.session.query(Trek.difficulty).distinct().all()]

    # Only relevant if a trekker happens to be browsing this public page while logged in
    my_booked_trek_ids = set()
    if current_user.is_authenticated and current_user.role == 'user':
        my_booked_trek_ids = {
            b.trek_id for b in Booking.query.filter_by(user_id=current_user.id, status='Booked').all()
        }

    return render_template(
        'explore_treks.html',
        treks=treks,
        search=search,
        location=location,
        difficulty=difficulty,
        all_locations=all_locations,
        all_difficulties=all_difficulties,
        my_booked_trek_ids=my_booked_trek_ids
    )


# --- PUBLIC: trek detail page (clicking a tile anywhere on the site leads here) ---
@app.route('/trek/<int:trek_id>')
def trek_detail(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    already_booked = False
    if current_user.is_authenticated and current_user.role == 'user':
        already_booked = Booking.query.filter_by(
            user_id=current_user.id, trek_id=trek.id, status='Booked'
        ).first() is not None

    return render_template('trek_detail.html', trek=trek, already_booked=already_booked)


# --- PUBLIC: attempt to book a trek from the public explore page ---
# - Guest (not logged in)          -> sent to login, then bounced back here to finish booking
# - Logged in, but not a trekker   -> blocked with a clear message
# - Logged in trekker              -> books immediately using the same shared logic
@app.route('/explore/treks/<int:trek_id>/book', methods=['POST'])
def explore_book_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if not current_user.is_authenticated:
        flash('Please log in to book this trek.', 'error')
        return_url = url_for('explore_treks', _anchor=f'trek-{trek.id}')
        return redirect(url_for('login', next=return_url))

    if current_user.role != 'user':
        flash('Only trekker accounts can book treks.', 'error')
        return redirect(url_for('explore_treks'))

    success, message = attempt_booking(trek, current_user)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('explore_treks'))


@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        flash('Access denied: Trekkers only.', 'error')
        return redirect(url_for('login'))

    upcoming_count = Booking.query.filter_by(user_id=current_user.id, status='Booked').count()
    return render_template('user_dashboard.html', upcoming_count=upcoming_count)


# --- Trekker: browse/search/filter open treks ---
@app.route('/user/treks')
@login_required
def user_browse_treks():
    if current_user.role != 'user':
        flash('Access denied: Trekkers only.', 'error')
        return redirect(url_for('login'))

    search = request.args.get('search', '')
    location = request.args.get('location', '')
    difficulty = request.args.get('difficulty', '')

    # Trekkers should only ever see treks that are Open and still have free slots
    query = Trek.query.filter(Trek.status == 'Open', Trek.available_slots > 0)

    if search:
        query = query.filter(Trek.name.contains(search))
    if location:
        query = query.filter(Trek.location == location)
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()

    # For populating the filter dropdowns with distinct existing values
    all_locations = [row[0] for row in db.session.query(Trek.location).distinct().all()]
    all_difficulties = [row[0] for row in db.session.query(Trek.difficulty).distinct().all()]

    # Find which treks (of those shown) the current trekker has already booked,
    # so the template can disable the Book button instead of letting them hit an error
    my_booked_trek_ids = {
        b.trek_id for b in Booking.query.filter_by(user_id=current_user.id, status='Booked').all()
    }

    return render_template(
        'user_treks.html',
        treks=treks,
        search=search,
        location=location,
        difficulty=difficulty,
        all_locations=all_locations,
        all_difficulties=all_difficulties,
        my_booked_trek_ids=my_booked_trek_ids
    )


def attempt_booking(trek, user):
    """
    Shared booking logic. Returns (success: bool, message: str).
    Used by both the logged-in trekker booking route and the public booking route,
    so there is only one place where booking rules are enforced.
    """
    if trek.status != 'Open':
        return False, 'This trek is not currently open for booking.'

    # Check for an existing active booking FIRST, so the trekker gets an accurate
    # message even if the trek happens to be full (rather than a misleading "fully booked")
    existing = Booking.query.filter_by(user_id=user.id, trek_id=trek.id, status='Booked').first()
    if existing:
        return False, 'You have already booked this trek.'

    if trek.available_slots <= 0:
        return False, 'Sorry, this trek is fully booked.'

    try:
        new_booking = Booking(user_id=user.id, trek_id=trek.id, status='Booked')
        trek.available_slots -= 1
        db.session.add(new_booking)
        db.session.commit()
        return True, f'Trek "{trek.name}" booked successfully!'
    except IntegrityError:
        # Safety net: the unique constraint on (user_id, trek_id) catches any race condition
        db.session.rollback()
        return False, 'You have already booked this trek.'


# --- Trekker: book a trek (must already be logged in as a trekker) ---
@app.route('/user/treks/<int:trek_id>/book', methods=['POST'])
@login_required
def user_book_trek(trek_id):
    if current_user.role != 'user':
        flash('Access denied: Trekkers only.', 'error')
        return redirect(url_for('login'))

    trek = Trek.query.get_or_404(trek_id)
    success, message = attempt_booking(trek, current_user)
    flash(message, 'success' if success else 'error')

    return redirect(url_for('user_browse_treks'))


# --- Trekker: view own bookings ---
@app.route('/user/bookings')
@login_required
def user_bookings():
    if current_user.role != 'user':
        flash('Access denied: Trekkers only.', 'error')
        return redirect(url_for('login'))

    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('user_bookings.html', bookings=bookings)


# --- Trekker: cancel a booking (frees up the slot immediately) ---
@app.route('/user/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def user_cancel_booking(booking_id):
    if current_user.role != 'user':
        flash('Access denied: Trekkers only.', 'error')
        return redirect(url_for('login'))

    booking = Booking.query.get_or_404(booking_id)

    # Security check: trekkers can only cancel their own bookings
    if booking.user_id != current_user.id:
        flash('You cannot cancel a booking that is not yours.', 'error')
        return redirect(url_for('user_bookings'))

    if booking.status != 'Booked':
        flash('This booking cannot be cancelled.', 'error')
        return redirect(url_for('user_bookings'))

    booking.status = 'Cancelled'
    booking.trek.available_slots += 1  # slot reopens immediately for others
    db.session.commit()

    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('user_bookings'))


if __name__ == '__main__':
    app.run(debug=True)
