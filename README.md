# Google Gemini 2.0 Flash Image Generation Toolkit for Open WebUI

![Version](https://img.shields.io/badge/version-0.2-blue)

**Author:** [Justin Miller](https://github.com/millerjl1980)
**Support This Project:** [Buy Me A Coffee](https://buymeacoffee.com/justinmillerdev)

---
## Update - 7/20/25
Gemini updated the Flash image generation from "Experimental" to "Preview."

## Overview

This toolkit integrates Google's powerful (and experimental) `gemini-2.0-flash-preview-image-generation` model directly into Open WebUI, allowing you to generate images based on text prompts within your chat interface.

Leveraging the Gemini API, this tool can generate images and potentially accompanying text in response to your prompts. The results (both image and text, if generated) are displayed directly in the Open WebUI chat.

**Note:** This tool utilizes the `gemini-2.0-flash-preview-image-generation` model, which is currently experimental [0, 1]. Google documentation notes that for this specific model, the response modalities must include both "Text" and "Image" [1]. This toolkit handles that configuration automatically.

## Features

*   **Image Generation:** Create images directly from text prompts using Google's Gemini 2.0 Flash Experimental model.
*   **Text + Image Output:** The model can return both generated text and an image in a single response. This tool handles displaying both in the UI.
*   **Configurable:**
    *   Set your Google AI API Key via the Open WebUI tool settings.
    *   Choose the output image format (PNG, GIF, JPEG).
    *   (Advanced) Change the specific Google AI model name if needed (though it defaults to the required experimental model).
*   **Seamless Integration:** Works within the Open WebUI tools framework, sending status updates and results directly to the chat interface.

## Requirements

*   **Open WebUI:** Version 0.5.3 or higher
*   **Python Packages:**
    *   `google-genai`
    *   `google-generativeai`
    *   `Pillow`
*   **Google AI API Key:** You need a valid API key from Google AI Studio or Google Cloud.

## Installation

1.  Ensure you have the required Python packages installed in your Open WebUI environment:
    ```bash
    pip install google-genai google-generativeai Pillow
    ```
2.  Place the tool's Python file (`.py`) into your Open WebUI `tools` directory as a new tool, or grab it from the [Open WebUI Community](https://openwebui.com/t/indymiller/gemini_2_0_flash_exp_image_generation)
3.  Restart Open WebUI.

## Configuration

1.  Navigate to the Tools settings within Open WebUI.
2.  Find the "Google Gemini 2.0 Flash Experimental Image Generation" tool.
3.  Enter your **Google AI API Key** in the `api_key` field. This is **required** for the tool to function.
4.  (Optional) Change the desired `image_format` (default is `png`).
5.  (Optional) Change the `model_name` if Google updates or changes the experimental model endpoint.

## Usage

Once installed and configured, you can invoke the tool within Open WebUI like any other tool.

Example prompt:

`Generate an image of a futuristic cityscape at sunset`

The tool will:
1.  Show a "Generating an image..." status message.
2.  Call the Google Gemini API with your prompt.
3.  If the API returns text, it will be displayed in the chat.
4.  If the API returns an image, it will be uploaded via Open WebUI's image handling and displayed in the chat.
5.  Provide a final status update (success or error).

## Important Notes

*   **Experimental Model:** The `gemini-2.0-flash-preview-image-generation` model is explicitly marked as experimental by Google. Its availability or behavior may change.
*   **API Key:** Keep your Google AI API key secure. Do not share it publicly.
*   **Safety Settings:** The underlying Google API may have safety filters that prevent generation for certain prompts. The tool will attempt to relay any error messages back to the user.

---

Enjoy generating images directly within Open WebUI!
