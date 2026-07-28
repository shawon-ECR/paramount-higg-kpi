import streamlit as st
import io
import pandas as pd
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
    layout="wide"
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
        url = st.secrets["SUPABASE_URL"].strip()
        key = st.secrets["SUPABASE_KEY"].strip()
        return create_client(url, key)
    except Exception as e:
        st.error(f"Database Connection Setup Error: {e}")
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
# 3. HIGG FEM & ZDHC SCORING ENGINE
# ----------------------------------------------------
def calculate_compliance_scores(water_kpi, energy_kpi, cod_eff, bod_eff):
    if water_kpi <= 50:
        water_level = "Level 3 (World Class)"
        water_score = 100
    elif water_kpi <= 80:
        water_level = "Level 2 (Good Practice)"
        water_score = 70
    else:
        water_level = "Level 1 (Baseline / Action Needed)"
        water_score = 40

    if energy_kpi <= 2.5:
        energy_level = "Level 3 (Highly Efficient)"
        energy_score = 100
    elif energy_kpi <= 4.0:
        energy_level = "Level 2 (Moderate Efficiency)"
        energy_score = 70
    else:
        energy_level = "Level 1 (High Consumption)"
        energy_score = 40

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
    
    if overall_score >= 85:
        overall_badge = "🟢 Gold / High Compliance"
    elif overall_score >= 65:
        overall_badge = "🟡 Silver / Satisfactory"
    else:
        overall_badge = "🔴 Bronze / Action Required"

    return {
        "water_level": water_level,
        "water_score": water_score,
        "energy_level": energy_level,
        "energy_score": energy_score,
        "etp_status": etp_status,
        "etp_score": etp_score,
        "overall_score": overall_score,
        "overall_badge": overall_badge
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
    story.append(Paragraph("The Heartbeat of Textile Sustainability & Savings | Compliance & ROI Engine", subtitle_style))
    
    meta_data = [
        [Paragraph("<b>Factory Name:</b>", styles['Normal']), Paragraph(factory_name, styles['Normal']),
         Paragraph("<b>Reporting Month:</b>", styles['Normal']), Paragraph(reporting_month, styles['Normal'])],
        [Paragraph("<b>Standard:</b>", styles['Normal']), Paragraph("Higg FEM 4.0 / ZDHC / DOE", styles['Normal']),
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

    story.append(Paragraph("2. Resource & Environmental KPIs", heading_style))
    kpi_data = [
        ["Metric Description", "Value", "Benchmark Status"],
        ["Total Fabric Production", f"{production_kg:,.0f} Kg", "Baseline Volume"],
        ["Water Intensity KPI", f"{water_kpi:.2f} L/kg fabric", comp_data['water_level']],
        ["Energy Intensity KPI", f"{energy_kpi:.2f} kWh/kg fabric", comp_data['energy_level']],
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

    story.append(Paragraph("3. TexPulse Financial ROI Engine", heading_style))
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

    story.append(Paragraph("4. GHG Carbon Footprint (Scope 1 & 2)", heading_style))
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
# 5. APP TABS & INTERFACE
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💧 Water & Energy", 
    "🧪 ETP & Waste", 
    "💰 Cost & Savings",
    "🌍 GHG Climate", 
    "🏆 Higg FEM Audit Report",
    "📊 Historical Analytics",
    "🧮 What-If ROI Calculator"
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

# Calculate Compliance Data
comp_data = calculate_compliance_scores(water_kpi, energy_kpi_kwh, cod_efficiency, bod_efficiency)

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

# Tab 5: PDF Audit Report & Higg FEM Scorecard
with tab5:
    st.subheader("🏆 Higg FEM 4.0 & ZDHC Compliance Audit Center")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.metric("Higg Overall Score", f"{comp_data['overall_score']} / 100", comp_data['overall_badge'])
    with sc2:
        st.metric("Water Rating", comp_data['water_level'].split()[0], f"{comp_data['water_score']} pts")
    with sc3:
        st.metric("Energy Rating", comp_data['energy_level'].split()[0], f"{comp_data['energy_score']} pts")
    with sc4:
        st.metric("Wastewater Status", comp_data['etp_status'].split()[0], f"{comp_data['etp_score']} pts")

    st.divider()

    factory_name = st.text_input("Factory Name", value="Paramount Textile PLC")
    reporting_month = st.selectbox("Reporting Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("☁️ Save Record to Cloud DB"):
            if supabase:
                try:
                    data = {
                        "user_email": st.session_state.user_email,
                        "factory_name": factory_name,
                        "reporting_month": reporting_month,
                        "production_kg": float(production_kg),
                        "water_kpi": round(float(water_kpi), 2),
                        "energy_kpi": round(float(energy_kpi_kwh), 2),
                        "monthly_savings": round(float(monthly_savings), 2),
                        "total_ghg": round(float(total_ghg_mt), 2)
                    }
                    res = supabase.table("factory_records").insert(data).execute()
                    st.success("✅ Data saved successfully to Supabase Database!")
                except Exception as e:
                    st.error(f"❌ DB Insert Error: {e}")
            else:
                st.error("Database Connection Missing.")

    with col_btn2:
        pdf_bytes = generate_pdf_report(
            factory_name, reporting_month, production_kg, water_kpi, energy_kpi_kwh,
            cod_efficiency, bod_efficiency, monthly_savings, yearly_savings,
            scope_1_mt, scope_2_mt, total_ghg_mt, comp_data
        )
        st.download_button(
            label="📥 Download Higg FEM PDF Audit Report",
            data=pdf_bytes,
            file_name=f"TexPulse_HiggAudit_{factory_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

# Tab 6: Historical Analytics
with tab6:
    st.subheader("📊 Historical Analytics & Performance Dashboard")
    st.caption("Live data retrieved directly from Supabase Cloud Database")

    if not supabase:
        st.error("🔴 Database Disconnected. Please configure Streamlit Secrets.")
    else:
        try:
            response = supabase.table("factory_records").select("*").order("id", desc=False).execute()
            records = response.data

            if not records:
                st.info("ℹ️ No historical records found in the database. Save some records first!")
            else:
                df = pd.DataFrame(records)

                factories = ["All Factories"] + list(df["factory_name"].unique())
                selected_factory = st.selectbox("🏢 Filter by Factory", factories)

                if selected_factory != "All Factories":
                    filtered_df = df[df["factory_name"] == selected_factory]
                else:
                    filtered_df = df.copy()

                st.markdown("### 📈 Executive Summary")
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    st.metric("Total Records Logged", f"{len(filtered_df)}")
                with m2:
                    avg_water = filtered_df["water_kpi"].mean() if "water_kpi" in filtered_df else 0
                    st.metric("💧 Avg Water KPI", f"{avg_water:.2f} L/kg")
                with m3:
                    tot_savings = filtered_df["monthly_savings"].sum() if "monthly_savings" in filtered_df else 0
                    st.metric("💰 Total Savings Logged", f"৳ {tot_savings:,.0f}")
                with m4:
                    tot_ghg = filtered_df["total_ghg"].sum() if "total_ghg" in filtered_df else 0
                    st.metric("🌱 Total GHG Emissions", f"{tot_ghg:.2f} tCO₂e")

                st.divider()

                st.markdown("### 📉 Resource & Performance Trends")
                c_chart1, c_chart2 = st.columns(2)
                
                with c_chart1:
                    st.markdown("#### 💧 Water KPI Trend (L/kg fabric)")
                    if "reporting_month" in filtered_df and "water_kpi" in filtered_df:
                        chart_water = filtered_df[["reporting_month", "water_kpi"]].set_index("reporting_month")
                        st.line_chart(chart_water)

                with c_chart2:
                    st.markdown("#### ⚡ Energy KPI Trend (kWh/kg fabric)")
                    if "reporting_month" in filtered_df and "energy_kpi" in filtered_df:
                        chart_energy = filtered_df[["reporting_month", "energy_kpi"]].set_index("reporting_month")
                        st.line_chart(chart_energy)

                st.divider()

                st.markdown("### 📋 Historical Audit Data Table")
                display_cols = ["id", "factory_name", "reporting_month", "production_kg", "water_kpi", "energy_kpi", "monthly_savings", "total_ghg", "user_email"]
                available_cols = [c for c in display_cols if c in filtered_df.columns]
                
                st.dataframe(filtered_df[available_cols], use_container_width=True)

                csv_data = filtered_df[available_cols].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Historical Data to CSV",
                    data=csv_data,
                    file_name="TexPulse_Historical_Analytics.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"❌ Error loading analytics: {e}")

# Tab 7: What-If ROI & Payback Calculator
with tab7:
    st.subheader("🧮 What-If Green Technology ROI & Payback Calculator")
    st.caption("Simulate payback periods and financial returns on sustainability investments")

    # Technology Presets
    preset = st.selectbox(
        "💡 Select Green Technology Preset (or Custom Input)",
        [
            "Custom Calculation",
            "☀️ Rooftop Solar System (500 kWp)",
            "♨️ Boiler Economizer & Waste Heat Recovery",
            "💧 RO Water Recycling Plant",
            "⚡ Variable Frequency Drives (VFD) Setup"
        ]
    )

    # Set default values based on preset
    def_capex = 4500000.0
    def_monthly_sav = 180000.0
    def_maint = 50000.0
    def_years = 10

    if preset == "☀️ Rooftop Solar System (500 kWp)":
        def_capex = 35000000.0
        def_monthly_sav = 550000.0
        def_maint = 200000.0
        def_years = 15
    elif preset == "♨️ Boiler Economizer & Waste Heat Recovery":
        def_capex = 4500000.0
        def_monthly_sav = 180000.0
        def_maint = 50000.0
        def_years = 8
    elif preset == "💧 RO Water Recycling Plant":
        def_capex = 8000000.0
        def_monthly_sav = 280000.0
        def_maint = 120000.0
        def_years = 10
    elif preset == "⚡ Variable Frequency Drives (VFD) Setup":
        def_capex = 2500000.0
        def_monthly_sav = 90000.0
        def_maint = 30000.0
        def_years = 7

    st.markdown("### 📥 Investment & Savings Inputs")
    col_roi1, col_roi2 = st.columns(2)
    with col_roi1:
        capex = st.number_input("Capital Investment / Equipment Cost (CAPEX in BDT)", min_value=1000.0, value=def_capex, step=100000.0)
        monthly_sav = st.number_input("Estimated Monthly Operational Savings (BDT)", min_value=0.0, value=def_monthly_sav, step=10000.0)
    with col_roi2:
        annual_maint = st.number_input("Annual Maintenance Cost (BDT)", min_value=0.0, value=def_maint, step=10000.0)
        project_lifetime = st.slider("Project Lifetime (Years)", min_value=1, max_value=20, value=def_years)

    # Financial Calculations
    annual_gross_sav = monthly_sav * 12
    annual_net_sav = annual_gross_sav - annual_maint

    st.divider()

    if annual_net_sav > 0:
        payback_years = capex / annual_net_sav
        payback_months = payback_years * 12
        annual_roi = (annual_net_sav / capex) * 100
        total_lifetime_profit = (annual_net_sav * project_lifetime) - capex

        st.markdown("### 🎯 Investment Return Summary")
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Payback Period", f"{payback_months:.1f} Months", f"{payback_years:.1f} Years")
        with r2:
            st.metric("Annual ROI (%)", f"{annual_roi:.1f} %")
        with r3:
            st.metric("Annual Net Savings", f"৳ {annual_net_sav:,.0f}")
        with r4:
            st.metric("Net Lifetime Profit", f"৳ {total_lifetime_profit:,.0f}")

        st.divider()

        # Cumulative Cash Flow Line Chart
        st.markdown("### 📈 Cumulative Cash Flow & Break-Even Timeline")
        
        cash_flow_list = []
        cum_cash = -capex
        cash_flow_list.append({"Year": "Year 0 (CAPEX)", "Cumulative Cashflow (BDT)": cum_cash})

        for y in range(1, project_lifetime + 1):
            cum_cash += annual_net_sav
            cash_flow_list.append({"Year": f"Year {y}", "Cumulative Cashflow (BDT)": cum_cash})

        df_cf = pd.DataFrame(cash_flow_list).set_index("Year")
        st.line_chart(df_cf)

        if payback_years <= project_lifetime:
            st.success(f"✅ **Highly Viable Investment!** The technology pays for itself in **{payback_months:.1f} months** ({payback_years:.1f} years). Total net profit over {project_lifetime} years will be **৳ {total_lifetime_profit:,.0f}**.")
        else:
            st.warning(f"⚠️ **Long Payback Notice:** Payback period ({payback_years:.1f} years) exceeds project lifetime ({project_lifetime} years).")
    else:
        st.error("❌ Annual maintenance cost is higher than or equal to annual savings. Negative or zero financial return.")
