from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
from datetime import datetime
from dotenv import load_dotenv

#load .env values
load_dotenv()

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S-%f")

client = genai.Client(api_key=os.environ.get('GOOGLE_API_KEY'))

contents = ('Hi, can you create a 3d rendered image of a pig '
            'with wings and a top hat flying over a happy '
            'futuristic scifi city with lots of greenery')

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
      response_modalities=['Text', 'Image']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    filename = "Generated Image " + get_current_datetime()
    image = Image.open(BytesIO((part.inline_data.data)))
    image.save(fp=filename, format="png")
    image.show()