import os

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

actual_key = os.getenv('key')
print(actual_key)