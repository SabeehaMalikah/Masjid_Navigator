import os
import re
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")



def build_database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS facilities (
        id BIGSERIAL primary key,
        google_places_id VARCHAR(50),
        has_womens_section BOOLEAN,
        nlp_verified BOOLEAN,
        CONSTRAINT fk_facilities_mosque FOREIGN KEY (google_places_id) REFERENCES mosque(google_places_id) ON DELETE CASCADE
    );
    ''')


def populate_database(cursor):
    query = ''' INSERT INTO facilities(google_places_id, has_womens_section, nlp_verified) 
    VALUES(%s, %s, %s);
    '''

    cursor.execute('''SELECT google_places_id, review_text FROM review''')
    reviews_list = cursor.fetchall()
    reviews_dict = dict()
    for id, review in reviews_list:
        if id in reviews_dict:
            reviews_dict[id].append(review)
        else:
            reviews_dict[id] = []
            reviews_dict[id].append(review)

    pattern = r"\bwom[ae]n'?s?'?|\bsister'?s?'?|ladies|female"

    for google_places_id, rlist in reviews_dict.items():
        has_womens_section = False
        for r in rlist:
            if r:
                if re.search(pattern, r.lower()):
                    has_womens_section = True
        cursor.execute(query, (
        google_places_id,
        has_womens_section,
        False
        ))




# main
connection = psycopg2.connect(
    db_url,
    options="-c client_encoding=utf8"
)
connection.set_client_encoding('UTF8')
cursor = connection.cursor()
build_database(cursor)
populate_database(cursor)
connection.commit()
cursor.close()
connection.close()

