import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
def GeminiAPI(user_input: str):

    prompt_api = f"Use this sentence '{user_input}' to create five sentences that contain it."
    response = model.generate_content(prompt_api)

    print("---Five sentences generate by Gemini API---\n")
    # Check and print the response content
    if response and hasattr(response, 'text'):
        # Extract the relevant sentences from the response
        generated_sentences = response.text.split('\n')

        for line in generated_sentences:
            # Filter out empty lines or lines that do not contain the actual content
            line = line.strip()
            if line and not line.isdigit() and not line.startswith("Here are five sentences"):
                print(line)
    else:
        print("No response generated.")

if __name__ == "__main__":
    print("Welcome to the Gemini API...\n")
    user_input = input("Enter your sentence to complete (or type 'exit' to quit): ")
    while user_input != "exit":
        GeminiAPI(user_input)
        user_input = input("\nEnter your sentence to complete (or type 'exit' to quit): ")