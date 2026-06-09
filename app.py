import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & THEME SETUP
# ==========================================
st.set_page_config(
    page_title="AgriSky: Drone Spraying & Resource Optimizer",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI/UX Custom CSS Injection
st.markdown("""
    <style>
    /* Main Background & Text Colors */
    .stApp {
        background-color: #121824;
        color: #E2E8F0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #2D3748;
    }
    
    /* Premium Metric Card Styling */
    div[data-testid="stMetricSimpleValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2ECC71 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Custom Card Containers */
    .metric-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2ECC71;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    
    /* Customizing Buttons */
    .stButton>button {
        background-color: #2ECC71 !important;
        color: #121824 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #27AE60 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
    }
    
    /* Tables and DataFrames styling */
    .dataframe {
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Success block override */
    div[data-testid="stNotification"] {
        background-color: #1C3D27 !important;
        border: 1px solid #2ECC71 !important;
        color: #EAFAF1 !important;
        border-radius: 10px;
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MOCK DATA GENERATION
# ==========================================
@st.cache_data
def get_drone_telemetry():
    # Mock coordinates centered around a local modern farm estate plot
    base_lat, base_lon = 33.78, 72.72
    drone_ids = [f"AGRI-DRONE-0{i}" for i in range(1, 5)]
    payloads = ["15L", "20L", "15L", "25L"]
    tasks = ["Spraying", "Returning to Base", "Charging", "Spraying"]
    batteries = ["76%", "18%", "95%", "42%"]
    
    df_status = pd.DataFrame({
        "Drone ID": drone_ids,
        "Payload Capacity": payloads,
        "Current Task": tasks,
        "Battery Status": batteries
    })
    
    # Random offset generation for active flight simulation path
    np.random.seed(42)
    map_data = pd.DataFrame(
        np.random.randn(15, 2) / [300, 300] + [base_lat, base_lon],
        columns=['lat', 'lon']
    )
    return df_status, map_data

@st.cache_data
def get_historical_analytics():
    dates = [datetime.now() - timedelta(days=x) for x in range(180, 0, -30)]
    dates_str = [d.strftime("%b %Y") for d in dates]
    return pd.DataFrame({
        "Month": dates_str,
        "Traditional Liters Used": [2400, 2600, 2300, 2700, 2500, 2800],
        "AgriSky Precision Liters": [850, 910, 800, 930, 870, 960]
    })

df_status, map_data = get_drone_telemetry()
df_history = get_historical_analytics()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://img.icons8.com/external-flat-icons-inoki-mithi/100/000000/external-drone-smart-farm-flat-icons-inoki-mithi.png", width=80)
st.sidebar.title("AgriSky Control")
st.sidebar.markdown("*ICT for Precision Agriculture*")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate System:",
    ["🛰️ Live Flight Dashboard", "📊 Resource Optimizer", "📈 Field Analytics"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("🌐 **System Status:** Online\n\n🛰️ **GNSS Lock:** Excellent (14 Sats)\n\n🔋 **Base Station:** 98%")

# ==========================================
# TAB 1: LIVE FLIGHT DASHBOARD
# ==========================================
if menu == "🛰️ Live Flight Dashboard":
    st.title("🛰️ Live Flight Dashboard")
    st.markdown("Real-time telemetry and active mission profiles for precision drone deployment.")
    
    # Top Row: Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Active Fleet Drones", value="2 / 4", delta="1 En-Route")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Area Covered today", value="42.8 Ha", delta="+5.2 Ha / hr")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Resource Saved", value="64.2 %", delta="vs Traditional", delta_color="normal")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(label="Fleet Avg Battery", value="57.5 %", delta="-12% / mission")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("### 🗺️ Live Target Plot Telemetry")
    # Streamlit native high-contrast map rendering over farm area
    st.map(map_data, zoom=14, use_container_width=True)
    
    st.markdown("### 📋 Active Fleet Status Matrix")
    st.dataframe(df_status, use_container_width=True, hide_index=True)

# ==========================================
# TAB 2: RESOURCE & SPRAYING OPTIMIZER
# ==========================================
elif menu == "📊 Resource Optimizer":
    st.title("📊 Resource & Spraying Optimizer")
    st.markdown("Configure tactical input attributes to compute ultra-precise chemical and mechanical requirements.")
    
    col_input, col_output = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 🌾 Target Parameters")
        crop_type = st.selectbox("Select Target Crop Profile:", ["Wheat", "Rice", "Maize", "Sugarcane"])
        field_size = st.slider("Field Dimension Layout (Hectares):", min_value=1, max_value=500, value=25)
        infestation = st.selectbox("Observed Pest/Infestation Severity Index:", ["Low", "Medium", "High"])
        
        st.markdown("---")
        optimize_btn = st.button("🚀 Optimize Resource Allocation")
        
    with col_output:
        st.markdown("### 🎯 Optimization Engineering Outputs")
        
        # Calculation parameters based on agronomic logic profiles
        base_spray_per_ha = {"Wheat": 15, "Rice": 20, "Maize": 18, "Sugarcane": 25}[crop_type]
        severity_multiplier = {"Low": 0.8, "Medium": 1.0, "High": 1.4}[infestation]
        
        # Drone precision parameters
        optimized_liquid = round(field_size * base_spray_per_ha * severity_multiplier, 1)
        traditional_liquid = round(optimized_liquid * 2.8, 1) # Traditional uses ~2.8x more runoff water/chemicals
        
        flight_time_mins = round((field_size * 8), 1) # Assumes avg 8 mins per hectare coverage
        battery_swaps = max(0, int(flight_time_mins // 25)) # 25-min industrial drone battery limit
        chemical_savings_cost = int((traditional_liquid - optimized_liquid) * 350) # Mock conversion factor
        
        if optimize_btn:
            # Output Data Cards
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Precision Liquid Required", value=f"{optimized_liquid} L")
            with c2:
                st.metric(label="Est. Mission Airtime", value=f"{flight_time_mins} Mins", delta=f"{battery_swaps} Swaps Required", delta_color="inverse")
                
            # Success Announcement Panel
            st.success(f"""
                ### 💰 Resource Conservation Impact Summary
                * **Chemical Substrate Saved:** {round(traditional_liquid - optimized_liquid, 1)} Liters target reduction.
                * **Mitigated Runoff Waste:** Precision targeting saves estimated input overhead.
            """)
            
            # Interactive Chart Visualizer Comparison
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Traditional Volumetric Waste',
                x=[crop_type], y=[traditional_liquid],
                marker_color='#E74C3C',
                text=[f"{traditional_liquid}L"], textposition='auto'
            ))
            fig.add_trace(go.Bar(
                name='AgriSky Ultra-Precision Volume',
                x=[crop_type], y=[optimized_liquid],
                marker_color='#2ECC71',
                text=[f"{optimized_liquid}L"], textposition='auto'
            ))
            
            fig.update_layout(
                title=f"Volumetric Resource Comparison for {field_size} Ha of {crop_type}",
                barmode='group',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#FFFFFF'),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                yaxis=dict(gridcolor='#2D3748', title="Total Liters (Water + Active Substrate)")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Adjust parameter targets on the left panel and click 'Optimize Resource Allocation' to generate system models.")

# ==========================================
# TAB 3: FIELD ANALYTICS & INSIGHTS
# ==========================================
else:
    st.title("📈 Field Analytics & Historical Insights")
    st.markdown("Macro tracking trends evaluating smart structural field integrations across the multi-month season layout.")
    
    # Line chart comparing seasonal consumption patterns
    fig_history = px.line(
        df_history, 
        x="Month", 
        y=["Traditional Liters Used", "AgriSky Precision Liters"],
        labels={"value": "Total Volumetric Consumption (L)", "variable": "Methodology"},
        title="6-Month Longitudinal Environmental Resource Conservation Report",
        color_discrete_sequence=["#E74C3C", "#2ECC71"]
    )
    
    fig_history.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF'),
        xaxis=dict(gridcolor='#2D3748'),
        yaxis=dict(gridcolor='#2D3748')
    )
    
    st.plotly_chart(fig_history, use_container_width=True)
    
    # Data Download Block
    st.markdown("### 📑 Export Analytical Field Dataset")
    st.markdown("Extract full precision system telemetry telemetry matrices for localized verification or institutional reporting.")
    
    csv_data = df_history.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Seasonal Performance Log (.CSV)",
        data=csv_data,
        file_name="AgriSky_Seasonal_Resource_Report.csv",
        mime="text/csv"
    )
