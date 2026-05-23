# Job Market Analysis (Big Data Pipeline)

An end-to-end Big Data project that ingests, cleans, and analyzes a large dataset of job postings using MongoDB Atlas (Aggregation Framework & Map-Reduce logic), with an interactive Dashboard built in Streamlit.

## 🚀 Features
- **Data Ingestion & Cleaning:** Handled via Jupyter Notebook (`notebooke.ipynb`) utilizing PyMongo.
- **Advanced Aggregations:** Complex MongoDB pipelines for extracting metrics (Salaries, Geographic distributions, Work types).
- **Map-Reduce Fallback Logic:** Native Map-Reduce logic implemented as JS functions with Aggregation pipeline equivalents (due to Atlas M0 tier constraints).
- **Interactive UI:** Streamlit-powered dashboard (`app.py`) featuring Plotly charts, CRUD operations, and advanced filtering.

## 📦 Getting the Dataset
The dataset for this project is quite large and is **not included** in this repository. 
To run this project locally, you must first download the dataset (e.g., from Kaggle) and place the CSV files in the corresponding directories at the root of the project:
- `companies/`
- `jobs/`
- `mappings/`
- `postings/`

*(Make sure to update the file paths in the notebook if your folder structure differs).*

## 🛠️ How to Run Locally

### 1. Setup the Environment
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/YOUR_USERNAME/Big-Data-Job-Market-Analysis.git
cd Big-Data-Job-Market-Analysis
pip install -r requirements.txt
```

### 2. Configure MongoDB
Create a `.env` file in the root directory and add your MongoDB Atlas connection string:
```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority"
```

### 3. Ingest Data (Jupyter Notebook)
Run the `notebooke.ipynb` file cell-by-cell. This notebook will:
- Connect to your MongoDB cluster.
- Load the CSV files from the dataset folders.
- Clean the data and insert it into MongoDB.

### 4. Run the Streamlit Dashboard
Once the database is populated, launch the dashboard:
```bash
streamlit run app.py
```
