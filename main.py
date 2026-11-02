import os
import sys
from dotenv import load_dotenv

# Ensure UTF-8 output encoding for emojis and multilingual text on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env
load_dotenv()

from sarvamai import SarvamAI

# Initialize the Sarvam AI client (reads SARVAM_API_KEY from environment)
client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

# Chat completion call with sarvam-105b-conversations
response = client.chat.completions(
    messages=[
        {"role": "user", "content": "Hello! Please reply with a brief greeting."}
    ],
    model="sarvam-105b-conversations",
)

# Print the reply
print(response.choices[0].message.content)
