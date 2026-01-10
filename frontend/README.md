# Frontend - Vue.js Application

Vue.js 3 frontend for the Internship Diary Generator.

## Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run serve
   ```

   The app will be available at `http://localhost:3000`

3. **Build for production**:
   ```bash
   npm run build
   ```

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.vue            # Main Vue component
│   ├── main.js             # Application entry point
│   └── style.css           # Global styles
├── vue.config.js           # Vue CLI configuration
└── package.json            # Dependencies
```

## Features

- Vue.js 3 with Composition API
- Responsive design with modern UI
- Axios for API calls
- Date formatting with date-fns
- Copy to clipboard functionality

## Development

The Vue app is configured to proxy API requests to `http://localhost:5000` (Flask backend) during development.

Make sure the Flask backend is running on port 5000 before starting the frontend.

## Dependencies

- **vue**: ^3.3.4 - Vue.js framework
- **axios**: ^1.6.0 - HTTP client
- **date-fns**: ^2.30.0 - Date formatting

## Troubleshooting

### Port already in use
If port 3000 is already in use, Vue CLI will automatically try the next available port.

### API connection errors
- Ensure the Flask backend is running on `http://localhost:5000`
- Check the proxy configuration in `vue.config.js`
- Verify CORS is enabled in the Flask backend

