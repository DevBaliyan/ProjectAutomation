import sqlite3
import json
import difflib
import re


class DataManager:
    def __init__(self, db_name):
        """Initialize the DataManager with a database connection and create necessary tables."""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create tables for tests and questions if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                test_id INTEGER PRIMARY KEY,
                test_name TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY,
                test_id INTEGER,
                question TEXT,
                options TEXT,  -- Stored as JSON string
                answer TEXT,
                FOREIGN KEY (test_id) REFERENCES tests (test_id)
            )
        ''')
        self.conn.commit()


    def add_question(self, test_name, question, options, answer, force=False):
        """
        Add a question to the specified test, checking for duplicates and similarity.

        Args:
            test_name (str): Name of the test.
            question (str): The question text.
            options (list): List of option strings.
            answer (str): The correct answer (must be in options).
            force (bool): If True, add the question even if similar questions exist.

        Returns:
            tuple: (success: bool, message: str)
                - success: True if question was added, False otherwise.
                - message: Explanation of the outcome.
        """
        if answer not in options:
            raise ValueError("Answer must be one of the options")

        cursor = self.conn.cursor()

        # Get or create test_id
        cursor.execute("SELECT test_id FROM tests WHERE test_name = ?", (test_name,))
        row = cursor.fetchone()
        if row:
            test_id = row[0]
        else:
            cursor.execute("INSERT INTO tests (test_name) VALUES (?)", (test_name,))
            test_id = cursor.lastrowid

        # Check for duplicates and similar questions
        cursor.execute("SELECT question, options FROM questions WHERE test_id = ?", (test_id,))
        similar_questions = []
        options_set = set(options)

        for row in cursor.fetchall():
            db_question = row[0]
            db_options = json.loads(row[1])
            db_options_set = set(db_options)

            # Exact duplicate check
            if db_question.lower() == question.lower() and db_options_set == options_set:
                return False, "Exact duplicate found"

            # Similarity check with same options
            if db_options_set == options_set:
                similarity = difflib.SequenceMatcher(None, question.lower(), db_question.lower()).ratio()
                if similarity > 0.94:
                    similar_questions.append((db_question, similarity))

        if similar_questions and not force:
            msg = "Similar questions with same options found:\n"
            for q, sim in similar_questions:
                msg += f"- {q} (similarity: {sim:.2f})\n"
            return False, msg

        # Add the question
        options_json = json.dumps(options)
        cursor.execute("INSERT INTO questions (test_id, question, options, answer) VALUES (?, ?, ?, ?)",
                       (test_id, question, options_json, answer))
        self.conn.commit()
        return True, f"Added"


    def get_similar_question(self, test_name, query_question, query_options=None, threshold=0.85):
        cursor = self.conn.cursor()

        # Get test_id
        cursor.execute("SELECT test_id FROM tests WHERE test_name = ?", (test_name,))
        row = cursor.fetchone()
        if not row:
            return None  # Test does not exist

        test_id = row[0]

        # Normalize query question and options
        query_question_norm = query_question.replace("\n", "").replace("\r", "").strip().lower()

        if query_question:
            query_options_set = set(query_options)  # Convert to set for order-independent comparison

            # Fetch all questions from the test
            cursor.execute("SELECT question, options, answer FROM questions WHERE test_id = ?", (test_id,))
            best_match = None
            highest_similarity = threshold

            for db_question, db_options_json, db_answer in cursor.fetchall():
                db_question_norm = db_question.replace("\n", "").replace("\r", "").strip().lower()
                db_options = json.loads(db_options_json)
                db_options_set = set(db_options)

                # Check if options match (irrespective of order)
                if query_options_set == db_options_set:
                    # Only calculate similarity if options match
                    similarity = difflib.SequenceMatcher(None, query_question_norm, db_question_norm).ratio()
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = {
                            "question": db_question,
                            "options": db_options,
                            "answer": db_answer,
                            "similarity": similarity
                        }
            

        return best_match

    def getSimilar(self, query_question, threshold=0.85):
        cursor = self.conn.cursor()
        query_question_norm = query_question#.replace("\n", "").replace("\r", "").strip().lower()

        # Fetch all questions from the test
        cursor.execute("SELECT question, options, answer FROM questions")
        best_match = None
        highest_similarity = threshold
        for db_question, db_options_json, db_answer in cursor.fetchall():
            db_question_norm = db_question#.replace("\n", "").replace("\r", "").strip().lower()
            db_options = json.loads(db_options_json)
            db_options_set = set(db_options)
            similarity = difflib.SequenceMatcher(None, query_question_norm, db_question_norm).ratio()
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = {
                    "question": db_question,
                    "options": db_options,
                    "answer": db_answer,
                    "similarity": similarity
                }

        return best_match

    def getAllSimilar(self, query_question, threshold=0.90):
        cursor = self.conn.cursor()
        query_question_norm = query_question#.replace("\n", "").replace("\r", "").strip().lower()

        # Fetch all questions from the test
        cursor.execute("SELECT question, options, answer FROM questions")
        best_match = None
        list_sim = []
        for db_question, db_options_json, db_answer in cursor.fetchall():
            db_question_norm = db_question#.replace("\n", "").replace("\r", "").strip().lower()
            db_options = json.loads(db_options_json)
            db_options_set = set(db_options)
            similarity = difflib.SequenceMatcher(None, query_question_norm, db_question_norm).ratio()
            if similarity > threshold:
                match = {
                    "question": db_question,
                    "options": db_options,
                    "answer": db_answer,
                    "similarity": similarity
                }
                list_sim.append(match)

        return list_sim

    
    def close(self):
        """Close the database connection."""
        self.conn.close()



def extract_test_name(test):
    match = re.search(r'Test \d+ : \[(.+)\] (.+)', test)
    return match.group(1)+" "+match.group(2)[:-2] if match else None


def ques_only(text):
    out = text.split('Options:\n')[0].replace('\n', '').replace("  ", "")
    return out if len(out)!=len(text) else None


def extract_options(options):
    """
    Extracts options labeled A:, B:, etc., while preserving indexing.
    Handles empty options, removes extra spaces, and ensures correct formatting.
    """
    # Find all option labels
    pattern = r'([A-E]:)'
    matches = list(re.finditer(pattern, options))
    if not matches:
        return []
    
    # Extract options by processing each label and the text up to the next label or end
    result = []
    for i in range(len(matches)):
        label = matches[i].group(1)  # e.g., "A:"
        start = matches[i].end()     # Position after the label
        # End is the start of the next label or the end of the string
        end = matches[i + 1].start() if i + 1 < len(matches) else len(options)
        value = options[start:end].strip()  # Get and clean the value
        # Append label alone if value is empty, otherwise label + space + value
        option = value#label + (" " + value if value else "")
        result.append(option.replace('\n', '').replace("  ", ""))
    
    return result



#print("Executed")
