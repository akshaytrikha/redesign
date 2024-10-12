import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'your-api-key'

def run_multimodal_query(text_input, image_path=None):
    # Initialize message with text input
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text_input},
    ]
    
    # Prepare image for multimodal input if an image path is provided
    if image_path:
        with open(image_path, 'rb') as image_file:
            response = openai.ChatCompletion.create(
                model="gpt-4-vision",  # Use GPT-4 multimodal model
                messages=messages,
                files={"image": image_file},  # Attach the image file
            )
    else:
        # If no image is provided, just run a text query
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use GPT-4 for text-only queries
            messages=messages,
        )

    # Extract and return the response text
    return response.choices[0].message["content"]

# Example text input and image path
text_query = "What can you tell me about the structure of a lithium-ion battery?"
image_file_path = "/path/to/image.jpg"  # Replace with the actual path to your image

# Call the function
response_text = run_multimodal_query(text_query, image_file_path)

# Print the response
print(response_text)
