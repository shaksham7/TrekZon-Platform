"""
trek_details.py

Curated, trek-specific details for all 22 seeded treks -- used by seed_treks.py.
Each entry has real/accurate pickup points, travel routes, accommodation style
(teahouse / camping / homestay -- these genuinely differ by trek), a day-wise
plan matching that trek's actual route, altitude, and pricing.
"""

COMMON_INCLUSIONS = (
    "All meals during the trek (breakfast, lunch, dinner, and evening tea with snacks), "
    "accommodation as per the itinerary, camping equipment (tents, sleeping bags, mats) where applicable, "
    "trek permits and forest/entry fees, first-aid kit and basic medical support, "
    "an experienced trek leader and support/kitchen staff, and safety equipment (microspikes/gaiters "
    "where the route requires them)."
)

COMMON_EXCLUSIONS = (
    "Transport to/from the pickup point (unless mentioned), personal trekking gear and clothing, "
    "personal expenses (phone charging, laundry, bottled water, snacks), travel and medical insurance, "
    "mules/porters for personal luggage (available on request at extra cost), "
    "any costs arising from delays due to weather, roadblocks, or natural calamities, "
    "and anything not explicitly mentioned under inclusions."
)

TREK_DETAILS = {
    'Kedarnath Trek': {
        'altitude': 3583,
        'pickup': 'Dehradun Railway Station, 6:00 AM sharp (10 minutes from Dehradun ISBT)',
        'travel': (
            "Drive from Dehradun to Sonprayag (approx 210 km, 8-9 hours) by private vehicle along the "
            "Rishikesh-Badrinath highway, following the Alaknanda and Mandakini river valleys. "
            "From Sonprayag, a short shared jeep ride takes you to Gaurikund, the actual trek starting point."
        ),
        'accommodation': (
            "Night 1: Guesthouse at Sonprayag/Gaurikund (twin sharing). "
            "Nights 2-3: Registered guesthouse/dharamshala near Kedarnath temple (dormitory or shared rooms, "
            "as availability during peak season is limited). Night 4 (return): Guesthouse at Sonprayag."
        ),
        'day_plan': [
            "Day 1: Pickup from Dehradun, scenic drive to Sonprayag via Rudraprayag, overnight stay.",
            "Day 2: Drive to Gaurikund, begin trek to Kedarnath (16 km, 7-8 hours) along the paved pilgrim "
            "route, gradual ascent through Rambara and Linchauli, overnight near the temple.",
            "Day 3: Morning darshan at Kedarnath temple, short acclimatization walk towards Bhairav Temple "
            "viewpoint, rest and explore the Mandakini valley, overnight stay.",
            "Day 4: Descend from Kedarnath to Gaurikund (16 km, 5-6 hours), drive to Sonprayag, overnight stay.",
            "Day 5: Drive back to Dehradun, drop at Railway Station by evening. Trip concludes.",
            "Day 6: Buffer day (in case of weather delays on the return journey).",
            "Day 7: Buffer day (in case of weather delays on the return journey).",
        ],
    },
    'Brahmatal Trek': {
        'altitude': 3734,
        'pickup': 'Rishikesh Railway Station, 6:30 AM sharp',
        'travel': (
            "Drive from Rishikesh to Lohajung (approx 220 km, 9-10 hours) via Karnaprayag and Gwaldam, "
            "a scenic route through pine and oak forests with views of Trishul and Nanda Ghunti peaks."
        ),
        'accommodation': (
            "Night 1: Guesthouse at Lohajung (twin/triple sharing). Nights 2 onward: Camping in "
            "insulated trekking tents (triple sharing) at Bekaltal, Brahmatal base, and Daldum campsites."
        ),
        'day_plan': [
            "Day 1: Pickup from Rishikesh, drive to Lohajung, evening trek briefing, overnight at guesthouse.",
            "Day 2: Trek from Lohajung to Bekaltal (5 km, 4 hours) through dense forest to a frozen lake "
            "campsite, overnight camping.",
            "Day 3: Trek from Bekaltal to Brahmatal base camp (4 km, 4 hours), first clear views of Mt. "
            "Trishul, overnight camping.",
            "Day 4: Summit day -- trek to Brahmatal Top (3734 m) for sunrise views of Trishul and Nanda "
            "Ghunti, descend to Daldum campsite, overnight camping.",
            "Day 5: Descend from Daldum to Lohajung (6 km, 5 hours), drive back to Rishikesh, drop by late "
            "evening. Trip concludes.",
        ],
    },
    'Roopkund Trek': {
        'altitude': 5029,
        'pickup': 'Kathgodam Railway Station, 6:00 AM sharp',
        'travel': (
            "Drive from Kathgodam to Lohajung (approx 210 km, 9-10 hours) via Almora and Gwaldam, "
            "a long but scenic Himalayan foothill drive."
        ),
        'accommodation': (
            "Night 1: Guesthouse at Lohajung. Nights 2-5: Camping in high-altitude trekking tents "
            "(triple sharing) at Didna, Ali Bugyal/Bedni Bugyal, Bhagwabasa, and back."
        ),
        'day_plan': [
            "Day 1: Pickup from Kathgodam, drive to Lohajung, overnight at guesthouse.",
            "Day 2: Trek to Didna village (6 km, 4-5 hours) through forest trails, overnight camping.",
            "Day 3: Trek to Bedni Bugyal (7 km, 6 hours), a vast alpine meadow with panoramic Himalayan "
            "views, overnight camping.",
            "Day 4: Trek to Bhagwabasa (6 km, 5-6 hours) via Patar Nachauni, gradual altitude gain, "
            "overnight camping.",
            "Day 5: Summit day -- trek to Roopkund (5029 m), the famous skeleton lake, and back to "
            "Bhagwabasa (8 km round trip, 7-8 hours), overnight camping.",
            "Day 6: Descend to Bedni Bugyal (8 km, 6 hours), overnight camping.",
            "Day 7: Descend to Lohajung (13 km, 6-7 hours), drive back to Kathgodam, drop by night. "
            "Trip concludes.",
        ],
    },
    'Valley of Flowers Trek': {
        'altitude': 3658,
        'pickup': 'Haridwar Railway Station, 6:00 AM sharp',
        'travel': (
            "Drive from Haridwar to Govindghat (approx 275 km, 10-11 hours) via Rishikesh, Joshimath, "
            "along the Alaknanda river valley."
        ),
        'accommodation': (
            "Nights 1 and 4: Guesthouse at Govindghat/Ghangaria (twin sharing). "
            "Nights 2-3: Guesthouse at Ghangaria (the base village inside the national park buffer zone)."
        ),
        'day_plan': [
            "Day 1: Pickup from Haridwar, drive to Govindghat, overnight at guesthouse.",
            "Day 2: Trek from Govindghat to Ghangaria (13 km, 6-7 hours) along a paved pilgrim trail "
            "alongside the Pushpawati river, overnight stay.",
            "Day 3: Day trek into the Valley of Flowers National Park (8 km round trip, 6 hours), "
            "walking among hundreds of species of Himalayan wildflowers, return to Ghangaria for the night.",
            "Day 4: Optional visit to Hemkund Sahib (12 km round trip) or rest day, descend to Govindghat "
            "(13 km, 5-6 hours), overnight stay.",
            "Day 5: Drive back to Haridwar, drop by evening. Trip concludes.",
        ],
    },
    'Hampta Pass Trek': {
        'altitude': 4270,
        'pickup': 'Manali Bus Stand, 7:00 AM sharp',
        'travel': (
            "Drive from Manali to Jobra (approx 18 km, 1 hour) via Prini village, the actual trek "
            "starting point. Return drive from Chatru/Manali on the last day."
        ),
        'accommodation': "Camping in trekking tents (triple sharing) at all campsites: Jobra, Jwara, Balu Ka Ghera, and Chatru.",
        'day_plan': [
            "Day 1: Pickup from Manali, drive to Jobra, short trek to Chika campsite (3 km, 2 hours), overnight camping.",
            "Day 2: Trek to Jwara (5 km, 5 hours) through pine forest into the Hampta valley, overnight camping.",
            "Day 3: Trek to Balu Ka Ghera (4 km, 4 hours), a wide sandy meadow with views of the pass ahead, overnight camping.",
            "Day 4: Cross Hampta Pass (4270 m) and descend to Shea Goru (8 km, 7-8 hours), dramatic change from "
            "green valley to the arid Lahaul landscape, overnight camping.",
            "Day 5: Trek to Chatru (7 km, 5 hours), optional side visit to Chandratal Lake, drive back to Manali, "
            "drop by evening. Trip concludes.",
        ],
    },
    'Kedarkantha Trek': {
        'altitude': 3810,
        'pickup': 'Dehradun Railway Station, 6:30 AM sharp',
        'travel': "Drive from Dehradun to Sankri (approx 210 km, 8-9 hours) via Mussoorie and Purola, the base village for the trek.",
        'accommodation': "Night 1 and last night: Guesthouse at Sankri (twin/triple sharing). Nights 2-4: Camping in trekking tents at Juda Ka Talab and Kedarkantha base.",
        'day_plan': [
            "Day 1: Pickup from Dehradun, drive to Sankri, overnight at guesthouse.",
            "Day 2: Trek to Juda Ka Talab (4 km, 4 hours) through pine and oak forest to a frozen lake campsite, overnight camping.",
            "Day 3: Trek to Kedarkantha base camp (4 km, 4 hours), first open views of the summit, overnight camping.",
            "Day 4: Summit day -- trek to Kedarkantha Top (3810 m) for a 360-degree view of the Garhwal and Kinnaur ranges, descend to Hargaon, overnight camping.",
            "Day 5: Descend to Sankri (6 km, 4-5 hours), drive back to Dehradun, drop by night. Trip concludes.",
        ],
    },
    'Triund Trek': {
        'altitude': 2850,
        'pickup': 'McLeod Ganj Bus Stand, Dharamshala, 9:00 AM sharp',
        'travel': "Short local transfer/walk from McLeod Ganj to Galu Devi Temple (approx 3 km), the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at Triund, with the option of a Himalayan-view sunset/sunrise campsite.",
        'day_plan': [
            "Day 1: Assemble at McLeod Ganj, trek to Triund (7 km, 5-6 hours) through rhododendron and oak "
            "forest with the Dhauladhar range coming into view, overnight camping with campfire.",
            "Day 2: Sunrise view of the Dhauladhar peaks, descend to McLeod Ganj (9 km, 4-5 hours). Trip concludes by early afternoon.",
        ],
    },
    'Har Ki Dun Trek': {
        'altitude': 3566,
        'pickup': 'Dehradun Railway Station, 6:00 AM sharp',
        'travel': "Drive from Dehradun to Sankri (approx 210 km, 8-9 hours) via Mussoorie and Purola.",
        'accommodation': "Night 1 and last night: Guesthouse at Sankri. Nights 2-5: Camping in trekking tents at Taluka/Osla, Har Ki Dun, and Kalkattiyadhar.",
        'day_plan': [
            "Day 1: Pickup from Dehradun, drive to Sankri, overnight at guesthouse.",
            "Day 2: Drive to Taluka, trek to Gangad/Osla village (7 km, 5 hours) along the Supin river, overnight camping.",
            "Day 3: Trek to Kalkattiyadhar (8 km, 6 hours) through forest, overnight camping.",
            "Day 4: Trek to Har Ki Dun (5 km, 4-5 hours), a wide valley ringed by Swargarohini and Bandarpoonch "
            "peaks, overnight camping and exploration.",
            "Day 5: Descend to Kalkattiyadhar/Osla (13 km, 6-7 hours), overnight camping.",
            "Day 6: Descend to Taluka (7 km, 5 hours), drive to Sankri, overnight at guesthouse.",
        ],
    },
    'Pin Parvati Pass Trek': {
        'altitude': 5319,
        'pickup': 'Bhuntar (Kullu), 7:00 AM sharp',
        'travel': "Drive from Bhuntar to Barshaini via Kasol and Manikaran (approx 45 km, 2-3 hours), the actual trek starting point in the Parvati valley.",
        'accommodation': "Camping in high-altitude trekking tents (triple sharing) throughout; this is a remote, high-altitude crossing with no permanent settlements en route.",
        'day_plan': [
            "Day 1: Pickup from Bhuntar, drive to Barshaini, trek to Kheerganga (3 km, 3 hours), overnight camping near the hot springs.",
            "Day 2: Trek to Tunda Bhuj (10 km, 6 hours) through dense forest, overnight camping.",
            "Day 3: Trek to Odi Thach (8 km, 6 hours), gradual altitude gain into alpine terrain, overnight camping.",
            "Day 4: Trek to Mantalai Lake base (7 km, 6 hours), the source of the Parvati river, overnight camping.",
            "Day 5: Acclimatization and rest day at Mantalai, short exploratory walk, overnight camping.",
            "Day 6: Trek to high camp below Pin Parvati Pass (5 km, 5 hours), overnight camping.",
            "Day 7: Cross Pin Parvati Pass (5319 m) and descend into the Pin Valley (Spiti side), long summit "
            "day (10-11 hours), overnight camping.",
            "Day 8: Descend towards Mud village in the Pin Valley, overnight camping.",
            "Day 9: Trek to roadhead near Mud village, drive towards Kaza. Trip concludes.",
            "Day 10: Buffer day for weather/acclimatization contingency.",
            "Day 11: Buffer day for weather/acclimatization contingency.",
            "Day 12: Buffer day for weather/acclimatization contingency.",
        ],
    },
    'Chadar Trek': {
        'altitude': 3390,
        'pickup': 'Leh Airport / Bus Stand, 9:00 AM sharp (after acclimatization stay in Leh)',
        'travel': (
            "Drive from Leh to Shingra Koma / Tilad Do (approx 45-60 km, 2 hours), the actual starting point "
            "where the group descends onto the frozen Zanskar river."
        ),
        'accommodation': (
            "2 nights pre-trek in Leh for mandatory acclimatization (guesthouse, twin sharing). "
            "On the trek: camping in insulated tents pitched on the riverbank/inside natural caves along the "
            "frozen Zanskar gorge -- a distinctive feature of this trek."
        ),
        'day_plan': [
            "Day 1: Arrive in Leh, rest and acclimatize (guesthouse stay).",
            "Day 2: Acclimatization walks around Leh, gear check and briefing, overnight in Leh.",
            "Day 3: Drive to Shingra Koma, begin walking on the Chadar (frozen river), overnight camping in a riverside cave/tent.",
            "Day 4: Walk along the Chadar to Tibb cave campsite (10-12 km, 6-7 hours), overnight camping.",
            "Day 5: Walk to Nerak village, view the frozen Nerak waterfall (10-11 km, 6-7 hours), overnight camping.",
            "Day 6: Rest/exploration day at Nerak, overnight camping.",
            "Day 7: Begin return journey along the Chadar to Tibb, overnight camping.",
            "Day 8: Walk back to Shingra Koma, drive back to Leh. Trip concludes.",
            "Day 9: Buffer day in Leh for weather contingency before departure.",
        ],
    },
    'Markha Valley Trek': {
        'altitude': 5150,
        'pickup': 'Leh Bus Stand, 8:00 AM sharp (after acclimatization stay in Leh)',
        'travel': "Drive from Leh to Chilling (approx 65 km, 2-3 hours) via the Indus valley, the actual trek starting point.",
        'accommodation': "1 night pre-trek in Leh (guesthouse). On the trek: a mix of homestays in Markha valley villages (Skiu, Markha, Hankar) and camping near Nimaling and the Kongmaru La base.",
        'day_plan': [
            "Day 1: Arrive in Leh, rest and acclimatize, overnight in Leh.",
            "Day 2: Drive to Chilling, trek to Skiu village (6 km, 3-4 hours) along the Zanskar river confluence, overnight homestay.",
            "Day 3: Trek to Markha village (14 km, 6-7 hours) along the Markha river, overnight homestay.",
            "Day 4: Trek to Hankar village (12 km, 5-6 hours), views of Kang Yatze peak, overnight homestay.",
            "Day 5: Trek to Nimaling (10 km, 5 hours), a high-altitude pasture below Kang Yatze, overnight camping.",
            "Day 6: Cross Kongmaru La (5150 m) and descend to Chuskirmo/Shang Sumdo (12 km, 7-8 hours), drive back to Leh. Trip concludes.",
        ],
    },
    'Sandakphu Trek': {
        'altitude': 3636,
        'pickup': 'New Jalpaiguri (NJP) Railway Station, 7:00 AM sharp',
        'travel': "Drive from NJP to Maneybhanjan (approx 95 km, 4 hours) via Darjeeling town, the actual trek starting point.",
        'accommodation': "Trekker's huts and homestays throughout the route (Tumling, Kalapokhri, Sandakphu, Phalut) -- a well-established teahouse-style trek, no camping required.",
        'day_plan': [
            "Day 1: Pickup from NJP, drive to Maneybhanjan, trek to Tumling (11 km, 5 hours), overnight at a homestay with views of Kanchenjunga.",
            "Day 2: Trek to Kalapokhri (11 km, 6 hours) through rhododendron forest, overnight at a trekker's hut.",
            "Day 3: Trek to Sandakphu (6 km, 4 hours), the highest point in West Bengal with views of four of the "
            "world's five highest peaks (Everest, Kanchenjunga, Lhotse, Makalu), overnight stay.",
            "Day 4: Trek to Phalut (10 km, 6 hours) along the ridge, expansive Himalayan panorama, overnight homestay.",
            "Day 5: Descend to Gorkhey via Sepi (13 km, 6-7 hours), overnight homestay.",
            "Day 6: Descend to Rimbik, drive back to NJP, drop by evening. Trip concludes.",
        ],
    },
    'Goechala Trek': {
        'altitude': 4940,
        'pickup': 'New Jalpaiguri (NJP) / Bagdogra, 7:00 AM sharp',
        'travel': "Drive from NJP/Bagdogra to Yuksom (approx 160 km, 6-7 hours) via Pelling, the actual trek starting point inside Sikkim.",
        'accommodation': "Camping in trekking tents (triple sharing) at all campsites: Sachen, Tshoka, Dzongri, Thansing, and Lamuney.",
        'day_plan': [
            "Day 1: Pickup from NJP, drive to Yuksom, overnight at a guesthouse.",
            "Day 2: Trek to Sachen (8 km, 5 hours) through Kanchenjunga National Park forest, overnight camping.",
            "Day 3: Trek to Tshoka (7 km, 5-6 hours), a Tibetan settlement, overnight camping.",
            "Day 4: Trek to Dzongri (10 km, 6 hours), first big views of the Kanchenjunga range, overnight camping.",
            "Day 5: Acclimatization day -- side trek to Dzongri Top for sunrise views, rest at Dzongri, overnight camping.",
            "Day 6: Trek to Thansing (10 km, 6 hours) via Kokchurang, overnight camping.",
            "Day 7: Trek to Lamuney (4 km, 3 hours), short day for acclimatization before the summit push, overnight camping.",
            "Day 8: Pre-dawn trek to Goecha La viewpoint (4940 m) for close-up Kanchenjunga views, return to Kokchurang, overnight camping.",
            "Day 9: Descend to Tshoka (13 km, 6-7 hours), overnight camping.",
            "Day 10: Descend to Yuksom (16 km, 7 hours), drive back towards NJP. Trip concludes.",
        ],
    },
    'Bhrigu Lake Trek': {
        'altitude': 4300,
        'pickup': 'Manali Bus Stand, 8:00 AM sharp',
        'travel': "Drive from Manali to Gulaba village (approx 20 km, 1 hour), the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at Rola Kholi and Bhrigu Lake base campsites.",
        'day_plan': [
            "Day 1: Pickup from Manali, drive to Gulaba, trek to Rola Kholi campsite (4 km, 3-4 hours), overnight camping.",
            "Day 2: Trek to Bhrigu Lake (5 km, 4-5 hours), a high-altitude lake surrounded by open meadows with "
            "views of the Pir Panjal range, return to a lower campsite, overnight camping.",
            "Day 3: Descend to Gulaba (7 km, 4 hours), drive back to Manali. Trip concludes.",
        ],
    },
    'Dayara Bugyal Trek': {
        'altitude': 3048,
        'pickup': 'Dehradun Railway Station, 6:30 AM sharp',
        'travel': "Drive from Dehradun to Raithal/Barsu village (approx 165 km, 7-8 hours) via Uttarkashi, the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at Gui village/Chilapada and Dayara Bugyal campsites.",
        'day_plan': [
            "Day 1: Pickup from Dehradun, drive to Raithal, overnight at a guesthouse.",
            "Day 2: Trek to Chilapada campsite (5 km, 4 hours) through oak and rhododendron forest, overnight camping.",
            "Day 3: Trek to Dayara Bugyal (4 km, 3-4 hours), a vast rolling meadow with views of Bandarpoonch "
            "peak, overnight camping.",
            "Day 4: Descend to Raithal (9 km, 5-6 hours), drive back to Dehradun, drop by evening. Trip concludes.",
        ],
    },
    'Rupin Pass Trek': {
        'altitude': 4650,
        'pickup': 'Dehradun Railway Station, 6:00 AM sharp',
        'travel': "Drive from Dehradun to Dhaula/Sankri (approx 200 km, 9 hours) via Mussoorie and Purola.",
        'accommodation': "Night 1: Guesthouse at Dhaula. On the trek: camping in trekking tents at Sewa, Jhaka, Saruwas Thatch, and Dhanderas Thatch, with a village homestay option at Jhaka.",
        'day_plan': [
            "Day 1: Pickup from Dehradun, drive to Dhaula, overnight at guesthouse.",
            "Day 2: Trek to Sewa village (8 km, 6 hours) along the Rupin river, overnight camping.",
            "Day 3: Trek to Jhaka village (4 km, 4 hours), known for its apple orchards, overnight homestay/camping.",
            "Day 4: Trek to Saruwas Thatch (6 km, 5 hours), passing the dramatic Rupin waterfall crossing, overnight camping.",
            "Day 5: Trek to Dhanderas Thatch (5 km, 5 hours), approach to the pass, overnight camping.",
            "Day 6: Cross Rupin Pass (4650 m) and descend to Ronti Gad (9 km, 8-9 hours), dramatic high-altitude crossing, overnight camping.",
            "Day 7: Descend to Sangla village in Kinnaur (7 km, 5 hours), drive towards Shimla/Dehradun. Trip concludes.",
        ],
    },
    'Tarsar Marsar Trek': {
        'altitude': 4100,
        'pickup': 'Srinagar Airport / Bus Stand, 7:00 AM sharp',
        'travel': "Drive from Srinagar to Aru village near Pahalgam (approx 100 km, 3 hours), the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at Lidderwat, Shekwas, and Sundarsar campsites.",
        'day_plan': [
            "Day 1: Pickup from Srinagar, drive to Aru, trek to Lidderwat (11 km, 5 hours) along the Lidder "
            "river through pine forest, overnight camping.",
            "Day 2: Trek to Shekwas (6 km, 4 hours), open meadows with views of surrounding peaks, overnight camping.",
            "Day 3: Trek to Tarsar Lake and on to Sundarsar (8 km, 6 hours), a stunning alpine lake, overnight camping.",
            "Day 4: Trek to Marsar Lake and back (8 km round trip, 6 hours), twin lake views, return to Sundarsar, overnight camping.",
            "Day 5: Descend to Homwas (10 km, 6 hours), overnight camping.",
            "Day 6: Descend to Aru, drive back to Srinagar, drop by evening. Trip concludes.",
        ],
    },
    'Kashmir Great Lakes Trek': {
        'altitude': 4191,
        'pickup': 'Srinagar Airport / Bus Stand, 7:00 AM sharp',
        'travel': "Drive from Srinagar to Sonamarg (approx 80 km, 2-3 hours), the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at Nichnai, Vishansar, Gadsar, Satsar, and Gangbal campsites.",
        'day_plan': [
            "Day 1: Pickup from Srinagar, drive to Sonamarg, trek to Nichnai (11 km, 5 hours), overnight camping.",
            "Day 2: Cross Nichnai Pass and trek to Vishansar Lake (12 km, 6 hours), a pristine alpine lake, overnight camping.",
            "Day 3: Trek to Gadsar via Gadsar Pass (4191 m) (14 km, 7-8 hours), the highest point of the trek, overnight camping.",
            "Day 4: Trek to Satsar (9 km, 6 hours), a cluster of seven small lakes, overnight camping.",
            "Day 5: Trek to Gangbal Lake via Zaj Pass (12 km, 7 hours), views of Mt. Harmukh, overnight camping.",
            "Day 6: Descend to Naranag, drive back to Srinagar, drop by evening. Trip concludes.",
            "Day 7: Buffer day for weather contingency.",
            "Day 8: Buffer day for weather contingency.",
        ],
    },
    'Nag Tibba Trek': {
        'altitude': 3022,
        'pickup': 'Dehradun Railway Station, 7:00 AM sharp',
        'travel': "Drive from Dehradun to Pantwari village (approx 85 km, 3-4 hours), the actual trek starting point.",
        'accommodation': "Camping in trekking tents (triple sharing) at the Nag Tibba base campsite.",
        'day_plan': [
            "Day 1: Pickup from Dehradun, drive to Pantwari, trek to Nag Tibba base camp (5 km, 4 hours) through "
            "oak and rhododendron forest, overnight camping.",
            "Day 2: Early morning summit of Nag Tibba (3022 m) for sunrise views of the Bandarpoonch and Gangotri "
            "ranges, descend to Pantwari, drive back to Dehradun. Trip concludes by evening.",
        ],
    },
    'Stok Kangri Trek': {
        'altitude': 6153,
        'pickup': 'Leh Airport / Bus Stand, 9:00 AM sharp (after acclimatization stay in Leh)',
        'travel': "Drive from Leh to Stok village (approx 15 km, 30 minutes), the actual trek starting point across the Indus from Leh.",
        'accommodation': (
            "2-3 nights pre-trek in Leh for mandatory high-altitude acclimatization (guesthouse). "
            "On the trek: camping in high-altitude mountaineering tents (triple sharing), with a dedicated "
            "summit-push high camp."
        ),
        'day_plan': [
            "Day 1: Arrive in Leh, rest and acclimatize, overnight in Leh.",
            "Day 2: Acclimatization walks and gear check in Leh, overnight in Leh.",
            "Day 3: Drive to Stok village, trek to Changma (5 km, 3-4 hours), overnight camping.",
            "Day 4: Trek to Mankarmo base camp (11 km, 5-6 hours), overnight camping.",
            "Day 5: Acclimatization and technical training day (rope work, use of ice axe/crampons), overnight camping.",
            "Day 6: Trek to Stok Kangri base camp (4 km, 3 hours), rest and prepare for summit push, overnight camping.",
            "Day 7: Summit day -- pre-dawn start for Stok Kangri (6153 m), a technical high-altitude climb, "
            "return to base camp (10-12 hours total), overnight camping.",
            "Day 8: Descend to Stok village, drive back to Leh. Trip concludes.",
            "Day 9: Buffer day for weather/acclimatization contingency.",
            "Day 10: Buffer day for weather/acclimatization contingency.",
            "Day 11: Buffer day for weather/acclimatization contingency.",
            "Day 12: Buffer day for weather/acclimatization contingency.",
        ],
    },
    'Pindari Glacier Trek': {
        'altitude': 3660,
        'pickup': 'Kathgodam Railway Station, 6:00 AM sharp',
        'travel': "Drive from Kathgodam to Song village via Bageshwar (approx 160 km, 7-8 hours), the actual trek starting point.",
        'accommodation': "Forest rest houses/guesthouses at Dhakuri, Khati, Dwali, and Phurkiya -- a well-established trail with permanent lodging, no camping required.",
        'day_plan': [
            "Day 1: Pickup from Kathgodam, drive to Song, trek to Dhakuri (8 km, 5 hours), overnight at a forest rest house.",
            "Day 2: Trek to Khati village (7 km, 5 hours), the last inhabited village on the route, overnight guesthouse stay.",
            "Day 3: Trek to Dwali (11 km, 6 hours) along the Pindar river, overnight guesthouse stay.",
            "Day 4: Trek to Phurkiya (5 km, 4 hours), overnight guesthouse stay.",
            "Day 5: Trek to Pindari Glacier viewpoint (Zero Point) and back to Phurkiya (10 km round trip, 6-7 hours), overnight guesthouse stay.",
            "Day 6: Descend to Khati (16 km, 7 hours), overnight guesthouse stay.",
        ],
    },
    'Annapurna Base Camp Trek': {
        'altitude': 4130,
        'pickup': 'Kathmandu Airport / Hotel, 6:00 AM sharp (after arrival day in Kathmandu)',
        'travel': (
            "Drive/flight from Kathmandu to Pokhara (approx 200 km, 6-7 hours by road or 25 minutes by air), "
            "then a short drive to Nayapul, the actual trek starting point."
        ),
        'accommodation': "Teahouse lodges throughout the route (Ghandruk, Chhomrong, Dovan, Machhapuchhre Base Camp, ABC) -- a classic teahouse trek, no camping required.",
        'day_plan': [
            "Day 1: Arrive in Kathmandu, rest and trek briefing, overnight in Kathmandu.",
            "Day 2: Travel to Pokhara, drive to Nayapul, trek to Ghandruk (village trek, 4-5 hours), overnight teahouse.",
            "Day 3: Trek to Chhomrong (5-6 hours), first views of Annapurna South and Machhapuchhre (Fishtail), overnight teahouse.",
            "Day 4: Trek to Dovan via Sinuwa and Bamboo (6 hours), overnight teahouse.",
            "Day 5: Trek to Machhapuchhre Base Camp (5-6 hours), overnight teahouse.",
            "Day 6: Early trek to Annapurna Base Camp (4130 m, 2-3 hours) for close-up views of the Annapurna "
            "massif, descend to Bamboo (7-8 hours total), overnight teahouse.",
            "Day 7: Descend to Jhinu Danda (6 hours), optional natural hot springs, overnight teahouse.",
            "Day 8: Trek to Nayapul, drive to Pokhara, overnight in Pokhara.",
            "Day 9: Travel back to Kathmandu. Trip concludes.",
            "Day 10: Buffer day for weather/flight delay contingency.",
            "Day 11: Buffer day for weather/flight delay contingency.",
        ],
    },
}
