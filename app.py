import streamlit as st

# Page configuration for mobile responsiveness
st.set_page_config(
    page_title="Paramount ETP&ECR",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling for UI & Dark/Light mode visibility
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
st.caption("Paramount Textile PLC - Environmental Management & Cheat Sheet KPIs")

# Navigation Tabs matching the Cheat Sheet
tab1, tab2, tab3, tab4 = st.tabs(["💧 Water & Waste", "⚡ Energy & Climate", "🧪 ETP & Pollution", "🔄 Unit Converter"])

# TAB 1: Water & Waste KPIs
with tab1:
    st.subheader("💧 Water Reuse & Waste Diversion KPIs")
    
    production_kg = st.number_input("Total Production (Kg Fabric)", min_value=1.0, value=100000.0)
    
    col1, col2 = st.columns(2)
    with col1:
        fresh_water_m3 = st.number_input("Fresh Water Used (m³)", min_value=0.0, value=5000.0)
        reused_water_m3 = st.number_input("Reused Water (m³)", min_value=0.0, value=1000.0)
    with col2:
        total_waste_kg = st.number_input("Total Solid Waste (Kg)", min_value=1.0, value=5000.0)
        recycled_waste_kg = st.number_input("Diverted/Recycled Waste (Kg)", min_value=0.0, value=4200.0)

    # Calculations (From Cheat Sheet Formulas)
    total_water_m3 = fresh_water_m3 + reused_water_m3
    water_reuse_rate = (reused_water_m3 / total_water_m3 * 100) if total_water_m3 > 0 else 0
    water_intensity = (total_water_m3 * 1000) / production_kg  # Liters / Kg
    waste_diversion_rate = (recycled_waste_kg / total_waste_kg) * 100

    st.markdown("---")
    st.subheader("📊 Water & Waste Results")
    st.metric(label="🔄 Water Reuse Rate (%)", value=f"{water_reuse_rate:.1f} %")
    st.metric(label="💧 Water Intensity", value=f"{water_intensity:.2f} L/kg fabric")
    st.metric(label="♻️ Waste Diversion Rate (%)", value=f"{waste_diversion_rate:.1f} %")

# TAB 2: Energy & GHG Climate KPIs
with tab2:
    st.subheader("⚡ Energy Intensity & Climate KPIs")
    
    col_a, col_b = st.columns(2)
    with col_a:
        electricity_kwh = st.number_input("Grid Electricity (kWh)", min_value=0.0, value=120000.0)
        natural_gas_m3 = st.number_input("Natural Gas (m³)", min_value=0.0, value=45000.0)
    with col_b:
        diesel_liters = st.number_input("Diesel (Liters)", min_value=0.0, value=1200.0)
        revenue_usd = st.number_input("Monthly Revenue (USD $)", min_value=1.0, value=500000.0)

    # Convert energy to GJ (1 kWh = 0.0036 GJ)
    total_kwh = electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liters * 10.0)
    total_gj = total_kwh * 0.0036
    
    # GHG Emissions (Scope 1 & 2)
    scope_1_mt = ((natural_gas_m3 * 1.98) + (diesel_liters * 2.68)) / 1000
    scope_2_mt = (electricity_kwh * 0.55) / 1000
    total_ghg_mt = scope_1_mt + scope_2_mt
    
    # Cheat Sheet Intensity Metrics
    ghg_revenue_intensity = total_ghg_mt / (revenue_usd / 1000000) # tCO2e / Million USD

    st.markdown("---")
    st.subheader("📊 Energy & GHG Results")
    st.metric(label="⚡ Total Energy Consumed (GJ)", value=f"{total_gj:.2f} GJ")
    st.metric(label="🔥 Total GHG Emissions", value=f"{total_ghg_mt:.2f} tCO₂e")
    st.metric(label="🌍 GHG Intensity (Revenue Based)", value=f"{ghg_revenue_intensity:.2f} tCO₂e / $1M")

# TAB 3: ETP & Pollution
with tab3:
    st.subheader("🧪 ETP Pollution Removal Efficiency")
    
    influent_cod = st.number_input("Influent COD (mg/L)", min_value=1.0, value=1200.0)
    effluent_cod = st.number_input("Effluent COD (mg/L)", min_value=0.0, value=110.0)
    
    etp_efficiency = ((influent_cod - effluent_cod) / influent_cod) * 100
    
    st.markdown("---")
    st.metric(label="⚙️ ETP Removal Efficiency (%)", value=f"{etp_efficiency:.1f} %")

# TAB 4: Unit Conversion Calculator
with tab4:
    st.subheader("🔄 Unit Conversions (Cheat Sheet Section 8)")
    
    conv_type = st.selectbox("Select Conversion", ["m³ to Liters", "kWh to GJ", "MT (Tonnes) to Kg"])
    input_val = st.number_input("Enter Value to Convert", min_value=0.0, value=10.0)
    
    if conv_type == "m³ to Liters":
        st.success(f"{input_val} m³ = **{input_val * 1000:,.0f} Liters**")
    elif conv_type == "kWh to GJ":
        st.success(f"{input_val} kWh = **{input_val * 0.0036:,.4f} GJ**")
    elif conv_type == "MT (Tonnes) to Kg":
        st.success(f"{input_val} MT = **{input_val * 1000:,.0f} Kg**")
