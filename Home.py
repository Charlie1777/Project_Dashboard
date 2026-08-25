import streamlit as st
# Reload trigger v2
import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(
    page_title="Final Year Project Dashboard",
    page_icon="🎓",
    layout="wide",
)

DB_PATH = Path("project_data.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT,
            member      TEXT,
            week_label  TEXT,
            raw_report  TEXT,
            tasks_json  TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            done  INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn

def load_tasks() -> pd.DataFrame:
    conn = get_db()
    rows = conn.execute("SELECT * FROM reports ORDER BY submitted_at DESC").fetchall()
    conn.close()
    if not rows:
        return pd.DataFrame()
    records = []
    for row in rows:
        tasks = json.loads(row[5]) if row[5] else []
        for t in tasks:
            t["member"]       = row[2]
            t["week_label"]   = row[3]
            t["submitted_at"] = row[1]
        records.extend(tasks)
    df = pd.DataFrame(records)
    if "hours" in df.columns:
        df["hours"] = pd.to_numeric(df["hours"], errors="coerce").fillna(0)
    return df

def load_milestones():
    conn = get_db()
    rows = conn.execute("SELECT title, done FROM milestones ORDER BY id").fetchall()
    conn.close()
    return rows

# ── HEADER ──────────────────────────────────────────────────────────────
col_title, col_refresh = st.columns([5, 1])
with col_title:
    st.title("🎓 Final Year Project — Progress Dashboard")
    st.caption(f"Live as of {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
with col_refresh:
    st.write("")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.divider()

df = load_tasks()

# ── EMPTY STATE ──────────────────────────────────────────────────────────
if df.empty:
    st.info("📋 No reports submitted yet. Go to **Submit Report** in the sidebar to log your first week.")
    st.stop()

# ── AT-A-GLANCE METRICS ──────────────────────────────────────────────────
st.subheader("📊 At a Glance")

total_hours   = df["hours"].sum()
total_tasks   = len(df)
total_weeks   = df["week_label"].nunique()
members       = df["member"].unique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("⏱ Total Hours Logged",  f"{total_hours:.1f} hrs")
c2.metric("✅ Tasks Completed",     total_tasks)
c3.metric("📅 Weeks Tracked",       total_weeks)
c4.metric("👥 Team Members",        len(members))

st.divider()

# ── MILESTONES ───────────────────────────────────────────────────────────
st.subheader("🏁 Project Milestones")

milestones = load_milestones()
if not milestones:
    st.info("No milestones added yet. Use the **Manage Milestones** page to add them.")
else:
    done_count = sum(1 for _, d in milestones if d)
    pct = done_count / len(milestones)
    st.progress(pct, text=f"{done_count}/{len(milestones)} completed — {int(pct*100)}%")
    cols = st.columns(2)
    for i, (title, done) in enumerate(milestones):
        icon = "✅" if done else "🔲"
        cols[i % 2].markdown(f"{icon} {title}")

st.divider()

# ── EFFORT CHARTS ────────────────────────────────────────────────────────
st.subheader("📈 Effort Breakdown")

col_cat, col_mem = st.columns(2)

with col_cat:
    if "category" in df.columns:
        cat_data = df.groupby("category")["hours"].sum().sort_values(ascending=False)
        st.bar_chart(cat_data)
        st.caption("Hours by work category")

with col_mem:
    mem_data = df.groupby("member")["hours"].sum().sort_values(ascending=False)
    st.bar_chart(mem_data)
    st.caption("Hours by team member")

st.divider()

# ── WEEKLY VELOCITY ──────────────────────────────────────────────────────
st.subheader("📅 Weekly Velocity")

weekly = df.groupby("week_label")["hours"].sum()
st.line_chart(weekly, use_container_width=True)
st.caption("Hours logged per week — this is your effort curve")

st.divider()

# ── RECENT WORK LOG ──────────────────────────────────────────────────────
st.subheader("📋 Recent Work Log")

show_cols = [c for c in ["week_label", "member", "category", "task", "hours", "evidence"] if c in df.columns]
display   = df[show_cols].sort_values("week_label", ascending=False).head(20)
display.columns = [c.title().replace("_", " ") for c in display.columns]
st.dataframe(display, use_container_width=True, hide_index=True)

with st.expander("View Full Log"):
    full = df[show_cols].sort_values("week_label", ascending=False)
    full.columns = [c.title().replace("_", " ") for c in full.columns]
    st.dataframe(full, use_container_width=True, hide_index=True)

# ── FOOTER ───────────────────────────────────────────────────────────────
st.divider()
st.caption("AI-powered project tracker · Reports processed by Claude · Built with Streamlit")
