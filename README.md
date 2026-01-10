# 📝 Internship Daily Diary Generator

A modern web application built with Flask (backend) and Vue.js (frontend) that helps internship students generate professional daily diary entries using OpenAI API.

## ✨ Features

- **Modern UI**: Beautiful, responsive interface with gradient designs and smooth animations
- **Professional Formatting**: Automatically generates clean, professional diary entries
- **Structured Output**: Includes Date, Work Summary, Learnings/Outcomes, Blockers/Risks (always meaningful), Skills (optional), and Reference Links
- **Easy Copy**: Copy individual fields or the entire entry with one click
- **Environment Variables**: Secure API key management via `.env` file
- **RESTful API**: Clean Flask backend with CORS support

## 🏗️ Architecture

- **Backend**: Flask REST API (Python)
- **Frontend**: Vue.js 3 (JavaScript)
- **AI**: OpenAI GPT-3.5-turbo

## 📦 Installation

### Prerequisites

- Python 3.7+
- Node.js 14+ and npm

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API Key**:
   - Create a `.env` file in the `backend` directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

4. **Run the Flask server**:
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install Node dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vue.js development server**:
   ```bash
   npm run serve
   ```
   The frontend will run on `http://localhost:3000` and automatically open in your browser

## 🎯 Usage

1. **Start both servers** (backend on port 5000, frontend on port 3000)

2. **Use the app**:
   - Select the date for your diary entry
   - Optionally enter your OpenAI API key (if not set in `.env`)
   - Paste your raw full-day work summary
   - Click "Generate Diary Entry"
   - Copy individual fields or the full entry

## 📋 Output Format

The app generates diary entries in the following format:

- **Date**: Selected date with 📅 emoji
- **Work Summary**: Professional summary of the day's work
- **Learnings / Outcomes**: What was learned and achieved
- **Blockers / Risks**: **Always includes meaningful content** - never just "None". Identifies realistic challenges, learning needs, or areas for improvement
- **Skills**: Optional field (only included if applicable)
- **Reference Links**: Optional field (or "Not Applicable")

## 🔒 Security

- API keys are stored in `.env` file (not committed to version control)
- `.env` file is already in `.gitignore`
- Never share your `.env` file or commit it to version control
- CORS is enabled for local development

## 📝 Important Notes

- **Blockers/Risks** will **always** contain meaningful content - never just "None"
- The system identifies realistic challenges, learning needs, or areas for improvement
- **Skills** field is optional and may be skipped if not applicable
- All entries are formatted professionally and ready for submission

## 🛠️ Development

### Backend API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/generate` - Generate diary entry
  - Body: `{ "date": "YYYY-MM-DD", "summary": "...", "api_key": "..." }`
  - Returns: `{ "success": true, "full_response": "...", "fields": {...} }`

### Project Structure

```
.
├── backend/
│   ├── app.py              # Flask backend
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment variables (create this)
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.vue         # Main Vue component
│   │   ├── main.js         # Vue entry point
│   │   └── style.css       # Global styles
│   ├── vue.config.js       # Vue configuration
│   └── package.json        # Node dependencies
├── .gitignore
└── README.md
```

## 🚀 Production Deployment

For production deployment:

1. **Backend**: Use a WSGI server like Gunicorn
2. **Frontend**: Build the React app (`npm run build`) and serve with a web server
3. **Environment**: Set production environment variables
4. **CORS**: Update CORS settings for your production domain

## 📄 License

This project is open source and available for personal use.
