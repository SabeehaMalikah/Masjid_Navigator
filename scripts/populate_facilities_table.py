import os
import re
import psycopg2
import spacy
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

def build_database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS facilities (
        id BIGSERIAL primary key,
        google_places_id VARCHAR(50),
        has_womens_section BOOLEAN,
        nlp_verified BOOLEAN,
        CONSTRAINT fk_facilities_mosque FOREIGN KEY (google_places_id) REFERENCES mosque(google_places_id) ON DELETE CASCADE
    );
    ''')

def check_womens_section(review, nlp):
    review = review.lower()
    has_womens_section = False
    womens_patterns = r"\bwom[ae]n'?s?'?|\bsister'?s?'?|ladies|female"
    neg_patterns = r"\bno\b|\bnot\b|\bdoes not\b|\bdoesn't|\bthere is no\b"

    doc = nlp(review)
    for sentence in doc.sents:
        if re.search(womens_patterns, sentence.text):
            has_womens_section = True
            if re.search(neg_patterns, sentence.text):
                has_womens_section = False

    return has_womens_section

def populate_database(cursor, nlp):
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

    for google_places_id, rlist in reviews_dict.items():
        has_womens_section = False
        for r in rlist:
            if r:
                has_womens_section = check_womens_section(r, nlp)
                if has_womens_section:
                    break
        cursor.execute(query, (
        google_places_id,
        has_womens_section,
        True
        ))

# main
connection = psycopg2.connect(
    db_url,
    options="-c client_encoding=utf8"
)
connection.set_client_encoding('UTF8')
cursor = connection.cursor()

build_database(cursor)
populate_database(cursor, nlp)

connection.commit()
cursor.close()
connection.close()

