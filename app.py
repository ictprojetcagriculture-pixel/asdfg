import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AgriSmart: Drone & Resource Optimizer",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR BRANDING (Green Accents) ---
st.markdown("""
    <style>
    :root {
        --primary-color: #2E7D32;
    }
    .main-title {
        color: #1B5E20;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- MOCK DATA GENERATION ---
@st.cache_data
def get_historical_data():
    date_today = datetime.now()
    dates = [date_today - timedelta(days=i) for i in range(30)]
    dates.reverse()
    
    # Simulating data
    water_saved = np.random.uniform(30, 45, size=30).cumsum() / 30 + 25
    chemical_eff = np.random.uniform(85, 96, size=30)
    ndvi_index = np.random.uniform(0.6, 0.85, size=30)
    
    df = pd.DataFrame({
        "Date": dates,
        "Water Saved (%)": water_saved,
        "Chemical Efficiency (%)": chemical_eff,
        "NDVI Health Index": ndvi_index
    })
    return df

df_metrics = get_historical_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h1 class='main-title'>🌱 AgriSmart</h1>", unsafe_allow_html=True)
st.sidebar.markdown("*Precision Agriculture via Drone Tech*")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation Menu",
    ["📊 Dashboard & Analytics", "🛸 Drone Mission Planner", "💧 Resource Optimizer"]
)

st.sidebar.divider()
st.sidebar.info(
    "💡 **Quick Tip:** Use the Drone Mission Planner to simulate optimal flight paths before calculating resource distribution."
)

# --- SECTION 1: DASHBOARD & ANALYTICS ---
if page == "📊 Dashboard & Analytics":
    st.markdown("<h2 class='main-title'>Dashboard & Analytics</h2>", unsafe_allow_html=True)
    st.markdown("Real-time operational metrics and field health analytics over the past 30 days.")
    st.write("---")
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Area Covered", value="1,248 ha", delta="+42 ha today")
    with col2:
        st.metric(label="Water Saved", value="38.4 %", delta="+1.2% vs last week")
    with col3:
        st.metric(label="Chemical Efficiency", value="94.2 %", delta="Optimal Range", delta_color="normal")
    with col4:
        st.metric(label="Active Drones", value="4 / 6", delta="2 Fleet Idle")
        
    st.write("---")
    
    # Interactive Charts
    tab1, tab2 = st.tabs(["📈 Resource Efficiency Trends", "🌿 Field Health Index (NDVI)"])
    
    with tab1:
        st.subheader("30-Day Resource Savings Trend")
        fig_resource = px.line(
            df_metrics, x="Date", y=["Water Saved (%)", "Chemical Efficiency (%)"],
            labels={"value": "Percentage (%)", "variable": "Metric"},
            color_discrete_sequence=["#2E7D32", "#81C784"]
        )
        fig_resource.update_layout(hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_resource, use_container_width=True)
        
    with tab2:
        st.subheader("Normalized Difference Vegetation Index (NDVI)")
        fig_ndvi = px.area(
            df_metrics, x="Date", y="NDVI Health Index",
            color_discrete_sequence=["#4CAF50"],
            labels={"NDVI Health Index": "NDVI Level"}
        )
        fig_ndvi.update_yaxes(range=[0.5, 1.0])
        fig_ndvi.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_ndvi, use_container_width=True)

# --- SECTION 2: DRONE MISSION PLANNER ---
elif page == "🛸 Drone Mission Planner":
    st.markdown("<h2 class='main-title'>Drone Mission Planner</h2>", unsafe_allow_html=True)
    st.markdown("Configure field operational parameters to compute optimized autonomous flight paths.")
    st.write("---")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        crop_type = st.selectbox("Crop Type", ["Corn", "Wheat", "Soy", "Rice"], help="Select target crop for localized algorithm tuning.")
        field_size = st.slider("Field Size (hectares)", min_value=1, max_value=500, value=75, step=5)
        weather = st.selectbox("Current Weather Conditions", ["Sunny", "Windy", "Rainy"])
        
        # Safety Environmental Logic
        if weather in ["Windy", "Rainy"]:
            st.warning(f"⚠️ **Hazard Warning:** Flight conditions are **{weather}**. Drone deployment might be hazardous. Proceed with extreme caution.")
        else:
            st.success("☀️ **Flight Status:** Weather Clear. Optimal deployment environment.")
            
        generate_btn = st.button("Generate Flight Path", use_container_width=True)
        
    with col2:
        st.subheader("Optimized Flight Vector Map")
        if generate_btn:
            with st.spinner("Calculating optimal patterns to minimize spray drift..."):
                # Mock path coordinate generation
                np.random.seed(42)
                x_coords = np.linspace(0, 10, 15)
                # Generate a zigzag pattern for drone spraying route
                y_coords = [i if idx % 2 == 0 else i + np.random.uniform(-0.5, 0.5) for idx, i in enumerate(np.sin(x_coords) * 2 + 5)]
                
                # Plotly path visualization
                fig_path = go.Figure()
                
                # Draw field boundaries
                fig_path.add_trace(go.Scatter(
                    x=[0, 10, 10, 0, 0], y=[0, 0, 10, 10, 0],
                    fill="toself", fillcolor="rgba(76, 175, 80, 0.1)",
                    line=dict(color="#4CAF50", dash="dash"), name="Field Boundary"
                ))
                
                # Draw flight path route
                fig_path.add_trace(go.Scatter(
                    x=x_coords, y=y_coords,
                    mode="lines+markers+text",
                    line=dict(color="#1B5E20", width=3),
                    marker=dict(size=8, color="#FF9800"),
                    name="Optimized Drone Path"
                ))
                
                fig_path.update_layout(
                    xaxis_title="Field Width Layout (Relative)",
                    yaxis_title="Field Length Layout (Relative)",
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=400
                )
                
                st.toast("Flight path generated successfully!", icon="✅")
                st.plotly_chart(fig_path, use_container_width=True)
                st.success(f"🎯 Path generated for **{field_size} hectares** of **{crop_type}**. Estimated Time of Completion: **{max(12, int(field_size * 0.4))} minutes**.")
        else:
            st.info("💡 Adjust the mission configurations on the left panel and click **'Generate Flight Path'** to view the telemetry grid simulation.")

# --- SECTION 3: RESOURCE OPTIMIZER ---
elif page == "💧 Resource Optimizer":
    st.markdown("<h2 class='main-title'>Resource Optimizer</h2>", unsafe_allow_html=True)
    st.markdown("Evaluate waste margins and compare traditional resource inputs against AI-optimized drone capabilities.")
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Manual Resource Baseline Input")
        manual_water = st.number_input("Manual Water Input (Liters per hectare)", min_value=10, max_value=5000, value=1200, step=50)
        manual_pesticide = st.number_input("Manual Chemical Input (Liters per hectare)", min_value=1.0, max_value=100.0, value=15.0, step=0.5)
        
        # Optimization Math Logic (Simulated 35% reduction optimization curve)
        saving_ratio = 0.35
        drone_water = round(manual_water * (1 - saving_ratio), 1)
        drone_pesticide = round(manual_pesticide * (1 - (saving_ratio + 0.05)), 1)
        
        saved_water = round(manual_water - drone_water, 1)
        saved_pesticide = round(manual_pesticide - drone_pesticide, 1)
        
    with col2:
        st.subheader("AI-Optimized Drone Allocation")
        
        # Display Comparative Metrics
        st.metric("Optimized Drone Water Volume", f"{drone_water} L/ha", delta=f"-{saving_ratio*100:.0f}% Reduction", delta_color="inverse")
        st.metric("Optimized Drone Chemical Volume", f"{drone_pesticide} L/ha", delta=f"-{(saving_ratio+0.05)*100:.0f}% Reduction", delta_color="inverse")
        
    st.write("---")
    st.subheader("Optimization Analysis Summary")
    
    # Dynamic Dataframe presentation
    summary_data = {
        "Resource Factor": ["Water Volume (L/ha)", "Chemical Vector (L/ha)"],
        "Traditional Manual Value": [manual_water, manual_pesticide],
