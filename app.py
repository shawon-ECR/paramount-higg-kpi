import streamlit as st
import pandas as pd

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="Paramount Higg FEM KPI",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling for mobile UI
st.markdown("""
    <style>
    .main { padding: 1rem; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Higg FEM KPI Tracker")
st.caption("Paramount Textile PLC - Sustainability & Compliance")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📊 KPI Calculator", "🌍 GHG Scope 1 & 2", "📋 Higg Guidance"])

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

    # KPI Calculations
    water_liters = water_m3 * 1000
    water_kpi = water_liters / production_kg  # Liters/Kg
    
    total_energy_kwh = grid_electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liter * 10.0)
    energy_kpi = total_energy_kwh / production_kg  # kWh/Kg
    
    st.markdown("---")
    st.subheader("🎯 Calculated Higg FEM KPIs")
    
    st.metric(label="💧 Water Intensity", value=f"{water_kpi:.2f} L/kg fabric")
    if water_kpi <= 60:
        st.success("✅ Water KPI is Best-in-Class (<= 60 L/kg)")
    elif water_kpi <= 90:
        st.warning("⚠️ Water KPI is Moderate (60-90 L/kg)")
    else:
        st.error("❌ High Water Usage (> 90 L/kg). Needs Reduction Action!")

    st.metric(label="⚡ Energy Intensity", value=f"{energy_kpi:.2f} kWh/kg fabric")
    st.info(f"Total Energy Consumed: {total_energy_kwh:,.0f} kWh equivalent")

with tab2:
    st.subheader("💨 Carbon Footprint (GHG Emissions)")
    st.caption("Standard Emission Factors for Bangladesh Textile Sector")
    
    # GHG Calculations (IPCC / Higg Standards)
    ng_ghg = natural_gas_m3 * 1.98     # kg CO2e per m3 Natural Gas
    diesel_ghg = diesel_liter * 2.68   # kg CO2e per Liter Diesel
    scope_1_total = (ng_ghg + diesel_ghg) / 1000 # Metric Tons CO2e
    
    grid_ghg = grid_electricity_kwh * 0.55  # kg CO2e per kWh (BD Grid Factor)
    scope_2_total = grid_ghg / 1000 # Metric Tons CO2e
    
    total_ghg_tons = scope_1_total + scope_2_total
    ghg_intensity = (total_ghg_tons * 1000) / production_kg # Kg CO2e / Kg Fabric
    
    st.metric(label="🔥 Scope 1 Emissions (Direct)", value=f"{scope_1_total:.2f} MT CO₂e")
    st.metric(label="🔌 Scope 2 Emissions (Grid)", value=f"{scope_2_total:.2f} MT CO₂e")
    st.metric(label="🌱 Total GHG Intensity", value=f"{ghg_intensity:.3f} kg CO₂e / kg fabric")

with tab3:
    st.subheader("📌 Higg FEM 4.0 Benchmark Guide")
    st.write("""
    * **Water Target:** Textile Processing target is ideally **< 60 Liters/Kg**.
    * **Energy Target:** Woven/Knit Processing energy target is **1.5 - 3.5 kWh/Kg**.
    * **GHG Reduction:** Target to reduce absolute Scope 1 & 2 emissions by **4.2% annually** as per SBTi alignment.
    """)
