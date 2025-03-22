import os
import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Disease Prediction", page_icon="⚕️", layout="wide")

# Hide Default Streamlit UI
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# Ultra-compact Layout and Styling
page_bg_img = """
<style>
/* Page Layout */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #e6e6e6;
    padding-top: 0px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(30, 30, 50, 0.95);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 5px;
}

/* Cards */
.result-card {
    background: rgba(76, 175, 80, 0.1);
    backdrop-filter: blur(5px);
    padding: 12px;
    border-radius: 8px;
    border: 1px solid rgba(76, 175, 80, 0.2);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-top: 10px;
    transition: all 0.3s ease;
}

.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
    height: 32px;
    min-height: 32px;
    line-height: 20px;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stButton>button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Input Fields */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: rgba(255, 255, 255, 0.05);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
    height: 32px;
    min-height: 32px;
    transition: all 0.3s ease;
}

.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
    border-color: #4CAF50;
    background-color: rgba(255, 255, 255, 0.08);
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

/* Headings */
h1 {
    background: linear-gradient(135deg, #4CAF50, #81C784);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 1.8em;
    margin: 10px 0;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    letter-spacing: 1px;
}

/* Compact Layout */
.block-container {
    padding: 0px !important;
    max-width: 98%;
    margin: auto;
}

/* Reduce expander padding */
.st-expander {
    padding: 0px !important;
    margin: 0px !important;
}

/* Reduce label size */
.st-emotion-cache-1gulkj5, .st-emotion-cache-10trblm, .st-af {
    font-size: 11px !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
}

/* Reduce help text size */
.st-emotion-cache-1helkxs {
    font-size: 9px !important;
    line-height: 1 !important;
}

/* Reduce expander title size */
.st-emotion-cache-pkbazv {
    font-size: 12px !important;
    padding: 0 !important;
}

/* Reduce result text size */
.result-card h3 {
    font-size: 14px !important;
    margin: 3px 0 !important;
}
.result-card p {
    font-size: 12px !important;
    margin: 3px 0 !important;
}

/* Reduce radio button size */
.st-emotion-cache-1qg05tj {
    font-size: 11px !important;
}

/* Reduce padding in columns */
.st-emotion-cache-1r6slb0, .st-emotion-cache-1kyxreq {
    padding: 0 !important;
    gap: 0 !important;
}

/* Reduce gap between inputs */
.row-widget {
    padding: 0 !important;
    margin: 0 !important;
}

/* Reduce padding in number inputs */
.st-emotion-cache-1qg05tj {
    padding: 0 !important;
}

/* Compact tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1px;
}
.stTabs [data-baseweb="tab"] {
    height: 30px;
    padding: 0px 8px;
    font-size: 12px;
}
</style>
"""

# Improved Tab Styling
page_bg_img += """
<style>
/* Improved Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: rgba(40, 40, 60, 0.3);
    padding: 5px 5px 0 5px;
    border-radius: 4px;
}

.stTabs [data-baseweb="tab"] {
    height: 35px;
    padding: 0px 12px;
    font-size: 13px;
    background-color: rgba(60, 60, 80, 0.2);
    border-radius: 4px 4px 0 0;
}

.stTabs [data-baseweb="tab"]:active {
    background-color: rgba(76, 175, 80, 0.2);
}

/* Improved Input Fields */
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: rgba(255, 255, 255, 0.08);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
    height: 30px;
}

/* Section Headers */
.section-header {
    font-size: 15px;
    color: #81C784;
    margin: 12px 0 8px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(129, 199, 132, 0.3);
    letter-spacing: 0.5px;
}

/* Column Spacing */
.st-emotion-cache-1r6slb0 {
    gap: 10px !important;
    padding: 5px !important;
}

/* Title Styling */
h1 {
    font-size: 1.8em;
    margin: 10px 0;
    padding: 5px;
}

/* Result Card Enhancement */
.result-card {
    margin: 10px 0;
    padding: 8px 12px;
    background: rgba(76, 175, 80, 0.1);
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: rgba(40, 40, 60, 0.3);
    padding: 6px 6px 0 6px;
    border-radius: 8px 8px 0 0;
    backdrop-filter: blur(5px);
}

.stTabs [data-baseweb="tab"] {
    height: 38px;
    padding: 0px 16px;
    font-size: 13px;
    background-color: rgba(60, 60, 80, 0.2);
    border-radius: 6px 6px 0 0;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(76, 175, 80, 0.1);
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: rgba(76, 175, 80, 0.2);
    border-bottom: 2px solid #4CAF50;
}

/* Column Containers */
.st-emotion-cache-1r6slb0 {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 8px;
    padding: 10px !important;
    margin: 5px 0;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Radio Buttons */
.st-emotion-cache-1qg05tj {
    font-size: 12px !important;
}

.st-emotion-cache-1qg05tj:hover {
    color: #4CAF50;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.result-card {
    animation: fadeIn 0.3s ease-out;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Get the directory of the script
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

# Model filenames
model_files = {
    'diabetes': "diabetes_model.sav",
    'heart_disease': "heart_disease_model.sav",
    'parkinsons': "parkinsons_model.sav",
    'lung_cancer': "lungs_disease_model.sav",
    'thyroid': "Thyroid_model.sav"
}

# Load models
models = {}
for disease, filename in model_files.items():
    path = os.path.join(MODEL_DIR, filename)
    if os.path.exists(path):
        models[disease] = pickle.load(open(path, 'rb'))
    else:
        print(f"❌ Missing file: {filename}")

# Improved disease prediction function
def predict_disease(model, input_data, disease_name):
    try:
        prediction = model.predict([input_data])
        result = prediction[0] == 1
        
        st.markdown(
            f"""
            <div class="result-card">
                <h3>{'🚨 ' if result else '✅ '}Prediction Result</h3>
                <p>The person {'has' if result else 'does not have'} {disease_name}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return result
    except Exception as e:
        st.error(f"Error: {e}")

# Main content area with tabs for each disease
st.title("AI-Powered Disease Prediction")

# Use tabs instead of sidebar for more space
tabs = st.tabs(["Diabetes", "Heart Disease", "Parkinson's", "Lung Cancer", "Hypo-Thyroid"])

# Diabetes Prediction Tab
with tabs[0]:
    st.markdown('<p class="section-header">Patient Information</p>', unsafe_allow_html=True)
    # Create a grid layout for inputs - 4 columns for Diabetes
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        preg = st.number_input("Pregnancies", step=1, format="%d", key="d_preg")
        skin = st.number_input("Skin Thickness", step=1, format="%d", key="d_skin")
    
    with col2:
        glucose = st.number_input("Glucose Level", step=1, format="%d", key="d_glucose")
        insulin = st.number_input("Insulin Level", step=1, format="%d", key="d_insulin")
    
    with col3:
        bp = st.number_input("Blood Pressure", step=1, format="%d", key="d_bp")
        bmi = st.number_input("Body Mass Index", step=0.1, format="%.1f", key="d_bmi")
    
    with col4:
        dpf = st.number_input("Diabetes Pedigree Function ", step=0.001, format="%.3f", key="d_dpf")
        age = st.number_input("Age", step=1, format="%d", key="d_age")
    
    # Prediction button
    if st.button('Predict Diabetes', key="btn_diabetes"):
        diabetes_input = [preg, glucose, bp, skin, insulin, bmi, dpf, age]
        predict_disease(models['diabetes'], diabetes_input, "Diabetes")

# Heart Disease Prediction Tab
with tabs[1]:
    st.markdown('<p class="section-header">Patient Information</p>', unsafe_allow_html=True)
    # Create a grid layout - 5 columns for Heart Disease
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        age = st.number_input("Age", step=1, format="%d", key="h_age")
        trestbps = st.number_input("Resting BP", step=1, format="%d", key="h_bp")
        slope = st.number_input("Slope of the peak exercise ST segment (0, 1, 2)", step=1, min_value=0, max_value=2, format="%d", key="h_slope")
    
    with col2:
        sex = st.number_input("Sex (1=M;0=F)", step=1, min_value=0, max_value=1, format="%d", key="h_sex")
        chol = st.number_input("Serum Cholesterol in mg/dl", step=1, format="%d", key="h_chol")
        ca = st.number_input("Major vessels colored by fluoroscopy    (0-3)", step=1, min_value=0, max_value=3, format="%d", key="h_ca")
    
    with col3:
        cp = st.number_input("Chest Pain Types (0-3)", step=1, min_value=0, max_value=3, format="%d", key="h_cp")
        fbs = st.number_input("Fasting Blood Sugar > 120 mg/dl    (1 = true; 0 = false)", step=1, min_value=0, max_value=1, format="%d", key="h_fbs")
        thal = st.number_input("Thal (0=normal; 1=fixed ; 2=reversible)", step=1, min_value=0, max_value=2, format="%d", key="h_thal")
    
    with col4:
        restecg = st.number_input("Resting Electrocardiographic results (0, 1, 2)", step=1, min_value=0, max_value=2, format="%d", key="h_ecg")
        exang = st.number_input("Excercise Induced Angina (1=Y;0=N)", step=1, min_value=0, max_value=1, format="%d", key="h_exang")
    
    with col5:
        thalach = st.number_input("Max Heart Rate", step=1, format="%d", key="h_thalach")
        oldpeak = st.number_input("ST depression induced by exercise", step=0.1, format="%.1f", key="h_oldpeak")
    
    # Prediction button
    if st.button('Predict Heart Disease', key="btn_heart"):
        heart_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
        predict_disease(models['heart_disease'], heart_input, "Heart Disease")

# Parkinson's Prediction Tab - This has many inputs, so we'll use 6 columns
with tabs[2]:
    st.markdown('<p class="section-header">Patient Information</p>', unsafe_allow_html=True)
    # Create a grid layout - 6 columns for Parkinson's
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        fo = st.number_input("MDVP:Fo(Hz)", step=0.001, format="%.3f", key="p_fo")
        jitter_percent = st.number_input("Jitter(%)", step=0.001, format="%.3f", key="p_jitter_percent")
        shimmer = st.number_input("Shimmer", step=0.001, format="%.3f", key="p_shimmer")
        nhr = st.number_input("NHR", step=0.001, format="%.3f", key="p_nhr")
    
    with col2:
        fhi = st.number_input("MDVP:Fhi(Hz)", step=0.001, format="%.3f", key="p_fhi")
        jitter_abs = st.number_input("Jitter(Abs)", step=0.000001, format="%.6f", key="p_jitter_abs")
        shimmer_db = st.number_input("Shimmer(dB)", step=0.001, format="%.3f", key="p_shimmer_db")
        hnr = st.number_input("HNR", step=0.001, format="%.3f", key="p_hnr")
    
    with col3:
        flo = st.number_input("MDVP:Flo(Hz)", step=0.001, format="%.3f", key="p_flo")
        rap = st.number_input("RAP", step=0.001, format="%.3f", key="p_rap")
        apq3 = st.number_input("APQ3", step=0.001, format="%.3f", key="p_apq3")
        rpde = st.number_input("RPDE", step=0.001, format="%.3f", key="p_rpde")
    
    with col4:
        ppq = st.number_input("PPQ", step=0.001, format="%.3f", key="p_ppq")
        apq5 = st.number_input("APQ5", step=0.001, format="%.3f", key="p_apq5")
        dfa = st.number_input("DFA", step=0.001, format="%.3f", key="p_dfa")
    
    with col5:
        ddp = st.number_input("DDP", step=0.001, format="%.3f", key="p_ddp")
        apq = st.number_input("APQ", step=0.001, format="%.3f", key="p_apq")
        spread1 = st.number_input("Spread1", step=0.001, format="%.3f", key="p_spread1")
    
    with col6:
        dda = st.number_input("DDA", step=0.001, format="%.3f", key="p_dda")
        spread2 = st.number_input("Spread2", step=0.001, format="%.3f", key="p_spread2")
        d2 = st.number_input("D2", step=0.001, format="%.3f", key="p_d2")
        ppe = st.number_input("PPE", step=0.001, format="%.3f", key="p_ppe")
    
    # Prediction button
    if st.button("Predict Parkinson's", key="btn_parkinsons"):
        parkinsons_input = [fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp, 
                           shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr, 
                           rpde, dfa, spread1, spread2, d2, ppe]
        predict_disease(models['parkinsons'], parkinsons_input, "Parkinson's Disease")

# Lung Cancer Prediction Tab
with tabs[3]:
    st.markdown('<p class="section-header">Patient Information</p>', unsafe_allow_html=True)
    # Create a grid layout - 5 columns for Lung Cancer
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        gender = st.number_input("Gender (1=M;0=F)", step=1, min_value=0, max_value=1, format="%d", key="l_gender")
        smoking = st.number_input("Smoking (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_smoking")
        chronic = st.number_input("Chronic Disease (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_chronic")
    
    with col2:
        age = st.number_input("Age", step=1, format="%d", key="l_age")
        yellow_fingers = st.number_input("Yellow Fingers (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_yellow")
        fatigue = st.number_input("Fatigue (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_fatigue")
    
    with col3:
        anxiety = st.number_input("Anxiety (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_anxiety")
        allergy = st.number_input("Allergy (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_allergy")
        coughing = st.number_input("Coughing (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_coughing")
    
    with col4:
        peer_pressure = st.number_input("Peer Pressure (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_peer")
        wheezing = st.number_input("Wheezing (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_wheezing")
        shortness = st.number_input("Shortness of Breath (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_shortness")
    
    with col5:
        alcohol = st.number_input("Alcohol (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_alcohol")
        swallowing = st.number_input("Swallowing Difficulty (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_swallowing")
        chest_pain = st.number_input("Chest Pain (1=N;2=Y)", step=1, min_value=1, max_value=2, format="%d", key="l_chest")
    
    # Prediction button
    if st.button("Predict Lung Cancer", key="btn_lung"):
        lung_input = [gender, age, smoking, yellow_fingers, anxiety, peer_pressure, 
                     chronic, fatigue, allergy, wheezing, alcohol, coughing, 
                     shortness, swallowing, chest_pain]
        predict_disease(models['lung_cancer'], lung_input, "Lung Cancer")

# Thyroid Prediction Tab
with tabs[4]:
    st.markdown('<p class="section-header">Patient Information</p>', unsafe_allow_html=True)
    # Create a grid layout - 4 columns for Thyroid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        age = st.number_input("Age", step=1, format="%d", key="t_age")
        t3_measured = st.number_input("T3 Measured (1=Y;0=N)", step=1, min_value=0, max_value=1, format="%d", key="t_t3_measured")
    
    with col2:
        sex = st.number_input("Sex (1=M;0=F)", step=1, min_value=0, max_value=1, format="%d", key="t_sex")
        t3 = st.number_input("T3 Level", step=0.01, format="%.2f", key="t_t3")
    
    with col3:
        on_thyroxine = st.number_input("On Thyroxine (1=Y;0=N)", step=1, min_value=0, max_value=1, format="%d", key="t_thyroxine")
        tt4 = st.number_input("TT4 Level", step=0.01, format="%.2f", key="t_tt4")
    
    with col4:
        tsh = st.number_input("TSH Level", step=0.01, format="%.2f", key="t_tsh")
    
    # Prediction button
    if st.button("Predict Hypo-Thyroid", key="btn_thyroid"):
        thyroid_input = [age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]
        predict_disease(models['thyroid'], thyroid_input, "Hypo-Thyroid")
