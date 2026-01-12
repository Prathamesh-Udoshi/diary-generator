from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from datetime import datetime
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist.',
        'available_endpoints': {
            'GET /': 'API information',
            'GET /api/health': 'Health check',
            'POST /api/generate': 'Generate diary entry'
        }
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An error occurred on the server.'
    }), 500

# System Prompt
SYSTEM_PROMPT = """You are an Internship Daily Diary Entry Generator.

Your task is to take a raw full-day work summary written by an internship student and generate clean, professional, internship-appropriate diary entries.

You MUST generate the output in the following fixed structure and format EXACTLY:

Here's your completed daily diary entry 👇

Work Summary:

[Provide a comprehensive and detailed summary of the day's work activities. Describe the specific tasks performed in detail, explain the step-by-step processes followed, mention all tools and technologies used, discuss methodologies and approaches applied, highlight challenges encountered and how they were overcome, and explain the overall scope and impact of the work. Write 3-4 detailed sentences that thoroughly describe the work accomplished, making it comprehensive and informative.]

Learnings / Outcomes:

[Provide extensive detail about the learning experiences and outcomes achieved. Explain specific technical concepts learned with examples, describe skills developed with concrete evidence, discuss challenges overcome with lessons learned, highlight measurable results and achievements with metrics or outcomes, and reflect on personal growth and development. Write 3-4 detailed sentences explaining what was learned, how it was applied, and what was accomplished.]

Blockers / Risks:

[CRITICAL: This field is MANDATORY and must ALWAYS contain meaningful content. NEVER write just "None".
Provide comprehensive analysis of challenges faced and potential risks throughout the work. Discuss 3-5 specific challenges or risks in detail, including:
- Time management challenges and specific strategies used to address them
- Areas where more learning or practice would be beneficial and why
- Potential future challenges that could arise and mitigation strategies
- Dependencies on other team members or resources and their impact
- Areas requiring further clarification or understanding and how they were handled
- Learning curve challenges with specific tools or technologies and adaptation methods
Always provide constructive, realistic content that demonstrates deep self-awareness and professional growth mindset. Write 3-4 detailed sentences with specific examples and insights.]

Skills: [OPTIONAL - include ONLY if skills can be clearly identified, otherwise skip this section entirely]

Reference Links: [include ONLY if applicable, otherwise write 'Not Applicable']

[Provide 3-6 relevant links to documentation, tutorials, code repositories, or resources that were referenced or would be helpful for similar work. Include brief descriptions of what each link contains and why it's relevant.]

RULES:
- Start with "Here's your completed daily diary entry 👇"
- Work Summary and Learnings / Outcomes are MANDATORY and must always be present with substantial content
- Keep the tone professional, concise, and suitable for internship submission
- Do NOT exaggerate, invent work, or add implementation details if the user mentions theory-only understanding
- If the user mentions discussion, understanding, learning, reviewing, or studying — keep it theoretical
- Blockers / Risks is MANDATORY and MUST contain meaningful content - NEVER just "None". Always identify realistic challenges, learning needs, or areas for improvement
- Skills is OPTIONAL - only include if skills can be clearly identified from the summary, otherwise skip the Skills section entirely
- If Skills section is skipped, go directly from Blockers/Risks to Reference Links
- Reference Links should only be included if clearly relevant; otherwise say 'Not Applicable'
- Use proper paragraph breaks for readability
- Output must be directly copy-paste ready"""

def generate_diary_entry(summary, api_key):
    """Generate diary entry using OpenAI API"""
    user_prompt = f"""Full Day Summary:

{summary}

Generate the internship daily diary entry strictly following the required structure and format rules. Use the exact format specified with the intro line. IMPORTANT: The Blockers/Risks field must contain meaningful content - never just "None"."""

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")

def parse_response(response_text):
    """Parse the LLM response into structured fields"""
    fields = {
        'Work Summary': '',
        'Learnings / Outcomes': '',
        'Blockers / Risks': '',
        'Skills': '',
        'Reference Links': ''
    }

    # Remove the intro line if present
    intro_pattern = r"Here's your completed daily diary entry.*?👇\s*\n"
    response_text = re.sub(intro_pattern, '', response_text, flags=re.IGNORECASE)

    # Split by field headers (Skills is optional)
    patterns = {
        'Work Summary': r'Work Summary:\s*(.*?)(?=\n\s*Learnings\s*/\s*Outcomes)',
        'Learnings / Outcomes': r'Learnings\s*/\s*Outcomes:\s*(.*?)(?=\n\s*Blockers\s*/\s*Risks)',
        'Blockers / Risks': r'Blockers\s*/\s*Risks:\s*(.*?)(?=\n\s*(?:Skills|Reference\s*Links|$))',
        'Skills': r'Skills:\s*(.*?)(?=\n\s*Reference\s*Links)',
        'Reference Links': r'Reference\s*Links:\s*(.*?)(?=\n|$)'
    }

    for field_name, pattern in patterns.items():
        match = re.search(pattern, response_text, re.DOTALL | re.IGNORECASE)
        if match:
            fields[field_name] = match.group(1).strip()
        else:
            # Fallback: try simple colon-based splitting
            if f"{field_name}:" in response_text:
                parts = response_text.split(f"{field_name}:")
                if len(parts) > 1:
                    next_field = None
                    for next_field_name in fields.keys():
                        if next_field_name != field_name and f"{next_field_name}:" in parts[1]:
                            next_field = next_field_name
                            break

                    if next_field:
                        fields[field_name] = parts[1].split(f"{next_field}:")[0].strip()
                    else:
                        fields[field_name] = parts[1].strip()

    return fields

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Internship Diary Generator API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API information',
            'GET /api/health': 'Health check',
            'POST /api/generate': 'Generate diary entry'
        },
        'status': 'running'
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'API is running'})

@app.route('/api/generate', methods=['POST'])
def generate_entry():
    """Generate diary entry endpoint"""
    try:
        data = request.get_json()
        summary = data.get('summary')
        api_key = data.get('api_key') or os.getenv("OPENAI_API_KEY")

        if not api_key:
            return jsonify({'error': 'OpenAI API key is required'}), 400

        if not summary or not summary.strip():
            return jsonify({'error': 'Work summary is required'}), 400

        # Generate diary entry
        response = generate_diary_entry(summary, api_key)
        fields = parse_response(response)

        return jsonify({
            'success': True,
            'full_response': response,
            'fields': fields
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 Flask Backend Server Starting...")
    print("=" * 50)
    print("📍 Server running at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("📝 API endpoint: http://localhost:5000/api/generate")
    print("=" * 50)
    app.run(debug=True, port=5000, host='0.0.0.0')

