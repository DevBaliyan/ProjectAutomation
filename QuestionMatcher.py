##import json
##import unicodedata
##import difflib
##
### Load JSON data
##with open('Ques.json', 'r', encoding='utf-8') as file:
##    data = json.load(file)
##
### Function to normalize and clean text
##def normalize_text(text):
##    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if c.isascii())  # ASCII only
##    text = text.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')  # Remove extra spaces
##    text = ' '.join(text.split())  # Collapse multiple spaces
##    # Remove non-alphabetic characters except spaces
##    return ''.join(c if c.isalpha() or c.isspace() else ' ' for c in text)
##
### Function to compute similarity between two strings
##def similarity(a, b):
##    return difflib.SequenceMatcher(None, a, b).ratio()
##
### Function to check partial match based on token overlap
##def partial_match(a, b, threshold=0.5):
##    a_tokens = set(a.split())
##    b_tokens = set(b.split())
##    common_tokens = a_tokens & b_tokens
##    overlap_ratio = len(common_tokens) / max(len(a_tokens), len(b_tokens))
##    return overlap_ratio >= threshold
##
### Function to find the best match for a given question
##def find_best_match(user_question, threshold=0.70, partial_threshold=0.5):
##    user_question = normalize_text(user_question)
##    best_match = None
##    best_score = 0
##
##    for item in data:
##        question = normalize_text(item['question'])
##        score = similarity(user_question, question)
##
##        # Allow partial matching if token overlap meets threshold
##        if partial_match(user_question, question, partial_threshold):
##            score = max(score, 0.9)  # Boost score for partial matches
##
##        if score > best_score:  # Always update for highest similarity
##            best_score = score
##            best_match = item
##
##    # Return match only if it meets the threshold or boosted partial match
##    return best_match if best_score >= threshold else None
##
##
##def find_best_match_opt(texts, keyword):#text=[] keyword=''
##    # Find the best match based on similarity ratio
##    matches = [(text, difflib.SequenceMatcher(None, text, keyword).ratio()) for text in texts]
##    best_match = max(matches, key=lambda x: x[1])
##    return best_match[0], best_match[1]
##
##
### Example usage
##if __name__ == "__main__":
##    user_question = input("Enter your question: ")
##    match = find_best_match(user_question)
##
##    if match:
##        print("Best Match Found:", match['question'])
##        print("Answer:", match['answer'])
##    else:
##        print("No suitable match found.")
##
##
##



import json
import unicodedata
import difflib

# Load JSON data
with open('Ques.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to normalize and clean text
def normalize_text(text):
    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if c.isascii())  # ASCII only
    text = text.lower().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')  # Remove extra spaces
    text = ' '.join(text.split())  # Collapse multiple spaces
    # Keep alphanumeric characters, spaces, and mathematical symbols
    return ''.join(c if c.isalnum() or c.isspace() or c in "+-*/()×−" else ' ' for c in text)


# Function to compute similarity between two strings
def similarity(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

# Function to check partial match based on token overlap
def partial_match(a, b, threshold=0.8):
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    common_tokens = a_tokens & b_tokens
    overlap_ratio = len(common_tokens) / max(len(a_tokens), len(b_tokens))
    return overlap_ratio >= threshold

# Function to find the best match for a given question
def find_best_match(user_question, threshold=0.85, partial_threshold=0.8):
    user_question = normalize_text(user_question)
    best_match = None
    best_score = 0

    for item in data:
        question = normalize_text(item['question'])
        score = similarity(user_question, question)

        # Allow partial matching if token overlap meets threshold
        if partial_match(user_question, question, partial_threshold):
            score = max(score, similarity(user_question, question))  # Keep the highest score

        if score > best_score:  # Always update for highest similarity
            best_score = score
            best_match = item
    print(best_score)#, user_question, question, sep="\n\n", end="\n\n\n")
    # Return match only if it meets the threshold
    matched =  best_match if best_score >= threshold else None
    if matched:
        print("Best Match Found:", match['question'])
        print("Answer:", match['answer'])
        return match['question']
    else:
        print("No suitable match found.")


# Function to find the best match based on similarity ratio for multiple texts
def find_best_match_opt(texts, keyword):
    matches = [(text, difflib.SequenceMatcher(None, text, keyword).ratio()) for text in texts]
    best_match = max(matches, key=lambda x: x[1])
    return best_match[0], best_match[1]


# Example usage
if __name__ == "__main__":
    from pyperclip import paste
    user_question = 'which of the following can replace the given underlined statement with a single word  abhishek is interested in reading books only and nothing else '
    ans = find_best_match(user_question)

