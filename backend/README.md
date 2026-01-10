# Backend API - Internship Diary Generator

Flask REST API for generating internship diary entries.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the server**:
   ```bash
   python app.py
   ```

   The server will start on `http://localhost:5000`

## API Endpoints

### GET `/`
Get API information and available endpoints.

**Response:**
```json
{
  "message": "Internship Diary Generator API",
  "version": "1.0.0",
  "endpoints": {...},
  "status": "running"
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

### POST `/api/generate`
Generate a diary entry.

**Request Body:**
```json
{
  "date": "2025-01-10",
  "summary": "Your work summary here...",
  "api_key": "optional_if_in_env"
}
```

**Response:**
```json
{
  "success": true,
  "full_response": "Full formatted diary entry...",
  "fields": {
    "Date": "...",
    "Work Summary": "...",
    "Learnings / Outcomes": "...",
    "Blockers / Risks": "...",
    "Skills": "...",
    "Reference Links": "..."
  }
}
```

## Testing

Run the test script to verify endpoints:
```bash
python test_api.py
```

**Note:** Make sure `requests` is installed: `pip install requests`

## Troubleshooting

### 404 Error
- Make sure you're accessing the correct endpoint
- Check that the server is running on port 5000
- Try accessing `http://localhost:5000/api/health` to verify the server is up

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the `backend` directory when running commands

### API Key Issues
- Ensure `.env` file exists in the `backend` directory
- Verify the API key is correct in the `.env` file
- Or pass the API key in the request body

