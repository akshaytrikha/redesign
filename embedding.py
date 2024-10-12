from openai import OpenAI
import os

client = OpenAI(api_key='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')

file_path = 'app/sliverpizzeria.com/index.html'

# Read the file contents into a string
with open(file_path, 'r', encoding='utf-8') as file:
    html_code = file.read()

# Only keep 20,000 characters
html_code = html_code[:20000]

# Embed the HTML snippet using OpenAI API
response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=[html_code]
)

# Extract the embedding vector
embedding_vector = response['data'][0]['embedding']
