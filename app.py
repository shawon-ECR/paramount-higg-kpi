import streamlit as st

# Page setup for mobile optimization
st.set_page_config(
    page_title="Paramount ETP & Sustainability Master Calculator",
    page_icon="🌱",
    layout="centered"
)

# Custom Styling for dark & light mode text visibility
st.markdown("""
    <style>
    .main { padding: 0.8rem; }
    div[data-testid="stMetric"] {
        background-color: #1e293b !important;
        padding: 12px !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Paramount ETP & ECR Master Calculator")
st.caption("Paramount Textile PLC - Environmental Compliance & Sustainability Dashboard")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💧 Water & Energy", 
    "🧪 ETP & Waste", 
    "🌍 GHG Climate", 
    "🔄 Unit Converter"
])

# ----------------------------------------------------
# TAB 1: Water & Energy (Higg FEM & Cheat Sheet KPIs)
# ----------------------------------------------------
with tab1:
    st.subheader("💧 Water & Energy Resource Inputs")
    
    production_kg = st.number_input("Total Production (Kg Fabric)", min_value=1.0, value=100000.0, step=1000.0)
    
    col1, col2 = st.columns(2)
    with col1:
        fresh_water_m3 = st.number_input("Fresh Water Consumed (m³)", min_value=0.0, value=5000.0)
        reused_water_m3 = st.number_input("Reused / Recycled Water (m³)", min_value=0.0, value=1000.0)
        grid_electricity_kwh = st.number_input("Grid Electricity (kWh)", min_value=0.0, value=120000.0)
    with col2:
        natural_gas_m3 = st.number_input("Natural Gas (m³)", min_value=0.0, value=45000.0)
        diesel_liter = st.number_input("Diesel Consumed (Liters)", min_value=0.0, value=1200.0)

    # Calculations
    total_water_m3 = fresh_water_m3 + reused_water_m3
    total_water_liters = total_water_m3 * 1000
    
    water_kpi = (total_water_liters / production_kg) if production_kg > 0 else 0
    water_reuse_rate = (reused_water_m3 / total_water_m3 * 100) if total_water_m3 > 0 else 0
    
    # Energy conversion (1 kWh = 0.0036 GJ; NG ~10.5 kWh/m³; Diesel ~10 kWh/L)
    total_energy_kwh = grid_electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liter * 10.0)
    total_energy_gj = total_energy_kwh * 0.0036
    energy_kpi_kwh = total_energy_kwh / production_kg
    energy_kpi_gj = total_energy_gj / production_kg

    st.markdown("---")
    st.subheader("📊 Water & Energy Calculated KPIs")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="💧 Water Intensity", value=f"{water_kpi:.2f} L/kg fabric")
        st.metric(label="🔄 Water Reuse Rate", value=f"{water_reuse_rate:.1f} %")
    with c2:
        st.metric(label="⚡ Energy Intensity (kWh)", value=f"{energy_kpi_kwh:.2f} kWh/kg")
        st.metric(label="🔥 Energy Intensity (GJ)", value=f"{energy_kpi_gj:.5f} GJ/kg")

    if water_kpi <= 60:
        st.success("✅ Water KPI is Best-in-Class (<= 60 L/kg)")
    elif water_kpi <= 90:
        st.warning("⚠️ Water KPI is Moderate (60-90 L/kg)")
    else:
        st.error("❌ High Water Usage (> 90 L/kg). Needs Reduction!")

# ----------------------------------------------------
# TAB 2: ETP Operations, Chemicals & Waste
# ----------------------------------------------------
with tab2:
    st.subheader("🧪 ETP Operation & Environmental Compliance")
    
    col_a, col_b = st.columns(2)
    with col_a:
        influent_cod = st.number_input("Influent COD (mg/L)", min_value=1.0, value=1200.0)
        effluent_cod = st.number_input("Effluent COD (mg/L)", min_value=0.0, value=110.0)
        influent_bod = st.number_input("Influent BOD (mg/L)", min_value=1.0, value=350.0)
        effluent_bod = st.number_input("Effluent BOD (mg/L)", min_value=0.0, value=25.0)
    with col_b:
        total_chemical_kg = st.number_input("Total Chemicals Used (Kg)", min_value=0.0, value=15000.0)
        sludge_produced_kg = st.number_input("ETP Sludge Produced (Kg)", min_value=0.0, value=2500.0)
        total_waste_kg = st.number_input("Total Solid Waste (Kg)", min_value=1.0, value=5000.0)
        diverted_waste_kg = st.number_input("Recycled / Diverted Waste (Kg)", min_value=0.0, value=4200.0)

    # Calculations
    cod_efficiency = ((influent_cod - effluent_cod) / influent_cod) * 100
    bod_efficiency = ((influent_bod - effluent_bod) / influent_bod) * 100
    chemical_intensity = total_chemical_kg / production_kg
    sludge_kpi_g = (sludge_produced_kg / production_kg) * 1000  # Grams per kg fabric
    waste_diversion_rate = (diverted_waste_kg / total_waste_kg) * 100

    st.markdown("---")
    st.subheader("📈 ETP & Waste Calculated KPIs")

    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="⚙️ COD Removal Efficiency", value=f"{cod_efficiency:.1f} %")
        st.metric(label="🧪 BOD Removal Efficiency", value=f"{bod_efficiency:.1f} %")
        st.metric(label="⚗️ Chemical Intensity", value=f"{chemical_intensity:.3f} kg/kg fabric")
    with c2:
        st.metric(label="🍂 Sludge KPI", value=f"{sludge_kpi_g:.2f} g/kg fabric")
        st.metric(label="♻️ Waste Diversion Rate", value=f"{waste_diversion_rate:.1f} %")

    # DOE Limits Warning Check
    if effluent_cod > 200:
        st.error("⚠️ Warning: Effluent COD exceeds DOE Limit (200 mg/L)!")
    if effluent_bod > 50:
        st.error("⚠️ Warning: Effluent BOD exceeds DOE Limit (50 mg/L)!")
    if effluent_cod <= 200 and effluent_bod <= 50:
        st.success("✅ ETP Discharge Parameters meet DOE Standards!")

# ----------------------------------------------------
# TAB 3: GHG Carbon Footprint & Revenue Intensity
# ----------------------------------------------------
with tab3:
    st.subheader("🌍 Carbon Footprint & GHG Intensity")
    
    revenue_usd = st.number_input("Monthly Revenue (USD $)", min_value=1.0, value=500000.0, step=10000.0)
    
    # GHG Calculations (IPCC Standards for BD)
    ng_ghg = natural_gas_m3 * 1.98       # kg CO2e per m3 Natural Gas
    diesel_ghg = diesel_liter * 2.68     # kg CO2e per Liter Diesel
    scope_1_mt = (ng_ghg + diesel_ghg) / 1000  # Metric Tons CO2e
    
    grid_ghg = grid_electricity_kwh * 0.55  # kg CO2e per kWh
    scope_2_mt = grid_ghg / 1000  # Metric Tons CO2e
    
    total_ghg_mt = scope_1_mt + scope_2_mt
    ghg_intensity_prod = (total_ghg_mt * 1000) / production_kg  # kg CO2e / kg fabric
    ghg_intensity_rev = total_ghg_mt / (revenue_usd / 1000000)  # tCO2e / Million USD

    st.markdown("---")
    st.subheader("📊 GHG Emissions Results")
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.metric(label="🔥 Scope 1 Emissions (Direct)", value=f"{scope_1_mt:.2f} tCO₂e")
        st.metric(label="🔌 Scope 2 Emissions (Grid)", value=f"{scope_2_mt:.2f} tCO₂e")
    with col_y:
        st.metric(label="🌱 Total GHG Emissions", value=f"{total_ghg_mt:.2f} tCO₂e")
        st.metric(label="📉 Production GHG Intensity", value=f"{ghg_intensity_prod:.3f} kg CO₂e/kg")

    st.metric(label="💼 Revenue GHG Intensity (Cheat Sheet)", value=f"{ghg_intensity_rev:.2f} tCO₂e / $1M")

# ----------------------------------------------------
# TAB 4: Unit Converter
# ----------------------------------------------------
with tab4:
    st.subheader("🔄 Quick Unit Converter (Cheat Sheet Section 8)")
    
    conv_type = st.selectbox(
        "Select Unit Conversion", 
        ["m³ to Liters", "Liters to m³", "kWh to GJ", "GJ to kWh", "MT (Tonnes) to Kg", "Kg to MT"]
    )
    input_val = st.number_input("Enter Value to Convert", min_value=0.0, value=100.0)
    
    if conv_type == "m³ to Liters":
        st.success(f"**{input_val:,.2f} m³** = **{input_val * 1000:,.2f} Liters**")
    elif conv_type == "Liters to m³":
        st.success(f"**{input_val:,.2f} Liters** = **{input_val / 1000:,.4f} m³**")
    elif conv_type == "kWh to GJ":
        st.success(f"**{input_val:,.2f} kWh** = **{input_val * 0.0036:,.4f} GJ**")
    elif conv_type == "GJ to kWh":
        st.success(f"**{input_val:,.2f} GJ** = **{input_val / 0.0036:,.2f} kWh**")
    elif conv_type == "MT (Tonnes) to Kg":
        st.success(f"**{input_val:,.2f} MT** = **{input_val * 1000:,.2f} Kg**")
    elif conv_type == "Kg to MT":
        st.success(f"**{input_val:,.2f} Kg** = **{input_val / 1000:,.4f} MT**")
