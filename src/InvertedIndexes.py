import hashlib
import os
import re
import zipfile
from collections import defaultdict
import pickle
from concurrent.futures import ThreadPoolExecutor
import heapq

def compute_file_checksum(file_path):
    """
    Computes the SHA-256 checksum of the specified file to detect changes.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
def extract_txt_files(zip_file_path, output_directory):
    """
    Extracts all .txt files from the ZIP archive, including those in subdirectories.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.txt') and not file_info.is_dir():
                extract_path = os.path.join(output_directory, file_info.filename)
                os.makedirs(os.path.dirname(extract_path), exist_ok=True)
                with open(extract_path, 'wb') as f:
                    f.write(zip_ref.read(file_info.filename))


def build_inverted_index(directory):
    """
    Builds an inverted index for words and sentences from all .txt files in the specified directory.
    """
    inverted_index = defaultdict(list)  # {word_or_sentence: [(filename, line_number), ...]}
    word_pattern = re.compile(r'\b\w+\b')  # Pattern to match words

    # Walk through all .txt files in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                base_filename = os.path.relpath(file_path, directory)  # Relative path
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    line_number = 1
                    for line in file:
                        #line = normalize_text(line)
                        line = line.strip().lower()
                        # Index each word in the line
                        words = word_pattern.findall(line)
                        for word in words:
                            inverted_index[word].append((base_filename, line_number))

                        # Index the entire sentence (line) for sentence search
                        if line:  # Ensure line is not empty
                            inverted_index[line].append((base_filename, line_number))

                        line_number += 1
    return inverted_index


def search_inverted_index(query, inverted_index, directory):
    """
    Searches for a word or sentence in the inverted index and returns all occurrences.
    """
    query = query.lower().strip()
    results = inverted_index.get(query, [])
    if not results:
        print(f"'{query}' not found.")
        return

    print(f"Occurrences of '{query}':")
    for filename, line_number in results:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for current_line_num, line in enumerate(file, start=1):
                if current_line_num == line_number:
                    print(f"File: {filename}, Line {line_number}: {line.strip()}")
                    break
    #return inverted_index.get(query, [])


def load_or_build_inverted_index(zip_file_path, extracted_files_directory, inverted_index_file, checksum_file):
    """
    Loads the inverted index if it exists and the data hasn't changed.
    Otherwise, rebuilds the index and stores it.
    """
    # Compute the checksum of the ZIP file
    current_checksum = compute_file_checksum(zip_file_path)

    # Check if inverted index and checksum files exist
    if os.path.exists(inverted_index_file) and os.path.exists(checksum_file):
        with open(checksum_file, 'r') as f:
            stored_checksum = f.read()

        # If the checksum matches, load the existing inverted index
        if stored_checksum == current_checksum:
            print("Checksum matches. Loading existing inverted index.")
            with open(inverted_index_file, 'rb') as f:
                return pickle.load(f)

    # Otherwise, build the inverted index from scratch
    print("Data has changed or no index exists. Building a new inverted index.")
    inverted_index = build_inverted_index(extracted_files_directory)

    # Store the newly built inverted index
    with open(inverted_index_file, 'wb') as f:
        pickle.dump(inverted_index, f)

    # Store the current checksum
    with open(checksum_file, 'w') as f:
        f.write(current_checksum)

    return inverted_index


def process_file_for_phrase(filename, line_numbers, phrase, directory):
    """
    Process a file to check if the phrase appears in the specified lines.
    Returns a list of (filename, line_number, original_line) for matching lines.
    """
    results = []
    file_path = os.path.join(directory, filename)

    # Read the entire file at once
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for line_number in line_numbers:
            if line_number <= len(lines):
                original_line = lines[line_number - 1].strip()
                normalized_line = normalize_text(original_line)
                if check_consecutive_words(normalized_line, phrase):
                    results.append((filename, line_number, original_line))

    return results

def calculate_score(user_input, match_candidate):
    # Initialize the score based on twice the number of characters in the user input
    base_score = 2 * len(user_input)
    #print(f"Calculating score for user_input: '{user_input}' and match_candidate: '{match_candidate}'")

    # If the user input is fully contained in the match candidate, return the base score
    if user_input in match_candidate:
        #print(f"User input is fully contained in match candidate. Score: {base_score}")
        return base_score

    # Calculate the Levenshtein distance and apply the custom scoring rules
    len_input = len(user_input)
    len_candidate = len(match_candidate)

    # Create a matrix to store distances
    dp = [[0 for _ in range(len_candidate + 1)] for _ in range(len_input + 1)]

    # Initialize the matrix
    for i in range(len_input + 1):
        dp[i][0] = i
    for j in range(len_candidate + 1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, len_input + 1):
        for j in range(1, len_candidate + 1):
            if user_input[i - 1] == match_candidate[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Deletion
                    dp[i][j - 1] + 1,  # Insertion
                    dp[i - 1][j - 1] + 1  # Substitution
                )

    # The Levenshtein distance
    lev_distance = dp[len_input][len_candidate]
    #print(f"Levenshtein distance: {lev_distance}")

    # Calculate the score based on the penalties
    score = base_score
    i, j = len_input, len_candidate

    while i > 0 or j > 0:
        if i > 0 and j > 0 and user_input[i - 1] == match_candidate[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Substitution penalty
            penalty = 5 if i == 1 else 4 if i == 2 else 3 if i == 3 else 2 if i == 4 else 1
            score -= penalty
            #print(f"Substitution penalty for character '{user_input[i - 1]}'. Penalty: {penalty}, New Score: {score}")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Deletion penalty
            penalty = 10 if i == 1 else 8 if i == 2 else 6 if i == 3 else 4 if i == 4 else 2
            score -= penalty
            #print(f"Deletion penalty for character '{user_input[i - 1]}'. Penalty: {penalty}, New Score: {score}")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Insertion penalty
            penalty = 10 if j == 1 else 8 if j == 2 else 6 if j == 3 else 4 if j == 4 else 2
            score -= penalty
            #print(f"Insertion penalty for character '{match_candidate[j - 1]}'. Penalty: {penalty}, New Score: {score}")
            j -= 1

    #print(f"Final score for user_input: '{user_input}' and match_candidate: '{match_candidate}' is {score}")
    return score


def search_phrase_with_scores(phrase, inverted_index, directory):
    """
    Searches for a phrase in the inverted index, returning the top 5 best matches based on a scoring system.
    """
    normalized_phrase = normalize_text(phrase)
    words = normalized_phrase.split()  # Split the phrase into individual words

    if not words:
        print(f"No words to search for in phrase: '{phrase}'")
        return

    # Get occurrences for each word in the phrase from the inverted index
    word_occurrences = [set(inverted_index.get(word, [])) for word in words]
    #print(f"Word occurrences: {word_occurrences}")

    if not all(word_occurrences):
        # If any word is not found, try to find the best possible match for each missing word
        corrected_words = []
        top_matches = []
        for word, occurrences in zip(words, word_occurrences):
            if occurrences:
                corrected_words.append(word)
            else:
                # Find the best match for the missing word by trying substitutions, additions, and deletions
                print(f"Finding best matches for missing word: '{word}'")
                possible_matches = []
                for candidate in inverted_index.keys():
                    # Filter candidates by length to reduce unnecessary calculations
                    if abs(len(word) - len(candidate)) > 1:
                        continue
                    lev_distance = calculate_levenshtein_distance(word, candidate)
                    if lev_distance <= 1:  # Allow one character difference
                        score = calculate_score(word, candidate)
                        heapq.heappush(possible_matches, (-score, candidate))

                # Get the top 5 best matches
                best_candidates = heapq.nsmallest(5, possible_matches)
                for _, best_candidate in best_candidates:
                    corrected_words.append(best_candidate)
                    print(f"Best match for word '{word}': '{best_candidate}'\n")
                    break
                else:
                    corrected_words.append(word)
                    print(f"No suitable match found for word '{word}', using original word.")

        # Update the phrase with corrected words
        normalized_phrase = " ".join(corrected_words)
        words = corrected_words
        word_occurrences = [set(inverted_index.get(word, [])) for word in words]
        #print(f"Corrected phrase: '{normalized_phrase}'")

    # Find the intersection of all word occurrences (i.e., same file and line)
    common_occurrences = word_occurrences[0]
    for word_occ in word_occurrences[1:]:
        common_occurrences &= word_occ
    #print(f"Common occurrences: {common_occurrences}")

    # Group common occurrences by filename
    occurrences_by_file = defaultdict(list)
    for filename, line_number in common_occurrences:
        occurrences_by_file[filename].append(line_number)
    #print(f"Occurrences grouped by file: {occurrences_by_file}")

    final_results = []

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file_for_phrase, filename, line_numbers, normalized_phrase, directory)
                   for filename, line_numbers in occurrences_by_file.items()]

        for future in futures:
            result = future.result()
            final_results.extend(result)

    # Calculate scores for each result
    scores = [(filename, line_number, line, calculate_score(phrase, line)) for filename, line_number, line in
              final_results]

    # Sort results by score in descending order and get the top 5
    best_matches = sorted(scores, key=lambda x: x[3], reverse=True)[:5]

    if best_matches:
        print(f"Top matches for phrase '{phrase}':\n")
        for filename, line_number, line, score in best_matches:
            print(f"File: {filename}, Line {line_number}, Score: {score}:, line: {line}")
    else:
        print(f"'{phrase}' not found with words in consecutive order.")


def calculate_levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0 for _ in range(len_s2 + 1)] for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + 1,  # Deletion
                    dp[i][j - 1] + 1,  # Insertion
                    dp[i - 1][j - 1] + 1  # Substitution
                )

    return dp[len_s1][len_s2]


def check_consecutive_words(line, phrase):
    """
    Checks if the phrase appears consecutively in the line.
    This method normalizes both the line and the phrase before matching.
    """
    # Normalize both the line and the phrase
    normalized_line = normalize_text(line)
    normalized_phrase = normalize_text(phrase)

    # Check if the normalized phrase appears in the normalized line
    return normalized_phrase in normalized_line

def normalize_text(text):
    """
    Normalizes the text by:
    1. Removing punctuation (e.g., ,./).
    2. Collapsing multiple spaces into a single space.
    3. Converting to lowercase for case-insensitive comparison.
    """
    # Remove punctuation and collapse spaces
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip().lower()