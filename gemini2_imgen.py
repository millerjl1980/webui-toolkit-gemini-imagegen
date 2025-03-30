"""
title: Google Gemini 2.0 Flash Experimental Image Generation
author: Justin Miller
author_url: https://github.com/millerjl1980
funding_url: https://buymeacoffee.com/justinmillerdev
version: 0.1
required_open_webui_version: 0.5.3
requirements: google-genai, google-generativeai, Pillow, pydantic
"""

import base64
from datetime import datetime

# Open WebUI imports
import os
import requests
from datetime import datetime
from typing import Callable
from fastapi import Request 
from pydantic import BaseModel, Field
from open_webui.routers.images import upload_image, load_b64_image_data
from open_webui.models.users import Users

# Google Gemini 2.0 Flash Experimental imports
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


class Tools:
    """Container class for Open WebUI tools."""

    class Valves(BaseModel):
       """User-configurable settings for the tool."""
       api_key: str = Field(default="", description="Your Google AI API key here")
       # Check Gemini docs for models supporting multi-modal output if 2.0 flash is deprecated
       model_name: str = Field(
           default="gemini-2.0-flash-exp-image-generation",
           description="The specific Google AI model name for image generation"
       )
       # Supported Pillow formats for image
       image_format: str = Field(
            default="png",
            description="The format of the generated image (PNG, GIF, JPEG)",
            enum=["png", "gif", "jpeg"]
        )

    def __init__(self):
        """Initialize the Tool."""
        self.valves = self.Valves()
        # Ensure Pillow is installed for image processing
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("Pillow library is required for image processing. Please install it: pip install Pillow")

    async def gemini_generate_image(
        self, prompt: str, __request__: Request, __user__: dict, __event_emitter__=None
    ) -> str:
        """
        Generates an image based on a prompt using a Google AI model.
        The model might also return accompanying text. Both the image (if generated)
        and text (if generated) are sent directly to the UI via events.
        This function returns a string confirming the outcome for the LLM.

        :param prompt: The text prompt to use for image generation.
        :param __event_emitter__: (Internal) Used by Open WebUI to send updates/results to the UI.
        :return: A string message summarizing the operation's result for the LLM.
        """
        if not self.valves.api_key:
             return "Error: API key is missing. Please configure it in the tool settings."
        
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": "Generating an image", "done": False},
            }
        )

        try:
            # https://ai.google.dev/gemini-api/docs/image-generation#gemini
            client = genai.Client(api_key=self.valves.api_key)

            response = client.models.generate_content(
                model=self.valves.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
                )
            )
            data = {
                "instances": {"prompt": prompt},
                "parameters": {
                    "sampleCount": 1,
                    "outputOptions": {"mimeType": "image/png"},
                },
            }

            generated_text = None
            image = None
            
            for part in response.candidates[0].content.parts:
                # In case multiple parts, emit both text and image once it is received
                if part.text:
                    generated_text = part.text
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "Received text with image:.", "done": False},
                        }
                    )
                    await __event_emitter__(
                        {
                            "type": "message",
                            "data": {"content": generated_text},
                        }
                    )
                else:
                    generated_text = None
                
                if part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    buffered = BytesIO()
                    image.save(buffered, format=self.valves.image_format)
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    image_data, content_type = load_b64_image_data(img_str)
                    url = upload_image(__request__, data, image_data, content_type,  user=Users.get_user_by_id(__user__["id"]))

                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {"description": "Generated an image", "done": True},
                        }
                    )
                    await __event_emitter__(
                    {
                        "type": "message",
                        "data": {"content": f"![Generated Image]({url})"},
                    }
                )
                else:
                    image = None

            if image is not None:
                return f"Notify the user that the image has been successfully generated"
            else:
                return f"Notify the user that the image has not been generated"

        except Exception as err:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"An error occurred: {err}", "done": True},
                }
            )
            return f"Tell the user: {err}"
