# Imports
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Application Configuration
st.set_page_config(
    page_title="Purchase Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg:        #F5F7FB;
    --white:     #FFFFFF;
    --border:    #E4E8F0;
    --text-1:    #111827;
    --text-2:    #374151;
    --text-3:    #9CA3AF;
    --teal:      #5CB8AA;
    --teal-dk:   #2C7A6E;
    --red:       #D95F4B;
    --sand:      #C9A96E;
    --blue:      #5073C8;
    --radius-sm: 10px;
    --radius:    14px;
    --shadow:    0 1px 6px rgba(0,0,0,0.05);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text-1) !important;
    font-size: 17px;
    line-height: 1.55;
}

#MainMenu, footer { visibility: hidden; }

.block-container {
    padding: 2.25rem 2.75rem !important;
    max-width: 1400px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #1A2035 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.75rem 1.25rem 1.25rem !important;
}
[data-testid="stSidebar"] * { color: #E5E9F4 !important; }

/* Navigation title */
.nav-title {
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45) !important;
    margin-bottom: 1.5rem;
    padding-left: 0.25rem;
}

[data-testid="stSidebar"] [data-baseweb="radio"] input[type="radio"] {
    display: none !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] {
    gap: 0 !important;
}

[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

/* NAV ITEM */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    padding: 1rem 1rem !important;
    margin-bottom: 12px !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

/* HOVER NAV ITEM*/
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.10) !important;
}

/* ACTIVE NAV ITEM */
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(61,158,143,0.25) !important;
    border-left: 4px solid #7DCFC5 !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] .stRadio label:has(input:checked) * {
    font-weight: 700 !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

.sidebar-stats {
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin-top: 2rem;
}
.sidebar-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    font-size: 0.9rem;
}
.sidebar-stat-label { color: rgba(255,255,255,0.4) !important; font-weight: 400; }
.sidebar-stat-val   { color: rgba(255,255,255,0.85) !important; font-weight: 600; }

/* PAGE HEADER */
.page-hdr { margin-bottom: 1.5rem; }
.page-hdr h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em;
    color: var(--text-1) !important;
    margin: 0 !important;
    line-height: 1.0 !important;
}
.page-hdr .sub {
    font-size: 1.1rem;
    color: var(--text-3);
    font-weight: 400;

    margin-top: 0.1rem !important;
    margin-bottom: 0 !important;

    line-height: 1.2 !important;
}

/* SECTION LABEL */
.sec-label {
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--text-3);
    margin: 0 0 0.75rem;
}

/* KPI GRID */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    border-radius: var(--radius);
    padding: 1.375rem 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 140px;
}
.kpi-card.red  { background: var(--red);  }
.kpi-card.sand { background: var(--sand); }
.kpi-card.teal { background: var(--teal); }
.kpi-card.blue { background: var(--blue); }
.kpi-top  { display: flex; justify-content: space-between; align-items: flex-start; }
/* Fix: larger icon, full opacity so it's visible */
.kpi-icon {
    font-size: 2.4rem;
    opacity: 1;
    line-height: 1;
}
.kpi-val  {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: #fff;
    line-height: 1;
    margin-top: 0.5rem;
}
.kpi-lbl  {
    font-size: 1rem;
    font-weight: 500;
    color: rgba(255,255,255,0.82);
    margin-top: 0.35rem;
}

/* WHITE CARD */
.card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 0.8rem 1.25rem 0.8rem 1.25rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
    border: 1px solid var(--border);
}
.card-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text-1);
    margin: 0 0 0.1rem;
    letter-spacing: -0.015em;
}
.card-sub {
    font-size: 1rem;
    color: var(--text-3);
    font-weight: 400;
    margin-bottom: 0.875rem;
}

/* FORM WIDGETS */
label[data-testid="stWidgetLabel"] p {
    font-size: 0.9rem !important;    
    font-weight: 600 !important;
    color: var(--text-2) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
.stSlider > div > div > div > div {
    background: var(--teal) !important;
}
.stNumberInput input, .stTextInput input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-size: 1rem !important;       /* was 0.9375rem */
    padding: 0.5rem 0.75rem !important;
}
.stSelectbox > div > div {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-size: 1rem !important;
}

[data-testid="stNumberInput"] div[data-testid="InputInstructions"] {
    display: none !important;
}

/* Primary button */
div[data-testid="stButton"] > button {
    background: var(--teal) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-size: 1rem !important;       /* was 0.9375rem */
    font-weight: 600 !important;
    padding: 0.7rem 1.75rem !important;
    width: 100% !important;
    transition: background 0.12s, transform 0.1s !important;
    letter-spacing: -0.01em;
}
div[data-testid="stButton"] > button:hover {
    background: var(--teal-dk) !important;
    transform: translateY(-1px) !important;
}

/* RESULT PANEL */
.result-wrap {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.5rem 1.625rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    margin-bottom: 1rem;
}
.result-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.result-badge.pos { background: #E6F7EE; color: #15803d; }
.result-badge.neg { background: #FEE2E2; color: #b91c1c; }

.result-prob {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    color: var(--text-1);
    line-height: 1;
}
.result-prob .unit {
    font-size: 1.6rem;
    color: var(--text-3);
    font-weight: 500;
    margin-left: 4px;   /* explicit gap between number and % */
}
.result-hint { font-size: 0.875rem; color: var(--text-3); margin-top: 0.35rem; }

/* Signal card */
.signal-card {
    background: var(--white);
    border-radius: var(--radius);
    padding: 1.375rem 1.5rem 1.25rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    margin-bottom: 1rem;
    /* no overflow:hidden — let chart breathe */
}

/* Empty state */
.empty-state {
    background: var(--bg);
    border: 1.5px dashed var(--border);
    border-radius: var(--radius);
    padding: 4rem 2rem;
    text-align: center;
    color: var(--text-3);
    font-size: 1rem;
    line-height: 1.8;
}
.empty-icon { font-size: 2rem; opacity: 0.3; margin-bottom: 0.75rem; }

/* Divider */
.divider { height: 1px; background: var(--border); margin: 1.25rem 0; }

[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:first-child > div:first-child > div:first-child {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

# Visualization Theme
COLORS = ["#D95F4B", "#C9A96E", "#3D9E8F", "#5073C8", "#9B5EA2", "#E07B54"]

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9CA3AF", size=15),
    margin=dict(t=12, b=12, l=4, r=4),
    xaxis=dict(
        gridcolor="#E4E8F0",
        linecolor="#E4E8F0",
        tickfont=dict(size=14, color="#9CA3AF"),
        title_font=dict(size=15, color="#6B7280"),
    ),
    yaxis=dict(
        gridcolor="#E4E8F0",
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=14, color="#9CA3AF"),
        title_font=dict(size=15, color="#6B7280"),
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=13, color="#6B7280"),
    ),
    colorway=COLORS,
)

def theme(fig, h=280, **kwargs):
    layout = _BASE_LAYOUT.copy()
    layout.update(kwargs)
    fig.update_layout(**layout, height=h)
    return fig


# LOAD MODEL PACKAGE
# The pickle is a dict bundling the trained model, the StandardScaler it was
# trained behind, the decision threshold, and the list of model input columns.
_pkg = joblib.load("prediction_model.pkl")
model            = _pkg["model"]
scaler           = _pkg["scaler"]
threshold        = float(_pkg.get("threshold", 0.5))
training_columns = list(_pkg["training_columns"])     # 39 cols the model expects
scaler_columns   = list(scaler.feature_names_in_)     # 47 cols the scaler expects


# LOAD ANALYTICS DATASET
# The real labelled training table, used to power the Analytics dashboard.
@st.cache_data
def load_analytics_df(path="combined_train.csv"):
    df = pd.read_csv(path)
    # Guard against stray categorical/interval dtypes when plotting.
    for col in df.columns:
        if str(df[col].dtype) in ("interval", "category"):
            df[col] = df[col].astype(str)
    return df

df = load_analytics_df()


def predict_purchase(user_inputs: dict):
    """Run the full training-time pipeline: assemble scaler columns ->
    StandardScaler.transform -> subset to model columns -> predict."""
    # Start every scaler column at 0 (mean after scaling), then fill knowns.
    row = {c: 0.0 for c in scaler_columns}
    for k, v in user_inputs.items():
        if k in row:
            row[k] = v
    X_full = pd.DataFrame([row])[scaler_columns]
    X_scaled = pd.DataFrame(scaler.transform(X_full), columns=scaler_columns)
    X_model = X_scaled[training_columns]
    prob = float(model.predict_proba(X_model)[0][1])
    pred = int(prob >= threshold)
    return prob, pred


# Sidebar
with st.sidebar:
    st.markdown(
        '<div class="nav-title">Navigation</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
    "",
    ["Customer Prediction", "Analytics Dashboard"],
    label_visibility="collapsed",
)
    page = "Prediction" if "Prediction" in page else "Analytics"

    # Sidebar summary stats
    purchase_rate_sb = df["target"].mean() * 100
    total_cust_sb    = len(df)
    st.markdown(
        f"""
        <div class="sidebar-stats">
            <div class="sidebar-stat">
                <span class="sidebar-stat-label">Customers</span>
                <span class="sidebar-stat-val">{total_cust_sb:,}</span>
            </div>
            <div class="sidebar-stat">
                <span class="sidebar-stat-label">Purchase rate</span>
                <span class="sidebar-stat-val">{purchase_rate_sb:.1f}%</span>
            </div>
            <div class="sidebar-stat">
                <span class="sidebar-stat-label">Model</span>
                <span class="sidebar-stat-val">Random Forest</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# PAGE 1 — PREDICTION
if page == "Prediction":

    st.markdown(
        """
        <div class="page-hdr">
            <h1>Customer Prediction</h1>
            <span class="sub">Score purchase likelihood from customer attributes</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.container()
        st.markdown('<p class="sec-label">Customer Profile</p>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age", 18, 100, 30)
            credit_limit = st.number_input("Credit Limit (USD)", 0, 100_000, 5_000, step=500)
            avg_pages_viewed = st.number_input("Avg Pages Viewed", 0, 100, 10)
        with c2:
            region = st.selectbox("Region", df["region"].unique())
            avg_order_value = st.number_input("Avg Order Value (USD)", 0, 5_000, 200, step=50)
            avg_session_duration = st.number_input("Session Duration (sec)", 0, 10_000, 300, step=30)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="sec-label">Engagement Signals</p>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
            loyalty_score = st.slider("Loyalty Score", 0, 100, 50)
            email_open_rate = st.slider("Email Open Rate", 0.0, 1.0, 0.5, step=0.01, format="%.2f")
        with c4:
            discount_usage_rate = st.slider("Discount Usage Rate", 0.0, 1.0, 0.3, step=0.01, format="%.2f")
            avg_review_score = st.slider("Avg Review Score", 0.0, 5.0, 3.5, step=0.1, format="%.1f")

        st.markdown("<br>", unsafe_allow_html=True)
        predict_btn = st.button("Run Prediction →")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        if predict_btn:
            user_inputs = {
                "discount_usage_rate":       discount_usage_rate,
                "loyalty_score":             loyalty_score,
                "avg_review_score":          avg_review_score,
                "email_open_rate":           email_open_rate,
                "credit_limit":              credit_limit,
                "avg_pages_viewed":          avg_pages_viewed,
                "avg_session_duration(sec)": avg_session_duration,
                "age":                       age,
                "avg_order_value(USD)":      avg_order_value,
            }
            prob, pred = predict_purchase(user_inputs)
            positive = pred == 1

            badge_cls  = "pos" if positive else "neg"
            badge_text = "Likely to purchase" if positive else "Unlikely to purchase"

            st.markdown(
                f"""
                <div class="result-wrap">
                    <div class="result-badge {badge_cls}">● &nbsp;{badge_text}</div>
                    <div class="result-prob">{prob*100:.1f}&nbsp;<span class="unit">%</span></div>
                    <div class="result-hint">Purchase probability</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            gauge_color = "#3D9E8F" if positive else "#D95F4B"
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(prob * 100, 1),
                number={"suffix": "%", "font": {"size": 28, "color": "#111827", "family": "Inter"}},
                gauge={
                    "axis": {
                        "range": [0, 100],
                        "tickcolor": "#E4E8F0",
                        "tickfont": {"size": 11, "color": "#9CA3AF"},
                        "nticks": 6,
                    },
                    "bar": {"color": gauge_color, "thickness": 0.2},
                    "bgcolor": "#F5F7FB",
                    "borderwidth": 0,
                    "steps": [{"range": [0, 100], "color": "#F5F7FB"}],
                    "threshold": {
                        "line": {"color": gauge_color, "width": 2.5},
                        "thickness": 0.72,
                        "value": round(prob * 100, 1),
                    },
                },
            ))
            fig_g = theme(fig_g, h=260, margin=dict(t=20, b=20, l=30, r=30))
            st.plotly_chart(fig_g, use_container_width=True)

            sigs = {
                "Loyalty":        loyalty_score / 100,
                "Email open":     email_open_rate,
                "Review score":   avg_review_score / 5,
                "Discount usage": discount_usage_rate,
            }
            sig_df = pd.DataFrame({"Signal": list(sigs.keys()), "Value": list(sigs.values())})
            fig_s = px.bar(
                sig_df, x="Value", y="Signal", orientation="h",
                color="Value",
                color_continuous_scale=["#E4E8F0", "#3D9E8F"],
                range_x=[0, 1],
            )
            fig_s.update_traces(marker_line_width=0, marker_cornerradius=4)
            fig_s.update_coloraxes(showscale=False)
            fig_s = theme(
                fig_s, h=220,
                margin=dict(t=16, b=16, l=8, r=16),
                xaxis_tickformat=".0%",
                xaxis_title=None,
                yaxis_title=None,
            )
            st.markdown(
                '<div class="signal-card"><div class="card-title">Signal Breakdown</div>'
                '<div class="card-sub">Normalised engagement inputs</div>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_s, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown(
                """
                <div class="empty-state">
                    <div class="empty-icon">◎</div>
                    Fill in customer attributes on the left<br>
                    and click <strong>Run Prediction</strong> to score.
                </div>
                """,
                unsafe_allow_html=True,
            )



# PAGE 2 — ANALYTICS
else:
    st.markdown(
        """
        <div class="page-hdr">
            <h1>Analytics Dashboard</h1>
            <span class="sub">Customer behaviour and purchase insights</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    purchase_rate = df["target"].mean() * 100
    avg_loyalty   = df["loyalty_score"].mean()
    avg_session   = df["avg_session_duration(sec)"].mean()
    total_cust    = len(df)

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card red">
                <div class="kpi-top"><span></span><span class="kpi-icon">👥</span></div>
                <div>
                    <div class="kpi-val">{total_cust:,}</div>
                    <div class="kpi-lbl">Total Customers</div>
                </div>
            </div>
            <div class="kpi-card sand">
                <div class="kpi-top"><span></span><span class="kpi-icon">🛒</span></div>
                <div>
                    <div class="kpi-val">{purchase_rate:.1f}%</div>
                    <div class="kpi-lbl">Purchase Rate</div>
                </div>
            </div>
            <div class="kpi-card teal">
                <div class="kpi-top"><span></span><span class="kpi-icon">⭐</span></div>
                <div>
                    <div class="kpi-val">{avg_loyalty:.1f}</div>
                    <div class="kpi-lbl">Average Loyalty Score</div>
                </div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-top"><span></span><span class="kpi-icon">🕑</span></div>
                <div>
                    <div class="kpi-val">{avg_session:.0f}s</div>
                    <div class="kpi-lbl">Average Session Duration</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ROW 1: Donut + Region bar
    r1a, r1b = st.columns([1, 2], gap="large")

    with r1a:
        counts = df["target"].value_counts().reset_index()
        counts.columns = ["target", "count"]
        counts["label"] = counts["target"].map({0: "No purchase", 1: "Purchase"})

        fig_d = go.Figure(go.Pie(
            labels=counts["label"],
            values=counts["count"],
            hole=0.68,
            marker=dict(colors=["#E4E8F0", "#3D9E8F"], line=dict(color="#FFFFFF", width=3)),
            textinfo="none",
            hovertemplate="%{label}: %{value:,}<extra></extra>",
        ))
        fig_d.add_annotation(
            text=f"<b>{purchase_rate:.1f}%</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=22, color="#111827", family="Inter"),
        )
        fig_d = theme(
            fig_d, h=240,
            showlegend=True,
            legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center"),
        )
        st.markdown(
            '<div class="card"><div class="card-title">Purchase Split</div>'
            '<div class="card-sub">Purchase outcome breakdown</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_d, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r1b:
        region_df = (
            df.groupby("region")["target"]
            .mean()
            .reset_index()
            .rename(columns={"target": "rate"})
        )
        region_df["pct"] = region_df["rate"] * 100
        # Many regions exist; show the top 12 by purchase rate for readability.
        region_df = region_df.sort_values("pct", ascending=False).head(12)
        region_df = region_df.sort_values("pct", ascending=True)

        fig_r = px.bar(
            region_df, x="pct", y="region", orientation="h",
            color="pct",
            color_continuous_scale=["#E4E8F0", "#C9A96E"],
            labels={"pct": "Purchase rate (%)", "region": ""},
            text=region_df["pct"].map(lambda v: f"{v:.1f}%"),
        )
        fig_r.update_traces(marker_line_width=0, marker_cornerradius=5, textposition="outside", textfont_size=12)
        fig_r.update_coloraxes(showscale=False)
        fig_r = theme(fig_r, h=240, xaxis_ticksuffix="%")
        st.markdown(
            '<div class="card"><div class="card-title">Purchase Performance by Region</div>'
            '<div class="card-sub">Top 12 regions by purchase rate</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 2: Age dist + Loyalty violin
    r2a, r2b = st.columns(2, gap="large")

    with r2a:
        fig_age = px.histogram(
            df, x="age",
            color=df["target"].map({0: "No purchase", 1: "Purchase"}),
            barmode="overlay", opacity=0.72, nbins=30,
            color_discrete_map={"No purchase": "#E4E8F0", "Purchase": "#D95F4B"},
            labels={"age": "Age", "color": ""},
        )
        fig_age.update_traces(marker_line_width=0)
        fig_age = theme(fig_age, h=260, legend=dict(orientation="h", y=1.08, x=1, xanchor="right"))
        st.markdown(
            '<div class="card"><div class="card-title">Age Distribution</div>'
            '<div class="card-sub">Age profile by purchase behaviour</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2b:
        fig_loy = px.violin(
            df,
            x=df["target"].map({0: "No purchase", 1: "Purchase"}),
            y="loyalty_score",
            color=df["target"].map({0: "No purchase", 1: "Purchase"}),
            color_discrete_map={"No purchase": "#C9A96E", "Purchase": "#3D9E8F"},
            box=True, points=False,
            labels={"x": "", "loyalty_score": "Loyalty score"},
        )
        fig_loy = theme(fig_loy, h=260, showlegend=False)
        st.markdown(
            '<div class="card"><div class="card-title">Loyalty Score vs Purchase</div>'
            '<div class="card-sub">Loyalty patterns by purchase outcome</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_loy, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 3: Email open + Session duration
    r3a, r3b = st.columns(2, gap="large")

    with r3a:
        fig_em = px.box(
            df,
            x=df["target"].map({0: "No purchase", 1: "Purchase"}),
            y="email_open_rate",
            color=df["target"].map({0: "No purchase", 1: "Purchase"}),
            color_discrete_map={"No purchase": "#C9A96E", "Purchase": "#5073C8"},
            points=False,
            labels={"x": "", "email_open_rate": "Email open rate"},
        )
        fig_em.update_traces(marker_line_width=0)
        fig_em = theme(fig_em, h=260, showlegend=False)
        st.markdown(
            '<div class="card"><div class="card-title">Email Open Rate</div>'
            '<div class="card-sub">Email engagement by purchase outcome</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_em, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r3b:
        fig_ses = px.box(
            df,
            x=df["target"].map({0: "No purchase", 1: "Purchase"}),
            y="avg_session_duration(sec)",
            color=df["target"].map({0: "No purchase", 1: "Purchase"}),
            color_discrete_map={"No purchase": "#D95F4B", "Purchase": "#3D9E8F"},
            points=False,
            labels={"x": "", "avg_session_duration(sec)": "Session duration (sec)"},
        )
        fig_ses.update_traces(marker_line_width=0)
        fig_ses = theme(fig_ses, h=260, showlegend=False)
        st.markdown(
            '<div class="card"><div class="card-title">Session Duration</div>'
            '<div class="card-sub">Browsing duration by purchase outcome</div>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_ses, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ROW 4: Correlation heatmap
    corr = df.select_dtypes(include=np.number).corr()

    fig_h = px.imshow(
        corr,
        aspect="auto",
        color_continuous_scale=[
            [0.0,  "#D95F4B"],
            [0.25, "#F5C4B3"],
            [0.5,  "#FFFFFF"],
            [0.75, "#9FE1CB"],
            [1.0,  "#1D9E75"],
        ],
        zmin=-1,
        zmax=1,
    )
    fig_h.update_traces(text=None, texttemplate=None)
    fig_h = theme(
        fig_h, h=440,
        coloraxis_colorbar=dict(
            thickness=10,
            len=0.75,
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1", "-0.5", "0", "+0.5", "+1"],
            tickfont=dict(size=11, color="#9CA3AF"),
            title=dict(text="r", font=dict(size=12, color="#6B7280")),
        ),
    )
    st.markdown(
        '<div class="card"><div class="card-title">Correlation Matrix</div>'
        '<div class="card-sub">Relationships between customer attributes</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig_h, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)