import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_openai_connection():
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'OpenAI connection successful!' if you can read this message."}
            ]
        )
        print(response.choices[0].message.content)
        print("Test completed successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Test failed.")

if __name__ == "__main__":
    test_openai_connection()