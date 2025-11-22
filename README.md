📄 AI-Powered Resume ATS Analyzer

Tech: FastAPI · Next.js · SentenceTransformers · PostgreSQL · Docker
Author: Ashwin R · Organization: ashwin-portfolio

🚀 Overview

The AI Resume ATS Analyzer is a full-stack web application that evaluates a resume against a job description and generates:

ATS Score (0–100)

Skill Match %

Keyword Match Report

Resume Weaknesses

Suggestions & Improvements

Missing Keywords List

JD vs Resume Comparison

Downloadable PDF Report (optional)

This project replicates the core features of an Applicant Tracking System (ATS) used by top companies.

🧠 Core Features
🔍 1. Resume Parsing

Extracts text from PDF/DOCX resumes

Cleans, normalizes & tokenizes text

No paid API required

📝 2. Job Description Analysis

Keyword extraction using NLP

Entity detection (skills, tools, domains)

🤖 3. AI-Based Matching (FREE)

Uses SentenceTransformers (all-MiniLM-L6-v2) to calculate:

Semantic similarity

Missing keywords

Domain match

📊 4. ATS Report

You get:

ATS-Friendly Score

Readability score

Resume gaps

Actionable suggestions

🌐 5. Web UI (Next.js)

Upload resume

Paste job description

View report in realtime

Modern UI + animations
