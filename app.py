import streamlit as st

# Page setup for mobile & desktop optimization
st.set_page_config(
    page_title="TexPulse | Textile Sustainability & Savings",
    page_icon="🫀",
    layout="centered"
)

# Custom Styling for modern TexPulse UI
st.markdown("""
    <style>
    .main { padding: 0.8rem; }
    div[data-testid="stMetric"] {
        background-color: #0f172a !important;
        padding: 12px !important;
        border-radius: 10px !important;
        border: 1px solid #1e293b !important;
        margin-bottom: 10px !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #38bdf8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }
    .stAppHeader { background-color: transparent; }
    </style>
""", unsafe_allow_html=True)

# TexPulse Header & Tagline
st.title("🫀 TexPulse")
st.markdown("##### *The Heartbeat of Textile Sustainability & Savings*")
st.caption("B2B Operational Compliance, Energy Optimization & Financial ROI Engine")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💧 Water & Energy", 
    "🧪 ETP & Waste", 
    "💰 Cost & Savings",
    "🌍 GHG Climate", 
    "📄 Audit Report"
])

# ----------------------------------------------------
# TAB 1: Water & Energy (Higg FEM & KPIs)
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
    
    total_energy_kwh = grid_electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liter * 10.0)
    total_energy_gj = total_energy_kwh * 0.0036
    energy_kpi_kwh = total_energy_kwh / production_kg

    st.markdown("---")
    st.subheader("📊 Water & Energy Calculated KPIs")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="💧 Water Intensity", value=f"{water_kpi:.2f} L/kg fabric")
        st.metric(label="🔄 Water Reuse Rate", value=f"{water_reuse_rate:.1f} %")
    with c2:
        st.metric(label="⚡ Energy Intensity (kWh)", value=f"{energy_kpi_kwh:.2f} kWh/kg")
        st.metric(label="🔥 Energy Intensity (GJ)", value=f"{total_energy_gj / production_kg:.5f} GJ/kg")

    if water_kpi <= 60:
        st.success("✅ Water KPI is Best-in-Class (<= 60 L/kg)")
    elif water_kpi <= 90:
        st.warning("⚠️ Water KPI is Moderate (60-90 L/kg)")
    else:
        st.error("❌ High Water Usage (> 90 L/kg). Needs Reduction!")

# ----------------------------------------------------
# TAB 2: ETP Operations & Waste
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
    sludge_kpi_g = (sludge_produced_kg / production_kg) * 1000
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

# ----------------------------------------------------
# TAB 3: COST, THERMAL & POWER SAVINGS CALCULATOR
# ----------------------------------------------------
with tab3:
    st.subheader("💰 রিসোর্স খরচ ও সর্বাত্মক শক্তি সাশ্রয় ক্যালকুলেটর")
    st.caption("কারখানার ইউনিট দর এবং বাস্তবায়িত পদক্ষেপগুলো অন/অফ করে সাশ্রয় দেখুন:")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        water_cost_per_m3 = st.number_input("পানির লিফটিং খরচ (টাকা/m³)", min_value=0.0, value=35.0)
        elec_cost_per_kwh = st.number_input("বিদ্যুৎ বিল (টাকা/kWh)", min_value=0.0, value=10.5)
        gas_cost_per_m3 = st.number_input("গ্যাস বিল (টাকা/m³)", min_value=0.0, value=30.0)
    with col_c2:
        diesel_cost_per_l = st.number_input("ডিজেল খরচ (টাকা/লিটার)", min_value=0.0, value=108.0)
        chem_cost_per_kg = st.number_input("গড় কেমিক্যাল দর (টাকা/Kg)", min_value=0.0, value=120.0)

    # Base Costs Calculation
    cost_water = fresh_water_m3 * water_cost_per_m3
    cost_elec = grid_electricity_kwh * elec_cost_per_kwh
    cost_gas = natural_gas_m3 * gas_cost_per_m3
    cost_diesel = diesel_liter * diesel_cost_per_l
    cost_chem = total_chemical_kg * chem_cost_per_kg
    
    total_monthly_cost = cost_water + cost_elec + cost_gas + cost_diesel + cost_chem

    st.markdown("---")
    st.subheader("📊 বর্তমান মাসিক মোট রিসোর্স খরচ")
    st.metric(label="💵 মোট মাসিক খরচ (টাকা)", value=f"৳ {total_monthly_cost:,.0f}")
    
    # Thermal & Gas Fuel Savings
    st.markdown("---")
    st.subheader("🔥 ১. থার্মাল এনার্জি ও স্টিম সাশ্রয়ের সব পদক্ষেপ")
    
    condensate_pct = st.slider("১.১ কনডেনসেট রিকভারি টার্গেট (%)", min_value=0, max_value=90, value=70)
    gas_saving_condensate = cost_gas * (condensate_pct / 100 * 0.10)
    
    phe_active = st.checkbox("১.২ PHE (Plate Heat Exchanger): ডাইং/ওয়াশিং গরম ড্রেন ওয়াটার হিট রিকভারি", value=True)
    gas_saving_phe = cost_gas * 0.04 if phe_active else 0.0
    
    econ_active = st.checkbox("১.৩ Boiler Economizer: বয়লারের ফ্লু গ্যাস দিয়ে পানি গরমকরণ", value=True)
    gas_saving_econ = cost_gas * 0.05 if econ_active else 0.0
    
    stenter_whr_active = st.checkbox("১.৪ Stenter Exhaust Heat Recovery: স্টেন্টারের গরম বাতাস থেকে হিট রিকভারি", value=True)
    gas_saving_stenter_whr = cost_gas * 0.04 if stenter_whr_active else 0.0
    
    whrb_active = st.checkbox("১.৫ WHRB / Co-generation: জেনারেটরের ধোঁয়া থেকে ফ্রি স্টিম উৎপাদন", value=True)
    gas_saving_whrb = cost_gas * 0.12 if whrb_active else 0.0
    
    insulation_active = st.checkbox("১.৬ Steam Pipe Insulation: পাইপ, ভালভ ও ফ্ল্যাঞ্জে ইনসুলেশন", value=True)
    gas_saving_insulation = cost_gas * 0.03 if insulation_active else 0.0

    steamtrap_active = st.checkbox("১.৭ Steam Trap Audit: স্টিম ট্র্যাপ অডিট ও লিকেজ বন্ধকরণ", value=True)
    gas_saving_steamtrap = cost_gas * 0.03 if steamtrap_active else 0.0

    total_gas_savings = (gas_saving_condensate + gas_saving_phe + gas_saving_econ + 
                         gas_saving_stenter_whr + gas_saving_whrb + gas_saving_insulation + gas_saving_steamtrap)
    
    st.info(f"🔥 **মোট গ্যাস ও স্টিম সাশ্রয়:** মাসে **৳ {total_gas_savings:,.0f}** | বছরে **৳ {total_gas_savings * 12:,.0f}** টাকা")

    # Electrical Power Savings
    st.markdown("---")
    st.subheader("⚡ ২. জেনারেটর ও ইলেকট্রিক্যাল বিদ্যুৎ সাশ্রয়ের পদক্ষেপ")
    
    vfd_active = st.checkbox("২.১ VFD (Variable Frequency Drive): ETP ব্লোয়ার, পাম্প ও স্টেন্টার ফ্যানে ইনভার্টার", value=True)
    elec_saving_vfd = cost_elec * 0.08 if vfd_active else 0.0
    
    air_leak_active = st.checkbox("২.২ Compressed Air Optimization: এয়ার কমপ্রেসার লিকেজ বন্ধ ও ১ বার প্রেসার কমানো", value=True)
    elec_saving_air = cost_elec * 0.07 if air_leak_active else 0.0

    ie3_motors_active = st.checkbox("২.৩ High-Efficiency Motors: IE3 / IE4 রেটিং সমৃদ্ধ সাশ্রয়ী মোটর ব্যবহার", value=True)
    elec_saving_motors = cost_elec * 0.05 if ie3_motors_active else 0.0

    absorption_chiller_active = st.checkbox("২.৪ Absorption Chiller: ওয়েস্ট হিট দিয়ে এসি/চিলার পরিচালনা", value=True)
    elec_saving_chiller = cost_elec * 0.06 if absorption_chiller_active else 0.0

    total_elec_savings = elec_saving_vfd + elec_saving_air + elec_saving_motors + elec_saving_chiller
    
    st.info(f"⚡ **মোট বিদ্যুৎ সাশ্রয়:** মাসে **৳ {total_elec_savings:,.0f}** | বছরে **৳ {total_elec_savings * 12:,.0f}** টাকা")

    # Process & Machine Optimization
    st.markdown("---")
    st.subheader("🧪 & 👗 ৩. প্রসেস ও মেশিন অপ্টিমাইজেশন সাশ্রয়")
    
    llr_active = st.checkbox("৩.১ Low Liquor Ratio (LLR) Dyeing: কম পানির রেশিওতে (১:৪/১:৫) ডাইং", value=True)
    gas_saving_llr = cost_gas * 0.05 if llr_active else 0.0
    water_saving_llr = (fresh_water_m3 * 0.10) * water_cost_per_m3 if llr_active else 0.0

    stenter_moisture_active = st.checkbox("৩.২ Stenter Moisture Control: অটো ড্রায়ার ও ড্যাম্পার দিয়ে কাপড় শুকানো", value=True)
    gas_saving_moisture = cost_gas * 0.04 if stenter_moisture_active else 0.0

    low_temp_enzyme_active = st.checkbox("৩.৩ Low-Temp Enzymes: কম তাপমাত্রায় স্কাউরিং ও ওয়াশিং পরিচালনা", value=True)
    gas_saving_enzyme = cost_gas * 0.03 if low_temp_enzyme_active else 0.0

    target_reuse_pct = st.slider("৩.৪ ETP ট্রিটেড পানি প্রসেসে পুনর্ব্যবহার/রিসাইকেল (%)", min_value=0, max_value=60, value=25)
    water_savings_reuse = (fresh_water_m3 * (target_reuse_pct / 100)) * water_cost_per_m3

    chem_opt_active = st.checkbox("৩.৫ Jar Test & Auto-Dosing: ETP কেমিক্যালের অপচয় রোধ", value=True)
    chem_savings = cost_chem * 0.05 if chem_opt_active else 0.0

    total_process_gas_savings = gas_saving_llr + gas_saving_moisture + gas_saving_enzyme
    total_water_savings = water_saving_llr + water_savings_reuse
    
    st.info(f"👗 **প্রসেস অপ্টিমাইজেশনের সুফল:** প্রসেস থেকে অতিরিক্ত গ্যাস সাশ্রয় **৳ {total_process_gas_savings:,.0f}**, পানি সাশ্রয় **৳ {total_water_savings:,.0f}** এবং কেমিক্যাল সাশ্রয় **৳ {chem_savings:,.0f}** টাকা/মাস।")

    # Grand Total Savings Summary
    st.markdown("---")
    grand_total_gas_savings = total_gas_savings + total_process_gas_savings
    grand_total_monthly_savings = grand_total_gas_savings + total_elec_savings + total_water_savings + chem_savings
    grand_total_yearly_savings = grand_total_monthly_savings * 12

    st.success(f"""
    🎯 **TexPulse Financial Savings Summary:**
    * ⛽ **গ্যাস ও স্টিম সাশ্রয়:** ৳ {grand_total_gas_savings:,.0f} / মাস
    * ⚡ **বিদ্যুৎ সাশ্রয়:** ৳ {total_elec_savings:,.0f} / মাস
    * 💧 **পানি ও কেমিক্যাল সাশ্রয়:** ৳ {total_water_savings + chem_savings:,.0f} / মাস
    
    🏆 **সর্বমোট প্রতি মাসে বাঁচবে:** **৳ {grand_total_monthly_savings:,.0f}**  
    🏆 **সর্বমোট প্রতি বছরে বাঁচবে:** **৳ {grand_total_yearly_savings:,.0f}**
    """)

# ----------------------------------------------------
# TAB 4: GHG Carbon Footprint & Revenue Intensity
# ----------------------------------------------------
with tab4:
    st.subheader("🌍 Carbon Footprint & GHG Intensity")
    
    revenue_usd = st.number_input("Monthly Revenue (USD $)", min_value=1.0, value=500000.0, step=10000.0)
    
    scope_1_mt = ((natural_gas_m3 * 1.98) + (diesel_liter * 2.68)) / 1000
    scope_2_mt = (grid_electricity_kwh * 0.55) / 1000
    total_ghg_mt = scope_1_mt + scope_2_mt
    
    ghg_intensity_prod = (total_ghg_mt * 1000) / production_kg
    ghg_intensity_rev = total_ghg_mt / (revenue_usd / 1000000)

    st.markdown("---")
    st.subheader("📊 GHG Emissions Results")
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.metric(label="🔥 Scope 1 Emissions", value=f"{scope_1_mt:.2f} tCO₂e")
        st.metric(label="🔌 Scope 2 Emissions", value=f"{scope_2_mt:.2f} tCO₂e")
    with col_y:
        st.metric(label="🌱 Total GHG Emissions", value=f"{total_ghg_mt:.2f} tCO₂e")
        st.metric(label="📉 Production GHG Intensity", value=f"{ghg_intensity_prod:.3f} kg CO₂e/kg")

    st.metric(label="💼 Revenue GHG Intensity", value=f"{ghg_intensity_rev:.2f} tCO₂e / $1M")

# ----------------------------------------------------
# TAB 5: AUDIT REPORT GENERATOR (NEW FEATURE)
# ----------------------------------------------------
with tab5:
    st.subheader("📄 TexPulse Executive Audit Report")
    st.caption("অডিটর, বায়ার বা ম্যানেজমেন্টের জন্য ১-ক্লিকে বিস্তারিত টেক্সট রিপোর্ট এক্সপোর্ট করুন:")
    
    factory_name = st.text_input("Factory Name", value="Paramount Textile PLC")
    reporting_month = st.selectbox("Reporting Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    report_content = f"""====================================================
🫀 TEXPULSE EXECUTIVE AUDIT REPORT
The Heartbeat of Textile Sustainability & Savings
====================================================

Factory Name    : {factory_name}
Reporting Month : {reporting_month}
Compliance Standard: Higg FEM 4.0 / ZDHC / DOE

----------------------------------------------------
1. PRODUCTION & RESOURCE KPI SUMMARY
----------------------------------------------------
- Total Production       : {production_kg:,.0f} Kg Fabric
- Water Intensity        : {water_kpi:.2f} Liters/Kg Fabric
- Water Reuse Rate       : {water_reuse_rate:.1f} %
- Energy Intensity       : {energy_kpi_kwh:.2f} kWh/Kg Fabric ({total_energy_gj / production_kg:.5f} GJ/Kg)

----------------------------------------------------
2. ETP & ENVIRONMENTAL COMPLIANCE
----------------------------------------------------
- COD Removal Efficiency : {cod_efficiency:.1f} %
- BOD Removal Efficiency : {bod_efficiency:.1f} %
- Chemical Intensity     : {chemical_intensity:.3f} Kg/Kg Fabric
- Waste Diversion Rate   : {waste_diversion_rate:.1f} %

----------------------------------------------------
3. TEXPULSE FINANCIAL SAVINGS ANALYSIS
----------------------------------------------------
- Thermal & Fuel Savings : BDT {grand_total_gas_savings:,.0f} / Month
- Power & Elec Savings   : BDT {total_elec_savings:,.0f} / Month
- Water & Chem Savings   : BDT {total_water_savings + chem_savings:,.0f} / Month

>>> TOTAL MONTHLY FINANCIAL SAVINGS : BDT {grand_total_monthly_savings:,.0f}
>>> TOTAL ANNUAL POTENTIAL SAVINGS  : BDT {grand_total_yearly_savings:,.0f}

----------------------------------------------------
4. GHG CARBON FOOTPRINT (SCOPE 1 & 2)
----------------------------------------------------
- Scope 1 (Direct Fuel)  : {scope_1_mt:.2f} tCO2e
- Scope 2 (Electricity)  : {scope_2_mt:.2f} tCO2e
- Total Carbon Footprint : {total_ghg_mt:.2f} tCO2e
- Revenue Intensity      : {ghg_intensity_rev:.2f} tCO2e / $1M Revenue

====================================================
Generated by TexPulse B2B Intelligence Engine
====================================================
"""

    st.text_area("Audit Summary Preview", value=report_content, height=350)
    
    st.download_button(
        label="📥 Download TexPulse Audit Report (.txt)",
        data=report_content,
        file_name=f"TexPulse_Audit_Report_{factory_name.replace(' ', '_')}.txt",
        mime="text/plain"
    )
