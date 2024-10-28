# Google Auto-Complete Enhancement
This project enhances the Google search experience by implementing an intelligent auto-complete feature. The system leverages a repository of articles, documentation, and technical files to provide relevant sentence completions for user queries.

### 📖 Project Overview
The system operates in two main phases:

### 1. Offline Phase (Initialization)
 * Prepares and structures a collection of text sources containing sentences to create an optimized, searchable index.
 * Uses an inverted index to map words to their occurrences across text sources, allowing quick sentence retrieval based on user input.
 * **Thread Pool for Concurrent File Reading**: A thread pool is implemented to read files concurrently, significantly reducing loading times when processing large datasets.
 * Checksum Validation: A checksum file is generated during initialization to track changes in the source data:
   * **No Change Detected**: Loads existing inverted indexes, skipping re-indexing.
   * **Change Detected**: Rebuilds inverted indexes to reflect the updated data.
### 2. Online Phase (Completion)
 * Uses the Levenshtein algorithm for fuzzy matching, allowing the system to suggest relevant completions even with minor spelling errors or typos in user input.
 * Returns the top five sentence completions based on relevance, proximity to input, and minor correction handling.
### 🔍 Core Components
### 🗂 Inverted Index
 * Allows fast lookup by associating each word with its position across multiple files and sentences.
 * Facilitates efficient searching, especially in large datasets, by rapidly retrieving possible matches.
### 🧵 Thread Pool for Faster File I/O
 * Enables concurrent file reading in the offline phase, reducing time required to process files in large directories.
 * Enhances I/O performance by processing multiple files in parallel.
### 🔒 Checksum Validation for Data Integrity
 * A checksum file is created to track data changes and prevent redundant indexing.
 * On each initialization, the checksum is checked:
  * No Data Changes: Loads the existing index.
  * Data Changes Detected: Rebuilds the inverted indexes to update the data structure.
### 🧮 Levenshtein Distance Algorithm
 * Calculates the minimum number of edits (insertions, deletions, substitutions) to transform the input text to match stored sentences.
 * Allows fuzzy matching, enabling suggestions despite minor input variations.
### 🛠️ Development Methodology
The project is designed for scalability and efficiency:

 * Data Processing: Text files, stored in nested directories, are processed into an inverted index with concurrent file loading (thread pool) and checksum validation to streamline initialization.
 * Interactive Query Interface: Continuously suggests completions as the user types, with suggestions ranked by relevance.
### ⚙️ Program Workflow
### Offline Initialization
 * Reads and indexes text sources using a thread pool for optimized file reading.
 * Validates data integrity with checksum validation to determine whether to reuse or rebuild the index.
### Interactive Query Mode
 * Waits for user input and provides real-time suggestions for the best sentence completions.
### 📦 Getting Started
To run the project:

### Clone the repository:
Copy code

```bash
git clone https://github.com/matanyaki/Google-Project.git
```
### Run the program:
Copy code

```bash
python main.py
```
The program will initialize and enter the interactive query mode, providing auto-complete suggestions based on user input.
### 🧩 Technologies Used
 * Python for core functionality and the auto-complete feature.
 * Levenshtein Algorithm for fuzzy matching and scoring.
 * Inverted Index for efficient text storage and search.
 * Thread Pool for concurrent file reading during initialization.
 * Checksum Validation for data integrity, ensuring efficient indexing by detecting changes in the data files.
### 🚀 Future Enhancements
 * Add additional scoring algorithms to improve the relevance of suggestions.
 *Implement advanced parallel processing techniques to further optimize performance for large datasets.
