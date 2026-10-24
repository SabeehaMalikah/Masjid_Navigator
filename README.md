# Masjid-Navigator
Sabeeha Malikah \
Advisor: Professor Shalva Landy

## Abstract
Muslims are required to pray five times a day and are often outside of their homes during prayer times due to school, work, or other activities. In these situations, they look for mosques (also known as masjid in Arabic) in their surrounding areas. Determining whether a masjid has designated women's prayer sections can be difficult, and I have often found myself searching through Google Maps reviews or other sources to identify if such facilities are available.

**Goal**: This web application presents a solution to this issue by providing a platform where users can easily view available facilities at nearby mosques.

**Features**: Each mosque will have a profile with information describing what facilities are available. Users will be able to interact with a map containing markers for nearby masjids. They can click on masjids for more detail or easily view their facilities at a glance.

## Project Management
Project milestones, completed tasks, and weekly timelines are tracked in [PROJECT_TRACKER.md](./PROJECT_TRACKER.md).

## Technical Stack
- **Database: PostgreSQL**
  - Used to store structured relationships between mosques, facility attributes, and reviews.
  
- **Backend API: Python (FastAPI)**
  - Provides high execution speed and automatically generates interactive Swagger UI documentation for testing REST endpoints[cite: 3].

- **NLP & Data Ingestion: spaCy & Requests**
  - *Requests:* HTTP library used to fetch raw mosque metadata, coordinates, and reviews from the Google Places API.
  - *spaCy:* NLP framework used for keyword extraction and context/sentiment analysis to parse review text. This will be used to distinguish "has a women's section" from "no women's section" and help set database facility flags automatically.

- **Frontend UI: React.js, Tailwind CSS & Google Maps SDK**
  - *React.js:* Allows for real-time UI updates when applying filters.
  - *Tailwind CSS:* Used to build a responsive and clean UI design.
  - *Google Maps SDK:* Dynamically renders map markers based on user location.

- **Version Control & Tooling:** Git, GitHub, VS Code

## Repository Structure
```
Masjid_Navigator/
├── .env.example                    # Template for required environment variables
├── .gitignore                      # Blocks secret API keys, caches, and raw output data
├── LICENSE                         # MIT Open-Source License
├── README.md                       # Project documentation & setup instructions
├── requirements.txt                # Tracked Python third-party dependencies
│
├── data/                           # Local datasets & search parameters
│   └── nyc_neighborhoods.txt
│
├── scripts/                         # Executable Python scripts to populate database
│   ├── api_testing.py               # Initial API call testing
│   ├── populate_mosque_table.py     # Populates mosque table in database
│   ├── populate_review_table.py     # Extracts reviews from mosque table and populates review table
│   ├── populate_facilities_table.py # Extracts reviews from review table and uses pattern matching and spaCy NLP 
|   |                                # for review parsing & facility tagging
│   └── prototype.py                 # Initial CLI proof-of-concept
│
└── public/                          # Frontend files
    └── index.html
```

## Installation and Execution Instructions

### Prerequisites
Ensure the following are installed:
* Python 3.12.6 or higher
```
python --version
```
* Git
```
git --version
```
* PostgreSQL 14+ (Running locally on port 5432)
* Google Places API Key (with Places (New) API enabled)

### Clone the Repository
```
git clone https://github.com/SabeehaMalikah/Masjid_Navigator.git
cd Masjid_Navigator
```

### Install Requirements
1. Install packages
```
pip install -r requirements.txt
```
2. Download spaCy English language model
```
python -m spacy download en_core_web_sm
```

### Configure the Environment
1. Copy the template file to create your local `.env`
```
cp .env.example .env
```
2. Open `.env` and fill in your credentials:
```
GOOGLE_PLACES_API_KEY=your_google_places_api_key_here
DATABASE_URL=postgresql://masjid_navigator:your_password@localhost:5432/masjid_navigator_db
```

### Set up the database
1. Create the local database in PostgreSQL
```
CREATE DATABASE masjid_navigator_db WITH ENCODING = 'UTF8';
```

2. Populate the database
```
python scripts/populate_mosque_table.py
python scripts/populate_review_table.py
python scripts/populate_facilities_table.py
```



