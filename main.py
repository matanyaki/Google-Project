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
