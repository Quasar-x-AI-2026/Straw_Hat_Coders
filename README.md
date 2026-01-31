# 🧠 Straw Hat Coders – AI Health & Intelligence System

An AI-powered multi-module application built using **Streamlit**, **Computer Vision**, and **Generative AI** to analyze mental health patterns, pose/movement data, and interactive AI insights — all in one dashboard.

---

## 🚀 Features

- 🧠 **Mental Health Analysis**
  - AI-based emotional and behavioral pattern tracking
  - Data visualization using charts and trends

- 🏃 **Pose & Movement Analysis**
  - Real-time posture and movement detection
  - Built using MediaPipe and OpenCV
  - Injury risk and motion pattern insights

- 🤖 **Generative AI Integration**
  - Uses Google Generative AI (Gemini) for intelligent responses
  - Environment-based secure API handling

- 📊 **Interactive Dashboards**
  - Built with Streamlit
  - Clean UI with dynamic charts and tables

- 🔌 **Gradio Client Support**
  - External AI inference and model interaction

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend:** Python  
- **Computer Vision:** OpenCV, MediaPipe  
- **Data Science:** Pandas, NumPy, SciPy  
- **Visualization:** Matplotlib  
- **AI / LLM:** Google Generative AI (Gemini)  
- **Environment Management:** python-dotenv  
- **Database:** SQLite  

# 🧠 Straw Hat Coders – AI Health & Intelligence System

An AI-powered multi-module application built using **Streamlit**, **Computer Vision**, and **Generative AI** to analyze mental health patterns, pose/movement data, and interactive AI insights — all in one dashboard.

---

## 🚀 Features

- 🧠 **Mental Health Analysis**
  - AI-based emotional and behavioral pattern tracking
  - Data visualization using charts and trends

- 🏃 **Pose & Movement Analysis**
  - Real-time posture and movement detection
  - Built using MediaPipe and OpenCV
  - Injury risk and motion pattern insights

- 🤖 **Generative AI Integration**
  - Uses Google Generative AI (Gemini) for intelligent responses
  - Environment-based secure API handling

- 📊 **Interactive Dashboards**
  - Built with Streamlit
  - Clean UI with dynamic charts and tables

- 🔌 **Gradio Client Support**
  - External AI inference and model interaction

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend:** Python  
- **Computer Vision:** OpenCV, MediaPipe  
- **Data Science:** Pandas, NumPy, SciPy  
- **Visualization:** Matplotlib  
- **AI / LLM:** Google Generative AI (Gemini)  
- **Environment Management:** python-dotenv  
- **Database:** SQLite  

---

## 📁 Project Structure

# 🧠 Straw Hat Coders – AI Health & Intelligence System

An AI-powered multi-module application built using **Streamlit**, **Computer Vision**, and **Generative AI** to analyze mental health patterns, pose/movement data, and interactive AI insights — all in one dashboard.

---

## 🚀 Features

- 🧠 **Mental Health Analysis**
  - AI-based emotional and behavioral pattern tracking
  - Data visualization using charts and trends

- 🏃 **Pose & Movement Analysis**
  - Real-time posture and movement detection
  - Built using MediaPipe and OpenCV
  - Injury risk and motion pattern insights

- 🤖 **Generative AI Integration**
  - Uses Google Generative AI (Gemini) for intelligent responses
  - Environment-based secure API handling

- 📊 **Interactive Dashboards**
  - Built with Streamlit
  - Clean UI with dynamic charts and tables

- 🔌 **Gradio Client Support**
  - External AI inference and model interaction

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend:** Python  
- **Computer Vision:** OpenCV, MediaPipe  
- **Data Science:** Pandas, NumPy, SciPy  
- **Visualization:** Matplotlib  
- **AI / LLM:** Google Generative AI (Gemini)  
- **Environment Management:** python-dotenv  
- **Database:** SQLite  


---

## 📁 Project Structure

Straw_Hat_Coders/
│
├── app.py / main.py # Streamlit entry point
├── mental_analysis/ # Mental health analysis modules
├── pose_estimation/ # Pose & movement analysis
├── data/ # SQLite DB / CSV files
├── assets/ # Images / static files
├── requirements.txt # Project dependencies
├── .env # Environment variables (not committed)
└── README.md # Project documentation


---

## 🏗️ Project Architecture

The **Straw Hat Coders – AI Health & Intelligence System** follows a **modular, layered architecture** that cleanly separates UI, logic, AI processing, and data handling.

---

### 🔹 High-Level Architecture Overview

┌──────────────────────────┐
│ User (Browser) │
└─────────────┬────────────┘
│
▼
┌──────────────────────────┐
│ Streamlit UI Layer │
│ (Dashboards & Controls) │
└─────────────┬────────────┘
│
▼
┌──────────────────────────┐
│ Application Logic Layer│
│ (Mental / Pose Modules) │
└─────────────┬────────────┘
│
┌─────────┴─────────┐
▼ ▼
┌───────────────┐ ┌────────────────┐
│ Computer Vision│ │ Generative AI │
│ (MediaPipe + │ │ (Gemini API) │
│ OpenCV) │ └────────────────┘
└───────────────┘
│
▼
┌──────────────────────────┐
│ Data & Storage Layer │
│ (SQLite, CSV, JSON) │
└──────────────────────────┘

mental_analysis/
│ ├── data_processing.py
│ ├── visualization.py
│ └── insights.py

pose_estimation/
│ ├── pose_detection.py
│ ├── movement_analysis.py
│ └── risk_evaluation.py


## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Quasar-x-AI-2026/Straw_Hat_Coders.git
cd Straw_Hat_Coders

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Environment Variables

Create a .env file in the root directory:

GOOGLE_API_KEY=your_google_generative_ai_key


streamlit run app.py

