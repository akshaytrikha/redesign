# External
import re
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import tiktoken
import os

# Internal
from scrape import fetch_source
from infer import give_improvement_ideas

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the form
    url = request.form.get('url')
    if not url:
        return jsonify({"status": "error", "message": "No URL provided."}), 400

    # Call the function from scrape.py
    result = fetch_source(url)

    # Return JSON response
    if result["status"] == "success":
        return jsonify(result), 200
    else:
        return jsonify(result), 400

criteria="""Usability
Explanation: The interface should be intuitive and easy to use, allowing users to achieve their goals effectively and efficiently without unnecessary complexity.
Key Aspects: Ease of Learning: New users should be able to learn how to use the interface quickly.
Efficiency of Use: Frequent users should be able to perform tasks swiftly.
Memorability: Users should be able to return to the interface after a period of not using it without having to relearn everything.
Consistency
Explanation: Consistent design elements and behaviors help users predict how things work, reducing the learning curve and preventing confusion.
Key Aspects:
Visual Consistency: Uniform colors, fonts, and layouts throughout the interface.
Functional Consistency: Similar operations should be triggered in the same way.
Internal and External Consistency: Aligning with both internal standards and common platform conventions.
Clarity
Explanation: The UI should communicate information clearly through simple language, unambiguous icons, and straightforward workflows.
Key Aspects:
Simplified Content: Avoid jargon and use familiar terminology.
Readable Text: Appropriate font sizes and styles for legibility.
Clear Icons and Labels: Icons should be easily interpretable, and labels should accurately describe functions.
Feedback
Explanation: The system should provide immediate and informative feedback in response to user actions, keeping users informed about what's happening.
Key Aspects:
Action Confirmation: Visual or auditory indications when actions are performed.
Progress Indicators: Show status for ongoing processes like downloads or uploads.
Error Messages: Clear explanations of issues and how to resolve them.
Accessibility
Explanation: The interface should be usable by people with a wide range of abilities and disabilities, adhering to accessibility standards like WCAG (Web Content Accessibility Guidelines).
Key Aspects:
Keyboard Navigation: All functionalities should be accessible via keyboard.
Screen Reader Support: Proper use of semantic HTML and ARIA labels.
Contrast Ratios: Sufficient color contrast between text and background.
Responsiveness
Explanation: The UI should respond quickly to user inputs without noticeable delays, providing a smooth and seamless experience.
Key Aspects:
Load Times: Optimize performance to reduce waiting times.
Interactive Elements: Immediate visual feedback when interacting with buttons or controls.
Adaptive Layouts: Interface adapts smoothly to different screen sizes and orientations.
Aesthetic Design
Explanation: An attractive and professional visual design enhances user satisfaction and can improve usability by guiding the user's eye to important elements.
Key Aspects:
Visual Hierarchy: Use size, color, and placement to indicate importance.
Consistency in Style: Cohesive color schemes, typography, and imagery.
Minimalism: Avoid clutter by keeping the design simple and focused.
Error Prevention and Handling
Explanation: The UI should minimize the chances of user errors and provide clear recovery options if errors occur.
Key Aspects:
Preventive Measures: Disable irrelevant options or provide constraints (e.g., date pickers).
Confirmation Dialogs: For critical actions like deletions.
Helpful Error Messages: Clear explanations and guidance on how to fix the issue.
Flexibility and Efficiency
Explanation: The interface should cater to both novice and expert users by allowing customization and providing shortcuts for frequent actions.
Key Aspects:
Customization Options: Users can adjust settings to suit their preferences.
Keyboard Shortcuts: For power users to perform actions faster.
Adaptive Interfaces: The UI can adjust to user behavior over time.
User Control and Freedom
Explanation: Users should feel in control of the interface, with the ability to navigate freely and undo or redo actions when necessary.
Key Aspects:
Undo/Redo Functions: Allow users to correct mistakes easily.
Flexible Navigation: Users can move backward and forward without losing progress.
Clear Exits: Options to cancel actions or exit processes at any point."""

client = OpenAI(api_key='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')

def create_chunks(input_code, chunk_size=125000, model_name='gpt-4o'):
    # Get the encoding for the specified model
    encoding = tiktoken.encoding_for_model(model_name)
    # Tokenize the content
    tokens = encoding.encode(input_code)
    # Return the number of tokens
    print(f"Number of tokens is: {len(tokens)}")
    token_chunks = [tokens[i:i+chunk_size] for i in range(0, len(tokens), chunk_size)]
    string_chunks = [encoding.decode(chunk) for chunk in token_chunks]
    return string_chunks


def give_improvement_ideas(url):
    input_code = ""
    print(url)
    for root, _, files in os.walk(url):
        for file in files:
            print(file)
            file_path = os.path.join(root, file)
            print(file_path)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    input_code += f.read() + '\n'
                    print(input_code)
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    chunks = create_chunks(input_code)
    overall_improvement_output = ""
    overall_summary_output = ""
    overall_scores_output = ""
    for i, chunk in enumerate(chunks):
        print(i)
        improvement_prompt = f"""
            You are an expert web developer. Based on the following website code,
            provide user interface/user experience improvement ideas for the 
            code base chunk. Your response should be in a bulleted list with 
            no other introduction or conclusion. Here is a summary of previous user interface/user experience aspects of the 
            code in the website. If this is blank, this is the first chunk of website code.
            Summary: {overall_summary_output}
            Given this context, write your improvement ideas for the user interface/user experience improvement of the following website code chunk.
            Use the following criteria when doing so.
            Criteria: {criteria}
            Below is the website code chunk.
            Website Code Chunk: {chunk}
            """
        summary_prompt = f"""
            You are an expert web developer. Based on the following website code,
            provide a summary of the user interface/user experience of the 
            code base chunk. Your response should be in a bulleted list with no other 
            introduction or conclusion. Here is a summary of previous user interface/user experience aspects of the 
            code in the website. If this is blank, this is the first chunk of website code.
            Summary: {overall_summary_output}
            Given this context, write your summary of the user interface/user experience improvement of the following website code chunk, and give a numerical grade from 0 to 100 for each criterion.
            Use the following criteria when doing so.
            Criteria: {criteria}
            Below is the website code chunk.
            Website Code Chunk: {chunk}"""
        if i == len(chunks) - 1:
            scores_prompt = f"""
                You are an expert web developer. Based on the following website code,
                provide scores from 0 (worst) to 100 (best) of user interface/user experience aspects for the 
                code base overall. Your response should be in a bulleted list with 
                no other introduction or conclusion. Here is a summary of previous user interface/user experience aspects of the 
                code in the website. If this is blank, this is the first chunk of website code.
                Summary: {overall_summary_output}
                Given this context, you will write your scores from 0 (worst) to 100 (best) for the user interface/user experience improvement of the website code overall.
                Below is the final website code chunk.
                Website Code Chunk: {chunk}
                Your response should be in the following format. Do not output anything else.
                Usability: score
                Consistency: score
                Clarity: score
                Feedback: score
                Accessibility: score
                Responsiveness: score
                Aesthetic Design: score
                Error Prevention and Handling: score
                Flexibility and Efficiency: score
                User Control and Freedom: score
                """
        completion = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": improvement_prompt
            }
        ])
        improvement_output = completion.choices[0].message.content
        overall_improvement_output += improvement_output
        completion = client.chat.completions.create(model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": summary_prompt
            }
        ])
        if i == len(chunks) - 1:
            scores_output = completion.choices[0].message.content
            completion = client.chat.completions.create(model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": scores_prompt
                }
            ])
            scores_output = completion.choices[0].message.content
            overall_scores_output += scores_output
    return overall_improvement_output, overall_scores_output

import time
@app.route('/feedback', methods=['GET'])
def feedback():
    start_time = time.time()
    print(start_time)
    print(request.args.get('text'))
    overall_improvement_output, overall_scores_output = give_improvement_ideas(request.args.get('text'))
    end_time = time.time()
    print(end_time)
    delta_time = end_time - start_time
    print(delta_time)
    print(overall_improvement_output)
    print(overall_scores_output)
    scores = [int(score) for score in re.findall(r'\b\d+\b', overall_scores_output)]
    return render_template('feedback.html', scores=scores, improvement_ideas=overall_improvement_output)

if __name__ == '__main__':
    app.run(debug=True)
