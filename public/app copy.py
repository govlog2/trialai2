from flask import Flask, render_template, request, jsonify
import openai
import pandas as pd
import io

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = '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'

# Load the Excel file
# Replace 'your_excel_file.xlsx' with the path to your actual Excel file
data = pd.read_excel('report1.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Convert the Excel data to text
    excel_data_text = convert_excel_to_text(data)

    # Prepare the prompt to send to the API
    prompt = (
        f"You are an assistant helping with influencer data. Here is the dataset:\n\n"
        f"{excel_data_text}\n\n"
        f"The user has asked: '{user_message}'\n"
        f"Please provide a helpful response based on the data provided."
    )

    # Send the request to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that helps people analyze and summarize data."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def convert_excel_to_text(data):
    # Convert the DataFrame to a CSV-like text format for easier reading by ChatGPT
    output = io.StringIO()
    data.to_csv(output, index=False)
    return output.getvalue()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
