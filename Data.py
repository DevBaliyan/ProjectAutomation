import sqlite3
import json
import difflib
import re

class DataManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.createTables()

    def createTables(self):
        """Create tables for tests and questions if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                test_id VARCHAR PRIMARY KEY,
                test_name TEXT UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY,
                test_id VARCHAR,
                question TEXT,
                options TEXT,  -- Stored as JSON string
                answer TEXT,
                FOREIGN KEY (test_id) REFERENCES tests (test_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questionsV2 (
                question_id VARCHAR PRIMARY KEY,
                test_id VARCHAR,
                question TEXT,
                options TEXT,  -- Stored as JSON string
                answer TEXT,
                FOREIGN KEY (test_id) REFERENCES tests (test_id)
            )
        ''')
        self.conn.commit()

    def addQuestionFromSummary(self, question, options, answer, test_id, test_name):
        if answer not in options:
            raise ValueError("Answer must be one of the options")

        cursor = self.conn.cursor()

        # Get or create test_id
        cursor.execute("SELECT test_id FROM tests WHERE test_id = ?", (test_id,))
        row = cursor.fetchone()
        if row:
            test_id = row[0]
        else:
            cursor.execute("INSERT INTO tests (test_id, test_name) VALUES (?, ?)", (test_id, test_name,))
            #test_id = cursor.lastrowid
            print('New Table Added')

        # Check for duplicates and similar questions
        cursor.execute("SELECT question, options FROM questions WHERE test_id = ?", (test_id,))
        similar_questions = []
        options_set = set(options)

        for row in cursor.fetchall():
            db_question = row[0]
            db_options = json.loads(row[1])
            db_options_set = set(db_options)

            # Exact duplicate check
            #print(db_options_set, options_set)
            if db_question.lower() == question.lower() and db_options_set == options_set:
                return False#, "Exact duplicate found"

            # Similarity check with same options
            if db_options_set == options_set:
                similarity = difflib.SequenceMatcher(None, question.lower(), db_question.lower()).ratio()
                if similarity > 0.96:
                    similar_questions.append((db_question, similarity))

        if similar_questions:
            msg = "Similar questions with same options found:\n"
            for q, sim in similar_questions:
                msg += f"- {q} (similarity: {sim:.2f})\n"
            return False#, msg

        # Add the question
        options_json = json.dumps(options)
        cursor.execute("INSERT INTO questions (test_id, question, options, answer) VALUES (?, ?, ?, ?)",
                       (test_id, question, options_json, answer))
        self.conn.commit()
        return True#, f"Added"


    def addQuestion(self, question, options, answer, test_id, test_name, question_id=None):
        if answer not in options:
            raise ValueError("Answer must be one of the options")

        cursor = self.conn.cursor()

        # Get or create test_id
        cursor.execute("SELECT test_id FROM tests WHERE test_id = ?", (test_id,))
        row = cursor.fetchone()
        if row:
            test_id = row[0]
        else:
            cursor.execute("INSERT INTO tests (test_id, test_name) VALUES (?, ?)", (test_id, test_name,))
            #test_id = cursor.lastrowid
            print('New Table Added')

        # Check for duplicates and similar questions
        cursor.execute("SELECT question, options FROM questionsV2 WHERE test_id = ?", (test_id,))
        similar_questions = []
        options_set = set(options)

        for row in cursor.fetchall():
            db_question = row[0]
            db_options = json.loads(row[1])
            db_options_set = set(db_options)

            # Exact duplicate check
            #print(db_options_set, options_set)
            if db_question.lower() == question.lower() and db_options_set == options_set:
                return False#, "Exact duplicate found"

            # Similarity check with same options
            if db_options_set == options_set:
                similarity = difflib.SequenceMatcher(None, question.lower(), db_question.lower()).ratio()
                if similarity > 0.95:
                    similar_questions.append((db_question, similarity))

        if similar_questions:#Change
            msg = "Similar questions with same options found:\n"
            for q, sim in similar_questions:
                msg += f"- {q} (similarity: {sim:.2f})\n"
            return False#, msg

        # Add the question
        options_json = json.dumps(options)
        if not question_id:
            cursor.execute("INSERT INTO questionsV2 (test_id, question, options, answer) VALUES (?, ?, ?, ?)",
                           (test_id, question, options_json, answer))
        else:
            cursor.execute("INSERT INTO questionsV2 (test_id, question_id, question, options, answer) VALUES (?, ?, ?, ?, ?)",
                           (test_id, question_id, question, options_json, answer))
        self.conn.commit()
        return True#, f"Added"


    def fetchQuestionByTestName(self, question, options, test_name):
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT test_id FROM tests WHERE test_name = ?", (test_name,))
        for  test_id in cursor.fetchall():
            print(test_id)

    def close(self):
        """Close the database connection."""
        self.conn.close()
            

##dm = DataManager('Trial.db')
##q = 'In a certain code language, the word ‘PHONE’ is written as ‘SERKH’. How will ‘SAMSUNG’ be written in that code?'
##o = ['VXPPXKJ', 'VXPQWKJ', 'VSPQXKJ', 'VXPPWKJ']
##a = 'VXPPXKJ'
##print(dm.addQuestion(q, o, a, '6634c4107e14581412fb5628', 'Random2'))
###sleep(2)
##print(dm.addQuestion(q, o, a, '6634c4107e14581412fb5628', 'Random2'))
###sleep(2)
##print(dm.addQuestion(q, o, a, '6634c4107e14581412fb5628', 'Random2'))
##
###sleep(2)
##print(dm.addQuestion(q, o, a, '6634c4107e14581412fb5628', 'Random2'))
##
###sleep(2)
##print(dm.addQuestionFromSummary(q, o, a, '6634c4107e14581412fb5628', 'Random2'))
##
##
