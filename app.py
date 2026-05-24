import streamlit as st
import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =====================================================================
# 1. PAGE CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="Job Market Analysis | Quantum Cortex",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. GLOBAL PREMIUM CSS
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ---- Base ---- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Dark sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    border-right: 1px solid rgba(99,102,241,0.2);
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ---- Main background ---- */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #111127 100%);
}

/* ---- KPI Card ---- */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(139,92,246,0.08) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 16px;
    padding: 20px 20px 20px 24px;
    box-shadow: 0 4px 24px rgba(99,102,241,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.25);
}
div[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #e2e8f0 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ---- Section header ---- */
.section-header {
    background: linear-gradient(90deg, rgba(99,102,241,0.15) 0%, transparent 100%);
    border-left: 4px solid #6366f1;
    border-radius: 0 8px 8px 0;
    padding: 12px 20px;
    margin: 24px 0 16px 0;
}
.section-header h3 {
    color: #e2e8f0 !important;
    margin: 0;
    font-weight: 600;
    font-size: 1.1rem;
}

/* ---- Hero banner ---- */
.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #1e3a5f 100%);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.5);
    color: #a5b4fc;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 0.05em;
}

/* ---- Info card ---- */
.info-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 8px 0;
}

/* ---- Tabs styling ---- */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #818cf8 !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* ---- Buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.5) !important;
}

/* ---- Form inputs ---- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}

/* ---- Scrollbar ---- */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0f0f1a; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }

/* ---- Sidebar logo ---- */
.sidebar-logo {
    text-align: center;
    padding: 16px 0 8px 0;
    border-bottom: 1px solid rgba(99,102,241,0.2);
    margin-bottom: 16px;
}
.sidebar-logo h2 {
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 4px 0 0 0;
}

/* ---- Divider ---- */
.gradient-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), transparent);
    border: none;
    margin: 24px 0;
}

/* ---- Pipeline viewer ---- */
.pipeline-stage {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 10px;
    padding: 12px 16px;
    margin: 6px 0;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #a5b4fc;
}
.pipeline-arrow {
    text-align: center;
    color: #6366f1;
    font-size: 1.2rem;
    margin: 2px 0;
}

/* ---- Status badge ---- */
.status-online {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.3);
    color: #6ee7b7;
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ---- Mobile Responsiveness ---- */
@media (max-width: 768px) {
    .hero-banner {
        padding: 24px 20px;
    }
    .hero-title {
        font-size: 1.6rem;
    }
    div[data-testid="metric-container"] {
        padding: 16px;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 1.6rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. DATABASE CONNECTION
# =====================================================================
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client['JobMarketAnalytics']
jobs_col   = db['job_postings']
skills_col = db['skills']
js_col     = db['job_skills']
comp_col   = db['companies']

# =====================================================================
# 4. CACHED DATA FUNCTIONS
# =====================================================================
@st.cache_data(ttl=600)
def get_kpis():
    total        = jobs_col.count_documents({"is_deleted": {"$ne": True}})
    high_pay     = jobs_col.count_documents({"salary_details.max_salary": {"$gt": 100000}})
    entry        = jobs_col.count_documents({"category": "Entry Level"})
    full_time    = jobs_col.count_documents({"work_type": "FULL_TIME", "is_deleted": {"$ne": True}})
    with_salary  = jobs_col.count_documents({"salary_details.max_salary": {"$gt": 0}})
    companies    = comp_col.count_documents({})
    skills_count = skills_col.count_documents({})
    return total, high_pay, entry, full_time, with_salary, companies, skills_count

@st.cache_data(ttl=600)
def get_top_locations(n=10):
    pipeline = [
        {"$match": {"is_deleted": {"$ne": True}, "location": {"$nin": ["Not Specified", ""]}}},
        {"$group": {"_id": "$location", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": n}
    ]
    data = list(jobs_col.aggregate(pipeline))
    return pd.DataFrame(data).rename(columns={"_id": "Location", "count": "Jobs"})

@st.cache_data(ttl=600)
def get_work_types():
    pipeline = [
        {"$match": {"is_deleted": {"$ne": True}, "work_type": {"$ne": "Not Specified"}}},
        {"$group": {"_id": "$work_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    data = list(jobs_col.aggregate(pipeline))
    return pd.DataFrame(data).rename(columns={"_id": "Work Type", "count": "Count"})

@st.cache_data(ttl=600)
def get_salary_by_worktype():
    pipeline = [
        {"$match": {"salary_details.max_salary": {"$gt": 0}, "work_type": {"$ne": "Not Specified"}}},
        {"$group": {
            "_id": "$work_type",
            "avg_salary": {"$avg": "$salary_details.max_salary"},
            "max_salary": {"$max": "$salary_details.max_salary"},
            "count": {"$sum": 1}
        }},
        {"$sort": {"avg_salary": -1}}
    ]
    data = list(jobs_col.aggregate(pipeline))
    return pd.DataFrame(data).rename(columns={"_id": "Work Type", "avg_salary": "Avg Salary", "max_salary": "Max Salary", "count": "Count"})

@st.cache_data(ttl=600)
def get_top_skills(n=15):
    pipeline = [
        {"$group": {"_id": "$skill_abr", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": n}
    ]
    data = list(js_col.aggregate(pipeline))
    return pd.DataFrame(data).rename(columns={"_id": "Skill", "count": "Demand"})

@st.cache_data(ttl=600)
def get_applies_distribution():
    pipeline = [
        {"$match": {"applies": {"$gt": 0}, "is_deleted": {"$ne": True}}},
        {"$bucket": {
            "groupBy": "$applies",
            "boundaries": [1, 10, 25, 50, 100, 500],
            "default": "500+",
            "output": {"count": {"$sum": 1}}
        }}
    ]
    data = list(jobs_col.aggregate(pipeline))
    df = pd.DataFrame(data)
    df["_id"] = df["_id"].astype(str)
    return df.rename(columns={"_id": "Applies Range", "count": "Jobs"})

@st.cache_data(ttl=600)
def get_salary_histogram():
    pipeline = [
        {"$match": {"salary_details.max_salary": {"$gt": 0, "$lt": 500000}}},
        {"$project": {"salary": "$salary_details.max_salary"}}
    ]
    data = list(jobs_col.aggregate(pipeline))
    return pd.DataFrame(data)

@st.cache_data(ttl=600)
def get_top_companies(n=10):
    pipeline = [
        {"$match": {"is_deleted": {"$ne": True}}},
        {"$group": {"_id": "$company_id", "job_count": {"$sum": 1}}},
        {"$sort": {"job_count": -1}},
        {"$limit": n}
    ]
    data = list(jobs_col.aggregate(pipeline))
    return pd.DataFrame(data).rename(columns={"_id": "Company ID", "job_count": "Job Count"})

@st.cache_data(ttl=600)
def get_mapreduce_results():
    agg1 = list(jobs_col.aggregate([
        {"$group": {"_id": "$work_type", "total_jobs": {"$sum": 1}}},
        {"$sort": {"total_jobs": -1}}
    ]))
    agg2 = list(jobs_col.aggregate([
        {"$group": {"_id": "$work_type", "total_views": {"$sum": "$views"}}},
        {"$sort": {"total_views": -1}}
    ]))
    agg3 = list(jobs_col.aggregate([
        {"$match": {"salary_details.max_salary": {"$gt": 0}}},
        {"$group": {"_id": "$work_type", "avg_salary": {"$avg": "$salary_details.max_salary"}, "count": {"$sum": 1}}},
        {"$sort": {"avg_salary": -1}}
    ]))
    return (
        pd.DataFrame(agg1).rename(columns={"_id": "Work Type", "total_jobs": "Job Count"}),
        pd.DataFrame(agg2).rename(columns={"_id": "Work Type", "total_views": "Total Views"}),
        pd.DataFrame(agg3).rename(columns={"_id": "Work Type", "avg_salary": "Avg Max Salary", "count": "Count"})
    )

# =====================================================================
# 5. SIDEBAR
# =====================================================================
with st.sidebar:
    st.image("logo.png", use_container_width=True)

    st.markdown("###  Navigation")
    page = st.radio(
        "Select Page",
        [
            " Dashboard & KPIs",
            " Analytics & Charts",
            " Search & Filter",
            " Map-Reduce Viewer",
            " Manage Data (CRUD)"
        ],
        label_visibility="collapsed"
    )

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    st.markdown("###  Global Filters")
    exclude_deleted = st.toggle("Exclude Soft-Deleted", value=True)
    exclude_no_salary = st.toggle("With Salary Only", value=False)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    st.markdown("###  Team")
    st.markdown("""
    <div class="info-card">
        <div style="color:#818cf8; font-weight:700; font-size:1rem;"> Quantum Cortex</div>
        <div style="color:#64748b; font-size:0.8rem; margin-top:4px;">Big Data Engineering Team</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###  Database")
    st.markdown("""
    <div class="info-card">
        <span class="status-online">● ONLINE</span>
        <div style="color:#64748b; font-size:0.78rem; margin-top:8px;">JobMarketAnalytics Cluster</div>
        <div style="color:#475569; font-size:0.75rem;">MongoDB Atlas </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# PAGE 1: DASHBOARD & KPIs
# =====================================================================
if page == " Dashboard & KPIs":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge"> BIG DATA ANALYTICS PLATFORM</div>
        <div class="hero-title">Job Market Intelligence Hub</div>
        <div class="hero-subtitle">
            Real-time insights from 30,000+ job postings · MongoDB Atlas · Streamlit · Plotly
        </div>
    </div>
    """, unsafe_allow_html=True)

    total, high_pay, entry, full_time, with_salary, companies, skills_count = get_kpis()

    # ---- Row 1: 4 KPIs ----
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(" Total Active Jobs",      f"{total:,}")
    c2.metric(" High-Paying (+$100k)",   f"{high_pay:,}",  delta=f"{high_pay/total*100:.1f}% of total")
    c3.metric(" Entry Level Jobs",       f"{entry:,}")
    c4.metric(" Full-Time Roles",        f"{full_time:,}", delta=f"{full_time/total*100:.1f}% of total")

    st.markdown("")

    # ---- Row 2: 3 KPIs ----
    c5, c6, c7, c8 = st.columns(4)
    c5.metric(" Jobs With Salary Data",  f"{with_salary:,}", delta=f"{with_salary/total*100:.1f}%")
    c6.metric(" Companies",              f"{companies:,}")
    c7.metric(" Unique Skills",          f"{skills_count:,}")
    c8.metric(" DB Cluster Status",      "Online ")

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # ---- Mini Charts ----
    st.markdown("""<div class="section-header"><h3> Quick Snapshot</h3></div>""", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        df_wt = get_work_types()
        if not df_wt.empty:
            fig = px.pie(
                df_wt, values="Count", names="Work Type", hole=0.5,
                color_discrete_sequence=["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b","#ef4444","#ec4899"],
                template="plotly_dark",
                title="Work Type Distribution"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(font=dict(color="#94a3b8")),
                title=dict(font=dict(color="#e2e8f0", size=14))
            )
            fig.update_traces(textfont_color="white")
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        df_loc = get_top_locations(6)
        if not df_loc.empty:
            fig2 = px.bar(
                df_loc, x="Jobs", y="Location", orientation="h",
                color="Jobs", color_continuous_scale="Purples",
                template="plotly_dark", title="Top 6 Locations"
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(color="#94a3b8"), xaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0", size=14)),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig2, use_container_width=True)

    with col_c:
        df_sal = get_salary_by_worktype()
        if not df_sal.empty:
            fig3 = px.bar(
                df_sal.head(5), x="Work Type", y="Avg Salary",
                color="Avg Salary", color_continuous_scale="Blues",
                template="plotly_dark", title="Avg Salary by Work Type"
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0", size=14)),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig3, use_container_width=True)

# =====================================================================
# PAGE 2: ANALYTICS & CHARTS
# =====================================================================
elif page == " Analytics & Charts":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge"> DEEP ANALYTICS</div>
        <div class="hero-title">Advanced Data Visualizations</div>
        <div class="hero-subtitle">Dive into salary distributions, skill demand, company insights & more.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        " Geographic & Work Type",
        " Salary Intelligence",
        " Skills Analysis",
        " Company Insights"
    ])

    # ---- Tab 1: Geographic ----
    with tab1:
        st.markdown("""<div class="section-header"><h3> Geographic Distribution</h3></div>""", unsafe_allow_html=True)
        n_locs = st.slider("Number of top locations to display:", 5, 20, 10, key="loc_slider")
        df_loc = get_top_locations(n_locs)

        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(
                df_loc, x="Location", y="Jobs",
                color="Jobs", color_continuous_scale="Viridis",
                template="plotly_dark", title=f"Top {n_locs} Job Locations"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#94a3b8", tickangle=-35),
                yaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0")),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.treemap(
                df_loc, path=["Location"], values="Jobs",
                color="Jobs", color_continuous_scale="Purples",
                template="plotly_dark", title="Treemap of Job Density"
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                title=dict(font=dict(color="#e2e8f0"))
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""<div class="section-header"><h3> Work Type Breakdown</h3></div>""", unsafe_allow_html=True)
        df_wt = get_work_types()
        col3, col4 = st.columns(2)
        with col3:
            fig3 = px.pie(
                df_wt, values="Count", names="Work Type", hole=0.45,
                color_discrete_sequence=["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b","#ef4444","#ec4899"],
                template="plotly_dark", title="Work Type Split (Donut)"
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(font=dict(color="#94a3b8")),
                title=dict(font=dict(color="#e2e8f0"))
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            fig4 = px.funnel(
                df_wt.sort_values("Count", ascending=False),
                x="Count", y="Work Type",
                color_discrete_sequence=["#6366f1"],
                template="plotly_dark", title="Work Type Funnel"
            )
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                yaxis=dict(color="#94a3b8"), xaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0"))
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Application engagement
        st.markdown("""<div class="section-header"><h3> Application Engagement Distribution</h3></div>""", unsafe_allow_html=True)
        df_apps = get_applies_distribution()
        if not df_apps.empty:
            fig5 = px.bar(
                df_apps, x="Applies Range", y="Jobs",
                color="Jobs", color_continuous_scale="Oranges",
                template="plotly_dark", title="Jobs by Applications Received"
            )
            fig5.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0")),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig5, use_container_width=True)

    # ---- Tab 2: Salary ----
    with tab2:
        st.markdown("""<div class="section-header"><h3> Salary Intelligence Center</h3></div>""", unsafe_allow_html=True)

        df_sal_type = get_salary_by_worktype()
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                df_sal_type, x="Work Type", y="Avg Salary",
                color="Avg Salary", color_continuous_scale="Teal",
                template="plotly_dark", title="Average Max Salary by Work Type",
                text_auto=".2s"
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                title=dict(font=dict(color="#e2e8f0")),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = go.Figure(go.Scatter(
                x=df_sal_type["Work Type"],
                y=df_sal_type["Max Salary"],
                mode="markers+lines",
                marker=dict(size=14, color="#818cf8", line=dict(color="#6366f1", width=2)),
                line=dict(color="#6366f1", width=2, dash="dot"),
                name="Max Salary"
            ))
            fig2.update_layout(
                title="Peak Salary per Work Type",
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                title_font=dict(color="#e2e8f0")
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Histogram
        st.markdown("""<div class="section-header"><h3> Salary Distribution Histogram</h3></div>""", unsafe_allow_html=True)
        df_hist = get_salary_histogram()
        if not df_hist.empty:
            col3, col4 = st.columns([3, 1])
            with col4:
                bins = st.slider("Histogram Bins:", 20, 100, 40)
                show_box = st.checkbox("Add Box Plot overlay", value=True)

            with col3:
                if show_box:
                    fig3 = px.histogram(
                        df_hist, x="salary", nbins=bins,
                        color_discrete_sequence=["#6366f1"],
                        template="plotly_dark",
                        title="Max Salary Distribution (Filtered: < $500k)",
                        marginal="box"
                    )
                else:
                    fig3 = px.histogram(
                        df_hist, x="salary", nbins=bins,
                        color_discrete_sequence=["#6366f1"],
                        template="plotly_dark",
                        title="Max Salary Distribution (Filtered: < $500k)"
                    )
                fig3.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(color="#94a3b8", title="Salary (USD)"),
                    yaxis=dict(color="#94a3b8", title="Count"),
                    title=dict(font=dict(color="#e2e8f0"))
                )
                st.plotly_chart(fig3, use_container_width=True)

        # Salary table
        st.markdown("""<div class="section-header"><h3> Salary Summary Table</h3></div>""", unsafe_allow_html=True)
        df_sal_type["Avg Salary"] = df_sal_type["Avg Salary"].round(2)
        df_sal_type["Max Salary"] = df_sal_type["Max Salary"].round(2)
        st.dataframe(
            df_sal_type,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Avg Salary": st.column_config.NumberColumn("Avg Salary", format="$%.2f"),
                "Max Salary": st.column_config.NumberColumn("Max Salary", format="$%.2f"),
                "Count": st.column_config.NumberColumn("# Jobs"),
            }
        )

    # ---- Tab 3: Skills ----
    with tab3:
        st.markdown("""<div class="section-header"><h3> Top In-Demand Skills</h3></div>""", unsafe_allow_html=True)
        n_skills = st.slider("Number of skills to show:", 5, 35, 15, key="skills_slider")
        df_skills = get_top_skills(n_skills)

        if not df_skills.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    df_skills, x="Demand", y="Skill", orientation="h",
                    color="Demand", color_continuous_scale="Plasma",
                    template="plotly_dark", title=f"Top {n_skills} Skills by Demand"
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                    title=dict(font=dict(color="#e2e8f0")),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig2 = px.scatter(
                    df_skills, x="Skill", y="Demand",
                    size="Demand", color="Demand",
                    color_continuous_scale="Viridis",
                    template="plotly_dark", title="Skill Bubble Chart"
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(color="#94a3b8", tickangle=-45),
                    yaxis=dict(color="#94a3b8"),
                    title=dict(font=dict(color="#e2e8f0")),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig2, use_container_width=True)

            # Skills data table
            st.dataframe(
                df_skills,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Demand": st.column_config.ProgressColumn("Demand", min_value=0, max_value=int(df_skills["Demand"].max())),
                    "Skill": st.column_config.TextColumn("Skill Abbreviation")
                }
            )
        else:
            st.info("No skill data found in the database.")

    # ---- Tab 4: Companies ----
    with tab4:
        st.markdown("""<div class="section-header"><h3> Top Hiring Companies</h3></div>""", unsafe_allow_html=True)
        n_comp = st.slider("Number of companies:", 5, 20, 10, key="comp_slider")
        df_comp = get_top_companies(n_comp)

        if not df_comp.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    df_comp, x="Job Count", y="Company ID", orientation="h",
                    color="Job Count", color_continuous_scale="Teal",
                    template="plotly_dark", title=f"Top {n_comp} Companies by Job Postings"
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
                    title=dict(font=dict(color="#e2e8f0")),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig2 = px.pie(
                    df_comp.head(8), values="Job Count", names="Company ID",
                    hole=0.4, template="plotly_dark",
                    color_discrete_sequence=px.colors.sequential.Purples_r,
                    title="Top 8 Companies Share"
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    legend=dict(font=dict(color="#94a3b8")),
                    title=dict(font=dict(color="#e2e8f0"))
                )
                st.plotly_chart(fig2, use_container_width=True)

# =====================================================================
# PAGE 3: SEARCH & FILTER
# =====================================================================
elif page == " Search & Filter":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge"> INTELLIGENT SEARCH</div>
        <div class="hero-title">Advanced Query Engine</div>
        <div class="hero-subtitle">Filter thousands of records instantly with multi-criteria search.</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("search_form"):
        st.markdown("""<div class="section-header"><h3> Search Criteria</h3></div>""", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        search_term = col1.text_input(" Job Title Keyword", placeholder="e.g. Engineer, Manager...")
        location_filter = col2.text_input(" Location Keyword", placeholder="e.g. New York, Texas...")
        work_type_filter = col3.selectbox(
            " Work Type",
            ["All", "FULL_TIME", "PART_TIME", "CONTRACT", "INTERNSHIP", "TEMPORARY", "VOLUNTEER", "OTHER"]
        )

        col4, col5, col6 = st.columns(3)
        min_salary = col4.number_input(" Minimum Salary ($)", min_value=0, value=0, step=10000)
        max_salary = col5.number_input(" Maximum Salary ($)", min_value=0, value=0, step=10000,
                                        help="0 = no upper limit")
        limit = col6.slider(" Max Results", 10, 500, 50)

        sort_by = st.selectbox(" Sort By", ["Max Salary (High→Low)", "Max Salary (Low→High)", "Views (High→Low)", "Applies (High→Low)"])

        submit = st.form_submit_button(" Execute Search", use_container_width=True)

    if submit:
        with st.spinner(" Querying MongoDB Atlas..."):
            query = {"is_deleted": {"$ne": True}}

            if search_term:
                query["title"] = {"$regex": search_term, "$options": "i"}
            if location_filter:
                query["location"] = {"$regex": location_filter, "$options": "i"}
            if work_type_filter != "All":
                query["work_type"] = work_type_filter
            if min_salary > 0:
                query.setdefault("salary_details.max_salary", {})["$gte"] = float(min_salary)
            if max_salary > 0:
                query.setdefault("salary_details.max_salary", {})["$lte"] = float(max_salary)

            sort_map = {
                "Max Salary (High→Low)": ("salary_details.max_salary", -1),
                "Max Salary (Low→High)": ("salary_details.max_salary",  1),
                "Views (High→Low)":      ("views",  -1),
                "Applies (High→Low)":    ("applies", -1),
            }
            sort_field, sort_dir = sort_map[sort_by]

            cursor = jobs_col.find(query).sort(sort_field, sort_dir).limit(limit)
            df = pd.DataFrame(list(cursor))

        if not df.empty:
            df["_id"] = df["_id"].astype(str)
            if "salary_details" in df.columns:
                df["Max Salary"] = df["salary_details"].apply(
                    lambda x: x.get("max_salary", 0) if isinstance(x, dict) else 0
                )
                df["Min Salary"] = df["salary_details"].apply(
                    lambda x: x.get("min_salary", 0) if isinstance(x, dict) else 0
                )

            st.toast(f" Found {len(df)} matching records!")

            # Summary metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Results Found", f"{len(df):,}")
            m2.metric("Avg Max Salary", f"${df.get('Max Salary', pd.Series([0])).mean():,.0f}")
            m3.metric("Unique Locations", df['location'].nunique() if 'location' in df.columns else "—")
            m4.metric("Work Types", df['work_type'].nunique() if 'work_type' in df.columns else "—")

            # Results table
            display_cols = [c for c in ['job_id','title','company_id','location','work_type','Max Salary','Min Salary','applies','views'] if c in df.columns]
            st.dataframe(
                df[display_cols],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "job_id": st.column_config.TextColumn("Job ID"),
                    "title": st.column_config.TextColumn("Job Title", width="large"),
                    "company_id": st.column_config.TextColumn("Company ID"),
                    "location": st.column_config.TextColumn("Location"),
                    "work_type": st.column_config.TextColumn("Work Type"),
                    "Max Salary": st.column_config.NumberColumn("Max Salary", format="$%d"),
                    "Min Salary": st.column_config.NumberColumn("Min Salary", format="$%d"),
                    "applies": st.column_config.NumberColumn("Applications"),
                    "views": st.column_config.NumberColumn("Views"),
                }
            )

            # Quick chart of results
            if "work_type" in df.columns:
                wt_summary = df["work_type"].value_counts().reset_index()
                wt_summary.columns = ["Work Type", "Count"]
                fig = px.pie(
                    wt_summary, values="Count", names="Work Type", hole=0.4,
                    color_discrete_sequence=["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b"],
                    template="plotly_dark", title="Search Results - Work Type Split"
                )
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", title_font_color="#e2e8f0")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(" No jobs found matching your criteria. Try adjusting your filters.")

# =====================================================================
# PAGE 4: MAP-REDUCE VIEWER
# =====================================================================
elif page == " Map-Reduce Viewer":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge"> MAP-REDUCE ENGINE</div>
        <div class="hero-title">Map-Reduce Logic & Results</div>
        <div class="hero-subtitle">Classical Big Data paradigm: Map → Shuffle → Reduce — executed via Aggregation Pipelines.</div>
    </div>
    """, unsafe_allow_html=True)

    st.info(" MongoDB Atlas Free Tier doesn't support native `mapReduce` commands. The logic below shows the exact JavaScript Map/Reduce functions, and the results are produced by equivalent Aggregation Pipelines.")

    mr1, mr2, mr3 = get_mapreduce_results()

    # ---- Job 1 ----
    st.markdown("""<div class="section-header"><h3> Job 1: Frequency Counting — Jobs per Work Type</h3></div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("** Map Function**")
        st.code("""function() {
    emit(this.work_type, 1);
}""", language="javascript")

        st.markdown("** Reduce Function**")
        st.code("""function(key, values) {
    return Array.sum(values);
}""", language="javascript")

    with col2:
        fig = px.bar(
            mr1, x="Work Type", y="Job Count",
            color="Job Count", color_continuous_scale="Blues",
            template="plotly_dark", title="Result: Job Count per Work Type"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
            title=dict(font=dict(color="#e2e8f0")), coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(mr1, use_container_width=True, hide_index=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # ---- Job 2 ----
    st.markdown("""<div class="section-header"><h3> Job 2: Summation — Total Views per Work Type</h3></div>""", unsafe_allow_html=True)

    col3, col4 = st.columns([1, 1])
    with col3:
        st.markdown("** Map Function**")
        st.code("""function() {
    emit(this.work_type, this.views);
}""", language="javascript")

        st.markdown("** Reduce Function**")
        st.code("""function(key, values) {
    return Array.sum(values);
}""", language="javascript")

    with col4:
        fig2 = px.bar(
            mr2, x="Work Type", y="Total Views",
            color="Total Views", color_continuous_scale="Greens",
            template="plotly_dark", title="Result: Total Views per Work Type"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
            title=dict(font=dict(color="#e2e8f0")), coloraxis_showscale=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(mr2, use_container_width=True, hide_index=True)

    st.markdown('<hr class="gradient-divider">', unsafe_allow_html=True)

    # ---- Job 3 ----
    st.markdown("""<div class="section-header"><h3> Job 3: Custom Finalize — Average Salary per Work Type</h3></div>""", unsafe_allow_html=True)

    col5, col6 = st.columns([1, 1])
    with col5:
        st.markdown("** Map Function**")
        st.code("""function() {
    if (this.salary_details &&
        this.salary_details.max_salary > 0) {
        emit(this.work_type, {
            count: 1,
            total: this.salary_details.max_salary
        });
    }
}""", language="javascript")

        st.markdown("** Reduce Function**")
        st.code("""function(key, values) {
    var res = { count: 0, total: 0 };
    for (var i = 0; i < values.length; i++) {
        res.count += values[i].count;
        res.total += values[i].total;
    }
    return res;
}""", language="javascript")

        st.markdown("** Finalize Function**")
        st.code("""function(key, reducedVal) {
    reducedVal.average =
        reducedVal.total / reducedVal.count;
    return reducedVal;
}""", language="javascript")

    with col6:
        mr3_rounded = mr3.copy()
        mr3_rounded["Avg Max Salary"] = mr3_rounded["Avg Max Salary"].round(2)
        fig3 = px.bar(
            mr3_rounded, x="Work Type", y="Avg Max Salary",
            color="Avg Max Salary", color_continuous_scale="Oranges",
            template="plotly_dark", title="Result: Avg Salary per Work Type",
            text_auto=".2s"
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color="#94a3b8"), yaxis=dict(color="#94a3b8"),
            title=dict(font=dict(color="#e2e8f0")), coloraxis_showscale=False
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(
        mr3_rounded,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Avg Max Salary": st.column_config.NumberColumn("Avg Max Salary", format="$%.2f"),
            "Count": st.column_config.NumberColumn("Jobs Analyzed")
        }
    )

# =====================================================================
# PAGE 5: MANAGE DATA (CRUD)
# =====================================================================
elif page == " Manage Data (CRUD)":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge"> DATABASE ADMINISTRATION</div>
        <div class="hero-title">Secure CRUD Operations</div>
        <div class="hero-subtitle">Create, Read, Update, and Delete records with full backend validation.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        " Insert New Job",
        " Update Record",
        " Delete Record",
        " Raw Document Viewer"
    ])

    # ---- CREATE ----
    with tab1:
        st.markdown("""<div class="section-header"><h3> Insert a New Job Posting</h3></div>""", unsafe_allow_html=True)

        with st.form("insert_form"):
            col1, col2 = st.columns(2)
            ins_id     = col1.text_input("Job ID (Unique)*", placeholder="e.g. 9999999")
            ins_title  = col2.text_input("Job Title*", placeholder="e.g. Data Engineer")
            ins_comp   = col1.text_input("Company ID", placeholder="e.g. 12345")
            ins_loc    = col2.text_input("Location", placeholder="e.g. New York, NY")
            ins_type   = col1.selectbox("Work Type", ["FULL_TIME", "PART_TIME", "CONTRACT", "INTERNSHIP", "TEMPORARY", "VOLUNTEER", "OTHER"])
            ins_desc   = st.text_area("Description", placeholder="Job description here...", height=80)

            col3, col4, col5 = st.columns(3)
            ins_max_sal = col3.number_input("Max Salary ($)", min_value=0, value=60000, step=5000)
            ins_min_sal = col4.number_input("Min Salary ($)", min_value=0, value=40000, step=5000)
            ins_period  = col5.selectbox("Pay Period", ["YEARLY", "MONTHLY", "HOURLY", "WEEKLY"])

            submit_insert = st.form_submit_button(" Insert Document", use_container_width=True)

            if submit_insert:
                target_id = int(ins_id) if ins_id.isdigit() else ins_id
                
                if not ins_id or not ins_title:
                    st.error(" Job ID and Job Title are required.")
                elif jobs_col.find_one({"job_id": target_id}):
                    st.error(f" A job with Job ID {target_id} already exists! Job ID must be unique.")
                elif ins_min_sal > ins_max_sal:
                    st.error(" Min Salary cannot exceed Max Salary.")
                else:
                    new_doc = {
                        "job_id":       target_id,
                        "company_id":   int(ins_comp) if ins_comp.isdigit() else ins_comp if ins_comp else "Not Specified",
                        "title":        ins_title,
                        "description":  ins_desc if ins_desc else "Not Specified",
                        "location":     ins_loc if ins_loc else "Not Specified",
                        "work_type":    ins_type,
                        "salary_details": {
                            "max_salary": float(ins_max_sal),
                            "min_salary": float(ins_min_sal),
                            "pay_period": ins_period,
                            "currency":   "USD"
                        },
                        "applies":      0,
                        "views":        0,
                        "posting_date": datetime.now().isoformat(),
                        "is_deleted":   False
                    }
                    jobs_col.insert_one(new_doc)
                    st.success(f" Successfully inserted: **{ins_title}** (Job ID: {ins_id})")
                    st.cache_data.clear()

    # ---- UPDATE ----
    with tab2:
        st.markdown("""<div class="section-header"><h3> Update Job Record</h3></div>""", unsafe_allow_html=True)

        update_tab_a, update_tab_b = st.tabs([" Update Salary", "️ Update Category / Status"])

        with update_tab_a:
            with st.form("update_salary_form"):
                update_id = st.text_input("Target Job ID*", placeholder="Enter exact Job ID")
                col1, col2 = st.columns(2)
                new_max = col1.number_input("New Max Salary ($)", value=0, step=5000)
                new_min = col2.number_input("New Min Salary ($)", value=0, step=5000)
                submit_sal = st.form_submit_button(" Commit Salary Update", use_container_width=True)

                if submit_sal:
                    if not update_id:
                        st.warning("Please enter a Job ID.")
                    elif new_max < 0 or new_min < 0:
                        st.error(" Salary cannot be negative. Update aborted.")
                    elif new_min > new_max and new_max > 0:
                        st.error(" Min salary cannot exceed max salary. Update aborted.")
                    else:
                        target = int(update_id) if update_id.isdigit() else update_id
                        result = jobs_col.update_one(
                            {"job_id": target},
                            {"$set": {
                                "salary_details.max_salary": float(new_max),
                                "salary_details.min_salary": float(new_min),
                                "last_updated": datetime.now()
                            }}
                        )
                        if result.matched_count > 0:
                            st.success(f" Job ID **{update_id}** salary updated successfully!")
                            st.cache_data.clear()
                        else:
                            st.error(" No record found with this Job ID.")

        with update_tab_b:
            with st.form("update_category_form"):
                cat_id = st.text_input("Target Job ID*", placeholder="Enter exact Job ID")
                new_cat = st.selectbox("New Category", ["Entry Level", "Mid Level", "Senior", "Executive", "Needs Promotion"])
                new_status = st.selectbox("New Status", ["Active", "Needs Promotion", "Archived", "Pending Review"])
                submit_cat = st.form_submit_button(" Commit Category Update", use_container_width=True)

                if submit_cat:
                    if not cat_id:
                        st.warning("Please enter a Job ID.")
                    else:
                        target = int(cat_id) if cat_id.isdigit() else cat_id
                        result = jobs_col.update_one(
                            {"job_id": target},
                            {"$set": {"category": new_cat, "status": new_status, "last_updated": datetime.now()}}
                        )
                        if result.matched_count > 0:
                            st.success(f" Job ID **{cat_id}** updated: Category → {new_cat}, Status → {new_status}")
                            st.cache_data.clear()
                        else:
                            st.error(" No record found with this Job ID.")

    # ---- DELETE ----
    with tab3:
        st.markdown("""<div class="section-header"><h3> Delete Operations</h3></div>""", unsafe_allow_html=True)

        del_tab_a, del_tab_b = st.tabs([" Hard Delete (Permanent)", " Soft Delete (Flag Only)"])

        with del_tab_a:
            st.warning(" **Critical:** This permanently removes the document from the database. This action CANNOT be undone.")
            delete_id = st.text_input("Enter Job ID to permanently delete:", key="hard_del_id")
            confirm_del = st.checkbox("I understand this is irreversible", key="confirm_hard_del")

            if st.button(" Execute Hard Delete", disabled=not confirm_del):
                if delete_id:
                    target = int(delete_id) if delete_id.isdigit() else delete_id
                    result = jobs_col.delete_one({"job_id": target})
                    if result.deleted_count > 0:
                        st.success(f" Job ID **{delete_id}** permanently deleted.")
                        st.cache_data.clear()
                    else:
                        st.error(" No record found with this Job ID.")
                else:
                    st.warning("Please enter a Job ID.")

        with del_tab_b:
            st.info(" **Soft Delete:** Marks the record as deleted without removing it. Data is preserved for audit purposes.")
            soft_id = st.text_input("Enter Job ID to soft-delete:", key="soft_del_id")

            if st.button(" Execute Soft Delete"):
                if soft_id:
                    target = int(soft_id) if soft_id.isdigit() else soft_id
                    result = jobs_col.update_one(
                        {"job_id": target},
                        {"$set": {"is_deleted": True, "deleted_at": datetime.now()}}
                    )
                    if result.matched_count > 0:
                        st.success(f" Job ID **{soft_id}** flagged as deleted (still in DB).")
                        st.cache_data.clear()
                    else:
                        st.error(" No record found with this Job ID.")
                else:
                    st.warning("Please enter a Job ID.")

    # ---- RAW VIEWER ----
    with tab4:
        st.markdown("""<div class="section-header"><h3> Raw Document Viewer</h3></div>""", unsafe_allow_html=True)
        st.markdown("Fetch and inspect any raw document from MongoDB by Job ID.")

        view_id = st.text_input("Enter Job ID to view:", key="view_doc_id")
        if st.button(" Fetch Document"):
            if view_id:
                target = int(view_id) if view_id.isdigit() else view_id
                doc = jobs_col.find_one({"job_id": target})
                if doc:
                    doc["_id"] = str(doc["_id"])
                    st.json(doc)
                else:
                    st.error(" No document found with this Job ID.")
            else:
                st.warning("Please enter a Job ID.")