import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")



def build_database(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS review (
        id BIGSERIAL PRIMARY KEY,
        google_places_id VARCHAR(50),
        author VARCHAR(100),
        rating FLOAT,
        review_text TEXT,
        review_date TIMESTAMPTZ,
        CONSTRAINT fk_review_mosque FOREIGN KEY (google_places_id) REFERENCES mosque(google_places_id) ON DELETE CASCADE
    );
    ''')


def populate_database(cursor):
    query = ''' INSERT INTO review(google_places_id, author, rating, review_text, review_date) 
    VALUES(%s, %s, %s, %s, %s);
    '''

    cursor.execute('''SELECT google_places_id, reviews FROM mosque''')
    mosques_list = cursor.fetchall()

    for mosque in mosques_list:
        google_places_id = mosque[0]
        reviews = mosque[1]
        for review in reviews:
            author_attr = review.get("authorAttribution", {})
            author = author_attr.get("displayName") if isinstance(author_attr, dict) else None
            rating = review.get("rating")
            text = review.get("text", {})
            review_text = text.get("text") if isinstance(text, dict) else None
            review_date = review.get("publishTime")

            cursor.execute(query, (
            google_places_id,
            author,
            rating,
            review_text,
            review_date
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

