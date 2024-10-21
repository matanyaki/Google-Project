from src import InvertedIndexes

if __name__ == '__main__':
    print("Loading the files and preprocessing data...")

    zip_file_path = 'Archive.zip'
    output_directory = 'extracted_files'

    inverted_index_file = 'inverted_index.pickle'  # Where to store the inverted index
    checksum_file = 'checksum.txt'  # Where to store the checksum

    # Step 1: Extract .txt files from the zip archive
    InvertedIndexes.extract_txt_files(zip_file_path, output_directory)

    # Step 2: Load or build the inverted index
    inverted_index = InvertedIndexes.load_or_build_inverted_index(zip_file_path, output_directory, inverted_index_file, checksum_file)

    print("The system is ready , Ready to be amazed!!!")
    user_input = input("Enter your text: ")
    while(user_input != "exit"):
        # Step 3: Search for a word or sentence
        search_term = 'concepts'  # This can be a single word or an entire sentence
        InvertedIndexes.search_phrase_with_scores(user_input, inverted_index, output_directory)
        user_input = input("Enter your text: ")


    # def calculate_score(user_input, match_candidate):
    #     # Initialize the score based on twice the number of characters in the user input
    #     base_score = 2 * len(user_input)
    #
    #     # If the user input is fully contained in the match candidate, return the base score
    #     if user_input in match_candidate:
    #         return base_score
    #
    #     # Calculate the Levenshtein distance and apply the custom scoring rules
    #     len_input = len(user_input)
    #     len_candidate = len(match_candidate)
    #
    #     # Create a matrix to store distances
    #     dp = [[0 for _ in range(len_candidate + 1)] for _ in range(len_input + 1)]
    #
    #     # Initialize the matrix
    #     for i in range(len_input + 1):
    #         dp[i][0] = i
    #     for j in range(len_candidate + 1):
    #         dp[0][j] = j
    #
    #     # Fill the matrix
    #     for i in range(1, len_input + 1):
    #         for j in range(1, len_candidate + 1):
    #             if user_input[i - 1] == match_candidate[j - 1]:
    #                 dp[i][j] = dp[i - 1][j - 1]
    #             else:
    #                 dp[i][j] = min(
    #                     dp[i - 1][j] + 1,  # Deletion
    #                     dp[i][j - 1] + 1,  # Insertion
    #                     dp[i - 1][j - 1] + 1  # Substitution
    #                 )
    #
    #     # The Levenshtein distance
    #     lev_distance = dp[len_input][len_candidate]
    #
    #     # Calculate the score based on the penalties
    #     score = base_score
    #     i, j = len_input, len_candidate
    #
    #     while i > 0 or j > 0:
    #         if i > 0 and j > 0 and user_input[i - 1] == match_candidate[j - 1]:
    #             i -= 1
    #             j -= 1
    #         elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
    #             # Substitution penalty
    #             penalty = 5 if i == 1 else 4 if i == 2 else 3 if i == 3 else 2 if i == 4 else 1
    #             score -= penalty
    #             i -= 1
    #             j -= 1
    #         elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
    #             # Deletion penalty
    #             penalty = 10 if i == 1 else 8 if i == 2 else 6 if i == 3 else 4 if i == 4 else 2
    #             score -= penalty
    #             i -= 1
    #         elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
    #             # Insertion penalty
    #             penalty = 10 if j == 1 else 8 if j == 2 else 6 if j == 3 else 4 if j == 4 else 2
    #             score -= penalty
    #             j -= 1
    #
    #     return score
    #
    #
    # # Example usage
    # user_input = "this is"
    # candidates = ["this is a test", "ths is", "thiss is", "this is good", "thiz is"]
    #
    # # Calculate scores for each candidate
    # scores = [(candidate, calculate_score(user_input, candidate)) for candidate in candidates]
    #
    # # Sort candidates by score in descending order and get the top 5
    # best_matches = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
    #
    # # Print the best matches
    # for match, score in best_matches:
    #     print(f"Match: {match}, Score: {score}")