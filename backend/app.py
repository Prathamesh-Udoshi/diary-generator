from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from datetime import datetime
import re
import os
import time
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Simple in-memory cache for responses (cleared on restart)
response_cache = {}
CACHE_EXPIRY = 3600  # 1 hour cache expiry

def cleanup_cache():
    """Clean up expired cache entries"""
    current_time = time.time()
    expired_keys = [k for k, (_, ts) in response_cache.items() if current_time - ts > CACHE_EXPIRY]
    for key in expired_keys:
        del response_cache[key]
    if expired_keys:
        print(f"Cleaned up {len(expired_keys)} expired cache entries")

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

# Conservative System Prompt
SYSTEM_PROMPT = """You are an Internship Daily Diary Entry Generator.

Convert raw work summaries into professional diary entries. Use the provided information as the foundation and make reasonable generalizations that naturally follow from the described work.

Structure your output exactly like this:

Here's your completed daily diary entry 👇

Work Summary:
[Provide a comprehensive 5-7 sentence summary covering the day's activities, tasks, tools, and processes. Make reasonable generalizations about related aspects of the work described.]

Learnings / Outcomes:
[Explain in 5-7 sentences what was learned and achieved. Include reasonable generalizations about skill development and outcomes that would naturally follow from the work performed.]

Blockers / Risks:
[Mandatory section with 5-7 sentences about challenges faced, potential risks, and areas for improvement. Make reasonable generalizations about typical challenges that would accompany this type of work. Never write "None".]

Skills: [Optional - include if specific skills can be reasonably inferred from the work described]

Reference Links: [Optional - include relevant resources that would typically be associated with this type of work]

GUIDELINES:
- Base content on the summary but allow reasonable generalizations
- Maintain professional internship-appropriate tone
- Ensure all sections have substantial, meaningful content
- Skip Skills section only if no skills can be reasonably inferred
- Skip Reference Links only if no relevant resources can be reasonably associated
- Make generalizations that enhance rather than contradict the original summary"""

def generate_diary_entry(summary, api_key):
    """Generate diary entry using OpenAI API with caching"""
    # Create cache key from summary (ignore minor differences)
    cache_key = hashlib.md5(summary.lower().strip()[:500].encode()).hexdigest()

    # Check cache
    current_time = time.time()
    if cache_key in response_cache:
        cached_data, timestamp = response_cache[cache_key]
        if current_time - timestamp < CACHE_EXPIRY:
            print(f"Cache hit for summary hash: {cache_key}")
            return cached_data

    user_prompt = f"""Full Day Summary:

{summary}

Generate the internship daily diary entry strictly following the required structure and format rules. Use the exact format specified with the intro line. IMPORTANT: The Blockers/Risks field must contain meaningful content - never just "None"."""

    try:
        client = OpenAI(api_key=api_key)
        start_time = time.time()

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=2000,  # Increased for detailed 5-7 sentence responses per field
            timeout=30  # Increased timeout for longer generation time
        )

        elapsed_time = time.time() - start_time
        result = response.choices[0].message.content

        # Cache the result
        response_cache[cache_key] = (result, current_time)
        print(f"OpenAI API call took {elapsed_time:.2f} seconds, cached result")

        return result
    except Exception as e:
        elapsed_time = time.time() - start_time if 'start_time' in locals() else 0
        error_msg = f"OpenAI API error after {elapsed_time:.2f}s: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)

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
            'POST /api/generate': 'Generate diary entry',
            'POST /api/cache/clear': 'Clear response cache'
        },
        'status': 'running'
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    cleanup_cache()  # Clean expired entries
    cache_size = len(response_cache)
    return jsonify({
        'status': 'ok',
        'message': 'API is running',
        'cache_entries': cache_size,
        'model': 'gpt-3.5-turbo'
    })

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear response cache"""
    global response_cache
    old_size = len(response_cache)
    response_cache.clear()
    return jsonify({
        'message': f'Cache cleared',
        'entries_removed': old_size
    })

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

