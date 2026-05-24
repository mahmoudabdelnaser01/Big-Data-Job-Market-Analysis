# 📊 Big Data Job Market Analytics Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-Charts-orange.svg)

An **End-to-End Big Data Engineering & Analytics** project designed to ingest, process, and visualize massive datasets of job postings. This project leverages the power of **MongoDB Atlas** for NoSQL data storage and complex Aggregation Pipelines (implementing classic Map-Reduce concepts), all wrapped in an interactive, premium **Streamlit** dashboard.

---

## 🎯 Project Overview
With the job market becoming increasingly data-driven, understanding salary trends, high-demand skills, and geographical distributions is critical. This project ingests over 30,000+ job postings, cleanses the raw data using Pandas in a Jupyter Notebook, and streams it into a cloud-hosted MongoDB Atlas cluster. The data is then dynamically queried and visualized in a real-time web application.

> **🎓 Academic Context:** This project was developed as a comprehensive final project for the **Big Data** course. It serves as a practical application of theoretical Big Data paradigms (such as Map-Reduce, Data Pipelines, and NoSQL Aggregation) on a real-world dataset to extract meaningful business intelligence.

---

## 🏗️ Architecture & Pipeline
1. **Data Source:** Raw CSV files containing job postings, skills, and company data.
2. **Data Processing (`notebooke.ipynb`):** Data cleaning, deduplication, formatting, and batch insertion into MongoDB using `PyMongo`.
3. **Data Storage:** Cloud-hosted NoSQL database (**MongoDB Atlas**).
4. **Data Analytics (`app.py`):** Execution of complex Aggregation Pipelines and pseudo-Map-Reduce logic.
5. **Visualization:** A multi-page Streamlit web application featuring advanced Plotly charts and metrics.

---

## 🚀 Key Features

### 1. 📈 Real-Time KPIs & Dashboard
- Live tracking of total jobs, high-paying roles (+$100k), entry-level positions, and active companies.
- Quick snapshot visualizations of Top Work Types and Geographic Distributions.

### 2. 📊 Deep Analytics Engine
- **Geographic & Work Type:** Treemaps and Funnel charts detailing job density across states and remote opportunities.
- **Salary Intelligence:** Scatter plots, Bar charts, and Box-Plot Overlaid Histograms analyzing salary distributions across different categories.
- **Skills Analysis:** Bubble charts and progress bars highlighting the most in-demand technical skills.
- **Company Insights:** Pie charts and horizontal bars showing the top hiring companies in the market.

### 3. 🧠 Map-Reduce & Aggregation Logic
- Dedicated module demonstrating classic Big Data **Map-Reduce** logic.
- Displays raw JavaScript Map and Reduce functions alongside their execution results via MongoDB's Aggregation Framework (adapted for modern Atlas clusters).

### 4. 🔍 Intelligent Search Engine
- Multi-criteria search allowing users to filter by Job Title, Location, Work Type, and Salary Ranges.
- Dynamic data tables and metric summaries generated instantly based on query results.

### 5. ⚙️ Full CRUD Administration
- **Create:** Insert new job postings with full data validation (e.g., Min/Max salary checks, Unique ID constraints).
- **Read:** Raw Document Viewer to inspect JSON payloads directly from the database.
- **Update:** Modify salaries, categories, and job statuses dynamically.
- **Delete:** Support for both Hard Deletes (permanent removal) and Soft Deletes (flagging records for audit purposes).

---

## 🗂️ Project Structure

```text
Big-Data-Job-Market-Analysis/
│
├── app.py                  # Main Streamlit Dashboard application
├── notebooke.ipynb         # Jupyter Notebook for data ingestion and cleaning
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (MongoDB connection string)
├── .gitignore              # Git ignore file (excludes datasets and secrets)
├── README.md               # Project documentation
│
└── [Dataset Folders]       # (Ignored in Git, download separately)
    ├── companies/
    ├── jobs/
    ├── mappings/
    └── postings/
```

---

## 📦 Getting the Dataset
Due to its large size, the raw dataset is **not included** in this repository. 
To run this project locally, you must first download the dataset from Kaggle:

👉 **[LinkedIn Job Postings (2023) - Kaggle Dataset](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings)**

After downloading, extract the archive and place the CSV folders directly into the root of this project:
- `companies/`
- `jobs/`
- `mappings/`
- `postings/`

*(Ensure the folder names exactly match the paths defined in `notebooke.ipynb`)*.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Big-Data-Job-Market-Analysis.git
cd Big-Data-Job-Market-Analysis
```

### 2. Install Dependencies
Create a virtual environment (optional but recommended) and install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Configure the Database
Create a `.env` file in the root directory and add your MongoDB Atlas connection URI:
```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
```

### 4. Ingest the Data
Open and run the `notebooke.ipynb` file cell-by-cell in your preferred Jupyter environment (VSCode, JupyterLab). This will parse the local CSV files and populate your cloud database.

### 5. Launch the Dashboard
Start the Streamlit application:
```bash
streamlit run app.py
```
The dashboard will open automatically in your browser at `http://localhost:8501`.

---
*Built by Quantum Cortex Team - Big Data Engineering.*
