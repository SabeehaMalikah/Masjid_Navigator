import os
import re
import psycopg2
import spacy
from dotenv import load_dotenv

# Script to build and populate the facilities table in the database.

load_dotenv()

db_url = os.getenv("DATABASE_URL")

nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

def build_database(cursor):
    '''
    Creates the facilities table in the database if it does not already exist.
    
    The table includes columns for the facility ID, Google Places ID, whether it has a women's section,
    and whether the information has been verified using NLP.
    
    It also establishes a foreign key relationship with the mosque table based on the Google Places ID.

    parameters:
        cursor (psycopg2.cursor): The database cursor used to execute SQL commands.

    returns:
        None
    '''

    cursor.execute('''CREATE TABLE IF NOT EXISTS facilities (
        id BIGSERIAL primary key,
        google_places_id VARCHAR(50),
        has_womens_section BOOLEAN,
        nlp_verified BOOLEAN,
        CONSTRAINT fk_facilities_mosque FOREIGN KEY (google_places_id) REFERENCES mosque(google_places_id) ON DELETE CASCADE
    );
    ''')

def check_womens_section(review, nlp):
    '''
    Checks if a review mentions the presence of a women's section using NLP.
    
    The function uses regular expressions to identify keywords related to women's sections
    and negation patterns to determine if the mention is negated.

    parameters:
        review (str): The review text to be analyzed.
        nlp (spacy.lang.en.English): The SpaCy NLP pipeline used for sentence segmentation.

    returns:
        bool: True if the review indicates the presence of a women's section, False otherwise.
    '''

    '''
    Code Review
    
    Current issues:
    - The function may produce false positives if negation patterns are not correctly identified.
    - It does not account for complex sentence structures where the mention of a women's section is implied rather than explicitly stated.
    - The regular expressions may not cover all possible variations of referring to women's sections.

    Resolved Issues:
    - The function now uses sentence segmentation to better handle complex sentence structures.
    - Negation patterns are checked within each sentence to reduce false positives.
    - The regular expressions have been refined to cover more variations of referring to women's sections and include negation patterns.
    '''

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
    '''
    Populates the facilities table in the database with information about women's sections.
    
    The function retrieves reviews from the review table, analyzes them using NLP to determine
    if they mention the presence of a women's section, and inserts the results into the facilities table.

    parameters:
        cursor (psycopg2.cursor): The database cursor used to execute SQL commands.
        nlp (spacy.lang.en.English): The SpaCy NLP pipeline used for sentence segmentation.

    returns:
        None
    '''

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

def main():
    '''
    Main function to build and populate the facilities table in the database.
    '''
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

main()

