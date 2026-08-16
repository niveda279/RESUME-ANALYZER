import streamlit as st
import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL", "http://127.0.0.1:5000/api/v2")

st.set_page_config(page_title="CareerCast Review UI", page_icon="📈", layout="wide")

st.title("CareerCast Milestone 3 - Review Interface")
st.markdown("Upload a resume to perform career prediction and skill gap analysis via the new FastAPI backend.")

uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])

if uploaded_file is not None:
    st.info("File uploaded successfully. Processing...")
    
    if st.button("Run Analysis"):
        with st.spinner("Analyzing resume..."):
            try:
                # 1. Prediction Endpoint
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                pred_response = requests.post(f"{API_URL}/predict", files=files)
                pred_response.raise_for_status()
                pred_data = pred_response.json()
                
                prediction = pred_data.get("prediction", {})
                parsed = pred_data.get("parsed_data", {})
                raw_text = parsed.get("raw_text", "")
                
                # 2. Skill Gap Endpoint
                gap_payload = {
                    "raw_text": raw_text,
                    "target_role": prediction.get("predicted_role", "Software Engineer")
                }
                gap_response = requests.post(f"{API_URL}/skill-gap", json=gap_payload)
                gap_response.raise_for_status()
                gap_data = gap_response.json()
                
                gap_analysis = gap_data.get("gap_analysis", {})
                
                st.success("Analysis Complete!")
                
                # Display Results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Career Prediction")
                    st.write(f"**Predicted Role:** {prediction.get('predicted_role', 'Unknown')}")
                    st.write(f"**Confidence:** {prediction.get('confidence', 0)}%")
                    
                    breakdown = prediction.get("breakdown", [])
                    if breakdown:
                        df_probs = pd.DataFrame(breakdown)
                        st.bar_chart(df_probs.set_index("role"))
                        
                with col2:
                    st.subheader("🛠️ Skill Gap Analysis")
                    st.write(f"**Target Role:** {gap_analysis.get('predicted_role')}")
                    match_percent = gap_analysis.get('match_percentage', 0)
                    st.progress(match_percent / 100.0, text=f"Skill Match: {match_percent}%")
                    
                    matched = gap_analysis.get("matched_skills", [])
                    missing = gap_analysis.get("missing_skills", [])
                    priority = gap_analysis.get("priority_gaps", [])
                    
                    st.write(f"**Matched Skills ({len(matched)}):**")
                    st.write(", ".join([m['skill'] for m in matched]) if matched else "None")
                    
                    st.write(f"**Missing Skills ({len(missing)}):**")
                    st.write(", ".join([m['skill'] for m in missing]) if missing else "None")
                
                st.subheader("🚀 Actionable Recommendations")
                if priority:
                    for gap in priority:
                        with st.expander(f"Improve {gap['skill']} (Priority: {gap['priority']})"):
                            st.write(gap['suggestion'])
                else:
                    st.write("No critical or high priority skill gaps found. Great job!")
                    
                # Generate Report text
                report = f"""# CareerCast Skill Gap Report
## Candidate Info
Name: {parsed.get('name')}
Email: {parsed.get('email')}
Phone: {parsed.get('phone')}

## Career Prediction
Predicted Role: {prediction.get('predicted_role')} (Confidence: {prediction.get('confidence')}%)

## Skill Match
Overall Match: {match_percent}%

## Matched Skills
{', '.join([m['skill'] for m in matched]) if matched else 'None'}

## Missing Skills
{', '.join([m['skill'] for m in missing]) if missing else 'None'}

## Priority Improvement Suggestions
"""
                for gap in priority:
                    report += f"- **{gap['skill']}**: {gap['suggestion']}\n"
                    
                st.download_button(
                    label="📥 Download Gap Report",
                    data=report,
                    file_name="skill_gap_report.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
