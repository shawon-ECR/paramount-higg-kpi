import streamlit as st
import pandas as pd

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="Paramount ETP&ECR",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling to fix text visibility in both Dark & Light modes
st.markdown("""
    <style>
    .main { padding: 1rem; }
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border: 1px solid #334155 !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Paramount ETP&ECR")
st.caption("Paramount Textile PLC - Environmental Compliance & Sustainability Dashboard")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Resource KPIs", "🌿 Env KPIs", "🌍 Carbon Footprint", "📋 Higg Guide"])

# TAB 1: Water & Energy KPIs
with tab1:
    st.subheader("Production & Resource Input")
    
    production_kg = st.number_input("Total Production (Kg Fabric)", min_value=1.0, value=100000.0, step=1000.0)
    
    col1, col2 = st.columns(2)
    with col1:
        water_m3 = st.number_input("Water Consumed (m³)", min_value=0.0, value=6000.0)
        grid_electricity_kwh = st.number_input("Grid Electricity (kWh)", min_value=0.0, value=120000.0)
    with col2:
        natural_gas_m3 = st.number_input("Natural Gas (m³)", min_value=0.0, value=45000.0)
        diesel_liter = st.number_input("Diesel Consumed (Liters)", min_value=0.0, value=1200.0)

    # Resource KPI Calculations
    water_liters = water_m3 * 1000
    water_kpi = water_liters / production_kg  # Liters/Kg
    
    total_energy_kwh = grid_electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liter * 10.0)
    energy_kpi = total_energy_kwh / production_kg  # kWh/Kg
    
    st.markdown("---")
    st.subheader("🎯 Water & Energy KPIs")
    
    st.metric(label="💧 Water Intensity", value=f"{water_kpi:.2f} L/kg fabric")
    if water_kpi <= 60:
        st.success("✅ Water KPI is Best-in-Class (<= 60 L/kg)")
    elif water_kpi <= 90:
        st.warning("⚠️ Water KPI is Moderate (60-90 L/kg)")
    else:
        st.error("❌ High Water Usage (> 90 L/kg). Needs Action!")

    st.metric(label="⚡ Energy Intensity", value=f"{energy_kpi:.2f} kWh/kg fabric")

# TAB 2: Environmental & ETP KPIs
with tab2:
    st.subheader("🧪 ETP Efficiency & Environmental Metrics")
    
    col_a, col_b = st.columns(2)
    with col_a:
        influent_cod = st.number_input("Influent COD (mg/L)", min_value=1.0, value=1200.0)
        effluent_cod = st.number_input("Effluent COD (mg/L)", min_value=0.0, value=110.0)
        total_chemical_kg = st.number_input("Total Chemical Used (Kg)", min_value=0.0, value=15000.0)
    with col_b:
        sludge_produced_kg = st.number_input("ETP Sludge Produced (Kg)", min_value=0.0, value=2500.0)
        total_waste_kg = st.number_input("Total Solid Waste (Kg)", min_value=1.0, value=5000.0)
        recycled_waste_kg = st.number_input("Recycled/Reused Waste (Kg)", min_value=0.0, value=4200.0)

    # Calculations
    etp_efficiency = ((influent_cod - effluent_cod) / influent_cod) * 100
    chemical_kpi = total_chemical_kg / production_kg  # Kg Chemical / Kg Fabric
    sludge_kpi = (sludge_produced_kg / production_kg) * 1000  # Gram Sludge / Kg Fabric
    waste_diversion_rate = (recycled_waste_kg / total_waste_kg) * 100

    st.markdown("---")
    st.subheader("📈 Calculated Environmental KPIs")

    st.metric(label="⚙️ ETP COD Removal Efficiency", value=f"{etp_efficiency:.1f} %")
    if etp_efficiency >= 85:
        st.success("✅ ETP Treatment Efficiency is Optimal (>= 85%)")
    else:
        st.warning("⚠️ Low ETP Efficiency! Check biological/chemical dosing.")

    st.metric(label="🧪 Chemical Intensity KPI", value=f"{chemical_kpi:.3f} kg chem/kg fabric")
    st.metric(label="🍂 Sludge Generation KPI", value=f"{sludge_kpi:.2f} g sludge/kg fabric")
    st.metric(label="♻️ Waste Diversion Rate", value=f"{waste_diversion_rate:.1f} %")

# TAB 3: Carbon Footprint
with tab3:
    st.subheader("💨 Carbon Footprint (GHG Emissions)")
    
    ng_ghg = natural_gas_m3 * 1.98     # kg CO2e per m3 Natural Gas
    diesel_ghg = diesel_liter * 2.68   # kg CO2e per Liter Diesel
    scope_1_total = (ng_ghg + diesel_ghg) / 1000 # Metric Tons CO2e
    
    grid_ghg = grid_electricity_kwh * 0.55  # kg CO2e per kWh
    scope_2_total = grid_ghg / 1000 # Metric Tons CO2e
    
    total_ghg_tons = scope_1_total + scope_2_total
    ghg_intensity = (total_ghg_tons * 1000) / production_kg # Kg CO2e / Kg Fabric
    
    st.metric(label="🔥 Scope 1 Emissions (Direct)", value=f"{scope_1_total:.2f} MT CO₂e")
    st.metric(label="🔌 Scope 2 Emissions (Grid)", value=f"{scope_2_total:.2f} MT CO₂e")
    st.metric(label="🌱 Total GHG Intensity", value=f"{ghg_intensity:.3f} kg CO₂e / kg fabric")

# TAB 4: Higg Guidance
with tab4:
    st.subheader("📌 Higg FEM 4.0 Standard Benchmark")
    st.write("""
    * **Water Intensity Target:** Ideally **< 60 Liters/Kg Fabric**.
    * **ETP Efficiency Target:** COD Removal Efficiency should be **> 85-90%**.
    * **Waste Diversion Target:** Zero Waste to Landfill requires **> 90% Waste Diversion Rate**.
    * **GHG Target:** Annual Scope 1 & 2 reduction aligned with SBTi (4.2% linear annual reduction).
    """)
