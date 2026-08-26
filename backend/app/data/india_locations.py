"""Static reference data: Indian states/UTs and their major cities.

This is master/reference data (not user-generated), so it's kept as a plain
Python structure and served read-only via the /locations API rather than
living in the database.

Most states list 20+ well-known cities. A handful of small states and union
territories genuinely don't have 20 sizable towns — for those, every real
town is listed (never padded with invented names) and a `note` explains why
the count is short.
"""

INDIA_LOCATIONS = [
    {"name": "Andhra Pradesh", "type": "state", "cities": [
        "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool",
        "Rajahmundry", "Tirupati", "Kadapa", "Kakinada", "Anantapur",
        "Vizianagaram", "Eluru", "Ongole", "Nandyal", "Machilipatnam",
        "Adoni", "Tenali", "Proddatur", "Chittoor", "Srikakulam",
    ]},
    {"name": "Arunachal Pradesh", "type": "state", "note": "A sparsely urbanized state — these are its district headquarters, not all large cities.", "cities": [
        "Itanagar", "Naharlagun", "Pasighat", "Aalo", "Ziro",
        "Bomdila", "Tawang", "Tezu", "Khonsa", "Changlang",
        "Roing", "Anini", "Daporijo", "Yingkiong", "Seppa",
        "Basar", "Namsai", "Longding", "Hawai", "Yupia",
    ]},
    {"name": "Assam", "type": "state", "cities": [
        "Guwahati", "Dibrugarh", "Silchar", "Jorhat", "Nagaon",
        "Tinsukia", "Tezpur", "Bongaigaon", "Karimganj", "Sivasagar",
        "Goalpara", "Barpeta", "Dhubri", "North Lakhimpur", "Diphu",
        "Golaghat", "Hailakandi", "Nalbari", "Mangaldoi", "Kokrajhar",
    ]},
    {"name": "Bihar", "type": "state", "cities": [
        "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga",
        "Purnia", "Arrah", "Begusarai", "Katihar", "Munger",
        "Chhapra", "Bihar Sharif", "Saharsa", "Hajipur", "Sasaram",
        "Dehri", "Siwan", "Motihari", "Bettiah", "Samastipur",
    ]},
    {"name": "Chhattisgarh", "type": "state", "cities": [
        "Raipur", "Bhilai", "Bilaspur", "Korba", "Durg",
        "Rajnandgaon", "Jagdalpur", "Raigarh", "Ambikapur", "Dhamtari",
        "Mahasamund", "Kanker", "Kawardha", "Chirmiri", "Champa",
        "Janjgir", "Bhatapara", "Tilda Newra", "Dongargarh", "Sakti",
    ]},
    {"name": "Goa", "type": "state", "note": "India's smallest state by area — it has far fewer than 20 towns.", "cities": [
        "Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda",
        "Bicholim", "Curchorem", "Sanquelim", "Cuncolim", "Canacona",
        "Valpoi", "Pernem", "Quepem", "Sanguem",
    ]},
    {"name": "Gujarat", "type": "state", "cities": [
        "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar",
        "Jamnagar", "Junagadh", "Gandhinagar", "Anand", "Nadiad",
        "Morbi", "Mehsana", "Bharuch", "Vapi", "Navsari",
        "Veraval", "Porbandar", "Godhra", "Palanpur", "Patan",
    ]},
    {"name": "Haryana", "type": "state", "cities": [
        "Faridabad", "Gurugram", "Panipat", "Ambala", "Yamunanagar",
        "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula",
        "Bhiwani", "Sirsa", "Bahadurgarh", "Jind", "Kurukshetra",
        "Kaithal", "Rewari", "Palwal", "Pundri", "Narnaul",
    ]},
    {"name": "Himachal Pradesh", "type": "state", "note": "A hill state with a small number of sizable towns.", "cities": [
        "Shimla", "Dharamshala", "Solan", "Mandi", "Palampur",
        "Baddi", "Nahan", "Una", "Kullu", "Hamirpur",
        "Bilaspur", "Chamba", "Sundarnagar", "Nalagarh", "Paonta Sahib",
        "Kangra",
    ]},
    {"name": "Jharkhand", "type": "state", "cities": [
        "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro Steel City", "Deoghar",
        "Hazaribagh", "Giridih", "Ramgarh", "Medininagar", "Chirkunda",
        "Phusro", "Dumka", "Madhupur", "Chaibasa", "Gumla",
        "Godda", "Sahibganj", "Chatra", "Lohardaga", "Jhumri Telaiya",
    ]},
    {"name": "Karnataka", "type": "state", "cities": [
        "Bengaluru", "Mysuru", "Hubballi-Dharwad", "Mangaluru", "Belagavi",
        "Kalaburagi", "Davanagere", "Ballari", "Vijayapura", "Shivamogga",
        "Tumakuru", "Raichur", "Bidar", "Hospet", "Hassan",
        "Gadag-Betageri", "Udupi", "Bagalkot", "Chitradurga", "Kolar",
    ]},
    {"name": "Kerala", "type": "state", "cities": [
        "Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur",
        "Kannur", "Alappuzha", "Kottayam", "Palakkad", "Malappuram",
        "Kasaragod", "Pathanamthitta", "Idukki", "Wayanad", "Muvattupuzha",
        "Punalur", "Neyyattinkara", "Thalassery", "Ponnani", "Guruvayur",
    ]},
    {"name": "Madhya Pradesh", "type": "state", "cities": [
        "Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain",
        "Sagar", "Dewas", "Satna", "Ratlam", "Rewa",
        "Katni", "Singrauli", "Burhanpur", "Khandwa", "Bhind",
        "Chhindwara", "Guna", "Shivpuri", "Vidisha", "Damoh",
    ]},
    {"name": "Maharashtra", "type": "state", "cities": [
        "Mumbai", "Pune", "Nagpur", "Nashik", "Thane",
        "Chhatrapati Sambhajinagar", "Solapur", "Amravati", "Kolhapur", "Sangli",
        "Malegaon", "Akola", "Latur", "Dhule", "Ahmednagar",
        "Chandrapur", "Parbhani", "Jalgaon", "Bhiwandi", "Nanded",
    ]},
    {"name": "Manipur", "type": "state", "note": "A small state — these are its main towns.", "cities": [
        "Imphal", "Thoubal", "Bishnupur", "Churachandpur", "Kakching",
        "Ukhrul", "Senapati", "Tamenglong", "Jiribam", "Moirang",
        "Mayang Imphal", "Kangpokpi",
    ]},
    {"name": "Meghalaya", "type": "state", "note": "A small state — these are its main towns.", "cities": [
        "Shillong", "Tura", "Jowai", "Nongstoin", "Baghmara",
        "Williamnagar", "Nongpoh", "Resubelpara", "Mairang", "Mawkyrwat",
    ]},
    {"name": "Mizoram", "type": "state", "note": "A small state — these are its main towns.", "cities": [
        "Aizawl", "Lunglei", "Champhai", "Serchhip", "Kolasib",
        "Saiha", "Lawngtlai", "Mamit", "Khawzawl", "Hnahthial",
    ]},
    {"name": "Nagaland", "type": "state", "note": "A small state — these are its main towns.", "cities": [
        "Kohima", "Dimapur", "Mokokchung", "Tuensang", "Wokha",
        "Zunheboto", "Mon", "Phek", "Kiphire", "Longleng", "Peren",
    ]},
    {"name": "Odisha", "type": "state", "cities": [
        "Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur",
        "Puri", "Balasore", "Bhadrak", "Baripada", "Jharsuguda",
        "Jeypore", "Bargarh", "Rayagada", "Kendujhar", "Angul",
        "Dhenkanal", "Paradip", "Koraput", "Balangir", "Nabarangpur",
    ]},
    {"name": "Punjab", "type": "state", "cities": [
        "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda",
        "Mohali", "Hoshiarpur", "Batala", "Pathankot", "Moga",
        "Abohar", "Malerkotla", "Khanna", "Phagwara", "Muktsar",
        "Barnala", "Rajpura", "Firozpur", "Kapurthala", "Sangrur",
    ]},
    {"name": "Rajasthan", "type": "state", "cities": [
        "Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner",
        "Ajmer", "Bhilwara", "Alwar", "Bharatpur", "Sikar",
        "Pali", "Sri Ganganagar", "Kishangarh", "Baran", "Dhaulpur",
        "Tonk", "Beawar", "Hanumangarh", "Churu", "Jhunjhunu",
    ]},
    {"name": "Sikkim", "type": "state", "note": "India's least populous state — it has very few towns.", "cities": [
        "Gangtok", "Namchi", "Gyalshing", "Mangan", "Rangpo",
        "Singtam", "Jorethang", "Nayabazar",
    ]},
    {"name": "Tamil Nadu", "type": "state", "cities": [
        "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem",
        "Tirunelveli", "Tiruppur", "Erode", "Vellore", "Thoothukudi",
        "Dindigul", "Thanjavur", "Ranipet", "Nagercoil", "Kanchipuram",
        "Karur", "Cuddalore", "Kumbakonam", "Hosur", "Nagapattinam",
    ]},
    {"name": "Telangana", "type": "state", "cities": [
        "Hyderabad", "Warangal", "Nizamabad", "Khammam", "Karimnagar",
        "Ramagundam", "Mahbubnagar", "Nalgonda", "Adilabad", "Suryapet",
        "Siddipet", "Miryalaguda", "Jagtial", "Mancherial", "Bhongir",
        "Sangareddy", "Wanaparthy", "Kamareddy", "Zaheerabad", "Medak",
    ]},
    {"name": "Tripura", "type": "state", "note": "A small state — these are its main towns.", "cities": [
        "Agartala", "Udaipur", "Dharmanagar", "Kailashahar", "Belonia",
        "Khowai", "Ambassa", "Sabroom", "Sonamura", "Ranirbazar",
    ]},
    {"name": "Uttar Pradesh", "type": "state", "cities": [
        "Lucknow", "Kanpur", "Ghaziabad", "Agra", "Meerut",
        "Varanasi", "Prayagraj", "Bareilly", "Aligarh", "Moradabad",
        "Saharanpur", "Gorakhpur", "Noida", "Firozabad", "Jhansi",
        "Muzaffarnagar", "Mathura", "Rampur", "Shahjahanpur", "Farrukhabad",
    ]},
    {"name": "Uttarakhand", "type": "state", "cities": [
        "Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrapur",
        "Kashipur", "Rishikesh", "Nainital", "Almora", "Pithoragarh",
        "Kotdwar", "Ramnagar", "Mussoorie", "Pauri", "Srinagar",
        "Bageshwar", "Champawat", "Tehri", "Vikasnagar", "Manglaur",
    ]},
    {"name": "West Bengal", "type": "state", "cities": [
        "Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri",
        "Bardhaman", "Malda", "Baharampur", "Habra", "Kharagpur",
        "Shantipur", "Krishnanagar", "Ranaghat", "Haldia", "Raiganj",
        "Jalpaiguri", "Cooch Behar", "Alipurduar", "Bankura", "Purulia",
    ]},
    # ---- Union Territories ----
    {"name": "Andaman and Nicobar Islands", "type": "union_territory", "note": "An island territory — most of its landmass is uninhabited.", "cities": [
        "Port Blair", "Diglipur", "Mayabunder", "Rangat", "Car Nicobar",
        "Havelock (Swaraj Dweep)", "Neil Island (Shaheed Dweep)", "Campbell Bay",
    ]},
    {"name": "Chandigarh", "type": "union_territory", "note": "A single planned city-UT.", "cities": [
        "Chandigarh",
    ]},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "type": "union_territory", "note": "One of India's smallest UTs.", "cities": [
        "Silvassa", "Daman", "Diu",
    ]},
    {"name": "Delhi", "type": "union_territory", "note": "Delhi NCT is administratively one city — these are its major localities, not separate cities.", "cities": [
        "New Delhi", "Dwarka", "Rohini", "Karol Bagh", "Connaught Place",
        "Saket", "Vasant Kunj", "Pitampura", "Janakpuri", "Lajpat Nagar",
        "Mayur Vihar", "Shahdara", "Najafgarh", "Narela", "Chandni Chowk",
        "Hauz Khas", "Greater Kailash", "Preet Vihar", "Paschim Vihar", "Dilshad Garden",
    ]},
    {"name": "Jammu and Kashmir", "type": "union_territory", "cities": [
        "Srinagar", "Jammu", "Anantnag", "Baramulla", "Sopore",
        "Kathua", "Udhampur", "Poonch", "Rajouri", "Kupwara",
        "Pulwama", "Budgam", "Bandipora", "Ganderbal", "Kulgam",
        "Shopian", "Doda", "Kishtwar", "Ramban", "Samba",
    ]},
    {"name": "Ladakh", "type": "union_territory", "note": "A vast, sparsely populated high-altitude UT with only two major towns.", "cities": [
        "Leh", "Kargil",
    ]},
    {"name": "Lakshadweep", "type": "union_territory", "note": "India's smallest UT — a coral island chain; entries are inhabited islands, not cities.", "cities": [
        "Kavaratti", "Agatti", "Amini", "Andrott", "Kalpeni",
        "Minicoy", "Kadmat", "Chetlat", "Bitra", "Bangaram",
    ]},
    {"name": "Puducherry", "type": "union_territory", "note": "This UT consists of four small, geographically separate regions.", "cities": [
        "Puducherry", "Karaikal", "Mahe", "Yanam",
    ]},
]
