# Google Auto-Complete Enhancement
This project enhances the Google search experience by implementing an intelligent auto-complete feature. The system leverages a repository of articles, documentation, and technical files to provide relevant sentence completions for user queries.Part 2 includes personalization, allowing the system to tailor suggestions based on user search history with integration to Google’s LLM tools.

### 📖 Overview
The project operates in two main parts:
 * Part 1: General auto-complete that provides quick, relevant sentence completions based on a static dataset.
 * Part 2: Personalized auto-complete that adapts suggestions to individual user preferences by leveraging Google’s Gemini LLM API, enabling a tailored search experience.
### 📦 Getting Started
To get started, clone the repository and follow the instructions for each part.

**Clone the repository**:
```
bash
Copy code
git clone https://github.com/matanyaki/Google-Project.git
```
### Part 1: General Auto-Complete
Navigate to the Part 1 directory:
```
bash
Copy code
cd src
```
Run the general auto-complete program:
```
bash
Copy code
python main.py
```
This will initialize the system and provide auto-complete suggestions based on the dataset.

### Part 2: Personalized Auto-Complete with LLM
Navigate to the Part 2 directory:
```
bash
Copy code
cd LLM
```
Run the personalized auto-complete program:
```
bash
Copy code
python GeminiAPI.py
```
This will connect to Google’s Gemini API to provide auto-complete suggestions customized to individual user history.

### 🧩 Technologies Used
 * Python: Core functionality for both parts.
 * Inverted Index and Levenshtein Algorithm: Fast and flexible matching and retrieval.
 * Thread Pooling and Checksum Validation: Efficient data loading and indexing.
 * Gemini API: For personalized, LLM-based completions.
### 🚀 Future Enhancements
 * Add more advanced scoring algorithms for relevance.
 * Scale parallel processing to support high-demand scenarios.
