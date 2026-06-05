from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_service import ask_gemini, ask_gemini_json
from cv_parser import extract_cv_text
from job_scraper import extract_job_text
import os
import json
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    description: str


class MatchRequest(BaseModel):
    job_description: str


class CoverLetterRequest(BaseModel):
    job_description: str


class JobPackageRequest(BaseModel):
    job_description: str
    
class JobUrlRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {
        "message": "AI Job Agent is running"
    }


@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    cv_text = extract_cv_text(file_path)
    
    from cv_profile import create_profile

    profile = create_profile(cv_text)
    
    with open(
    "uploads/profile.json",
    "w",
    encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            ensure_ascii=False,
            indent=4
        )
    
    with open("uploads/cv.txt", "w", encoding="utf-8") as f:
        f.write(cv_text)

    return {
        "message": "CV uploaded successfully"
    }


@app.post("/analyze-job")
def analyze_job(job: JobRequest):

    prompt = f"""
    Analyze this job description.

    Return:
    - Job Title
    - Required Skills
    - Experience Level
    - Short Summary

    Job Description:
    {job.description}
    """

    result = ask_gemini(prompt)

    return {
        "analysis": result
    }


@app.post("/match-job")
def match_job(data: MatchRequest):

    with open("uploads/cv.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()

    prompt = f"""
    Compare this CV with the job description.

    Return:
    - Match Score
    - Strengths
    - Missing Skills
    - Recommendation

    CV:
    {cv_text}

    Job Description:
    {data.job_description}
    """

    result = ask_gemini(prompt)

    return {
        "result": result
    }


@app.post("/generate-cover-letter")
def generate_cover_letter(data: CoverLetterRequest):

    with open("uploads/cv.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()

    prompt = f"""
    Write a professional cover letter.

    Candidate CV:
    {cv_text}

    Job Description:
    {data.job_description}

    Requirements:
    - Professional English
    - Max 400 words
    - Mention relevant experience
    - Mention relevant technologies
    """

    result = ask_gemini(prompt)

    return {
        "cover_letter": result
    }


@app.post("/job-package")
def job_package(data: JobPackageRequest):

    with open("uploads/cv.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()

    prompt = f"""
    Return VALID JSON ONLY.

    No markdown.
    No explanation.
    No ```json.

    Format:

    {{
        "match_score": 0,
        "strengths": [],
        "missing_skills": [],
        "recommendation": "",
        "cover_letter": ""
    }}

    CV:
    {cv_text}

    Job Description:
    {data.job_description}
    """

    result = ask_gemini_json(prompt)

    return result

@app.post("/analyze-job-url")
def analyze_job_url(data: JobUrlRequest):
    file_path = "data/applied_jobs.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            applied_jobs = json.load(f)
    except:
        applied_jobs = []

    if not os.path.exists("uploads/profile.json"):
        return {
            "error": "Please upload your CV first"
        }

    with open(
        "uploads/profile.json",
        "r",
        encoding="utf-8"
    ) as f:

        profile = json.load(f)

    job_description = extract_job_text(data.url)

    if len(job_description.strip()) < 100:
        return {
            "error": "Could not extract job description"
        }

    prompt = f"""
    Return VALID JSON ONLY.

    No markdown.
    No explanation.

    Format:

    {{
        "match_score": 0,
        "strengths": [],
        "missing_skills": [],
        "recommendation": "",
        "cover_letter": ""
    }}

    Candidate Profile:
    {profile}

    Job Description:
    {job_description}
    """

    result = ask_gemini_json(prompt)
    result["already_applied"] = data.url in applied_jobs
    return result

@app.get("/profile")
def get_profile():

    if not os.path.exists("uploads/profile.json"):
        return {
            "error": "No profile found"
        }

    with open(
        "uploads/profile.json",
        "r",
        encoding="utf-8"
    ) as f:

        profile = json.load(f)

    return profile

@app.post("/mark-applied")
def mark_applied(data: JobUrlRequest):

    file_path = "data/applied_jobs.json"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)
    except:
        jobs = []

    if data.url not in jobs:
        jobs.append(data.url)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4)
    
    return {
        "message": "Job marked as applied"
    }