# AI Job Agent

AI-powered job matching platform built with FastAPI, React, and Google Gemini.

## Features

* Upload and analyze CVs
* Extract candidate profile automatically
* Match CV against job descriptions
* Analyze job URLs directly
* Generate personalized cover letters
* Track applied jobs
* AI-powered recommendations using Google Gemini

## Tech Stack

### Backend

* FastAPI
* Python
* Google Gemini API

### Frontend

* React
* Axios
* Bootstrap

## Project Workflow

1. Upload CV
2. Extract candidate profile
3. Paste job URL
4. Analyze job compatibility
5. Generate cover letter
6. Track job applications

## Installation

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

## Future Improvements

* Multi-user authentication
* Auto job search
* PDF export
* Dashboard analytics
* Email application automation

## License

MIT License
