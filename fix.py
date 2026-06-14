import os

path = r'c:\DR2\visioncare\visioncare-ai\pages\2_Eye_Scan.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                        scan_id = db.save_scan(patient_id, image_path, analysis, quality_score)
            <div style=\"font-size:3rem;\">{overall.get('emoji', '❓')}</div>'''

replacement = '''                        scan_id = db.save_scan(patient_id, image_path, analysis, quality_score)
                    
                    # Store in session state
                    st.session_state["last_analysis"] = analysis
                    st.session_state["last_risks"] = risks
                    st.session_state["last_recommendations"] = recommendations
                    st.session_state["last_scan_id"] = scan_id
                    st.session_state["last_image_path"] = image_path
                    st.session_state["last_patient_info"] = {
                        "name": patient_name,
                        "age": patient_age,
                        "gender": patient_gender
                    }
                    
                    st.success("✅ Analysis complete!")
                    st.rerun()
        
        elif quality_status == "poor":
            st.error("❌ Poor image quality detected. Please upload a clearer photo.")
            st.info("💡 Try taking a photo in better lighting conditions, ensuring the eye is in focus.")
    
    # Display analysis results if available
    if st.session_state.get("last_analysis") is not None:
        analysis = st.session_state["last_analysis"]
        risks = st.session_state["last_risks"]
        recommendations = st.session_state["last_recommendations"]
        scan_id = st.session_state.get("last_scan_id")
        image_path = st.session_state.get("last_image_path")
        patient_info = st.session_state.get("last_patient_info", {})
        
        st.markdown("---")
        st.markdown('<div class="main-header" style="font-size:1.8rem;">📋 Analysis Results</div>', unsafe_allow_html=True)
        
        # Overall Status
        overall = risks.get("overall", {})
        overall_color = overall.get("color", "blue")
        st.markdown(f\"\"\"
        <div class="card card-{overall_color}" style="text-align: center;">
            <div style="font-size:3rem;">{overall.get('emoji', '❓')}</div>'''

new_content = content.replace(target, replacement)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Fixed!')
