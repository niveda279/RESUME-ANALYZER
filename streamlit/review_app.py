"""
CareerCast — Enhanced Streamlit Review Interface (Milestone 4)
==============================================================
Tabs:
  1. 📄 Resume Analysis   — upload & analyse a resume via FastAPI v2
  2. 📊 Cohort Analytics  — aggregate stats from the SQLite DB
  3. 🔀 Career Comparison — side-by-side required-skills comparison
  4. 📥 PDF Export        — generate & download a professional PDF report

Requirements (install individually if not already in requirements.txt):
    pip install streamlit>=1.25.0 reportlab>=4.0.0 pandas altair python-dotenv
"""

import os
import sys
import io
import json
import sqlite3
import datetime

import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
for _p in [ROOT_DIR, BACKEND_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

load_dotenv()
API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000/api/v2")
DB_PATH = os.environ.get("DB_PATH", os.path.join(BACKEND_DIR, "careercast.db"))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerCast · Review Interface",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: #f8fafc;
        margin-bottom: 0.75rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.75rem;
    }
    .badge-green  { color: #22c55e; font-weight: 600; }
    .badge-red    { color: #ef4444; font-weight: 600; }
    .badge-yellow { color: #f59e0b; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="hero-title">🚀 CareerCast — Milestone 4</div>', unsafe_allow_html=True)
st.caption("AI-Powered Resume Analyzer · Review Interface")
st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# Tabs
# ═══════════════════════════════════════════════════════════════════════════════
TAB_ANALYSIS, TAB_COHORT, TAB_COMPARE, TAB_PDF = st.tabs([
    "📄 Resume Analysis",
    "📊 Cohort Analytics",
    "🔀 Career Comparison",
    "📥 PDF Export",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Resume Analysis
# ═══════════════════════════════════════════════════════════════════════════════
with TAB_ANALYSIS:
    st.subheader("Upload a Resume for Instant Analysis")
    uploaded_file = st.file_uploader(
        "Drop your resume here (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        help="Maximum 10 MB. The file is sent to the local FastAPI backend for processing.",
    )

    if uploaded_file:
        st.info(f"✅ **{uploaded_file.name}** loaded — click **Run Analysis** to proceed.")

        if st.button("▶ Run Analysis", type="primary"):
            with st.spinner("Contacting backend…"):
                try:
                    # ── Prediction ────────────────────────────────────────────
                    files     = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    pred_resp = requests.post(f"{API_URL}/predict", files=files, timeout=60)
                    pred_resp.raise_for_status()
                    pred_data = pred_resp.json()

                    prediction = pred_data.get("prediction", {})
                    parsed     = pred_data.get("parsed_data", {})
                    raw_text   = parsed.get("raw_text", "")

                    # ── Skill Gap ─────────────────────────────────────────────
                    gap_resp = requests.post(
                        f"{API_URL}/skill-gap",
                        json={"raw_text": raw_text,
                              "target_role": prediction.get("predicted_role", "Software Engineer")},
                        timeout=30,
                    )
                    gap_resp.raise_for_status()
                    gap_data     = gap_resp.json()
                    gap_analysis = gap_data.get("gap_analysis", {})

                    # ── Recommendation (all 3 models) ─────────────────────────
                    rec_resp = requests.post(
                        f"{API_URL}/recommendation",
                        json={"raw_text": raw_text},
                        timeout=30,
                    )
                    all_models = {}
                    if rec_resp.status_code == 200:
                        all_models = rec_resp.json().get("recommendations", {})

                    # Store in session state for PDF tab
                    st.session_state["analysis_result"] = {
                        "parsed": parsed,
                        "prediction": prediction,
                        "gap_analysis": gap_analysis,
                        "all_models": all_models,
                    }

                    st.success("✅ Analysis complete!")

                    # ── Results layout ────────────────────────────────────────
                    col_pred, col_gap = st.columns(2, gap="large")

                    with col_pred:
                        st.markdown("#### 🎯 Career Prediction")
                        role       = prediction.get("predicted_role", "Unknown")
                        confidence = prediction.get("confidence", 0)
                        color = "badge-green" if confidence >= 70 else (
                                "badge-yellow" if confidence >= 40 else "badge-red")
                        st.markdown(
                            f'<div class="metric-card">'
                            f'<div style="font-size:1.4rem;font-weight:700;">{role}</div>'
                            f'<div class="{color}" style="margin-top:4px;">Confidence: {confidence:.1f}%</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

                        breakdown = prediction.get("breakdown", [])
                        if breakdown:
                            df_br = pd.DataFrame(breakdown).set_index("role")
                            st.bar_chart(df_br["probability"], height=200)

                        # All 3 models
                        if all_models:
                            st.markdown("**All Model Predictions**")
                            model_labels = {
                                "logistic_regression": "LR",
                                "random_forest":       "RF",
                                "xgboost":             "XGB",
                            }
                            for key, label in model_labels.items():
                                m = all_models.get(key, {})
                                if m.get("predicted_role"):
                                    st.caption(
                                        f"**{label}**: {m['predicted_role']} "
                                        f"({m.get('confidence', 0):.1f}%)"
                                    )

                    with col_gap:
                        st.markdown("#### 🛠️ Skill Gap")
                        match_pct = gap_analysis.get("match_percentage", 0)
                        st.progress(match_pct / 100.0, text=f"Skill Match: {match_pct}%")

                        matched = gap_analysis.get("matched_skills", [])
                        missing = gap_analysis.get("missing_skills", [])
                        st.markdown(
                            f'<span class="badge-green">✔ Matched ({len(matched)})</span>: '
                            f'{", ".join(s["skill"] for s in matched) or "None"}',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<span class="badge-red">✘ Missing ({len(missing)})</span>: '
                            f'{", ".join(s["skill"] for s in missing) or "None"}',
                            unsafe_allow_html=True,
                        )

                        priority_gaps = gap_analysis.get("priority_gaps", [])
                        if priority_gaps:
                            st.markdown("**🚨 Priority Improvements**")
                            for gap_item in priority_gaps:
                                with st.expander(
                                    f"{gap_item['skill']} · {gap_item['priority']}"
                                ):
                                    st.write(gap_item["suggestion"])

                    # ── Parsed entities ───────────────────────────────────────
                    with st.expander("🔍 Parsed Resume Entities"):
                        st.json({k: v for k, v in parsed.items() if k != "raw_text"})

                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Cannot reach backend. "
                        "Make sure the FastAPI server is running on `http://127.0.0.1:5000`."
                    )
                except Exception as exc:
                    st.error(f"❌ Error: {exc}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Cohort Analytics
# ═══════════════════════════════════════════════════════════════════════════════
with TAB_COHORT:
    st.subheader("Cohort Analytics — Aggregate Resume Data")
    st.caption(f"Reading from: `{DB_PATH}`")

    if not os.path.isfile(DB_PATH):
        st.warning(
            "⚠️ Database file not found. "
            "Upload at least one resume via the API to populate data."
        )
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            df_raw = pd.read_sql_query(
                "SELECT id, prediction, confidence, green_flags, red_flags, "
                "parsed_entities, created_at FROM resumes ORDER BY created_at DESC",
                conn,
            )
            conn.close()
        except Exception as exc:
            st.error(f"DB read error: {exc}")
            df_raw = pd.DataFrame()

        if df_raw.empty:
            st.info("No resume records found in the database yet.")
        else:
            # ── KPI row ───────────────────────────────────────────────────────
            st.markdown('<div class="section-header">Overview</div>', unsafe_allow_html=True)
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Total Resumes Analysed", len(df_raw))
            k2.metric("Unique Roles Predicted", df_raw["prediction"].nunique())
            k3.metric("Avg Confidence", f"{df_raw['confidence'].mean():.1f}%")
            k4.metric("Latest Analysis", df_raw["created_at"].iloc[0][:10]
                      if df_raw["created_at"].notna().any() else "—")

            st.divider()

            # ── Role distribution ─────────────────────────────────────────────
            st.markdown('<div class="section-header">Role Distribution</div>',
                        unsafe_allow_html=True)
            role_counts = df_raw["prediction"].value_counts().reset_index()
            role_counts.columns = ["Role", "Count"]
            col_chart, col_table = st.columns([2, 1])
            with col_chart:
                st.bar_chart(role_counts.set_index("Role"), height=280)
            with col_table:
                st.dataframe(role_counts, hide_index=True, use_container_width=True)

            # ── Confidence distribution ───────────────────────────────────────
            st.divider()
            st.markdown('<div class="section-header">Confidence Score Distribution</div>',
                        unsafe_allow_html=True)
            conf_bins = pd.cut(
                df_raw["confidence"],
                bins=[0, 40, 60, 80, 100],
                labels=["Low (<40%)", "Medium (40-60%)", "Good (60-80%)", "High (>80%)"],
            )
            conf_dist = conf_bins.value_counts().reset_index()
            conf_dist.columns = ["Confidence Tier", "Count"]
            st.bar_chart(conf_dist.set_index("Confidence Tier"), height=200)

            # ── Skill frequency ───────────────────────────────────────────────
            st.divider()
            st.markdown('<div class="section-header">Most Common Skills (across all resumes)</div>',
                        unsafe_allow_html=True)
            all_skills = []
            for row in df_raw["parsed_entities"]:
                try:
                    entities = json.loads(row) if isinstance(row, str) else row
                    all_skills.extend(entities.get("skills", []))
                except Exception:
                    pass

            if all_skills:
                skill_series = pd.Series(all_skills).value_counts().head(15)
                skill_df = skill_series.reset_index()
                skill_df.columns = ["Skill", "Frequency"]
                st.bar_chart(skill_df.set_index("Skill"), height=260)
            else:
                st.info("No skill data found in stored entities.")

            # ── Raw data table ────────────────────────────────────────────────
            with st.expander("📋 View Raw Records"):
                st.dataframe(
                    df_raw[["id", "prediction", "confidence", "created_at"]],
                    use_container_width=True,
                    hide_index=True,
                )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Career Comparison
# ═══════════════════════════════════════════════════════════════════════════════
with TAB_COMPARE:
    st.subheader("Career Comparison — Required Skills Side-by-Side")
    st.caption("Compare the skill requirements for up to 4 career roles simultaneously.")

    try:
        from services.skill_gap import COMPETENCY_MAPPING
        ALL_ROLES = list(COMPETENCY_MAPPING.keys())
    except ImportError:
        ALL_ROLES = [
            "Data Scientist", "Software Engineer", "Web Developer", "Data Analyst",
            "DevOps Engineer", "Business Analyst", "ML Engineer", "Product Manager",
            "Cyber Security Specialist", "Cloud Architect",
        ]
        COMPETENCY_MAPPING = {}

    selected_roles = st.multiselect(
        "Select roles to compare (2–4 recommended):",
        options=ALL_ROLES,
        default=ALL_ROLES[:3],
        max_selections=4,
    )

    if len(selected_roles) < 2:
        st.info("Please select at least 2 roles to compare.")
    elif COMPETENCY_MAPPING:
        # ── Build comparison table ────────────────────────────────────────────
        priority_order = {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1}
        priority_emoji = {"Critical": "🔴", "High": "🟠", "Moderate": "🟡", "Low": "🟢"}

        all_skills = set()
        for role in selected_roles:
            all_skills.update(COMPETENCY_MAPPING.get(role, {}).keys())

        rows = []
        for skill in sorted(all_skills):
            row = {"Skill": skill}
            for role in selected_roles:
                priority = COMPETENCY_MAPPING.get(role, {}).get(skill)
                if priority:
                    row[role] = f"{priority_emoji.get(priority, '')} {priority}"
                else:
                    row[role] = "—"
            rows.append(row)

        df_compare = pd.DataFrame(rows)
        st.markdown("##### Skill Requirements Matrix")
        st.caption("🔴 Critical  🟠 High  🟡 Moderate  🟢 Low  — Not required")
        st.dataframe(df_compare.set_index("Skill"), use_container_width=True)

        # ── Skill count bar chart ─────────────────────────────────────────────
        st.divider()
        st.markdown("##### Number of Required Skills by Priority")
        chart_data = {}
        for role in selected_roles:
            skills_map = COMPETENCY_MAPPING.get(role, {})
            counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}
            for p in skills_map.values():
                counts[p] = counts.get(p, 0) + 1
            chart_data[role] = counts

        df_chart = pd.DataFrame(chart_data).T
        st.bar_chart(df_chart, height=280)
    else:
        st.warning("COMPETENCY_MAPPING not available. Ensure backend is on sys.path.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PDF Export
# ═══════════════════════════════════════════════════════════════════════════════
with TAB_PDF:
    st.subheader("PDF Export — Download Professional Analysis Report")

    if "analysis_result" not in st.session_state:
        st.info(
            "👆 Run a resume analysis in the **Resume Analysis** tab first, "
            "then come back here to download a PDF report."
        )
    else:
        result = st.session_state["analysis_result"]
        parsed     = result.get("parsed", {})
        prediction = result.get("prediction", {})
        gap        = result.get("gap_analysis", {})

        st.markdown(f"""
        **Candidate**: {parsed.get('name', 'N/A')}  
        **Predicted Role**: {prediction.get('predicted_role', 'N/A')} ({prediction.get('confidence', 0):.1f}%)  
        **Skill Match**: {gap.get('match_percentage', 0)}%  
        """)

        if st.button("📄 Generate PDF Report", type="primary"):
            with st.spinner("Generating PDF…"):
                pdf_bytes = _generate_pdf_report(parsed, prediction, gap)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"careercast_report_{parsed.get('name', 'candidate').replace(' ', '_')}.pdf",
                    mime="application/pdf",
                )
            st.success("✅ PDF ready!")


# ═══════════════════════════════════════════════════════════════════════════════
# PDF generation helper (placed after tabs so it can be called from the tab)
# ═══════════════════════════════════════════════════════════════════════════════
def _generate_pdf_report(parsed: dict, prediction: dict, gap: dict) -> bytes:
    """
    Generate a CareerCast skill gap PDF report using reportlab.
    Returns raw PDF bytes.
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, KeepTogether,
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        # Fallback: plain-text if reportlab is missing
        text_report = _generate_text_report(parsed, prediction, gap)
        return text_report.encode("utf-8")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    PURPLE = colors.HexColor("#6366f1")
    DARK   = colors.HexColor("#1e293b")
    SLATE  = colors.HexColor("#64748b")
    GREEN  = colors.HexColor("#22c55e")
    RED    = colors.HexColor("#ef4444")
    AMBER  = colors.HexColor("#f59e0b")

    title_style = ParagraphStyle(
        "Title", parent=styles["Title"],
        textColor=PURPLE, fontSize=22, spaceAfter=4, alignment=TA_CENTER,
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Normal"],
        textColor=SLATE, fontSize=9, alignment=TA_CENTER, spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Heading2"],
        textColor=PURPLE, fontSize=13, spaceBefore=12, spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        textColor=DARK, fontSize=10, leading=14,
    )
    tag_style = ParagraphStyle(
        "Tag", parent=body_style, textColor=SLATE, fontSize=9,
    )

    elements = []

    # ── Header ────────────────────────────────────────────────────────────────
    elements.append(Paragraph("CareerCast", title_style))
    elements.append(Paragraph(
        f"AI-Powered Career Analysis Report · {datetime.date.today().strftime('%B %d, %Y')}",
        sub_style,
    ))
    elements.append(HRFlowable(width="100%", thickness=1, color=PURPLE))
    elements.append(Spacer(1, 0.2 * inch))

    # ── Candidate Info ────────────────────────────────────────────────────────
    elements.append(Paragraph("Candidate Information", h2_style))
    info_data = [
        ["Name",           parsed.get("name", "N/A")],
        ["Email",          parsed.get("email", "N/A")],
        ["Phone",          parsed.get("phone", "N/A")],
        ["Education",      parsed.get("education", "N/A")],
        ["Certifications", parsed.get("certifications", "N/A")],
    ]
    info_table = Table(info_data, colWidths=[1.5 * inch, 5 * inch])
    info_table.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",   (0, 0), (0, -1), PURPLE),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.15 * inch))

    # ── Career Prediction ─────────────────────────────────────────────────────
    elements.append(Paragraph("Career Prediction", h2_style))
    role       = prediction.get("predicted_role", "Unknown")
    confidence = prediction.get("confidence", 0)
    conf_color = GREEN if confidence >= 70 else (AMBER if confidence >= 40 else RED)
    pred_data  = [
        ["Predicted Role", role],
        ["Confidence", f"{confidence:.1f}%"],
    ]
    pred_table = Table(pred_data, colWidths=[1.5 * inch, 5 * inch])
    pred_table.setStyle(TableStyle([
        ("FONTNAME",    (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME",    (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",   (0, 0), (0, -1), PURPLE),
        ("TEXTCOLOR",   (1, 0), (1, 0), DARK),
        ("TEXTCOLOR",   (1, 1), (1, 1), conf_color),
        ("FONTSIZE",    (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
    ]))
    elements.append(pred_table)
    elements.append(Spacer(1, 0.15 * inch))

    # ── Skills ────────────────────────────────────────────────────────────────
    elements.append(Paragraph("Detected Skills", h2_style))
    skills = parsed.get("skills", [])
    elements.append(Paragraph(
        ", ".join(skills) if skills else "No skills detected.",
        body_style,
    ))
    elements.append(Spacer(1, 0.1 * inch))

    # ── Skill Gap ─────────────────────────────────────────────────────────────
    elements.append(Paragraph("Skill Gap Analysis", h2_style))
    match_pct = gap.get("match_percentage", 0)
    fill_bar  = "█" * int(match_pct / 5)
    empty_bar = "░" * (20 - int(match_pct / 5))
    bar_color = GREEN if match_pct >= 70 else (AMBER if match_pct >= 40 else RED)

    elements.append(Paragraph(f"Overall Match: {match_pct}%", body_style))
    elements.append(Spacer(1, 0.05 * inch))

    matched = gap.get("matched_skills", [])
    missing = gap.get("missing_skills", [])

    gap_data = [
        [Paragraph("<b>✔ Matched Skills</b>", body_style),
         Paragraph(", ".join(s["skill"] for s in matched) or "None", tag_style)],
        [Paragraph("<b>✘ Missing Skills</b>", body_style),
         Paragraph(", ".join(s["skill"] for s in missing) or "None", tag_style)],
    ]
    gap_table = Table(gap_data, colWidths=[1.5 * inch, 5 * inch])
    gap_table.setStyle(TableStyle([
        ("FONTNAME",     (0, 0), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",    (0, 0), (0, 0), GREEN),
        ("TEXTCOLOR",    (0, 1), (0, 1), RED),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 0), (-1, -1), [colors.white, colors.HexColor("#fef2f2")]),
        ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
    ]))
    elements.append(gap_table)
    elements.append(Spacer(1, 0.15 * inch))

    # ── Priority Recommendations ───────────────────────────────────────────────
    priority_gaps = gap.get("priority_gaps", [])
    if priority_gaps:
        elements.append(Paragraph("Priority Improvement Recommendations", h2_style))
        for item in priority_gaps:
            pri_color = RED if item["priority"] == "Critical" else AMBER
            elements.append(KeepTogether([
                Paragraph(
                    f'<font color="{pri_color.hexval()}"><b>[{item["priority"]}]</b></font> '
                    f'<b>{item["skill"]}</b>',
                    body_style,
                ),
                Paragraph(f"→ {item['suggestion']}", tag_style),
                Spacer(1, 0.08 * inch),
            ]))

    # ── Footer ────────────────────────────────────────────────────────────────
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=SLATE))
    elements.append(Paragraph(
        "Generated by CareerCast AI · careercast.ai · Confidential",
        ParagraphStyle("Footer", parent=styles["Normal"], textColor=SLATE,
                       fontSize=8, alignment=TA_CENTER),
    ))

    doc.build(elements)
    return buf.getvalue()


def _generate_text_report(parsed, prediction, gap) -> str:
    """Fallback plain-text report when reportlab is unavailable."""
    lines = [
        "# CareerCast Skill Gap Report",
        f"Generated: {datetime.date.today()}",
        "",
        "## Candidate Information",
        f"Name:  {parsed.get('name', 'N/A')}",
        f"Email: {parsed.get('email', 'N/A')}",
        f"Phone: {parsed.get('phone', 'N/A')}",
        "",
        "## Career Prediction",
        f"Role:       {prediction.get('predicted_role', 'N/A')}",
        f"Confidence: {prediction.get('confidence', 0):.1f}%",
        "",
        "## Skill Gap",
        f"Match: {gap.get('match_percentage', 0)}%",
        f"Matched: {', '.join(s['skill'] for s in gap.get('matched_skills', []))}",
        f"Missing: {', '.join(s['skill'] for s in gap.get('missing_skills', []))}",
        "",
        "## Priority Recommendations",
    ]
    for item in gap.get("priority_gaps", []):
        lines.append(f"[{item['priority']}] {item['skill']}: {item['suggestion']}")
    return "\n".join(lines)
