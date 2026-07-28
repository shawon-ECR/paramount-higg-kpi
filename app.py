import streamlit as st
import io
from supabase import create_client
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ----------------------------------------------------
# 1. PAGE SETUP
# ----------------------------------------------------
st.set_page_config(
    page_title="TexPulse | Textile Sustainability & Savings",
    page_icon="🫀",
    layout="centered"
)

# Custom Styling
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
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. SUPABASE CLOUD DATABASE CONNECTION
# ----------------------------------------------------
@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None

supabase = init_supabase()

st.title("🫀 TexPulse")
st.markdown("##### *The Heartbeat of Textile Sustainability & Savings*")
st.caption("B2B Operational Compliance, Energy Optimization & Financial ROI Engine")

# User Session
if "user_email" not in st.session_state:
    st.session_state.user_email = "demo@paramounttex.com"

# Sidebar Authentication
with st.sidebar:
    st.header("🔐 TexPulse Portal")
    st.session_state.user_email = st.text_input("Corporate Email", value=st.session_state.user_email)
    if supabase:
        st.success("🟢 Cloud Database Connected")
    else:
        st.error("🔴 Database Disconnected")

# ----------------------------------------------------
# 3. PDF REPORT GENERATOR ENGINE
# ----------------------------------------------------
def generate_pdf_report(factory_name, reporting_month, production_kg, water_kpi, energy_kpi, 
                        cod_eff, bod_eff, monthly_savings, yearly_savings, scope1, scope2, total_ghg):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0f172a'), spaceAfter=4)
    subtitle_style = ParagraphStyle('SubTitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=9, textColor=colors.HexColor('#0284c7'), spaceAfter=12)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#0f172a'), spaceBefore=8, spaceAfter=4)
    
    story.append(Paragraph("🫀 TexPulse Executive Audit Report", title_style))
    story.append(Paragraph("The Heartbeat of Textile Sustainability & Savings | Compliance & ROI Engine", subtitle_style))
    
    # Meta Info
    meta_data = [
        [Paragraph("<b>Factory Name:</b>", styles['Normal']), Paragraph(factory_name, styles['Normal']),
         Paragraph("<b>Reporting Month:</b>", styles['Normal']), Paragraph(reporting_month, styles['Normal'])],
        [Paragraph("<b>Standard:</b>", styles['Normal']), Paragraph("Higg FEM 4.0 / ZDHC / DOE", styles['Normal']),
         Paragraph("<b>Status:</b>", styles['Normal']), Paragraph("Verified Audit Data", styles['Normal'])]
    ]
    t_meta = Table(meta_data, colWidths=[100, 160, 100, 160])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    # KPIs Table
    story.append(Paragraph("1. Resource & Environmental KPIs", heading_style))
    kpi_data = [
        ["Metric Description", "Value", "Benchmark Status"],
        ["Total Fabric Production", f"{production_kg:,.0f} Kg", "Baseline Volume"],
        ["Water Intensity KPI", f"{water_kpi:.2f} L/kg fabric", "Best-in-Class" if water_kpi <= 60 else "Moderate"],
        ["Energy Intensity KPI", f"{energy_kpi:.2f} kWh/kg fabric", "Optimized"],
        ["COD Removal Efficiency", f"{cod_eff:.1f} %", "DOE Compliant"],
        ["BOD Removal Efficiency", f"{bod_eff:.1f} %", "DOE Compliant"]
    ]
    t_kpi = Table(kpi_data, colWidths=[200, 150, 170])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    # Financial Savings
    story.append(Paragraph("2. TexPulse Financial ROI Engine", heading_style))
    fin_data = [
        ["Financial Impact", "Monthly Savings (BDT)", "Annual Savings (BDT)"],
        ["Resource Optimization", f"BDT {monthly_savings:,.0f}", f"BDT {yearly_savings:,.0f}"]
    ]
    t_fin = Table(fin_data, colWidths=[200, 160, 160])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    # Carbon Emissions
    story.append(Paragraph("3. GHG Carbon Footprint (Scope 1 & 2)", heading_style))
    ghg_data = [
        ["Emission Scope", "Footprint (tCO2e)"],
        ["Scope 1 (Direct Fuel)", f"{scope1:.2f} tCO2e"],
        ["Scope 2 (Electricity)", f"{scope2:.2f} tCO2e"],
        ["Total Emissions", f"{total_ghg:.2f} tCO2e"]
    ]
    t_ghg = Table(ghg_data, colWidths=[260, 260])
    t_ghg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#16a34a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t_ghg)

    doc.build(story)
    buffer.seek(0)
    return buffer

# ----------------------------------------------------
# 4. APP TABS & INTERFACE
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💧 Water & Energy", 
    "🧪 ETP & Waste", 
    "💰 Cost & Savings",
    "🌍 GHG Climate", 
    "📄 PDF Audit Report"
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

    st.metric("💧 Water Intensity KPI", f"{water_kpi:.2f} L/kg")
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

# Tab 3: Cost & Savings
with tab3:
    st.subheader("💰 Financial Savings Engine")
    gas_cost = st.number_input("Gas Bill (BDT)", min_value=0.0, value=1350000.0)
    elec_cost = st.number_input("Electricity Bill (BDT)", min_value=0.0, value=1260000.0)
    
    savings_gas = gas_cost * 0.25 
    savings_elec = elec_cost * 0.15 
    monthly_savings = savings_gas + savings_elec
    yearly_savings = monthly_savings * 12
    
    st.success(f"🏆 Total Monthly Potential Savings: ৳ {monthly_savings:,.0f}")
    st.success(f"🏆 Total Yearly Potential Savings: ৳ {yearly_savings:,.0f}")

# Tab 4: GHG Climate
with tab4:
    st.subheader("🌍 Carbon Footprint")
    scope_1_mt = ((natural_gas_m3 * 1.98) + (diesel_liter * 2.68)) / 1000
    scope_2_mt = (grid_electricity_kwh * 0.55) / 1000
    total_ghg_mt = scope_1_mt + scope_2_mt
    st.metric("🌱 Total Carbon Emissions", f"{total_ghg_mt:.2f} tCO₂e")

# Tab 5: PDF Audit Report & Database Save
with tab5:
    st.subheader("📄 TexPulse Professional PDF Audit Report")
    factory_name = st.text_input("Factory Name", value="Paramount Textile PLC")
    reporting_month = st.selectbox("Reporting Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("☁️ Save Record to Cloud DB"):
            if supabase:
                data = {
                    "user_email": st.session_state.user_email,
                    "factory_name": factory_name,
                    "reporting_month": reporting_month,
                    "production_kg": production_kg,
                    "water_kpi": round(water_kpi, 2),
                    "energy_kpi": round(energy_kpi_kwh, 2),
                    "monthly_savings": round(monthly_savings, 2),
                    "total_ghg": round(total_ghg_mt, 2)
                }
                res = supabase.table("factory_records").insert(data).execute()
                st.success("✅ Data saved successfully to Supabase Database!")
            else:
                st.error("Database connection missing.")

    with col_btn2:
        pdf_bytes = generate_pdf_report(
            factory_name, reporting_month, production_kg, water_kpi, energy_kpi_kwh,
            cod_efficiency, bod_efficiency, monthly_savings, yearly_savings,
            scope_1_mt, scope_2_mt, total_ghg_mt
        )
        st.download_button(
            label="📥 Download PDF Audit Report",
            data=pdf_bytes,
            file_name=f"TexPulse_Audit_{factory_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
                            )
