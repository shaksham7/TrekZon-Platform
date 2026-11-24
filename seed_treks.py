"""
seed_treks.py

One-time script to bulk-add sample treks into the TrekZon database.
Run this ONCE from your project folder (with venv activated):

    python seed_treks.py

Safe to re-run: it skips any trek whose name already exists, so it
won't create duplicates if you run it more than once.

Trek-specific details (pickup points, travel routes, accommodation style,
day-wise plans, altitude) live in trek_details.py -- this keeps this file
focused on the seeding logic, and that file focused on content.
"""

from app import app, db, Trek
from datetime import datetime, timedelta
from trek_details import TREK_DETAILS, COMMON_INCLUSIONS, COMMON_EXCLUSIONS

# Maps difficulty names used in the old data to the ones this project uses
DIFFICULTY_MAP = {
    'Easy': 'Easy',
    'Moderate': 'Moderate',
    'Difficult': 'Hard',
}

# Maps each trek to its real photo in the images/ folder
IMAGE_MAP = {
    'Kedarnath Trek': 'images/kedarnath1.jpeg',
    'Kedarkantha Trek': 'images/kedarkantha1.jpeg',
    'Valley of Flowers Trek': 'images/valley_of_flowers1.jpeg',
    'Hampta Pass Trek': 'images/hampta_pass1.jpeg',
    'Roopkund Trek': 'images/roopkund1.jpeg',
    'Chadar Trek': 'images/chadar1.jpeg',
    'Kashmir Great Lakes Trek': 'images/kashmir1.jpeg',
    'Brahmatal Trek': 'images/brahmatal.jpg',
    'Triund Trek': 'images/triund.jpg',
    'Har Ki Dun Trek': 'images/har.jpg',
    'Pin Parvati Pass Trek': 'images/pin.jpg',
    'Markha Valley Trek': 'images/markha.jpg',
    'Sandakphu Trek': 'images/sandakphu.jpg',
    'Goechala Trek': 'images/goechala.jpg',
    'Bhrigu Lake Trek': 'images/bhrigu.jpg',
    'Dayara Bugyal Trek': 'images/dayara.jpg',
    'Rupin Pass Trek': 'images/rupin.jpg',
    'Tarsar Marsar Trek': 'images/tarsar.jpg',
    'Nag Tibba Trek': 'images/nag.jpg',
    'Stok Kangri Trek': 'images/stok.jpg',
    'Pindari Glacier Trek': 'images/pindari.jpg',
    'Annapurna Base Camp Trek': 'images/annapurna.jpg',
}

# Base data per trek: name, location, difficulty, starting date, slots, and price.
# Duration and end date are NOT set here -- they are derived automatically from
# the length of that trek's day_plan in trek_details.py, so the two can never
# fall out of sync with each other.
TREKS = [
    {'name': 'Kedarnath Trek', 'location': 'Kedarnath, Uttarakhand', 'difficulty': 'Difficult', 'start': '2026-09-10', 'max': 20, 'price': 8999},
    {'name': 'Brahmatal Trek', 'location': 'Brahmatal, Uttarakhand', 'difficulty': 'Moderate', 'start': '2026-12-20', 'max': 25, 'price': 6499},
    {'name': 'Roopkund Trek', 'location': 'Chamoli, Uttarakhand', 'difficulty': 'Difficult', 'start': '2026-09-05', 'max': 18, 'price': 11999},
    {'name': 'Valley of Flowers Trek', 'location': 'Chamoli, Uttarakhand', 'difficulty': 'Moderate', 'start': '2026-07-15', 'max': 25, 'price': 8499},
    {'name': 'Hampta Pass Trek', 'location': 'Kullu, Himachal Pradesh', 'difficulty': 'Moderate', 'start': '2026-08-10', 'max': 20, 'price': 7999},
    {'name': 'Kedarkantha Trek', 'location': 'Uttarkashi, Uttarakhand', 'difficulty': 'Easy', 'start': '2026-12-20', 'max': 30, 'price': 6999},
    {'name': 'Triund Trek', 'location': 'Dharamshala, Himachal Pradesh', 'difficulty': 'Easy', 'start': '2026-10-05', 'max': 35, 'price': 1999},
    {'name': 'Har Ki Dun Trek', 'location': 'Uttarkashi, Uttarakhand', 'difficulty': 'Moderate', 'start': '2026-09-18', 'max': 22, 'price': 8999},
    {'name': 'Pin Parvati Pass Trek', 'location': 'Kullu, Himachal Pradesh', 'difficulty': 'Difficult', 'start': '2026-08-01', 'max': 15, 'price': 16999},
    {'name': 'Chadar Trek', 'location': 'Zanskar, Ladakh', 'difficulty': 'Difficult', 'start': '2027-01-10', 'max': 16, 'price': 18999},
    {'name': 'Markha Valley Trek', 'location': 'Leh, Ladakh', 'difficulty': 'Moderate', 'start': '2026-07-25', 'max': 20, 'price': 14999},
    {'name': 'Sandakphu Trek', 'location': 'Darjeeling, West Bengal', 'difficulty': 'Moderate', 'start': '2026-11-10', 'max': 24, 'price': 7499},
    {'name': 'Goechala Trek', 'location': 'Yuksom, Sikkim', 'difficulty': 'Difficult', 'start': '2026-10-12', 'max': 18, 'price': 15999},
    {'name': 'Bhrigu Lake Trek', 'location': 'Manali, Himachal Pradesh', 'difficulty': 'Easy', 'start': '2026-09-01', 'max': 28, 'price': 5499},
    {'name': 'Dayara Bugyal Trek', 'location': 'Uttarkashi, Uttarakhand', 'difficulty': 'Easy', 'start': '2026-12-05', 'max': 30, 'price': 5999},
    {'name': 'Rupin Pass Trek', 'location': 'Dehradun, Uttarakhand', 'difficulty': 'Difficult', 'start': '2026-09-22', 'max': 16, 'price': 12999},
    {'name': 'Tarsar Marsar Trek', 'location': 'Pahalgam, Kashmir', 'difficulty': 'Moderate', 'start': '2026-08-05', 'max': 20, 'price': 13999},
    {'name': 'Kashmir Great Lakes Trek', 'location': 'Sonamarg, Kashmir', 'difficulty': 'Difficult', 'start': '2026-08-18', 'max': 18, 'price': 15499},
    {'name': 'Nag Tibba Trek', 'location': 'Dehradun, Uttarakhand', 'difficulty': 'Easy', 'start': '2026-11-22', 'max': 35, 'price': 2499},
    {'name': 'Stok Kangri Trek', 'location': 'Leh, Ladakh', 'difficulty': 'Difficult', 'start': '2026-07-10', 'max': 12, 'price': 24999},
    {'name': 'Pindari Glacier Trek', 'location': 'Bageshwar, Uttarakhand', 'difficulty': 'Moderate', 'start': '2026-10-01', 'max': 22, 'price': 7999},
    {'name': 'Annapurna Base Camp Trek', 'location': 'Annapurna, Nepal', 'difficulty': 'Difficult', 'start': '2026-10-15', 'max': 14, 'price': 26999},
]


def build_itinerary_text(details):
    """Assembles the full itinerary block from a trek's curated details."""
    lines = []
    lines.append("PICKUP & DROP")
    lines.append(details['pickup'])
    lines.append("")
    lines.append("TRAVEL DETAILS")
    lines.append(details['travel'])
    lines.append("")
    lines.append("ACCOMMODATION")
    lines.append(details['accommodation'])
    lines.append("")
    lines.append(f"DAY-WISE PLAN ({len(details['day_plan'])} Days)")
    lines.extend(details['day_plan'])
    lines.append("")
    lines.append("INCLUSIONS")
    lines.append(COMMON_INCLUSIONS)
    lines.append("")
    lines.append("EXCLUSIONS")
    lines.append(COMMON_EXCLUSIONS)
    return "\n".join(lines)


def seed_treks():
    with app.app_context():
        added_count = 0
        skipped_count = 0

        for trek_data in TREKS:
            existing = Trek.query.filter_by(name=trek_data['name']).first()
            if existing:
                # Trek already exists (from a previous run) -- just make sure
                # its image_url is up to date with the current IMAGE_MAP,
                # without touching anything else (status, bookings, etc).
                correct_image = IMAGE_MAP.get(trek_data['name'])
                if correct_image and existing.image_url != correct_image:
                    existing.image_url = correct_image
                skipped_count += 1
                continue

            details = TREK_DETAILS[trek_data['name']]
            duration = len(details['day_plan'])
            start_date = datetime.strptime(trek_data['start'], '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=duration - 1)

            new_trek = Trek(
                name=trek_data['name'],
                location=trek_data['location'],
                difficulty=DIFFICULTY_MAP[trek_data['difficulty']],
                duration_days=duration,
                total_slots=trek_data['max'],
                available_slots=trek_data['max'],
                assigned_staff_id=None,
                status='Open',
                start_date=start_date,
                end_date=end_date,
                description=f"Experience the breathtaking {trek_data['name']} through stunning Himalayan terrain.",
                price=float(trek_data['price']),
                altitude=details['altitude'],
                image_url=IMAGE_MAP.get(trek_data['name']),
                itinerary=build_itinerary_text(details)
            )
            db.session.add(new_trek)
            added_count += 1

        db.session.commit()
        print(f"Done! Added {added_count} new treks, skipped {skipped_count} that already existed.")


if __name__ == '__main__':
    seed_treks()
