# Final Year Project — Progress Dashboard

A web-based dashboard to track and present the progress, effort, and contributions made during our final year project. Built as part of our academic submission to maintain transparency, accountability, and structured documentation throughout the project lifecycle.

---

## About This Project

Managing a final year project involves more than just writing code. It includes research, system design, debugging, writing, and regular team coordination. This dashboard was built to capture all of that work in one place and present it clearly to supervisors and panel members.

---

## Features

- **Weekly Progress Tracking** — Log work done each week with dates and categories
- **Effort Breakdown** — Visual charts showing time spent on Research, Coding, Engineering, Debugging, and Writing
- **Team Contribution View** — Individual hours tracked per team member separately
- **Milestone Progress Bar** — Key project milestones tracked from start to completion
- **Weekly Velocity Chart** — Effort curve showing consistency of work across the semester
- **Full Task Log** — Every task logged is stored and visible with dates and categories

---

## Tech Stack

- **Frontend & Backend:** Streamlit
- **Language:** Python 3
- **Database:** SQLite (local, lightweight)
- **AI Processing:** Google Gemini API (for extracting structured data from weekly text reports)
- **Deployment:** Streamlit Community Cloud

---

## Project Structure

```
project-dashboard/
│
├── Home.py                        # Main dashboard page
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
│
├── pages/
│   ├── 1_📝_Submit_Report.py      # Weekly report submission page
│   └── 2_🏁_Milestones.py         # Milestone management page
│
└── .streamlit/
    └── secrets.toml               # API keys (not uploaded to GitHub)
```

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Charlie1777/Project_Dashboard.git
cd Project_Dashboard
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a file `.streamlit/secrets.toml` and add:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

**5. Run the app**
```bash
streamlit run Home.py
```

---

## Deployment

This dashboard is deployed live on Streamlit Community Cloud and can be accessed via the project URL without any local setup.

---

## Team

- **Member 1** — [Your Name]
- **Member 2** — [Partner Name]

**Institution:** [Your College/University Name]
**Academic Year:** 2025–2026
