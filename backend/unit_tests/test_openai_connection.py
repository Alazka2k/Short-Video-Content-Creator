# backend/unit_tests/test_openai_connection.py

import unittest
import os
from dotenv import load_dotenv
from openai import OpenAI

class TestOpenAIConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def test_openai_connection(self):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'OpenAI connection successful!' if you can read this message."}
                ]
            )
            self.assertIn("OpenAI connection successful!", response.choices[0].message.content)
            print("OpenAI connection test passed.")
        except Exception as e:
            self.fail(f"OpenAI connection test failed: {str(e)}")

if __name__ == "__main__":
    unittest.main()