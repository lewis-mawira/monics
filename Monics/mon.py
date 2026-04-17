import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import os
import io
import base64
import uuid

# ════════════════════════════════════════════════════════════════
#  PAGE CONFIG  — must be first Streamlit call
# ════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Special Stars Ventures | Billing OS",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════
#  BRAND PALETTE
# ════════════════════════════════════════════════════════════════
BLUE     = "#1A4DA1"
BLUE2    = "#1565C0"
GREEN    = "#4CAF50"
GREEN2   = "#2E7D32"
LGRAY    = "#EEF3FC"
WHITE    = "#FFFFFF"
BLACK    = "#111111"
ACCENT   = "#FFC107"
RED      = "#E53935"
DARK_BG  = "#0D1B3E"
STAR_GOLD= "#FFD700"

# ════════════════════════════════════════════════════════════════
#  LOGO  — JPEG embedded as base64. No file reading required.
#  To update: replace the string below with a new base64 JPEG.
# ════════════════════════════════════════════════════════════════
LOGO_B64 = "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4b9D6EE3hAFCskqW4zyBj1/c8MpMgDsdrSXaHnAPnonuJ7ABzamIAaLn1cY76GpmHsLzGHjraA4t33AO9HX8j/cVGeTcXrcywS72G01IprpJC2ptdQXaEFwge2allP0bPHE4j3AIQEoVIbtbW3ZtidWRivfTmrbTns50IcGuePmA5zQdenU3fqFasAy+jz7C7NmVFCYGXajjqHwOdt1PKRqSF378bw5jvk5pVHk12o7NnGG+dYW1M97mrrJDcPO6XUfVTOrHM6NfG2QUHc7GjG35oCWLHXh16v8AIRgRd6usFG7++IFZFUB8P8flcFceN2D1Yva39v3qWM//ABQjiTh9bRx1kVufVwtq54pJooDIBI+NhYHva31LWmSMEjsC9u/UL2UZguGPXTkertooXuveN2aGT70XfAymuE0nVEAD+IutrHO2Ow6NHuV+8kZkzAMJumVCifXVNLG2Ohomb66ysle2Kmp26BO5JnxsB126toSRrf8AlB5e1/WWLjnufds99qIf9v3ell/h1Vn7UfbJSi3GeHS4LhdvsFdWNrbmfMrLtWga++XCd5lqZvQdnSveQPZvSPQKUoAiIgCKjtF5tN/oW3OyXGmr6N8kkTZ6eQSRudG90bwHDsdPY5p+oKrEAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREARFZ8qyu04ba/01fRWNoGSBk89PSS1Ap26J8yQRtc5sY1ov10t2C4gbIAvCKktV3tV+t0F4sdzpLjQVTPMgqqSZs0Mrfm17SWuH1BVWgCIiAgGZYdfLbe38lcaxRf0gEbI7papJBFT5BTMHwxvce0dSwb8qc+n4H7YdskuIZdZs3scV+skkoje58M0FRGYqiknYemSCaM945WOBa5p9CPcaKvSh2QYzcbTeps8wmma+5ysa262wPbHHeImDTTt2msqmNGo5CQHNAjkIb0PhAqckstHbLpLyXRW241l3tdpqKV1Hb3M67lT7ErYC13Z72vaTH3aQZHjYD3A3mw3205PZaHIrDWsrLdcqdlTSzsBAkjeNtOiAR2PoQCD2IBXxj2RWnKbVFeLNUGWCQuY5r2GOSGVhLXxSMcA6ORjgWuY4BzXAggEKIU//ANGuafcDtmLZfVukp3ukAZbbxIS58QB/DFVHqe32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EREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAEREAREQBERAf//Z"
LOGO_SRC = f"data:image/jpeg;base64,{LOGO_B64}"

# ════════════════════════════════════════════════════════════════
#  TIMEZONE
# ════════════════════════════════════════════════════════════════
EAT = pytz.timezone("Africa/Nairobi")
def now_eat():
    return datetime.now(EAT).replace(tzinfo=None)

def fmt(amount):
    return f"KES {amount:,.0f}"

# ════════════════════════════════════════════════════════════════
#  DATABASE
# ════════════════════════════════════════════════════════════════
DB = "special_stars.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS inventory
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category_id INTEGER,
                  item_name TEXT NOT NULL,
                  buying_price REAL DEFAULT 0,
                  selling_price REAL DEFAULT 0,
                  quantity REAL DEFAULT 0,
                  FOREIGN KEY(category_id) REFERENCES categories(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  item_name TEXT, category TEXT,
                  qty REAL DEFAULT 1,
                  unit_sold TEXT DEFAULT 'Unit',
                  unit_price REAL, total REAL, profit REAL,
                  payment_method TEXT DEFAULT 'Cash')""")
    c.execute("""CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  category TEXT, amount REAL, description TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS activity_log
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  action_type TEXT, description TEXT,
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

init_db()

def run_query(sql, params=()):
    conn = get_conn()
    try:
        df = pd.read_sql(sql, conn, params=params)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def run_write(sql, params=()):
    conn = get_conn()
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()

def run_write_many(ops):
    conn = get_conn()
    try:
        c = conn.cursor()
        for sql, params in ops:
            c.execute(sql, params)
        conn.commit()
    finally:
        conn.close()

def log_activity(action_type, description):
    run_write(
        "INSERT INTO activity_log (action_type, description, timestamp) VALUES (?,?,?)",
        (action_type, description, now_eat()),
    )

def fmt(amount):
    return f"KES {amount:,.0f}"

# ════════════════════════════════════════════════════════════════
#  PDF RECEIPT  — robust, no silent failures, unique style names
# ════════════════════════════════════════════════════════════════
def build_pdf_receipt(items, payment_method, receipt_no=None):
    """
    Build a branded A6 PDF receipt. Returns bytes on success, raises on failure.
    Uses uuid-suffixed ParagraphStyle names to prevent ReportLab registry clashes.
    """
    from reportlab.lib.pagesizes import A6
    from reportlab.lib import colors
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, HRFlowable, Image as RLImage)
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

    # Unique ID for this call — prevents ParagraphStyle name collisions
    uid = uuid.uuid4().hex[:8]

    def ps(name, **kwargs):
        return ParagraphStyle(f"{name}_{uid}", **kwargs)

    brand_blue  = colors.HexColor(BLUE)
    brand_green = colors.HexColor(GREEN)

    # Pre-define all styles with unique names
    st_title  = ps("title",  fontName="Helvetica-Bold",    fontSize=12, textColor=brand_blue,              alignment=TA_CENTER, spaceAfter=1)
    st_tag    = ps("tag",    fontName="Helvetica-Oblique", fontSize=7,  textColor=colors.HexColor("#555"), alignment=TA_CENTER, spaceAfter=2)
    st_addr   = ps("addr",   fontName="Helvetica",         fontSize=7,  textColor=colors.HexColor("#333"), alignment=TA_CENTER, spaceAfter=1)
    st_lbl    = ps("lbl",    fontName="Helvetica-Bold",    fontSize=7.5, textColor=colors.HexColor(DARK_BG), alignment=TA_LEFT)
    st_val    = ps("val",    fontName="Helvetica",         fontSize=7.5, textColor=colors.HexColor(DARK_BG), alignment=TA_RIGHT)
    st_footer = ps("footer", fontName="Helvetica-Oblique", fontSize=6.5, textColor=colors.HexColor("#666"), alignment=TA_CENTER)
    st_tot_l  = ps("totl",   fontName="Helvetica-Bold",    fontSize=10, textColor=colors.white,             alignment=TA_LEFT)
    st_tot_v  = ps("totv",   fontName="Helvetica-Bold",    fontSize=10, textColor=colors.HexColor(ACCENT),  alignment=TA_RIGHT)
    st_hdr    = ps("hdr",    fontName="Helvetica-Bold",    fontSize=7.5, textColor=colors.white,            alignment=TA_CENTER)
    st_hdr_l  = ps("hdrl",   fontName="Helvetica-Bold",    fontSize=7.5, textColor=colors.white,            alignment=TA_LEFT)

    buf   = io.BytesIO()
    doc   = SimpleDocTemplate(buf, pagesize=A6,
                              rightMargin=8*mm, leftMargin=8*mm,
                              topMargin=4*mm,   bottomMargin=4*mm)

    ts  = now_eat().strftime("%d %b %Y  %H:%M:%S")
    rno = receipt_no or f"SSV-{now_eat().strftime('%Y%m%d%H%M%S')}"
    grand_total = sum(i["total"] for i in items)

    story = []

    # ── Logo (optional — skipped gracefully if decode fails)
    try:
        raw = base64.b64decode(LOGO_B64)
        logo_buf = io.BytesIO(raw)
        logo_img = RLImage(logo_buf, width=24*mm, height=24*mm)
        logo_img.hAlign = "CENTER"
        story.append(logo_img)
        story.append(Spacer(1, 2))
    except Exception:
        pass  # Receipt still prints without logo

    # ── Header text
    story.append(Paragraph("SPECIAL STARS VENTURES", st_title))
    story.append(Paragraph('"Uncovering Special Capabilities"', st_tag))
    story.append(Paragraph("Westlands opp Safaricom Center  |  +254 740 143 957", st_addr))
    story.append(Paragraph("info@specialstarsventures.co.ke", st_addr))
    story.append(HRFlowable(width="100%", thickness=2, color=brand_blue, spaceAfter=3))

    # ── Receipt meta
    meta = [
        [Paragraph("Receipt No:", st_lbl), Paragraph(rno, st_val)],
        [Paragraph("Date:",       st_lbl), Paragraph(ts,  st_val)],
        [Paragraph("Payment:",    st_lbl), Paragraph(payment_method, st_val)],
    ]
    t_meta = Table(meta, colWidths=["45%", "55%"])
    t_meta.setStyle(TableStyle([
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)
    story.append(HRFlowable(width="100%", thickness=1, color=brand_green,
                             spaceAfter=3, spaceBefore=3))

    # ── Items table
    col_header = [
        Paragraph("<b>Item</b>",  st_hdr_l),
        Paragraph("<b>Qty</b>",   st_hdr),
        Paragraph("<b>Unit</b>",  st_hdr),
        Paragraph("<b>Total</b>", ps("th_total", fontName="Helvetica-Bold",
                                     fontSize=7.5, textColor=colors.white, alignment=TA_RIGHT)),
    ]
    item_rows = [col_header]
    for n, itm in enumerate(items):
        item_rows.append([
            Paragraph(str(itm["item"]),            ps(f"ri{n}", fontName="Helvetica", fontSize=7.5, alignment=TA_LEFT)),
            Paragraph(str(int(itm["qty"])),         ps(f"rq{n}", fontName="Helvetica", fontSize=7.5, alignment=TA_CENTER)),
            Paragraph(fmt(itm["unit_price"]),        ps(f"ru{n}", fontName="Helvetica", fontSize=7.5, alignment=TA_CENTER)),
            Paragraph(fmt(itm["total"]),             ps(f"rt{n}", fontName="Helvetica", fontSize=7.5, alignment=TA_RIGHT)),
        ])

    t_items = Table(item_rows, colWidths=["44%", "14%", "22%", "20%"])
    t_items.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), brand_blue),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.HexColor("#F0F6FF"), colors.white]),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING",    (0,0), (-1,-1), 3),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
    ]))
    story.append(t_items)
    story.append(Spacer(1, 4))

    # ── Grand total bar
    t_total = Table(
        [[Paragraph("GRAND TOTAL", st_tot_l), Paragraph(fmt(grand_total), st_tot_v)]],
        colWidths=["55%", "45%"]
    )
    t_total.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colors.HexColor(DARK_BG)),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (0,0),   7),
        ("RIGHTPADDING",  (-1,0),(-1,-1), 7),
    ]))
    story.append(t_total)
    story.append(Spacer(1, 5))
    story.append(HRFlowable(width="100%", thickness=1, color=brand_green, spaceAfter=4))
    story.append(Paragraph(
        "Every child has a star inside them. We help them shine bright.", st_footer))
    story.append(Paragraph("www.specialstarsventures.co.ke", st_footer))

    doc.build(story)
    buf.seek(0)
    return buf.read()

# ════════════════════════════════════════════════════════════════
#  RECORD SALE
# ════════════════════════════════════════════════════════════════
def record_basket_sale(basket, method):
    """Record all basket items atomically. Returns (success, errors)."""
    conn = get_conn()
    errors = []
    try:
        c = conn.cursor()
        for entry in basket:
            item_id   = entry["id"]
            item_name = entry["item"]
            category  = entry["category"]
            qty       = entry["qty"]
            sell_price= entry["unit_price"] * qty
            buy_price = entry["buy_price"] * qty

            c.execute("SELECT quantity FROM inventory WHERE id = ?", (item_id,))
            row = c.fetchone()
            if row is None or float(row[0]) < float(qty):
                errors.append(f"⛔ {item_name} has insufficient stock ({row[0] if row else 0} left)")
                continue

            profit = float(sell_price) - float(buy_price)
            c.execute("""INSERT INTO sales
                         (timestamp,item_name,category,qty,unit_sold,unit_price,total,profit,payment_method)
                         VALUES (?,?,?,?,?,?,?,?,?)""",
                      (now_eat(), item_name, category, qty, f"x{qty} Unit",
                       entry["unit_price"], sell_price, profit, method))
            c.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?", (float(qty), item_id))

        conn.commit()
        return True, errors
    except Exception as e:
        conn.rollback()
        return False, [str(e)]
    finally:
        conn.close()

# ════════════════════════════════════════════════════════════════
#  ACTIVITY LOG
# ════════════════════════════════════════════════════════════════
def log_activity(action_type, description):
    run_write(
        "INSERT INTO activity_log (action_type, description, timestamp) VALUES (?,?,?)",
        (action_type, description, now_eat()),
    )

# ════════════════════════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════════════════════════
_defaults = {
    "sale_complete":          False,
    "sale_msg":               "",
    "out_of_stock":           False,
    "vault_unlocked":         False,
    "activity_log_unlocked":  False,
    "receipt_pdf":            None,
    "basket":                 [],
    "inv_toast":              None,
    "confirm_restock":        None,
    "pdf_error":              None,
    "receipts_history":       [],   # list of {rno, ts, label, pdf_bytes}
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ════════════════════════════════════════════════════════════════
_now = now_eat()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
.stApp {{ background: {LGRAY}; }}
[data-testid="stHeader"] {{ display: none !important; }}
#MainMenu, footer, .stDeployButton {{ visibility: hidden; }}
.stApp > .main {{ padding-top: 0 !important; }}
.stMainBlockContainer {{ padding-top: 0 !important; }}
[data-testid="stMainBlockContainer"] {{ padding-top: 0 !important; }}
section[data-testid="stSidebar"] {{ padding-top: 0 !important; top: 0 !important; }}

/* ── TOP BAR ── */
.ssv-topbar {{
    background: linear-gradient(135deg, {DARK_BG} 0%, {BLUE} 100%);
    border-bottom: 4px solid {GREEN};
    position: sticky; top: 0; left: 0; right: 0; z-index: 999;
    padding: 10px 24px 10px 60px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 24px rgba(26,77,161,0.35);
    width: 100%;
}}
.ssv-topbar-title {{
    flex: 1;
    display: flex; justify-content: center; pointer-events: none;
    font-family: 'Nunito', sans-serif;
    font-size: clamp(0.9rem, 2vw, 1.3rem);
    color: {WHITE}; font-weight: 900; letter-spacing: 1px;
    text-transform: uppercase;
}}
.ssv-topbar-title .gs {{ color: {GREEN}; }}
.topbar-spacer {{ height: 0px; }}
.live-dot {{
    width: 9px; height: 9px; background: {GREEN};
    border-radius: 50%; box-shadow: 0 0 10px {GREEN};
    animation: blink 1s linear infinite; flex-shrink: 0;
}}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.live-clock {{
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    color: {ACCENT}; background: rgba(255,255,255,0.1);
    padding: 4px 12px; border: 1px solid rgba(255,255,255,0.2);
    letter-spacing: 1px; white-space: nowrap; border-radius: 20px;
}}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARK_BG} 0%, #0a2060 100%) !important;
    border-right: 4px solid {GREEN};
    padding-top: 0 !important;
}}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 0 !important; }}
[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
[data-testid="stSidebar"] .stRadio label {{
    background: rgba(255,255,255,0.07);
    border-radius: 10px; padding: 11px 14px;
    margin-bottom: 6px; display: block;
    transition: all 0.2s; font-weight: 600;
    border-left: 4px solid transparent; font-size: 0.9rem;
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(76,175,80,0.2);
    border-left-color: {GREEN}; padding-left: 18px;
}}

/* ── STREAMLIT NATIVE SIDEBAR COLLAPSE/EXPAND BUTTON ──
   Target both the collapsed-control and the header button inside sidebar.
   Borrowed from mie.py — forces visibility even when stHeader is hidden. */
/* Sidebar collapse/expand button — show always */
button[data-testid="stSidebarCollapsedControl"] {{
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: fixed !important;
    top: 10px !important;
    left: 10px !important;
    z-index: 10000 !important;
    background: linear-gradient(135deg, {GREEN}, {GREEN2}) !important;
    border: 2px solid rgba(255,255,255,0.4) !important;
    border-radius: 8px !important;
    width: 38px !important;
    height: 38px !important;
    padding: 6px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 16px rgba(76,175,80,0.6) !important;
}}
button[data-testid="stSidebarCollapsedControl"]:hover {{
    background: linear-gradient(135deg, {BLUE}, {BLUE2}) !important;
    transform: scale(1.08) !important;
}}
button[data-testid="stSidebarCollapsedControl"] svg {{
    fill: white !important;
    stroke: white !important;
    width: 20px !important;
    height: 20px !important;
}}
/* Also style the collapse button INSIDE the sidebar */
button[data-testid="stBaseButton-headerNoPadding"] {{
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 8px !important;
    color: white !important;
}}
button[data-testid="stBaseButton-headerNoPadding"] svg {{
    fill: white !important;
    stroke: white !important;
}}
button[data-testid="stBaseButton-headerNoPadding"]:hover {{
    background: rgba(76,175,80,0.4) !important;
}}

/* ── METRIC GRID ── */
.metric-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 14px; margin-bottom: 24px;
}}
.metric-card {{
    background: linear-gradient(135deg, {BLUE} 0%, {BLUE2} 100%) !important;
    border-radius: 14px; padding: 16px 14px;
    box-shadow: 0 4px 20px rgba(26,77,161,0.1); text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    border-top: 4px solid {GREEN}; position: relative; overflow: hidden;
}}
.metric-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 28px rgba(26,77,161,0.18); }}
.metric-card .m-label {{
    font-size: 0.62rem; text-transform: uppercase; color: rgba(255,255,255,0.85) !important;
    letter-spacing: 1.2px; margin-bottom: 6px; font-weight: 700;
}}
.metric-card .m-value {{
    font-family: 'Nunito', sans-serif;
    font-size: clamp(1rem, 3.5vw, 1.7rem);
    color: {WHITE} !important; font-weight: 900; line-height: 1;
}}
.metric-card .m-delta {{ font-size: 0.65rem; color: rgba(255,255,255,0.65) !important; margin-top: 4px; }}
.mc-blue   {{ background: linear-gradient(135deg, {BLUE} 0%, {BLUE2} 100%) !important; border-top-color: {GREEN}; }}
.mc-green  {{ background: linear-gradient(135deg, {GREEN} 0%, {GREEN2} 100%) !important; border-top-color: {ACCENT}; }}
.mc-amber  {{ background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important; border-top-color: rgba(255,255,255,0.4); }}
.mc-dark   {{ background: linear-gradient(135deg, {DARK_BG} 0%, #1a3a6e 100%) !important; border-top-color: {ACCENT}; }}
.mc-red    {{ background: linear-gradient(135deg, {RED} 0%, #C62828 100%) !important; border-top-color: rgba(255,255,255,0.4); }}
.mc-teal   {{ background: linear-gradient(135deg, #00897B 0%, #00695C 100%) !important; border-top-color: {ACCENT}; }}
.mc-purple {{ background: linear-gradient(135deg, #7B1FA2 0%, #4A148C 100%) !important; border-top-color: {GREEN}; }}

/* ── NEO PRODUCT CARDS ── */
.neo-card {{
    background: {WHITE}; border-radius: 12px; padding: 14px 16px;
    box-shadow: 0 3px 14px rgba(26,77,161,0.08); margin-bottom: 14px;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden; border-top: 4px solid {BLUE};
}}
.neo-card::before {{
    content:''; position:absolute; top:0; left:0;
    width:4px; height:100%; background:linear-gradient({GREEN},{BLUE});
}}
.neo-card:hover {{ transform:translateY(-3px); box-shadow: 0 10px 28px rgba(26,77,161,0.16); }}
.nc-cat   {{ color:{GREEN}; font-size:0.62rem; font-weight:800; text-transform:uppercase; letter-spacing:1.5px; }}
.nc-name  {{ font-family:'Nunito',sans-serif; font-size:clamp(0.85rem,2.5vw,1.05rem); font-weight:800; margin:4px 0; color:{BLACK}; }}
.nc-price {{ color:{BLUE}; font-family:'Nunito',sans-serif; font-size:clamp(1rem,3vw,1.35rem); font-weight:900; }}
.nc-stock {{ display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.65rem; font-weight:700; text-transform:uppercase; margin-top:6px; }}
.stock-ok  {{ background:#DCFCE7; color:#166534; }}
.stock-low {{ background:#FEF9C3; color:#713F12; }}
.stock-out {{ background:#FEE2E2; color:#991B1B; }}

/* ── SECTION CARD ── */
.section-card {{
    background:{WHITE}; border-radius:14px; padding:20px 22px;
    box-shadow:0 3px 16px rgba(26,77,161,0.08); margin-bottom:20px;
    border-top:4px solid {BLUE};
}}
.section-title {{
    font-family:'Nunito',sans-serif; font-size:1.05rem;
    color:{BLUE}; font-weight:800; margin-bottom:14px;
    padding-bottom:10px; border-bottom:2px solid {LGRAY};
}}

/* ── BUTTONS ── */
.stButton > button {{
    border-radius:10px !important; font-weight:700 !important;
    font-family:'Poppins',sans-serif !important; transition:all 0.18s !important;
    font-size:0.82rem !important;
    background: linear-gradient(135deg, {BLUE} 0%, {BLUE2} 100%) !important;
    color: {WHITE} !important;
    border: none !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, {GREEN} 0%, {GREEN2} 100%) !important;
    color: {WHITE} !important;
    box-shadow: 0 6px 20px rgba(76,175,80,0.4) !important;
    transform: translateY(-2px) !important;
}}
.stButton > button[kind="primary"] {{
    background:linear-gradient(135deg, {BLUE} 0%, {BLUE2} 100%) !important;
    color:{WHITE} !important; box-shadow: 0 4px 14px rgba(26,77,161,0.35) !important;
}}
.stButton > button[kind="primary"]:hover {{
    background:linear-gradient(135deg, {GREEN} 0%, {GREEN2} 100%) !important;
    box-shadow: 0 6px 20px rgba(76,175,80,0.4) !important; transform: translateY(-2px) !important;
}}
.sell-btn > button {{
    background:linear-gradient(135deg, {GREEN} 0%, {GREEN2} 100%) !important;
    color:{WHITE} !important; font-weight:900 !important;
    box-shadow: 0 4px 14px rgba(76,175,80,0.35) !important;
    border-radius:10px !important; border: none !important;
}}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{
    gap:4px; background:rgba(26,77,161,0.07); padding:5px; border-radius:12px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius:9px; font-weight:700; padding:8px 18px; color:#555; font-size:0.82rem;
}}
.stTabs [aria-selected="true"] {{
    background:{BLUE} !important; color:{WHITE} !important;
    box-shadow:0 3px 10px rgba(26,77,161,0.25);
}}

/* ── LOW STOCK ── */
.low-stock {{
    background:linear-gradient(135deg,#FEF2F2,#FFF5F5);
    border-left:5px solid {RED}; color:#991B1B;
    padding:8px 14px; font-size:0.82rem; font-weight:700;
    margin-bottom:6px; border-radius:0 10px 10px 0;
}}

/* ── EOD CARD ── */
.eod-card {{
    background:linear-gradient(135deg, {DARK_BG} 0%, {BLUE} 100%);
    color:{WHITE}; border-radius:16px; padding:22px;
    box-shadow:0 8px 32px rgba(26,77,161,0.3); margin-bottom:20px;
}}
.eod-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:14px; }}
.eod-cell {{ border-top:1px solid rgba(255,255,255,0.15); padding-top:10px; }}
.eod-cell p {{ margin:0; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.6); }}
.eod-cell h2 {{ margin:4px 0 0; font-family:'Nunito',sans-serif; font-size:clamp(1.1rem,3.5vw,1.8rem); font-weight:900; }}

/* ── ACTIVITY LOG ── */
.act-entry {{
    background:#0f2345; border-left:4px solid; padding:10px 16px;
    margin-bottom:8px; border-radius:0 10px 10px 0;
    display:flex; gap:12px; align-items:flex-start;
}}

/* ── PAGE HEADER ── */
.page-header {{
    font-family: 'Nunito', sans-serif; font-size: clamp(1.3rem, 4vw, 2rem);
    font-weight: 900; color: {BLUE}; margin-bottom: 18px; text-align: center;
    padding: 10px 0; border-bottom: 3px solid {GREEN};
}}
.page-subtitle {{
    text-align: center; color: #888; font-size: 0.82rem;
    margin-top: -12px; margin-bottom: 20px;
}}

/* ── INSIGHT CARD ── */
.insight-card {{
    background:{WHITE}; border-radius:12px; padding:16px;
    box-shadow:0 3px 14px rgba(26,77,161,0.08);
    border-left:5px solid {GREEN}; margin-bottom:12px;
}}
.insight-title {{ font-weight:700; color:{BLUE}; font-size:0.85rem; margin-bottom:4px; }}
.insight-val {{ font-family:'Nunito',sans-serif; font-size:1.3rem; font-weight:900; color:{DARK_BG}; }}
.insight-sub {{ font-size:0.72rem; color:#888; margin-top:2px; }}

/* ── HOVER EFFECTS ── */
.stButton > button:active {{ transform: scale(0.97) !important; }}
.stSelectbox > div:hover {{ border-color: {BLUE} !important; }}
[data-testid="stSidebar"] .stRadio label:active {{
    background: rgba(76,175,80,0.35) !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    background: rgba(26,77,161,0.1) !important;
    color: {BLUE} !important;
}}
.stDownloadButton > button {{
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: all 0.18s !important;
}}
.stDownloadButton > button:hover {{
    background: linear-gradient(135deg, {GREEN}, {GREEN2}) !important;
    color: white !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(76,175,80,0.4) !important;
}}
.stExpander > details > summary {{
    border-radius: 10px !important;
    padding: 10px 14px !important;
    transition: all 0.18s !important;
    font-weight: 600 !important;
}}
.stExpander > details > summary:hover {{
    background: rgba(26,77,161,0.07) !important;
    border-color: {BLUE} !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {BLUE} !important;
    box-shadow: 0 0 0 2px rgba(26,77,161,0.15) !important;
}}
.stNumberInput > div > div > input:focus {{
    border-color: {BLUE} !important;
    box-shadow: 0 0 0 2px rgba(26,77,161,0.15) !important;
}}
.sell-btn > button:hover {{
    background: linear-gradient(135deg, #43A047, #1B5E20) !important;
    box-shadow: 0 8px 24px rgba(76,175,80,0.5) !important;
    transform: translateY(-3px) !important;
}}
.neo-card:hover .nc-name {{ color: {BLUE}; }}
.neo-card:hover .nc-price {{ color: {GREEN}; }}
.stPopover button:hover {{
    background: linear-gradient(135deg, {BLUE}, {BLUE2}) !important;
    color: white !important;
}}

/* ── FOOTER ── */
.ssv-footer {{
    background:linear-gradient(135deg, {DARK_BG} 0%, #0a2060 100%);
    border-top:4px solid {GREEN}; padding:18px 20px;
    margin-top:40px; text-align:center;
}}

/* ── SIDEBAR BRAND ── */
.sidebar-brand {{
    background: linear-gradient(180deg, rgba(76,175,80,0.15) 0%, transparent 100%);
    padding: 16px 12px 10px; text-align: center;
    border-bottom: 2px solid rgba(76,175,80,0.3); margin-bottom: 10px;
}}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  TOPBAR  — centred title, live clock, no custom toggle button
# ════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="ssv-topbar" id="ssv-topbar">
    <div class="ssv-topbar-title">
        Special Stars <span class="gs">Ventures</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;z-index:1;">
        <div class="live-dot"></div>
        <div class="live-clock" id="ssv-clock">{_now.strftime('%d %b %Y | %H:%M:%S')}</div>
    </div>
</div>
<div class="topbar-spacer"></div>
<script>
(function(){{
    function pad(n){{return String(n).padStart(2,'0');}}
    var mo=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    function tick(){{
        var el=document.getElementById('ssv-clock');
        if(!el)return;
        var d=new Date();
        el.textContent=pad(d.getDate())+' '+mo[d.getMonth()]+' '+d.getFullYear()+
                       ' | '+pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());
    }}
    setInterval(tick,1000); tick();
}})();
</script>
""", unsafe_allow_html=True)

# ── SIDEBAR TOGGLE — adapted from mie.py (confirmed working) ──────────────────
# Strategy:
#   1. Look for stSidebarCollapsedControl (exists when sidebar is COLLAPSED) → style it, remove custom btn
#   2. Look for stBaseButton-headerNoPadding (exists when sidebar is EXPANDED) → inject custom btn that clicks it
#   3. Poll every 800ms so state changes are caught immediately
import streamlit.components.v1 as _comps
_comps.html("""<script>
(function() {
  function ensureSidebarToggle() {
    var doc = window.parent.document;

    // ── Sidebar is COLLAPSED: native expand button is in the main page ──
    var native = doc.querySelector('button[data-testid="stSidebarCollapsedControl"]');
    if (native) {
      native.style.cssText = [
        'display:flex!important','visibility:visible!important','opacity:1!important',
        'position:fixed!important','top:12px!important','left:12px!important',
        'z-index:10100!important','width:36px!important','height:36px!important',
        'border-radius:8px!important','cursor:pointer!important','padding:6px!important',
        'align-items:center!important','justify-content:center!important',
        'background:linear-gradient(135deg,#4CAF50,#2E7D32)!important',
        'border:2px solid rgba(255,255,255,0.35)!important',
        'box-shadow:0 4px 16px rgba(76,175,80,0.55)!important'
      ].join(';');
      native.querySelectorAll('svg').forEach(function(s) {
        s.style.fill = 'white';
        s.style.stroke = 'white';
        s.style.width = '18px';
        s.style.height = '18px';
      });
      // Remove injected custom button — native one is now visible
      var old = doc.getElementById('ssv-sidebar-toggle');
      if (old) old.remove();
      return;
    }

    // ── Sidebar is EXPANDED: inject a custom button that triggers the native collapse ──
    if (!doc.getElementById('ssv-sidebar-toggle')) {
      var btn = doc.createElement('button');
      btn.id = 'ssv-sidebar-toggle';
      btn.title = 'Hide sidebar';
      btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18"><path fill="white" d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>';
      btn.style.cssText = [
        'position:fixed','top:12px','left:12px','z-index:10100',
        'width:36px','height:36px','border-radius:8px',
        'border:2px solid rgba(255,255,255,0.35)',
        'background:linear-gradient(135deg,#4CAF50,#2E7D32)',
        'cursor:pointer','display:flex','align-items:center','justify-content:center',
        'padding:6px','box-shadow:0 4px 16px rgba(76,175,80,0.55)'
      ].join(';');
      btn.onmouseover = function() { this.style.background = 'linear-gradient(135deg,#1A4DA1,#1565C0)'; };
      btn.onmouseout  = function() { this.style.background = 'linear-gradient(135deg,#4CAF50,#2E7D32)'; };
      btn.onclick = function() {
        // Click Streamlit's native collapse button inside the sidebar header
        var inner = doc.querySelector('button[data-testid="stBaseButton-headerNoPadding"]');
        if (!inner) inner = doc.querySelector('[data-testid="stSidebar"] button');
        if (inner) { inner.click(); return; }
        // Absolute last resort
        var sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) sidebar.style.display = 'none';
      };
      doc.body.appendChild(btn);
    }

    // Keep polling — sidebar state will change and we need to react
    setTimeout(ensureSidebarToggle, 800);
  }

  setTimeout(ensureSidebarToggle, 300);
})();
</script>""", height=0, scrolling=False)

# ════════════════════════════════════════════════════════════════
#  OUT-OF-STOCK POPUP
# ════════════════════════════════════════════════════════════════
if st.session_state.out_of_stock:
    st.markdown('<div style="position:fixed;top:-9999px;opacity:0;pointer-events:none;">', unsafe_allow_html=True)
    _oos_close = st.button("__CLOSE_OOS__", key="close_oos_hidden")
    st.markdown('</div>', unsafe_allow_html=True)
    if _oos_close:
        st.session_state.out_of_stock = False
        st.rerun()
    components.html(f"""<!DOCTYPE html><html><head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@900&display=swap');
    *{{margin:0;padding:0;box-sizing:border-box;}}
    body{{background:{RED};font-family:'Nunito',sans-serif;display:flex;flex-direction:column;
         justify-content:center;align-items:center;width:100vw;height:100vh;
         text-align:center;padding:20px;overflow:hidden;}}
    .x-btn{{position:fixed;top:20px;right:20px;width:56px;height:56px;background:{BLACK};
             color:{WHITE};border:3px solid {WHITE};font-size:1.6rem;font-weight:900;
             border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;}}
    .big{{font-size:clamp(3rem,14vw,8rem);color:{WHITE};font-weight:900;line-height:0.9;
          text-shadow:6px 6px 0 rgba(0,0,0,0.2);}}
    .sub{{font-size:clamp(0.9rem,3vw,1.6rem);color:{WHITE};background:rgba(0,0,0,0.3);
          padding:10px 22px;margin-top:18px;max-width:90vw;word-break:break-word;border-radius:8px;}}
    .btn{{margin-top:32px;background:{WHITE};color:{RED};border:none;
          font-size:clamp(0.9rem,3vw,1.2rem);font-family:'Nunito',sans-serif;
          font-weight:900;text-transform:uppercase;padding:14px 30px;cursor:pointer;
          border-radius:50px;box-shadow:0 6px 24px rgba(0,0,0,0.2);}}
    </style></head><body>
    <button class="x-btn" onclick="doClose()">✕</button>
    <div class="big">OUT OF<br>STOCK!</div>
    <div class="sub">Please restock in Admin Vault</div>
    <button class="btn" onclick="doClose()">✖ CLOSE</button>
    <script>
    function doClose(){{
        var btns=window.parent.document.querySelectorAll('button');
        for(var i=0;i<btns.length;i++){{
            if(btns[i].innerText==='__CLOSE_OOS__'){{btns[i].click();return;}}
        }}
        window.parent.location.reload();
    }}
    </script></body></html>""", height=700, scrolling=False)
    st.stop()

# ════════════════════════════════════════════════════════════════
#  SOLD! POPUP + PDF DOWNLOAD
#
#  ARCHITECTURE:
#  The popup runs inside components.html (a real sandboxed iframe).
#  PDF bytes are stored in session_state, base64-encoded, then
#  embedded directly into the iframe HTML as a JS variable.
#  Download uses a data: URI anchor click — works in sandboxed iframes.
#  Close button sends postMessage to parent window.
#  A st.markdown <script> in the main page listens and clicks the
#  hidden Streamlit button to trigger st.rerun().
#
#  NOTE: st.markdown <script> tags DO run in the main page window
#  (not sandboxed), so postMessage communication works correctly.
# ════════════════════════════════════════════════════════════════
if st.session_state.sale_complete:
    _msg_display = (st.session_state.sale_msg
                    .replace("\n", " | ").replace("<", "").replace(">", ""))
    _ts = now_eat().strftime("%Y%m%d_%H%M%S")

    # ── SOLD banner — pure Streamlit, no iframe, no postMessage issues ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4CAF50 0%,#2E7D32 100%);
         border-radius:18px;padding:36px 28px;text-align:center;
         box-shadow:0 12px 40px rgba(76,175,80,0.4);margin-bottom:20px;">
        <div style="font-family:'Nunito',sans-serif;
             font-size:clamp(3rem,12vw,7rem);font-weight:900;color:white;
             line-height:0.85;text-shadow:4px 4px 0 rgba(0,0,0,0.15);
             letter-spacing:-2px;">SOLD!</div>
        <div style="font-size:2rem;margin:12px 0;letter-spacing:10px;">⭐ ⭐ ⭐</div>
        <div style="font-family:'Poppins',sans-serif;font-size:0.95rem;
             color:white;background:rgba(0,0,0,0.22);padding:12px 22px;
             margin:14px auto;max-width:640px;border-radius:10px;
             line-height:1.6;word-break:break-word;">{_msg_display}</div>
        <div style="color:rgba(255,255,255,0.95);font-size:0.92rem;
             font-weight:700;margin-top:10px;">✅ STOCK &amp; DATABASE UPDATED</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.pdf_error:
        st.error(f"⚠️ PDF generation error: {st.session_state.pdf_error}")

    # ── Native Streamlit buttons — reliable on all browsers/OS ──
    _btn_col1, _btn_col2 = st.columns(2)
    with _btn_col1:
        if st.session_state.receipt_pdf:
            st.download_button(
                label="⬇️ Download Receipt PDF",
                data=st.session_state.receipt_pdf,
                file_name=f"SSV-Receipt-{_ts}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
                key="sale_pdf_download",
            )
        else:
            st.info("PDF not available for this sale.")
    with _btn_col2:
        _done_key = "close_sale_done"
        if st.button("✅ Done — Next Transaction", use_container_width=True, key=_done_key):
            st.session_state.sale_complete = False
            st.session_state.basket = []
            st.session_state.receipt_pdf = None
            st.session_state.pdf_error = None
            st.rerun()

    st.info("📄 Receipt also saved in **Analytics Hub → Receipts** tab.")
    st.stop()

# ════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo at top
    st.markdown(
        f'<div class="sidebar-brand">'
        f'<img src="{LOGO_SRC}" alt="Special Stars Ventures"'
        f' style="width:120px;height:120px;object-fit:contain;display:block;margin:0 auto 6px;'
        f'filter:drop-shadow(0 2px 8px rgba(0,0,0,0.3));"/>'
        f'<div style="font-size:0.62rem;color:rgba(255,255,255,0.5);letter-spacing:1.5px;'
        f'text-transform:uppercase;margin-top:4px;">"Uncovering Special Capabilities"</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    page = st.radio("NAVIGATION", [
        "🛒  POS Terminal",
        "📊  Analytics Hub",
        "💸  Expenses",
        "🔐  Admin Vault",
    ], label_visibility="collapsed")

    st.markdown("---")

    # Today's quick stat
    today_q = run_query(
        "SELECT COALESCE(SUM(total),0) as rev, COUNT(*) as txns FROM sales WHERE DATE(timestamp)=DATE('now','localtime')"
    )
    t_rev  = today_q["rev"].iloc[0]  if not today_q.empty else 0
    t_txns = today_q["txns"].iloc[0] if not today_q.empty else 0
    basket_count = len(st.session_state.basket)
    basket_total = sum(i["unit_price"] * i["qty"] for i in st.session_state.basket)

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.08);border-radius:12px;padding:14px;text-align:center;margin-bottom:10px;">
        <div style="font-size:0.6rem;color:rgba(255,255,255,0.5);letter-spacing:1px;text-transform:uppercase;">Today's Revenue</div>
        <div style="font-family:'Nunito',sans-serif;font-size:1.5rem;font-weight:900;color:{ACCENT};margin-top:3px;">{fmt(t_rev)}</div>
        <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);margin-top:2px;">{t_txns} transaction(s)</div>
    </div>
    <div style="background:rgba(76,175,80,0.15);border-radius:12px;padding:10px;text-align:center;border:1px solid rgba(76,175,80,0.3);">
        <div style="font-size:0.6rem;color:rgba(255,255,255,0.5);letter-spacing:1px;text-transform:uppercase;">🛒 Basket</div>
        <div style="font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:900;color:{GREEN};margin-top:2px;">{basket_count} item(s)</div>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.6);">{fmt(basket_total)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

    if st.session_state.vault_unlocked:
        st.markdown(f"<p style='color:{RED};font-size:0.7rem;margin-top:8px;'>⚠️ VAULT UNLOCKED — DANGER ZONE</p>", unsafe_allow_html=True)
        if st.button("🗑 CLEAR ALL DATA", use_container_width=True):
            st.session_state["confirm_clear"] = True
        if st.session_state.get("confirm_clear"):
            st.warning("Deletes ALL data. Enter password:")
            cp = st.text_input("Password", type="password", key="clear_pw")
            ca, cb = st.columns(2)
            if ca.button("✅ YES", use_container_width=True):
                if cp == "Rishmaya":
                    run_write_many([
                        ("DELETE FROM sales", ()), ("DELETE FROM expenses", ()),
                        ("DELETE FROM inventory", ()), ("DELETE FROM activity_log", ()),
                        ("DELETE FROM categories", ()),
                    ])
                    st.session_state["confirm_clear"] = False
                    st.success("All data cleared.")
                    st.rerun()
                else:
                    st.error("Wrong password.")
            if cb.button("✕ No", use_container_width=True):
                st.session_state["confirm_clear"] = False
                st.rerun()

    st.markdown("---")
    st.caption(f"Billing OS v5.0  |  {_now.strftime('%d %b %Y')}")


# ════════════════════════════════════════════════════════════════
#  INVENTORY TOAST
# ════════════════════════════════════════════════════════════════
if st.session_state.inv_toast:
    _kind, _msg_t = st.session_state.inv_toast
    st.toast(_msg_t, icon="✅" if _kind == "success" else "⚠️")
    st.session_state.inv_toast = None

# ════════════════════════════════════════════════════════════════
#  POS TERMINAL
# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
#  ①  POS TERMINAL  — basket model
# ════════════════════════════════════════════════════════════════
if page == "🛒  POS Terminal":

    st.markdown(f'<div class="page-header">🛒 POS Terminal</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Select items → Add to Basket → Press Sell</div>', unsafe_allow_html=True)

    items_df = run_query("""
        SELECT i.id, i.item_name, i.buying_price, i.selling_price, i.quantity,
               c.name as category
        FROM inventory i JOIN categories c ON i.category_id = c.id
        ORDER BY c.name, i.item_name
    """)

    if items_df.empty:
        st.warning("⚠️ Inventory is empty. Go to **Admin Vault** → Add Product.")
    else:
        # ── BASKET PANEL at top
        basket = st.session_state.basket
        if basket:
            basket_total_amt = sum(i["unit_price"] * i["qty"] for i in basket)
            st.markdown(f"""
            <div style="background:{WHITE};border-radius:16px;box-shadow:0 6px 28px rgba(26,77,161,0.13);
                 border-top:5px solid {GREEN};padding:0;margin-bottom:18px;overflow:hidden;">
                <div style="background:linear-gradient(135deg,{DARK_BG},{BLUE});
                     padding:14px 20px;display:flex;align-items:center;justify-content:space-between;">
                    <div style="font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:900;color:{WHITE};">
                        🛒 Shopping Basket
                    </div>
                    <div style="background:rgba(76,175,80,0.25);border:1px solid {GREEN};
                         border-radius:20px;padding:3px 14px;">
                        <span style="color:{GREEN};font-weight:800;font-size:0.85rem;">{len(basket)} item(s)</span>
                    </div>
                </div>
                <div style="padding:14px 18px 0;">
            """, unsafe_allow_html=True)

            for idx, itm in enumerate(basket):
                subtotal = itm['unit_price'] * itm['qty']
                # Use columns: name | minus | qty display | plus | price | remove
                cn, cm, cq, cp_btn, cpr, cd = st.columns([4, 1, 1, 1, 2, 1])
                cn.markdown(f"""
                <div style="padding:6px 0;">
                    <div style="font-weight:700;color:{BLACK};font-size:0.88rem;">{itm['item']}</div>
                    <div style="font-size:0.72rem;color:#888;">{itm['category']} &middot; {fmt(itm['unit_price'])}/unit</div>
                </div>""", unsafe_allow_html=True)

                if cm.button("−", key=f"bm_{idx}", use_container_width=True):
                    if st.session_state.basket[idx]['qty'] > 1:
                        st.session_state.basket[idx]['qty'] -= 1
                    else:
                        st.session_state.basket.pop(idx)
                    st.rerun()

                cq.markdown(f"""
                <div style="text-align:center;padding:8px 0;font-weight:900;
                     color:{BLUE};font-size:1rem;">{int(itm['qty'])}</div>""",
                unsafe_allow_html=True)

                if cp_btn.button("＋", key=f"bp_{idx}", use_container_width=True):
                    st.session_state.basket[idx]['qty'] += 1
                    st.rerun()

                cpr.markdown(f"""
                <div style="padding:8px 0;font-family:'Nunito',sans-serif;
                     font-weight:800;color:{BLUE};font-size:0.95rem;text-align:right;">
                    {fmt(subtotal)}
                </div>""", unsafe_allow_html=True)

                if cd.button("✕", key=f"br_{idx}", use_container_width=True, help="Remove"):
                    st.session_state.basket.pop(idx)
                    st.rerun()

                st.markdown(f'<hr style="margin:4px 0;border:none;border-top:1px solid {LGRAY};">', unsafe_allow_html=True)

            st.markdown(f"""
                </div>
                <div style="background:linear-gradient(135deg,{DARK_BG},{BLUE});
                     padding:14px 20px;margin-top:4px;display:flex;
                     justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;
                             color:rgba(255,255,255,0.6);">Grand Total</div>
                        <div style="font-family:'Nunito',sans-serif;font-size:1.8rem;font-weight:900;
                             color:{STAR_GOLD};line-height:1.1;">{fmt(basket_total_amt)}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);">
                            {len(basket)} item(s) · basket total
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Payment method + SELL button
            pay_col, sell_col, clr_col = st.columns([3, 2, 1])
            pay_method = pay_col.selectbox("Payment Method", ["Cash", "M-Pesa", "Bank Transfer"], key="basket_pay")

            with sell_col:
                st.markdown('<div class="sell-btn">', unsafe_allow_html=True)
                do_sell = st.button(f"✅ SELL — {fmt(basket_total_amt)}", use_container_width=True, type="primary", key="do_basket_sell")
                st.markdown('</div>', unsafe_allow_html=True)

            if clr_col.button("🗑 Clear", use_container_width=True, key="clear_basket"):
                st.session_state.basket = []
                st.rerun()

            if do_sell:
                # Build PDF FIRST (while basket still intact)
                _pdf_items = [{"item": i["item"], "qty": i["qty"],
                               "unit_price": i["unit_price"],
                               "total": i["unit_price"] * i["qty"]}
                              for i in st.session_state.basket]
                _items_sold = ", ".join(f"{i['item']} x{round(i['qty'])}" for i in st.session_state.basket)
                try:
                    _pdf_bytes = build_pdf_receipt(_pdf_items, pay_method)
                    st.session_state.pdf_error = None
                except Exception as _pdf_exc:
                    _pdf_bytes = None
                    st.session_state.pdf_error = str(_pdf_exc)

                success, errors = record_basket_sale(st.session_state.basket, pay_method)
                if success:
                    st.session_state.receipt_pdf  = _pdf_bytes
                    st.session_state.sale_msg     = f"{_items_sold}\n{pay_method} — {fmt(basket_total_amt)}"
                    st.session_state.sale_complete = True
                    # ── Store in receipts history for Analytics download ──
                    if _pdf_bytes:
                        _rno = f"SSV-{now_eat().strftime('%Y%m%d%H%M%S')}"
                        _ts_label = now_eat().strftime("%d %b %Y %H:%M:%S")
                        st.session_state.receipts_history.append({
                            "rno": _rno,
                            "ts": _ts_label,
                            "label": f"{_rno}  |  {_items_sold[:40]}  |  {fmt(basket_total_amt)}  |  {pay_method}",
                            "pdf_bytes": _pdf_bytes,
                        })
                    if errors:
                        for e in errors:
                            st.warning(e)
                    log_activity("SALE", f"Basket: {_items_sold} | Total: {fmt(basket_total_amt)} | {pay_method}")
                    # Clear basket state for next transaction (kept in sale popup close)
                    st.rerun()
                else:
                    for e in errors:
                        st.error(e)
                    if any("insufficient" in e for e in errors):
                        st.session_state.out_of_stock = True
                        st.rerun()

            st.markdown("---")

        # ── SEARCH + PRODUCT CARDS ──
        search = st.text_input("🔍 Search product", placeholder="Type product name…", key="pos_search")

        cats = sorted(items_df["category"].unique().tolist())
        tab_labels = ["🔍 ALL"] + cats
        tabs = st.tabs(tab_labels)

        for t_idx, tab in enumerate(tabs):
            with tab:
                tab_prefix = f"t{t_idx}"
                if t_idx == 0:
                    filtered = items_df.copy()
                else:
                    filtered = items_df[items_df["category"] == cats[t_idx - 1]].copy()

                if search:
                    filtered = filtered[
                        filtered["item_name"].str.contains(search, case=False, na=False)
                    ]

                if filtered.empty:
                    st.info("No products found.")
                    continue

                cols = st.columns(3)
                for card_idx, (_, row) in enumerate(filtered.reset_index(drop=True).iterrows()):
                    with cols[card_idx % 3]:
                        if row["quantity"] <= 0:
                            s_cls, s_txt = "stock-out", "OUT OF STOCK"
                        elif row["quantity"] <= 3:
                            s_cls, s_txt = "stock-low", f"LOW: {row['quantity']:.0f}"
                        else:
                            s_cls, s_txt = "stock-ok", f"Stock: {row['quantity']:.0f}"

                        st.markdown(f"""
                        <div class="neo-card">
                            <div class="nc-cat">{row['category']}</div>
                            <div class="nc-name">{row['item_name']}</div>
                            <div class="nc-price">{fmt(row['selling_price'])}</div>
                            <div class="nc-stock {s_cls}">{s_txt}</div>
                        </div>
                        """, unsafe_allow_html=True)

                        if row["quantity"] > 0:
                            with st.popover(f"➕ Add to Basket", use_container_width=True):
                                st.markdown(f"**{row['item_name']}** · {row['category']}")
                                st.markdown(f"Price: **{fmt(row['selling_price'])}** per unit")
                                q_max = max(1, int(row["quantity"]))
                                qty = st.number_input(
                                    "Quantity",
                                    min_value=1, max_value=q_max, value=1,
                                    key=f"qty_{tab_prefix}_{row['id']}",
                                )
                                line_total = row["selling_price"] * qty
                                st.markdown(f"""
                                <div style="background:{LGRAY};border-radius:8px;padding:10px 14px;
                                     margin:8px 0;border-left:4px solid {BLUE};">
                                    <span style="font-size:0.75rem;color:#888;">SUBTOTAL</span><br>
                                    <span style="font-family:'Nunito',sans-serif;font-size:1.4rem;
                                          font-weight:900;color:{BLUE};">{fmt(line_total)}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                if st.button(
                                    f"🛒 ADD TO BASKET",
                                    key=f"add_{tab_prefix}_{row['id']}",
                                    type="primary",
                                    use_container_width=True,
                                ):
                                    # Check if already in basket → update qty
                                    existing = next((i for i in st.session_state.basket if i["id"] == int(row["id"])), None)
                                    if existing:
                                        existing["qty"] = min(existing["qty"] + qty, q_max)
                                    else:
                                        st.session_state.basket.append({
                                            "id": int(row["id"]),
                                            "item": row["item_name"],
                                            "category": row["category"],
                                            "qty": float(qty),
                                            "unit_price": float(row["selling_price"]),
                                            "buy_price": float(row["buying_price"]),
                                        })
                                    st.toast(f"✅ {row['item_name']} added to basket!", icon="🛒")
                                    # No st.rerun() here — avoids page flash.
                                    # Basket updates reflect on next interaction.

# ════════════════════════════════════════════════════════════════
#  ANALYTICS HUB
# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
#  ②  ANALYTICS HUB  — richer statistics
# ════════════════════════════════════════════════════════════════
elif page == "📊  Analytics Hub":

    st.markdown(f'<div class="page-header">📊 Analytics Hub</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Financial Intelligence & Business Insights</div>', unsafe_allow_html=True)

    all_sales = run_query("SELECT * FROM sales ORDER BY timestamp DESC")
    all_expenses = run_query("SELECT * FROM expenses ORDER BY timestamp DESC")

    if all_sales.empty:
        st.info("No sales data yet. Start selling in the POS Terminal!")
    else:
        all_sales["timestamp"] = pd.to_datetime(all_sales["timestamp"])

        t_today, t_week, t_month, t_alltime, t_eod, t_receipts = st.tabs([
            "⚡ TODAY", "📅 THIS WEEK", "📊 THIS MONTH", "🌟 ALL TIME", "🗂 END OF DAY", "📄 RECEIPTS"
        ])

        analytics_tabs = [
            (t_today, 0,  "Today"),
            (t_week,  7,  "Week"),
            (t_month, 30, "Month"),
        ]

        for tab, days, label in analytics_tabs:
            with tab:
                today_dt = now_eat().date()
                if days == 0:
                    df = all_sales[all_sales["timestamp"].dt.date == today_dt].copy()
                else:
                    df = all_sales[
                        all_sales["timestamp"].dt.date >= (now_eat() - timedelta(days=days)).date()
                    ].copy()

                rev   = df["total"].sum()
                prof  = df["profit"].sum()
                cash  = df[df["payment_method"].str.lower() == "cash"]["total"].sum()
                mpesa = df[df["payment_method"].str.lower() == "m-pesa"]["total"].sum()
                bank  = df[df["payment_method"].str.lower() == "bank transfer"]["total"].sum()
                txns  = len(df)
                margin_pct = (prof / rev * 100) if rev > 0 else 0

                # Total expenses for period
                exp_rev = 0
                if not all_expenses.empty:
                    all_expenses["timestamp"] = pd.to_datetime(all_expenses["timestamp"])
                    if days == 0:
                        exp_df = all_expenses[all_expenses["timestamp"].dt.date == today_dt]
                    else:
                        exp_df = all_expenses[all_expenses["timestamp"].dt.date >= (now_eat() - timedelta(days=days)).date()]
                    exp_rev = exp_df["amount"].sum()
                net_income = prof - exp_rev

                # Metrics row 1
                st.markdown(f"""
                <div class="metric-grid">
                    <div class="metric-card mc-blue">
                        <div class="m-label">💰 Revenue</div><div class="m-value">{fmt(rev)}</div>
                        <div class="m-delta">{txns} transactions</div>
                    </div>
                    <div class="metric-card mc-green">
                        <div class="m-label">📈 Gross Profit</div><div class="m-value">{fmt(prof)}</div>
                        <div class="m-delta">{margin_pct:.1f}% margin</div>
                    </div>
                    <div class="metric-card mc-teal">
                        <div class="m-label">🏦 Net Income</div><div class="m-value">{fmt(net_income)}</div>
                        <div class="m-delta">After expenses</div>
                    </div>
                    <div class="metric-card mc-amber">
                        <div class="m-label">💵 Cash</div><div class="m-value">{fmt(cash)}</div>
                        <div class="m-delta">{'%.0f%%' % (cash/rev*100) + ' of sales' if rev>0 else ''}</div>
                    </div>
                    <div class="metric-card mc-dark">
                        <div class="m-label">📱 M-Pesa</div><div class="m-value">{fmt(mpesa)}</div>
                        <div class="m-delta">{'%.0f%%' % (mpesa/rev*100) + ' of sales' if rev>0 else ''}</div>
                    </div>
                    <div class="metric-card mc-teal">
                        <div class="m-label">🏦 Bank Transfer</div><div class="m-value">{fmt(bank)}</div>
                        <div class="m-delta">{'%.0f%%' % (bank/rev*100) + ' of sales' if rev>0 else ''}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if df.empty:
                    st.info(f"No sales yet for this {label.lower()} period.")
                    continue

                # ── Charts row 1
                c1, c2 = st.columns(2)
                with c1:
                    if days == 0:
                        cd = df.copy()
                        cd["hour"] = cd["timestamp"].dt.strftime("%H:00")
                        cd = cd.groupby("hour")[["total","profit"]].sum().reset_index()
                        fig = px.bar(cd, x="hour", y=["total","profit"], barmode="group",
                                     title="Hourly Sales vs Profit",
                                     color_discrete_sequence=[BLUE, GREEN])
                    else:
                        cd = df.groupby(df["timestamp"].dt.date)[["total","profit"]].sum().reset_index()
                        cd.columns = ["Date","Revenue","Profit"]
                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=cd["Date"], y=cd["Revenue"], name="Revenue",
                                             marker_color=BLUE, opacity=0.8))
                        fig.add_trace(go.Scatter(x=cd["Date"], y=cd["Profit"], name="Profit",
                                                 mode="lines+markers",
                                                 line=dict(color=GREEN, width=3),
                                                 marker=dict(size=7)))
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0,r=0,t=30,b=0), hovermode="x unified",
                        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#E5E7EB"),
                        title_font=dict(size=12, color=BLUE), legend=dict(orientation="h"),
                    )
                    st.plotly_chart(fig, use_container_width=True, key=f"trend_{label}")

                with c2:
                    top = (df.groupby("item_name")["total"]
                             .sum().sort_values(ascending=False).head(10).reset_index())
                    top.columns = ["Product", "Revenue"]
                    fig_top = go.Figure(go.Bar(
                        x=top["Revenue"], y=top["Product"], orientation="h",
                        marker=dict(color=top["Revenue"],
                                    colorscale=[[0,"#BFD7FF"],[1,BLUE]],
                                    line=dict(width=0)),
                        text=[fmt(v) for v in top["Revenue"]],
                        textposition="outside",
                    ))
                    fig_top.update_layout(
                        title="Best Selling Products",
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10,r=90,t=30,b=0),
                        xaxis=dict(showgrid=True,gridcolor="#E5E7EB",zeroline=False),
                        yaxis=dict(autorange="reversed",showgrid=False,tickfont=dict(size=11)),
                        title_font=dict(size=12, color=BLUE),
                    )
                    st.plotly_chart(fig_top, use_container_width=True, key=f"top_{label}")

                # ── Charts row 2: Payment mix + Category breakdown
                c3, c4 = st.columns(2)
                with c3:
                    pm = df.groupby("payment_method")["total"].sum().reset_index()
                    fig_pm = px.pie(pm, values="total", names="payment_method", hole=0.52,
                                    color_discrete_sequence=[BLUE, GREEN, ACCENT, "#7B1FA2"],
                                    title="Payment Method Mix")
                    fig_pm.update_traces(textposition="outside", textinfo="label+percent")
                    fig_pm.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10,r=10,t=30,b=0), showlegend=False,
                        title_font=dict(size=12, color=BLUE),
                    )
                    st.plotly_chart(fig_pm, use_container_width=True, key=f"pm_{label}")

                with c4:
                    cat_rev = df.groupby("category")[["total","profit"]].sum().reset_index()
                    fig_cat = px.bar(cat_rev, x="category", y=["total","profit"],
                                     barmode="group", title="Revenue & Profit by Category",
                                     color_discrete_sequence=[BLUE, GREEN])
                    fig_cat.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=0,r=0,t=30,b=0),
                        xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#E5E7EB"),
                        title_font=dict(size=12, color=BLUE), legend=dict(orientation="h"),
                    )
                    st.plotly_chart(fig_cat, use_container_width=True, key=f"cat_{label}")

                # ── Extra plot: Cumulative revenue line + profit margin trend
                if not df.empty and len(df) > 1:
                    c5 = st.container()
                    with c5:
                        df_sorted = df.sort_values("timestamp")
                        df_sorted["cumulative_rev"] = df_sorted["total"].cumsum()
                        df_sorted["cumulative_profit"] = df_sorted["profit"].cumsum()
                        fig_cum = go.Figure()
                        fig_cum.add_trace(go.Scatter(
                            x=df_sorted["timestamp"], y=df_sorted["cumulative_rev"],
                            name="Cumulative Revenue", fill="tozeroy",
                            line=dict(color=BLUE, width=2.5),
                            fillcolor="rgba(26,77,161,0.1)"
                        ))
                        fig_cum.add_trace(go.Scatter(
                            x=df_sorted["timestamp"], y=df_sorted["cumulative_profit"],
                            name="Cumulative Profit",
                            line=dict(color=GREEN, width=2.5, dash="dot"),
                        ))
                        fig_cum.update_layout(
                            title="Cumulative Revenue & Profit Growth",
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0,r=0,t=30,b=0), hovermode="x unified",
                            xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#E5E7EB"),
                            title_font=dict(size=12, color=BLUE), legend=dict(orientation="h"),
                        )
                        st.plotly_chart(fig_cum, use_container_width=True, key=f"cumrev_{label}")

                # ── Insights row
                if txns > 0:
                    top_prod = df.groupby("item_name")["total"].sum().idxmax()
                    top_cat  = df.groupby("category")["total"].sum().idxmax()
                    best_hr_row = df.copy()
                    best_hr_row["hour"] = best_hr_row["timestamp"].dt.hour
                    best_hr  = best_hr_row.groupby("hour")["total"].sum().idxmax()
                    st.markdown(f"""
                    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:18px;">
                        <div class="insight-card">
                            <div class="insight-title">🏆 Top Product</div>
                            <div class="insight-val">{top_prod}</div>
                            <div class="insight-sub">{fmt(df.groupby("item_name")["total"].sum()[top_prod])} generated</div>
                        </div>
                        <div class="insight-card" style="border-left-color:{BLUE};">
                            <div class="insight-title">📂 Top Category</div>
                            <div class="insight-val">{top_cat}</div>
                            <div class="insight-sub">{fmt(df.groupby("category")["total"].sum()[top_cat])} generated</div>
                        </div>
                        <div class="insight-card" style="border-left-color:{ACCENT};">
                            <div class="insight-title">🕐 Peak Hour</div>
                            <div class="insight-val">{best_hr:02d}:00 – {best_hr+1:02d}:00</div>
                            <div class="insight-sub">Highest sales activity</div>
                        </div>
                        <div class="insight-card" style="border-left-color:{RED};">
                            <div class="insight-title">💸 Expenses</div>
                            <div class="insight-val">{fmt(exp_rev)}</div>
                            <div class="insight-sub">Net income: {fmt(net_income)}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Transaction log
                st.markdown(f"#### 📋 {label} Transaction Log")
                disp = df[["timestamp","item_name","category","qty","unit_price","total","profit","payment_method"]].sort_values("timestamp", ascending=False).copy()
                disp.columns = ["Time","Product","Category","Qty","Unit Price","Total","Profit","Method"]
                st.dataframe(disp, use_container_width=True, hide_index=True)

                csv = disp.to_csv(index=False).encode()
                st.download_button(
                    f"⬇ Export {label} CSV", csv,
                    file_name=f"ssv_{label.lower()}_{now_eat().strftime('%Y%m%d')}.csv",
                    mime="text/csv", key=f"csv_{label}",
                )

                # Sale reversal (today only)
                if label == "Today":
                    st.markdown("#### ↩️ Reverse Recent Transaction")
                    st.caption("Transactions within the last 5 minutes. Password required. Stock will be restored.")
                    cutoff = now_eat() - timedelta(minutes=5)
                    recent = df[pd.to_datetime(df["timestamp"]) >= cutoff]
                    if recent.empty:
                        st.info("No transactions in the last 5 minutes.")
                    else:
                        opts = {
                            f"#{r['id']} — {r['item_name']} ({r['unit_sold']}) {fmt(r['total'])} @ {pd.to_datetime(r['timestamp']).strftime('%H:%M:%S')}": r['id']
                            for _, r in recent.iterrows()
                        }
                        chosen_lbl = st.selectbox("Select transaction", list(opts.keys()), key="rev_sel")
                        chosen_id  = opts[chosen_lbl]
                        chosen_row = recent[recent["id"] == chosen_id].iloc[0]
                        st.markdown(f"""
                        <div style="background:{RED};border-radius:10px;padding:10px 14px;margin:8px 0;">
                            <span style="color:{WHITE};font-size:0.8rem;font-weight:700;">
                            ⚠️ {chosen_row['item_name']} | {fmt(chosen_row['total'])} | Qty {chosen_row['qty']:.0f} → back to stock
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        rev_pw = st.text_input("Admin password", type="password", key="rev_pw")
                        if st.button("↩ CONFIRM REVERSAL", key="do_rev"):
                            if rev_pw == "Rishmaya":
                                run_write_many([
                                    ("UPDATE inventory SET quantity = quantity + ? WHERE item_name = ?",
                                     (float(chosen_row["qty"]), str(chosen_row["item_name"]))),
                                    ("DELETE FROM sales WHERE id = ?", (int(chosen_id),)),
                                ])
                                log_activity("SALE REVERSED",
                                             f"Sale #{chosen_id} | {chosen_row['item_name']} | {fmt(chosen_row['total'])}")
                                st.success("Sale reversed and stock restored.")
                                st.rerun()
                            else:
                                st.error("Wrong password.")

        # ── ALL TIME TAB ──
        with t_alltime:
            st.markdown(f"<h3 style='font-family:Nunito,sans-serif;color:{BLUE};text-align:center;'>🌟 All-Time Performance</h3>", unsafe_allow_html=True)

            total_rev   = all_sales["total"].sum()
            total_prof  = all_sales["profit"].sum()
            total_txns  = len(all_sales)
            total_exp   = all_expenses["amount"].sum() if not all_expenses.empty else 0
            net_all     = total_prof - total_exp
            best_day_df = all_sales.groupby(all_sales["timestamp"].dt.date)["total"].sum()
            best_day    = best_day_df.idxmax() if not best_day_df.empty else None
            best_day_rev= best_day_df.max() if not best_day_df.empty else 0
            unique_prods = all_sales["item_name"].nunique()
            avg_daily   = total_rev / max(len(best_day_df), 1)

            st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-card mc-blue">
                    <div class="m-label">💰 Total Revenue</div><div class="m-value">{fmt(total_rev)}</div>
                    <div class="m-delta">All time</div>
                </div>
                <div class="metric-card mc-green">
                    <div class="m-label">📈 Total Profit</div><div class="m-value">{fmt(total_prof)}</div>
                    <div class="m-delta">{'%.1f%% margin' % (total_prof/total_rev*100) if total_rev>0 else ''}</div>
                </div>
                <div class="metric-card mc-teal">
                    <div class="m-label">🏦 Net (After Exp)</div><div class="m-value">{fmt(net_all)}</div>
                    <div class="m-delta">Expenses: {fmt(total_exp)}</div>
                </div>
                <div class="metric-card mc-dark">
                    <div class="m-label">🧾 Total Transactions</div><div class="m-value">{total_txns}</div>
                    <div class="m-delta">All time</div>
                </div>
                <div class="metric-card mc-amber">
                    <div class="m-label">📅 Avg Daily Revenue</div><div class="m-value">{fmt(avg_daily)}</div>
                    <div class="m-delta">Per trading day</div>
                </div>
                <div class="metric-card mc-purple">
                    <div class="m-label">📦 Products Sold</div><div class="m-value">{unique_prods}</div>
                    <div class="m-delta">Unique products</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if best_day:
                st.markdown(f"""
                <div class="insight-card" style="border-left-color:{STAR_GOLD};">
                    <div class="insight-title">🏆 Best Day Ever</div>
                    <div class="insight-val">{str(best_day)}</div>
                    <div class="insight-sub">Revenue: {fmt(best_day_rev)}</div>
                </div>
                """, unsafe_allow_html=True)

            # Revenue over time
            daily = all_sales.groupby(all_sales["timestamp"].dt.date)[["total","profit"]].sum().reset_index()
            daily.columns = ["Date","Revenue","Profit"]
            fig_all = go.Figure()
            fig_all.add_trace(go.Scatter(x=daily["Date"], y=daily["Revenue"], name="Revenue",
                                         fill="tozeroy", line=dict(color=BLUE, width=2.5),
                                         fillcolor=f"rgba(26,77,161,0.12)"))
            fig_all.add_trace(go.Scatter(x=daily["Date"], y=daily["Profit"], name="Profit",
                                         line=dict(color=GREEN, width=2.5)))
            fig_all.update_layout(
                title="Revenue & Profit Over Time",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=30,b=0), hovermode="x unified",
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#E5E7EB"),
                title_font=dict(size=13, color=BLUE), legend=dict(orientation="h"),
            )
            st.plotly_chart(fig_all, use_container_width=True, key="alltime_trend")

            # Top products all time
            c_a, c_b = st.columns(2)
            with c_a:
                top_all = all_sales.groupby("item_name")["total"].sum().sort_values(ascending=False).head(12).reset_index()
                top_all.columns = ["Product","Revenue"]
                fig_ta = go.Figure(go.Bar(
                    x=top_all["Revenue"], y=top_all["Product"], orientation="h",
                    marker=dict(color=top_all["Revenue"], colorscale=[[0,"#BFD7FF"],[1,BLUE]]),
                    text=[fmt(v) for v in top_all["Revenue"]], textposition="outside",
                ))
                fig_ta.update_layout(title="All-Time Top Products",
                                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                      margin=dict(l=10,r=90,t=30,b=0),
                                      yaxis=dict(autorange="reversed",showgrid=False),
                                      xaxis=dict(showgrid=True,gridcolor="#E5E7EB"),
                                      title_font=dict(size=12, color=BLUE))
                st.plotly_chart(fig_ta, use_container_width=True, key="at_top_prod")

            with c_b:
                cat_all = all_sales.groupby("category")["total"].sum().reset_index()
                fig_ca = px.pie(cat_all, values="total", names="category", hole=0.5,
                                 color_discrete_sequence=[BLUE, GREEN, ACCENT, RED, "#7B1FA2", "#00897B"],
                                 title="Revenue by Category — All Time")
                fig_ca.update_traces(textposition="outside", textinfo="label+percent")
                fig_ca.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10,r=10,t=30,b=0), showlegend=False,
                    title_font=dict(size=12, color=BLUE),
                )
                st.plotly_chart(fig_ca, use_container_width=True, key="at_cat_pie")

        # ── END OF DAY ──
        with t_eod:
            st.markdown(f"<h3 style='font-family:Nunito,sans-serif;color:{BLUE};text-align:center;'>End of Day Report</h3>", unsafe_allow_html=True)
            eod_dates = sorted(all_sales["timestamp"].dt.date.unique(), reverse=True)
            eod_date  = st.selectbox("Select date", eod_dates, key="eod_date_sel")
            df_day    = all_sales[all_sales["timestamp"].dt.date == eod_date].copy()

            if df_day.empty:
                st.info("No sales for this date.")
            else:
                d_rev   = df_day["total"].sum()
                d_prof  = df_day["profit"].sum()
                d_cash  = df_day[df_day["payment_method"].str.lower() == "cash"]["total"].sum()
                d_mpesa = df_day[df_day["payment_method"].str.lower() == "m-pesa"]["total"].sum()
                d_bank  = df_day[df_day["payment_method"].str.lower() == "bank transfer"]["total"].sum()
                d_txns  = len(df_day)

                st.markdown(f"""
                <div class="eod-card">
                    <div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:rgba(255,255,255,0.5);letter-spacing:2px;text-transform:uppercase;">End of Day Report</div>
                    <div style="font-family:'Nunito',sans-serif;font-size:clamp(1.2rem,4vw,1.9rem);font-weight:900;color:{WHITE};margin:4px 0;">{eod_date.strftime('%d %B %Y')}</div>
                    <div class="eod-grid">
                        <div class="eod-cell"><p>💰 Revenue</p><h2 style="color:{ACCENT};">{fmt(d_rev)}</h2></div>
                        <div class="eod-cell"><p>📈 Net Profit</p><h2 style="color:{GREEN};">{fmt(d_prof)}</h2></div>
                        <div class="eod-cell"><p>💵 Cash</p><h2 style="color:{WHITE};">{fmt(d_cash)}</h2></div>
                        <div class="eod-cell"><p>📱 M-Pesa</p><h2 style="color:{GREEN};">{fmt(d_mpesa)}</h2></div>
                        <div class="eod-cell"><p>🏦 Bank Transfer</p><h2 style="color:{WHITE};">{fmt(d_bank)}</h2></div>
                        <div class="eod-cell"><p>🧾 Transactions</p><h2 style="color:{ACCENT};">{d_txns}</h2></div>
                        <div class="eod-cell"><p>📊 Avg. Sale</p><h2 style="color:{WHITE};">{fmt(d_rev/d_txns if d_txns>0 else 0)}</h2></div>
                        <div class="eod-cell"><p>💹 Margin %</p><h2 style="color:{GREEN};">{(d_prof/d_rev*100):.1f}%</h2></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                ec1, ec2 = st.columns(2)
                with ec1:
                    cat_bd = df_day.groupby("category")["total"].sum().reset_index().sort_values("total", ascending=False)
                    fig_cb = px.bar(cat_bd, x="category", y="total",
                                    title="Revenue by Category",
                                    color="category",
                                    color_discrete_sequence=[BLUE,GREEN,ACCENT,RED,DARK_BG],
                                    text="total")
                    fig_cb.update_traces(texttemplate="KES %{text:,.0f}", textposition="outside")
                    fig_cb.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                         showlegend=False, margin=dict(l=0,r=0,t=30,b=0),
                                         title_font=dict(color=BLUE, size=12))
                    st.plotly_chart(fig_cb, use_container_width=True, key="eod_cat")

                with ec2:
                    top_e = df_day.groupby("item_name")["total"].sum().sort_values(ascending=False).head(8).reset_index()
                    fig_te = go.Figure(go.Bar(
                        x=top_e["total"], y=top_e["item_name"], orientation="h",
                        marker=dict(color=top_e["total"], colorscale=[[0,"#BFD7FF"],[1,BLUE]]),
                        text=[fmt(v) for v in top_e["total"]], textposition="outside",
                    ))
                    fig_te.update_layout(title="Top Products (Day)",
                                         plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                         margin=dict(l=10,r=90,t=30,b=0),
                                         yaxis=dict(autorange="reversed",showgrid=False),
                                         title_font=dict(color=BLUE, size=12))
                    st.plotly_chart(fig_te, use_container_width=True, key="eod_top")

                st.markdown("#### 📋 Full Transaction Log")
                st.dataframe(
                    df_day[["timestamp","item_name","category","qty","unit_price","total","profit","payment_method"]]
                    .sort_values("timestamp", ascending=False),
                    use_container_width=True, hide_index=True,
                )

                low_s = run_query("SELECT i.item_name, c.name as category, i.quantity FROM inventory i JOIN categories c ON i.category_id=c.id WHERE i.quantity < 3 ORDER BY i.quantity ASC")
                if not low_s.empty:
                    st.markdown("#### ⚠️ Low Stock Alerts")
                    for _, lr in low_s.iterrows():
                        st.markdown(f'<div class="low-stock">🔴 {lr["item_name"]} ({lr["category"]}) — {lr["quantity"]:.0f} unit(s) left</div>', unsafe_allow_html=True)

                csv_day = df_day.to_csv(index=False).encode()
                st.download_button("⬇ Export Day CSV", csv_day,
                                   file_name=f"ssv_eod_{eod_date}.csv", mime="text/csv")

        # ── RECEIPTS TAB ──
        with t_receipts:
            st.markdown(f"<h3 style='font-family:Nunito,sans-serif;color:{BLUE};text-align:center;'>📄 Download Receipts</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;color:#888;font-size:0.85rem;'>Receipts generated during this session. Complete a sale on the POS Terminal to generate receipts.</p>", unsafe_allow_html=True)

            receipts = st.session_state.receipts_history
            if not receipts:
                st.markdown(f"""
                <div style="background:{WHITE};border-radius:14px;padding:40px;text-align:center;
                     box-shadow:0 3px 16px rgba(26,77,161,0.08);border-top:4px solid {BLUE};">
                    <div style="font-size:3rem;">📄</div>
                    <div style="font-family:'Nunito',sans-serif;font-size:1.1rem;font-weight:800;
                         color:{BLUE};margin-top:10px;">No receipts yet this session</div>
                    <div style="color:#888;font-size:0.82rem;margin-top:6px;">
                        Go to <strong>🛒 POS Terminal</strong>, make a sale, then come back here to download the PDF receipt.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,{DARK_BG},{BLUE});border-radius:12px;
                     padding:14px 20px;margin-bottom:18px;display:flex;align-items:center;gap:14px;">
                    <div style="font-size:2rem;">📄</div>
                    <div>
                        <div style="font-family:'Nunito',sans-serif;font-weight:900;color:white;font-size:1rem;">
                            {len(receipts)} Receipt(s) Available
                        </div>
                        <div style="color:rgba(255,255,255,0.6);font-size:0.75rem;">
                            Click the download button next to any receipt below
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                for idx, receipt in enumerate(reversed(receipts)):
                    r_col, d_col = st.columns([5, 1])
                    r_col.markdown(f"""
                    <div style="background:{WHITE};border-radius:10px;padding:12px 16px;
                         box-shadow:0 2px 10px rgba(26,77,161,0.08);border-left:5px solid {GREEN};">
                        <div style="font-family:'Nunito',sans-serif;font-weight:800;color:{BLUE};font-size:0.88rem;">
                            📄 {receipt['rno']}
                        </div>
                        <div style="font-size:0.75rem;color:#555;margin-top:3px;">{receipt['label']}</div>
                        <div style="font-size:0.68rem;color:#aaa;margin-top:2px;">🕐 {receipt['ts']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    d_col.markdown("<div style='padding-top:8px;'>", unsafe_allow_html=True)
                    d_col.download_button(
                        label="⬇ PDF",
                        data=receipt["pdf_bytes"],
                        file_name=f"{receipt['rno']}.pdf",
                        mime="application/pdf",
                        key=f"dl_receipt_{idx}_{receipt['rno']}",
                        use_container_width=True,
                    )
                    d_col.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

                if st.button("🗑 Clear Receipt History", key="clear_receipts"):
                    st.session_state.receipts_history = []
                    st.rerun()


# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
#  ③  EXPENSES
# ════════════════════════════════════════════════════════════════
elif page == "💸  Expenses":

    st.markdown(f'<div class="page-header">💸 Expense Tracker</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Log and monitor all operational costs</div>', unsafe_allow_html=True)

    EXPENSE_CATS = ["Rent","Electricity","Staff Wages","Transport",
                    "Program Materials","Therapy Supplies","Marketing","Other"]

    with st.expander("➕ Log New Expense", expanded=True):
        with st.form("expense_form"):
            xc1, xc2 = st.columns([2,1])
            cat  = xc1.selectbox("Category", EXPENSE_CATS)
            amt  = xc2.number_input("Amount (KES)", min_value=0.0, step=100.0)
            note = st.text_input("Description / Remark")
            if st.form_submit_button("💾 SAVE EXPENSE", type="primary"):
                if amt > 0:
                    run_write("INSERT INTO expenses (category,amount,description,timestamp) VALUES (?,?,?,?)",
                              (cat, amt, note, now_eat()))
                    log_activity("EXPENSE LOGGED", f"{cat} | {fmt(amt)} | {note}")
                    st.success(f"Expense saved: {cat} — {fmt(amt)}")
                    st.rerun()
                else:
                    st.warning("Amount must be greater than 0.")

    df_e = run_query("SELECT * FROM expenses ORDER BY timestamp DESC")

    if df_e.empty:
        st.info("No expenses logged yet.")
    else:
        total_exp = df_e["amount"].sum()
        by_cat    = df_e.groupby("category")["amount"].sum()
        this_month_exp = df_e[pd.to_datetime(df_e["timestamp"]).dt.month == now_eat().month]["amount"].sum() if not df_e.empty else 0
        largest_exp = df_e.loc[df_e["amount"].idxmax()] if not df_e.empty else None

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card mc-red">
                <div class="m-label">💸 Total Expenses</div><div class="m-value">{fmt(total_exp)}</div>
                <div class="m-delta">{len(df_e)} entries</div>
            </div>
            <div class="metric-card mc-dark">
                <div class="m-label">📅 This Month</div><div class="m-value">{fmt(this_month_exp)}</div>
                <div class="m-delta">Current month</div>
            </div>
            <div class="metric-card mc-amber">
                <div class="m-label">📊 Avg. Expense</div><div class="m-value">{fmt(total_exp/len(df_e) if len(df_e)>0 else 0)}</div>
                <div class="m-delta">Per entry</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        c_exp1, c_exp2 = st.columns(2)
        with c_exp1:
            fig_exp = px.bar(by_cat.reset_index(), x="category", y="amount",
                             title="Expenses by Category",
                             color_discrete_sequence=[RED], text="amount")
            fig_exp.update_traces(texttemplate="KES %{text:,.0f}", textposition="outside")
            fig_exp.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   showlegend=False, margin=dict(l=0,r=0,t=30,b=0),
                                   title_font=dict(color=RED, size=12))
            st.plotly_chart(fig_exp, use_container_width=True)
        with c_exp2:
            fig_pie = px.pie(by_cat.reset_index(), values="amount", names="category", hole=0.5,
                              color_discrete_sequence=[RED,"#EF5350","#E57373","#EF9A9A","#FFCDD2","#C62828","#B71C1C"],
                              title="Expense Distribution")
            fig_pie.update_traces(textposition="outside", textinfo="label+percent")
            fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   margin=dict(l=10,r=10,t=30,b=0), showlegend=False,
                                   title_font=dict(size=12, color=RED))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("#### 🛠 Expense Editor")
        for _, row in df_e.iterrows():
            ts = pd.to_datetime(row["timestamp"]).strftime("%d %b %Y %H:%M") if row["timestamp"] else "—"
            with st.expander(f"🧾 {row['category']} — {fmt(row['amount'])}  |  {ts}"):
                nc1, nc2 = st.columns([2,1])
                nc = nc1.selectbox("Category", EXPENSE_CATS,
                                   index=EXPENSE_CATS.index(row["category"])
                                   if row["category"] in EXPENSE_CATS else 0,
                                   key=f"ec_{row['id']}")
                na = nc2.number_input("Amount", value=float(row["amount"]), min_value=0.0, key=f"ea_{row['id']}")
                nd = st.text_input("Description", value=str(row["description"] or ""), key=f"ed_{row['id']}")
                xa, xb = st.columns(2)
                if xa.button("💾 Update", key=f"eu_{row['id']}", type="primary"):
                    run_write("UPDATE expenses SET category=?,amount=?,description=? WHERE id=?",
                              (nc, na, nd, int(row["id"])))
                    st.toast(f"Expense updated: {nc} — {fmt(na)}", icon="✅")
                    st.rerun()
                if xb.button("🗑 Delete", key=f"ex_{row['id']}"):
                    run_write("DELETE FROM expenses WHERE id=?", (int(row["id"]),))
                    st.toast("Expense deleted.", icon="🗑")
                    st.rerun()

# ════════════════════════════════════════════════════════════════
#  ADMIN VAULT
# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
#  ④  ADMIN VAULT
# ════════════════════════════════════════════════════════════════
elif page == "🔐  Admin Vault":

    st.markdown(f'<div class="page-header">🔐 Admin Vault</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Manage inventory, categories & activity logs</div>', unsafe_allow_html=True)

    if not st.session_state.vault_unlocked:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;font-size:3rem;'>🔒</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;color:{BLUE};font-weight:600;'>Enter password to access Admin Vault</p>", unsafe_allow_html=True)
        vp = st.text_input("Admin Password", type="password", key="vault_pw")
        col_v = st.columns([1,2,1])
        if col_v[1].button("🔓 UNLOCK VAULT", type="primary", use_container_width=True):
            if vp == "Rishmaya":
                st.session_state.vault_unlocked = True
                log_activity("VAULT UNLOCKED", f"Admin vault accessed at {now_eat().strftime('%H:%M:%S')}")
                st.rerun()
            else:
                st.error("Incorrect password.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.button("🔒 Lock Vault", key="lock_vault"):
            st.session_state.vault_unlocked = False
            st.rerun()

        t_cats, t_add, t_stock, t_edit, t_log = st.tabs([
            "📁 Categories", "➕ Add Product", "📦 Stock Levels",
            "✏️ Edit / Delete", "📋 Activity Log"
        ])

        # ── CATEGORIES ──
        with t_cats:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Manage Categories</div>', unsafe_allow_html=True)
            cats_df = run_query("SELECT * FROM categories ORDER BY name")

            # Add new category
            st.markdown("**➕ Add New Category**")
            nc_col, nb_col = st.columns([3,1])
            new_cat = nc_col.text_input("New Category Name", key="new_cat_input", placeholder="e.g. Therapy Materials")
            if nb_col.button("➕ Add", type="primary", use_container_width=True, key="add_cat_btn"):
                if new_cat.strip():
                    # Check duplicate
                    existing = run_query("SELECT name FROM categories WHERE LOWER(name)=LOWER(?)", (new_cat.strip(),))
                    if not existing.empty:
                        st.error(f"⚠️ Category '{new_cat.strip()}' already exists!")
                    else:
                        run_write("INSERT INTO categories (name) VALUES (?)", (new_cat.strip(),))
                        log_activity("CATEGORY ADDED", f"Category '{new_cat.strip()}' created")
                        st.session_state.inv_toast = ("success", f"✅ Category '{new_cat.strip()}' added!")
                        st.rerun()
                else:
                    st.warning("Category name cannot be empty.")

            if not cats_df.empty:
                st.markdown("<br>**✏️ Edit Existing Categories**", unsafe_allow_html=True)
                for _, cat_row in cats_df.iterrows():
                    with st.expander(f"📁 {cat_row['name']}", expanded=False):
                        ec1, ec2, ec3 = st.columns([3, 1, 1])
                        new_name = ec1.text_input("Rename to", value=cat_row['name'],
                                                  key=f"cat_rename_{cat_row['id']}")
                        if ec2.button("💾 Save", key=f"cat_save_{cat_row['id']}", type="primary", use_container_width=True):
                            if new_name.strip() and new_name.strip() != cat_row['name']:
                                try:
                                    run_write("UPDATE categories SET name=? WHERE id=?",
                                              (new_name.strip(), int(cat_row['id'])))
                                    # Also update existing sales records
                                    run_write("UPDATE sales SET category=? WHERE category=?",
                                              (new_name.strip(), cat_row['name']))
                                    log_activity("CATEGORY EDITED",
                                                 f"'{cat_row['name']}' → '{new_name.strip()}'")
                                    st.session_state.inv_toast = ("success", f"✅ Category renamed to '{new_name.strip()}'!")
                                    st.rerun()
                                except Exception as ex:
                                    st.error(f"Error: {ex}")
                            else:
                                st.info("No change made.")
                        if ec3.button("🗑 Del", key=f"cat_del_{cat_row['id']}", use_container_width=True):
                            linked = run_query("SELECT COUNT(*) as cnt FROM inventory WHERE category_id=?",
                                               (int(cat_row['id']),))
                            if not linked.empty and linked['cnt'].iloc[0] > 0:
                                st.error(f"Cannot delete — {linked['cnt'].iloc[0]} product(s) use this category.")
                            else:
                                run_write("DELETE FROM categories WHERE id=?", (int(cat_row['id']),))
                                log_activity("CATEGORY DELETED", f"Category '{cat_row['name']}' removed")
                                st.session_state.inv_toast = ("warning", f"🗑 Category '{cat_row['name']}' deleted.")
                                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # ── ADD PRODUCT ──
        with t_add:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Register New Product</div>', unsafe_allow_html=True)
            cats_df = run_query("SELECT * FROM categories ORDER BY name")
            if cats_df.empty:
                st.warning("Please add a category first.")
            else:
                cat_choice = st.selectbox("Category", cats_df["name"].tolist(), key="add_prod_cat")
                item_name  = st.text_input("Product Name", key="add_prod_name")
                p1, p2, p3 = st.columns(3)
                b_price = p1.number_input("Buying Price (KES)", min_value=0.0, step=50.0)
                s_price = p2.number_input("Selling Price (KES)", min_value=0.0, step=50.0)
                qty     = p3.number_input("Initial Quantity", min_value=0, step=1)
                if s_price > 0:
                    margin = s_price - b_price
                    st.markdown(f"""
                    <div style="background:#F0FDF4;border-left:4px solid {GREEN};
                         padding:10px 14px;border-radius:0 10px 10px 0;margin-top:6px;">
                        Margin: <strong>{fmt(margin)}</strong> per unit &nbsp;|&nbsp;
                        Margin %: <strong>{(margin/s_price*100):.1f}%</strong>
                    </div>
                    """, unsafe_allow_html=True)
                if st.button("💾 Register Product", type="primary"):
                    if item_name.strip():
                        # Duplicate check
                        dup = run_query("SELECT id FROM inventory WHERE LOWER(item_name)=LOWER(?)", (item_name.strip(),))
                        if not dup.empty:
                            st.error(f"⚠️ A product named **'{item_name.strip()}'** already exists! Please use a unique name or edit the existing product.")
                        else:
                            cat_id = int(cats_df[cats_df["name"] == cat_choice]["id"].iloc[0])
                            run_write(
                                "INSERT INTO inventory (category_id,item_name,buying_price,selling_price,quantity) VALUES (?,?,?,?,?)",
                                (cat_id, item_name.strip(), b_price, s_price, qty),
                            )
                            log_activity("PRODUCT ADDED",
                                         f"{item_name} | {cat_choice} | Buy:{fmt(b_price)} Sell:{fmt(s_price)} Qty:{qty}")
                            st.session_state.inv_toast = ("success", f"✅ '{item_name.strip()}' added successfully!")
                            st.rerun()
                    else:
                        st.warning("Product name cannot be empty.")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── STOCK LEVELS ──
        with t_stock:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Stock Overview & Quick Restock by Category</div>', unsafe_allow_html=True)
            inv_df = run_query("""
                SELECT i.id, c.name as Category, i.item_name as Product,
                       i.buying_price as 'Buy KES', i.selling_price as 'Sell KES',
                       i.quantity as Qty,
                       (i.selling_price - i.buying_price) as Margin
                FROM inventory i JOIN categories c ON i.category_id=c.id
                ORDER BY c.name, i.item_name
            """)
            if inv_df.empty:
                st.info("No inventory yet.")
            else:
                low = inv_df[inv_df["Qty"] < 3]
                if not low.empty:
                    st.markdown("#### ⚠️ Low Stock Alerts")
                    for _, r in low.iterrows():
                        st.markdown(f'<div class="low-stock">🚨 {r["Product"]} ({r["Category"]}) — {r["Qty"]:.0f} unit(s) left</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                # ── Group by category, show each in its own expander ──
                categories = inv_df["Category"].unique().tolist()
                for cat_name in categories:
                    cat_df = inv_df[inv_df["Category"] == cat_name].copy()
                    low_count = (cat_df["Qty"] < 3).sum()
                    badge = f" 🔴 {low_count} low" if low_count > 0 else ""
                    total_items = len(cat_df)
                    with st.expander(f"📁 {cat_name}  ({total_items} product(s)){badge}", expanded=bool(low_count > 0)):
                        st.dataframe(
                            cat_df[["Product", "Buy KES", "Sell KES", "Qty", "Margin"]],
                            use_container_width=True, hide_index=True
                        )
                        # Restock form inside each category expander
                        st.markdown(f"**➕ Add Stock — {cat_name}** *(enter units to ADD to current stock)*")
                        rs1, rs2, rs3 = st.columns([3, 1, 1])
                        cat_products = cat_df["Product"].tolist()
                        sel_item = rs1.selectbox(
                            "Product", cat_products, label_visibility="collapsed",
                            key=f"rs_item_{cat_name}"
                        )
                        new_qty = rs2.number_input(
                            "Qty", min_value=0, label_visibility="collapsed",
                            key=f"rs_qty_{cat_name}"
                        )
                        if rs3.button("➕ Add Stock", type="primary", use_container_width=True, key=f"rs_btn_{cat_name}"):
                            old_qty = float(cat_df[cat_df["Product"] == sel_item]["Qty"].iloc[0])
                            if new_qty <= 0:
                                st.warning("⚠️ Enter a quantity greater than 0 to add.")
                            else:
                                updated_qty = old_qty + new_qty
                                run_write("UPDATE inventory SET quantity=? WHERE item_name=?", (updated_qty, sel_item))
                                log_activity("STOCK RESTOCK", f"{sel_item} ({cat_name}) | {old_qty:.0f} + {new_qty} = {updated_qty:.0f}")
                                st.session_state.inv_toast = ("success", f"✅ {sel_item}: {old_qty:.0f} + {new_qty} = {updated_qty:.0f} units")
                                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── EDIT / DELETE ──
        with t_edit:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Edit or Remove Products</div>', unsafe_allow_html=True)
            inv_all = run_query("""
                SELECT i.id, c.name as category, i.item_name,
                       i.buying_price, i.selling_price, i.quantity
                FROM inventory i JOIN categories c ON i.category_id=c.id
                ORDER BY c.name, i.item_name
            """)
            if inv_all.empty:
                st.info("No products yet.")
            else:
                sel_p = st.selectbox("Select product to edit / delete", inv_all["item_name"].tolist())
                pr    = inv_all[inv_all["item_name"] == sel_p].iloc[0]
                e1, e2, e3 = st.columns(3)
                nn = e1.text_input("Name", value=pr["item_name"])
                nb = e2.number_input("Buy Price (KES)", value=float(pr["buying_price"]), step=50.0)
                ns = e3.number_input("Sell Price (KES)", value=float(pr["selling_price"]), step=50.0)
                bs, bd = st.columns(2)
                if bs.button("💾 Save Changes", type="primary", use_container_width=True):
                    run_write(
                        "UPDATE inventory SET item_name=?,buying_price=?,selling_price=? WHERE id=?",
                        (nn, nb, ns, int(pr["id"])),
                    )
                    log_activity("PRODUCT EDITED", f"{sel_p} → Name:{nn} Buy:{fmt(nb)} Sell:{fmt(ns)}")
                    st.session_state.inv_toast = ("success", f"✅ '{nn}' updated!")
                    st.rerun()
                if bd.button("🗑 Delete Product", use_container_width=True):
                    run_write("DELETE FROM inventory WHERE id=?", (int(pr["id"]),))
                    log_activity("PRODUCT DELETED", f"{sel_p} removed from inventory")
                    st.session_state.inv_toast = ("warning", f"🗑 '{sel_p}' deleted.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # ── ACTIVITY LOG ──
        with t_log:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📋 Activity Log</div>', unsafe_allow_html=True)

            if not st.session_state.activity_log_unlocked:
                ap = st.text_input("Password to view log", type="password", key="act_pw")
                if st.button("🔓 Unlock Log"):
                    if ap == "Rishmaya":
                        st.session_state.activity_log_unlocked = True
                        st.rerun()
                    else:
                        st.error("Wrong password.")
            else:
                if st.button("🔒 Lock Log"):
                    st.session_state.activity_log_unlocked = False
                    st.rerun()
                al1, al2 = st.columns([2, 1])
                act_date = al1.date_input("Date", now_eat().date(), key="act_date")
                act_type = al2.selectbox("Type", [
                    "ALL","PRODUCT ADDED","STOCK ADJUSTMENT","PRODUCT DELETED",
                    "SALE REVERSED","EXPENSE LOGGED","VAULT UNLOCKED","CATEGORY ADDED","SALE",
                ], key="act_type")

                if act_type == "ALL":
                    df_act = run_query("SELECT * FROM activity_log WHERE DATE(timestamp)=? ORDER BY timestamp DESC", (act_date,))
                else:
                    df_act = run_query("SELECT * FROM activity_log WHERE DATE(timestamp)=? AND action_type=? ORDER BY timestamp DESC", (act_date, act_type))

                if df_act.empty:
                    st.info("No activity for this date / filter.")
                else:
                    COLOR_MAP = {
                        "PRODUCT ADDED": GREEN, "CATEGORY ADDED": GREEN,
                        "STOCK ADJUSTMENT": BLUE, "PRODUCT DELETED": RED,
                        "SALE REVERSED": ACCENT, "EXPENSE LOGGED": "#9333EA",
                        "VAULT UNLOCKED": "#0EA5E9", "SALE": "#00897B",
                    }
                    ICON_MAP = {
                        "PRODUCT ADDED": "📦", "CATEGORY ADDED": "📁",
                        "STOCK ADJUSTMENT": "🔄", "PRODUCT DELETED": "🗑",
                        "SALE REVERSED": "↩️", "EXPENSE LOGGED": "💸",
                        "VAULT UNLOCKED": "🔓", "SALE": "✅",
                    }
                    for _, ar in df_act.iterrows():
                        ts_s = pd.to_datetime(ar["timestamp"]).strftime("%d %b %Y  %H:%M:%S") if ar["timestamp"] else "—"
                        col  = COLOR_MAP.get(ar["action_type"], "#607D8B")
                        icon = ICON_MAP.get(ar["action_type"], "📌")
                        st.markdown(f"""
                        <div style="background:#0f2345;border-left:4px solid {col};border-radius:0 10px 10px 0;
                             padding:10px 16px;margin-bottom:8px;display:flex;gap:12px;align-items:flex-start;">
                            <div style="font-size:1.3rem;flex-shrink:0;margin-top:1px;">{icon}</div>
                            <div style="flex:1;min-width:0;">
                                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;">
                                    <span style="background:{col};color:white;font-size:0.58rem;letter-spacing:1.5px;
                                         text-transform:uppercase;font-weight:800;padding:2px 8px;border-radius:4px;">
                                        {ar['action_type']}
                                    </span>
                                    <span style="font-family:'DM Mono',monospace;color:rgba(255,255,255,0.35);font-size:0.65rem;">
                                        {ts_s}
                                    </span>
                                </div>
                                <div style="color:rgba(255,255,255,0.85);font-size:0.83rem;margin-top:5px;
                                     word-break:break-word;line-height:1.45;">{ar['description']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="ssv-footer">
    <img src="{LOGO_SRC}" alt="logo"
         style="width:48px;height:48px;object-fit:contain;display:block;margin:0 auto 10px;" />
    <div style="font-family:'Nunito',sans-serif;font-size:1rem;font-weight:900;color:{WHITE};margin-bottom:4px;">
        ⭐ Special Stars Ventures
    </div>
    <div style="color:rgba(255,255,255,0.5);font-size:0.7rem;letter-spacing:1.5px;text-transform:uppercase;">
        Westlands opp Safaricom Center &nbsp;|&nbsp; +254 740 143 957 &nbsp;|&nbsp; info@specialstarsventures.co.ke
    </div>
    <div style="margin-top:8px;color:rgba(255,255,255,0.3);font-size:0.65rem;">
        Billing OS v9.0 &nbsp;©&nbsp; {now_eat().year} &nbsp;|&nbsp; All Rights Reserved
    </div>
    <div style="margin-top:6px;">
        <span style="color:{GREEN};font-size:0.72rem;font-weight:700;">
            ✨ Crafted by <span style="color:{ACCENT};">Lewis</span>
        </span>
    </div>
</div>
""", unsafe_allow_html=True)