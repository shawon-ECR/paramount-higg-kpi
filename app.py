import streamlit as st
import io
import pandas as pd
from supabase import create_client
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ----------------------------------------------------
# 1. PAGE SETUP & STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="TexPulse | Enterprise Worldly & Higg FEM Platform",
    page_icon="🫀",
    layout="wide"
)

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
    .tech-card {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #0284c7;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. SUPABASE CLOUD DATABASE CONNECTION
# ----------------------------------------------------
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"].strip()
        key = st.secrets["SUPABASE_KEY"].strip()
        return create_client(url, key)
    except Exception as e:
        st.error(f"Database Connection Setup Error: {e}")
        return None

supabase = init_supabase()

st.title("🫀 TexPulse")
st.markdown("##### *Worldly (Higg FEM 4.0) Enterprise Compliance & Technology ROI Engine*")

# User Session
if "user_email" not in st.session_state:
    st.session_state.user_email = "demo@paramounttex.com"

with st.sidebar:
    st.header("🔐 Portal Settings")
    st.session_state.user_email = st.text_input("Corporate Email", value=st.session_state.user_email)
    if supabase:
        st.success("🟢 Cloud DB Connected")
    else:
        st.error("🔴 Cloud DB Disconnected")

# ----------------------------------------------------
# 3. HIGG FEM 4.0 SCORING ENGINE
# ----------------------------------------------------
def calculate_compliance_scores(water_kpi, energy_kpi, cod_eff, bod_eff):
    water_score = 100 if water_kpi <= 50 else (70 if water_kpi <= 80 else 40)
    water_level = "Level 3 (World Class)" if water_kpi <= 50 else ("Level 2 (Good)" if water_kpi <= 80 else "Level 1 (Baseline)")

    energy_score = 100 if energy_kpi <= 2.5 else (70 if energy_kpi <= 4.0 else 40)
    energy_level = "Level 3 (Highly Efficient)" if energy_kpi <= 2.5 else ("Level 2 (Moderate)" if energy_kpi <= 4.0 else "Level 1 (Baseline)")

    if cod_eff >= 85 and bod_eff >= 90:
        etp_status = "ZDHC & DOE Compliant (Pass)"
        etp_score = 100
    elif cod_eff >= 75:
        etp_status = "DOE Compliant / ZDHC Partial"
        etp_score = 70
    else:
        etp_status = "Non-Compliant / High Risk"
        etp_score = 30

    overall_score = round((water_score * 0.35) + (energy_score * 0.35) + (etp_score * 0.30), 1)
    overall_badge = "🟢 Gold / High Compliance" if overall_score >= 85 else ("🟡 Silver / Satisfactory" if overall_score >= 65 else "🔴 Bronze / Action Required")

    return {
        "water_level": water_level, "water_score": water_score,
        "energy_level": energy_level, "energy_score": energy_score,
        "etp_status": etp_status, "etp_score": etp_score,
        "overall_score": overall_score, "overall_badge": overall_badge
    }

# ----------------------------------------------------
# 4. PDF REPORT GENERATOR ENGINE
# ----------------------------------------------------
def generate_pdf_report(factory_name, reporting_month, production_kg, water_kpi, energy_kpi, 
                        cod_eff, bod_eff, monthly_savings, yearly_savings, scope1, scope2, total_ghg, comp_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0f172a'), spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#0284c7'), spaceAfter=12)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#0f172a'), spaceBefore=8, spaceAfter=4)
    
    story.append(Paragraph("🫀 TexPulse Executive Audit Report", title_style))
    story.append(Paragraph("Worldly / Higg FEM 4.0 Standard Compliance Audit & ROI Summary", subtitle_style))
    
    meta_data = [
        [Paragraph("<b>Factory Name:</b>", styles['Normal']), Paragraph(factory_name, styles['Normal']),
         Paragraph("<b>Reporting Month:</b>", styles['Normal']), Paragraph(reporting_month, styles['Normal'])],
        [Paragraph("<b>Standard:</b>", styles['Normal']), Paragraph("Worldly / Higg FEM 4.0 / ZDHC", styles['Normal']),
         Paragraph("<b>Status:</b>", styles['Normal']), Paragraph(f"<b>{comp_data['overall_badge']}</b>", styles['Normal'])]
    ]
    t_meta = Table(meta_data, colWidths=[100, 160, 100, 160])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Higg FEM 4.0 & ZDHC Compliance Scorecard", heading_style))
    score_table_data = [
        ["Compliance Area", "Measured Value", "Higg FEM / ZDHC Rating", "Score Points"],
        ["Water Intensity", f"{water_kpi:.2f} L/kg", comp_data['water_level'], f"{comp_data['water_score']} / 100"],
        ["Energy Efficiency", f"{energy_kpi:.2f} kWh/kg", comp_data['energy_level'], f"{comp_data['energy_score']} / 100"],
        ["Wastewater (ETP)", f"COD {cod_eff:.1f}%, BOD {bod_eff:.1f}%", comp_data['etp_status'], f"{comp_data['etp_score']} / 100"],
        ["OVERALL HIGG SCORE", "-", comp_data['overall_badge'], f"{comp_data['overall_score']} / 100"]
    ]
    t_score = Table(score_table_data, colWidths=[130, 130, 160, 100])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
    ]))
    story.append(t_score)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Financial Savings & Carbon Footprint", heading_style))
    fin_data = [
        ["Financial & Carbon Impact", "Monthly Value", "Annual Projection"],
        ["Resource Savings", f"BDT {monthly_savings:,.0f}", f"BDT {yearly_savings:,.0f}"],
        ["Scope 1 Direct Carbon", f"{scope1:.2f} tCO2e", f"{scope1*12:.2f} tCO2e"],
        ["Scope 2 Indirect Carbon", f"{scope2:.2f} tCO2e", f"{scope2*12:.2f} tCO2e"],
        ["Total Carbon Footprint", f"{total_ghg:.2f} tCO2e", f"{total_ghg*12:.2f} tCO2e"]
    ]
    t_fin = Table(fin_data, colWidths=[200, 160, 160])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_fin)

    doc.build(story)
    buffer.seek(0)
    return buffer

# ----------------------------------------------------
# 5. APP TABS & INTERFACE
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💧 Water & Energy", 
    "🧪 ETP & Waste", 
    "🌐 Worldly 7 Modules",
    "💰 Cost & Savings",
    "🌍 GHG Climate", 
    "💡 Tech & Innovation Hub",
    "🧮 What-If ROI Engine",
    "🏆 Higg PDF & Analytics"
])

# Tab 1: Water & Energy
with tab1:
    st.subheader("💧 Water & Energy Inputs")
    production_kg = st.number_input("Total Production (Kg Fabric)", min_value=1.0, value=100000.0)
    col1, col2 = st.columns(2)
    with col1:
        fresh_water_m3 = st.number_input("Fresh Water (m³)", min_value=0.0, value=5000.0)
        reused_water_m3 = st.number_input("Reused Water (m³)", min_value=0.0, value=1000.0)
        grid_electricity_kwh = st.number_input("Grid Electricity (kWh)", min_value=0.0, value=120000.0)
    with col2:
        natural_gas_m3 = st.number_input("Natural Gas (m³)", min_value=0.0, value=45000.0)
        diesel_liter = st.number_input("Diesel Consumed (Liters)", min_value=0.0, value=1200.0)

    total_water_m3 = fresh_water_m3 + reused_water_m3
    water_kpi = (total_water_m3 * 1000 / production_kg) if production_kg > 0 else 0
    total_energy_kwh = grid_electricity_kwh + (natural_gas_m3 * 10.5) + (diesel_liter * 10.0)
    energy_kpi_kwh = total_energy_kwh / production_kg

    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric("💧 Water Intensity KPI", f"{water_kpi:.2f} L/kg")
    with c_m2:
        st.metric("⚡ Energy Intensity KPI", f"{energy_kpi_kwh:.2f} kWh/kg")

# Tab 2: ETP
with tab2:
    st.subheader("🧪 ETP Operational Inputs")
    c1, c2 = st.columns(2)
    with c1:
        influent_cod = st.number_input("Influent COD (mg/L)", min_value=1.0, value=1200.0)
        effluent_cod = st.number_input("Effluent COD (mg/L)", min_value=0.0, value=110.0)
    with c2:
        influent_bod = st.number_input("Influent BOD (mg/L)", min_value=1.0, value=350.0)
        effluent_bod = st.number_input("Effluent BOD (mg/L)", min_value=0.0, value=25.0)

    cod_efficiency = ((influent_cod - effluent_cod) / influent_cod) * 100
    bod_efficiency = ((influent_bod - effluent_bod) / influent_bod) * 100
    st.metric("⚙️ COD Removal Efficiency", f"{cod_efficiency:.1f} %")

comp_data = calculate_compliance_scores(water_kpi, energy_kpi_kwh, cod_efficiency, bod_efficiency)

# Tab 3: Worldly 7 Impact Modules Checklist
with tab3:
    st.subheader("🌐 Worldly (Higg FEM 4.0) 7 Impact Modules Checklist")
    st.caption("Self-Assessment module following official Worldly architecture")

    mod1, mod2 = st.columns(2)
    with mod1:
        st.markdown("#### 1. Environmental Management System (EMS)")
        st.checkbox("EMS Team & Environmental Policy active")
        st.checkbox("Valid Environmental Clearance Certificate (ECC)")

        st.markdown("#### 2. Energy & Greenhouse Gas (GHG)")
        st.checkbox("Sub-meters installed for high energy machinery")
        st.checkbox("Annual Energy Reduction Target established")

        st.markdown("#### 3. Water Use & Management")
        st.checkbox("Water meters installed on groundwater & production lines")
        st.checkbox("Water reuse/recycling system operational")

        st.markdown("#### 4. Wastewater & ETP Management")
        st.checkbox("Daily testing of COD, BOD, pH, TSS in ETP lab")
        st.checkbox("ZDHC Wastewater Guidelines conformance test passed")

    with mod2:
        st.markdown("#### 5. Air Emissions Management")
        st.checkbox("Boiler exhaust stack emission periodic testing done")
        st.checkbox("Scrubber / Electrostatic Precipitator installed")

        st.markdown("#### 6. Waste Management")
        st.checkbox("Hazardous waste segregated and licensed disposal")
        st.checkbox("Zero Waste to Landfill policy initiated")

        st.markdown("#### 7. Chemicals Management")
        st.checkbox("Chemical Inventory List (CIL) updated with ZDHC MRSL")
        st.checkbox("Safety Data Sheets (SDS) available in local language")

# Tab 4: Cost & Savings
with tab3:
    pass # Managed in Tab 4 below
with tab4:
    st.subheader("💰 Financial Savings Engine")
    col_sav1, col_sav2 = st.columns(2)
    with col_sav1:
        gas_cost = st.number_input("Monthly Gas Bill (BDT)", min_value=0.0, value=1350000.0, step=50000.0)
        elec_cost = st.number_input("Monthly Electricity Bill (BDT)", min_value=0.0, value=1260000.0, step=50000.0)
        water_chem_cost = st.number_input("Monthly Water & Chemical Cost (BDT)", min_value=0.0, value=400000.0, step=20000.0)
    with col_sav2:
        energy_target_pct = st.slider("Energy Optimization Target (%)", min_value=0.0, max_value=40.0, value=10.0, step=0.5)
        water_target_pct = st.slider("Water & Chemical Optimization Target (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.5)

    monthly_energy_savings = (gas_cost + elec_cost) * (energy_target_pct / 100.0)
    monthly_water_savings = water_chem_cost * (water_target_pct / 100.0)
    monthly_savings = monthly_energy_savings + monthly_water_savings
    yearly_savings = monthly_savings * 12

    m_s1, m_s2, m_s3 = st.columns(3)
    with m_s1:
        st.metric("⚡ Energy Savings", f"৳ {monthly_energy_savings:,.0f} / month")
    with m_s2:
        st.metric("💧 Water & Chem Savings", f"৳ {monthly_water_savings:,.0f} / month")
    with m_s3:
        st.metric("🏆 Total Monthly Savings", f"৳ {monthly_savings:,.0f} / month")

# Tab 5: GHG Climate
with tab5:
    st.subheader("🌍 Carbon Footprint (Scope 1 & Scope 2)")
    scope_1_mt = ((natural_gas_m3 * 1.98) + (diesel_liter * 2.68)) / 1000.0
    scope_2_mt = (grid_electricity_kwh * 0.55) / 1000.0
    total_ghg_mt = scope_1_mt + scope_2_mt

    g1, g2, g3 = st.columns(3)
    with g1:
        st.metric("🔥 Scope 1 (Direct Fuel)", f"{scope_1_mt:.2f} tCO₂e")
    with g2:
        st.metric("⚡ Scope 2 (Grid Electricity)", f"{scope_2_mt:.2f} tCO₂e")
    with g3:
        st.metric("🌱 Total GHG Footprint", f"{total_ghg_mt:.2f} tCO₂e")

# Tab 6: Technology & Innovation Hub (উন্নত ও ভবিষ্যৎ প্রযুক্তি)
with tab6:
    st.subheader("💡 Advanced Green Technology & Future Innovation Hub")
    st.caption("Guide to current best practices and upcoming technologies in sustainable textiles")

    tech_sub1, tech_sub2 = st.tabs(["🛠️ 1. Currently Available Advanced Tech", "🚀 2. Upcoming Next-Gen Tech"])

    with tech_sub1:
        st.markdown("### 🛠️ বর্তমান সময়ে ব্যবহৃত উন্নত প্রযুক্তি ও তাদের সুবিধাবলী")
        
        with st.expander("💧 Low Liquor Ratio Dyeing Machines (1:3 to 1:4)"):
            st.markdown("""
            * **কীভাবে কাজ করে:** সাধারণ ডাইং মেশিনে ১ কেজি কাপড়ের জন্য ৮-১০ লিটার পানি লাগে (1:8/1:10)। কিন্তু আধুনিক স্মার্ট মেশিনে মাত্র ৩-৪ লিটার পানি লাগে।
            * **প্রধান সুবিধা:** পানির খরচ ৫০-৬০% কমে, ডাইং সময় কমে, স্টিম ও কেমিক্যাল খরচ ৩০% সাশ্রয় হয়।
            * **গড় Payback Period:** ১২ থেকে ১৮ মাস।
            """)

        with st.expander("♨️ Waste Heat Recovery System (WHRS) from Stenter & Exhaust"):
            st.markdown("""
            * **কীভাবে কাজ করে:** স্টেন্টারের ধোঁয়া এবং বয়লারের নিষ্কাশিত গরম বাতাস থেকে হিট এক্সচেঞ্জারের মাধ্যমে তাপ রিকভার করে বয়লারের ফিড ওয়াটার বা বাতাস গরম করা হয়।
            * **প্রধান সুবিধা:** বয়লারে ১০-১৫% গ্যাস/ডিজেল সাশ্রয় হয়। Carbon Footprint সরাসরি কমে যায়।
            * **গড় Payback Period:** ৮ থেকে ১৪ মাস।
            """)

        with st.expander("🔄 MVR Evaporator & Zero Liquid Discharge (ZLD)"):
            st.markdown("""
            * **কীভাবে কাজ করে:** ETP-এর পরিশোধিত পানিকে বাষ্পীভূত করে ৯৫% বিশুদ্ধ পানি ফেরত নিয়ে পুনরায় ডাইং প্রক্রিয়ায় ব্যবহার করা হয়।
            * **প্রধান সুবিধা:** ভূগর্ভস্থ পানির নির্ভরতা শূন্যের কাছাকাছি চলে আসে। ZDHC ও ব্র্যান্ড অডিটে সর্বোচ্চ স্কোর পাওয়া যায়।
            * **গড় Payback Period:** ২৪ থেকে ৩৬ মাস।
            """)

        with st.expander("☀️ Rooftop Solar PV System"):
            st.markdown("""
            * **কীভাবে কাজ করে:** কারখানার ছাদের খালি জায়গায় সোলার প্যানেল বসিয়ে সরাসরি গ্রিড বা ফ্যাক্টরি লাইনে বিদ্যুৎ সরবরাহ করা হয়।
            * **প্রধান সুবিধা:** প্রতি ইউনিট বিদ্যুতের খরচ ৩৫-৪০% কমে এবং Scope 2 কার্বন নির্গমন উল্লেখযোগ্যভাবে কমে।
            * **গড় Payback Period:** ৪ থেকে ৫ বছর।
            """)

    with tech_sub2:
        st.markdown("### 🚀 ভবিষ্যতে আসছে এমন টেক্সটাইল প্রযুক্তি (Next-Gen Future Innovations)")
        
        st.info("💡 **২০২৬-২০৩০ সালের মধ্যে নিচের প্রযুক্তিগুলো টেক্সটাইল শিল্পকে সম্পূর্ণ পরিবর্তন করে দেবে:**")

        st.markdown("""
        1. **💨 Supercritical $CO_2$ Waterless Dyeing (পাইনমুক্ত ডাইং):**
           * তরল পানির বদলে অতি-উচ্চ চাপের $CO_2$ গ্যাস ব্যবহার করে সিন্থেটিক কাপড় কালার করা হয়। রঙ করার পর গ্যাস আবার রিকভার করা হয়। **১ ফোঁটা পানিও অপচয় হয় না।**
        
        2. **⚡ Dry Plasma Fabric Treatment (প্লাজমা প্রসেসিং):**
           * পানি ও ভেজা কেমিক্যালের বদলে প্লাজমা রশ্মি দিয়ে ফ্যাব্রিক স্কাউরিং, ব্লিচিং ও ফিনিশিং করা হয়। পানির ব্যবহার ১০০% শূন্য।
        
        3. **🤖 AI Digital Twin for Dyeing & ETP Optimization:**
           * কৃত্রিম বুদ্ধিমত্তা (AI) সেন্সরের মাধ্যমে কাপড়ের শেড ও বয়লার প্রেশার অটোমেটিক মনিটর করবে, ফলে শেড নষ্ট হওয়া বা রি-ডাইং (Re-dyeing) হার শূন্যে নেমে আসবে।
        
        4. **🔥 High-Temperature Industrial Electric Heat Pumps:**
           * প্রাকৃতিক গ্যাস বা ডিজেল ছাড়াই সরাসরি বিদ্যুতের মাধ্যমে উচ্চমাত্রার স্টিম তৈরি করা সম্ভব হবে, যা কারখানার **Scope 1 এমিশন শূন্যে নামিয়ে আনবে**।
        """)

# Tab 7: What-If ROI Calculator
with tab7:
    st.subheader("🧮 What-If Green Technology ROI & Payback Calculator")
    
    preset = st.selectbox(
        "💡 Select Technology Preset",
        [
            "Custom Calculation",
            "☀️ Rooftop Solar System (500 kWp)",
            "♨️ Boiler Economizer & Waste Heat Recovery",
            "💧 RO Water Recycling Plant",
            "⚡ Variable Frequency Drives (VFD) Setup"
        ]
    )

    def_capex = 35000000.0 if "Solar" in preset else (4500000.0 if "Boiler" in preset else 8000000.0)
    def_monthly_sav = 550000.0 if "Solar" in preset else (180000.0 if "Boiler" in preset else 280000.0)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        capex = st.number_input("Capital Investment (CAPEX BDT)", min_value=1000.0, value=def_capex)
        monthly_sav = st.number_input("Monthly Operational Savings (BDT)", min_value=0.0, value=def_monthly_sav)
    with col_r2:
        annual_maint = st.number_input("Annual Maintenance (BDT)", min_value=0.0, value=50000.0)
        project_lifetime = st.slider("Lifetime (Years)", min_value=1, max_value=20, value=10)

    annual_net_sav = (monthly_sav * 12) - annual_maint
    if annual_net_sav > 0:
        payback_months = (capex / annual_net_sav) * 12
        annual_roi = (annual_net_sav / capex) * 100
        
        r1, r2, r3 = st.columns(3)
        with r1: st.metric("Payback Period", f"{payback_months:.1f} Months")
        with r2: st.metric("Annual ROI", f"{annual_roi:.1f} %")
        with r3: st.metric("Annual Net Savings", f"৳ {annual_net_sav:,.0f}")

# Tab 8: PDF & Database
with tab8:
    st.subheader("🏆 Higg FEM Audit Report Generator & Cloud DB")
    
    factory_name = st.text_input("Factory Name", value="Paramount Textile PLC")
    reporting_month = st.selectbox("Reporting Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    btn1, btn2 = st.columns(2)
    with btn1:
        if st.button("☁️ Save Record to Cloud DB"):
            if supabase:
                data = {
                    "user_email": st.session_state.user_email, "factory_name": factory_name,
                    "reporting_month": reporting_month, "production_kg": float(production_kg),
                    "water_kpi": round(float(water_kpi), 2), "energy_kpi": round(float(energy_kpi_kwh), 2),
                    "monthly_savings": round(float(monthly_savings), 2), "total_ghg": round(float(total_ghg_mt), 2)
                }
                supabase.table("factory_records").insert(data).execute()
                st.success("✅ Saved to Supabase Database!")

    with btn2:
        pdf_bytes = generate_pdf_report(
            factory_name, reporting_month, production_kg, water_kpi, energy_kpi_kwh,
            cod_efficiency, bod_efficiency, monthly_savings, yearly_savings,
            scope_1_mt, scope_2_mt, total_ghg_mt, comp_data
        )
        st.download_button("📥 Download Worldly Higg Audit Report PDF", data=pdf_bytes, file_name=f"Higg_Audit_{factory_name}.pdf", mime="application/pdf")
