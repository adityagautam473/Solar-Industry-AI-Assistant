import streamlit as st
from vision_analysis import analyze_rooftop
from roi_calculator import compute_roi

st.set_page_config(page_title="Solar AI Assistant", layout="centered")

st.title("☀️ Solar Industry AI Assistant")
st.write("Upload your rooftop image to get solar installation insights.")

uploaded_file = st.file_uploader("Upload rooftop image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = uploaded_file.read()

    st.subheader("📸 Analyzing Rooftop...")
    analysis_result = analyze_rooftop(image)
    st.json(analysis_result)

    # Check if analysis was successful before computing ROI
    if "error" not in analysis_result:
        st.subheader("💸 Calculating ROI...")
        roi_data = compute_roi(analysis_result)
        
        # Check if ROI calculation was successful
        if "error" not in roi_data:
            st.write("### Estimated Power Output (kWh/year):", roi_data["annual_output_kwh"])
            st.write("### Estimated Payback Period (years):", roi_data["payback_period"])
            st.write("### Total Installation Cost (INR):", roi_data["total_cost_inr"])
            st.write("### Government Incentives (INR):", roi_data["incentive_inr"])
            st.write("### Net Cost after Incentives (INR):", roi_data["net_cost_inr"])
        else:
            st.error(f"ROI Calculation Error: {roi_data['error']}")
    else:
        st.error(f"Analysis Error: {analysis_result['error']}")
        if "raw_response" in analysis_result:
            st.write("Raw API Response:", analysis_result["raw_response"])