import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import pandas as pd

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="BinomPlay",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf5 100%);
    }
    
    /* Main title */
    .main-title {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Info cards */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    
    .info-card h4 {
        color: #667eea;
        margin: 0 0 8px 0;
        font-size: 16px;
    }
    
    .info-card p {
        color: #555;
        margin: 0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.2);
    }
    
    .metric-icon {
        font-size: 28px;
        margin-bottom: 5px;
    }
    
    .metric-label {
        color: #888;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #667eea;
        font-size: 32px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    
    .metric-desc {
        color: #999;
        font-size: 12px;
        font-style: italic;
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102,126,234,0.3);
        margin: 20px 0;
    }
    
    .result-label {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 10px;
    }
    
    .result-value {
        font-size: 56px;
        font-weight: 800;
        margin: 10px 0;
    }
    
    .result-desc {
        font-size: 14px;
        opacity: 0.85;
        margin-top: 10px;
    }
    
    /* Sidebar info */
    .sidebar-info {
        background: #f0f4ff;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 13px;
        color: #555;
        border-left: 3px solid #667eea;
    }
    
    /* Explanation box */
    .explanation-box {
        background: #fff9e6;
        padding: 15px 20px;
        border-radius: 12px;
        border-left: 4px solid #ffb800;
        margin: 15px 0;
    }
    
    .explanation-box b {
        color: #d97706;
    }
</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown('<div class="main-title">🎲 BinomPlay</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Binomial Distribution Calculator — Calculate probabilities easily</div>', unsafe_allow_html=True)

# ==================== SIDEBAR ====================
st.sidebar.markdown("## ⚙️ Parameters")

# n - number of trials
st.sidebar.markdown("### 1️⃣ Number of trials (n)")
n = st.sidebar.number_input(
    "n:",
    min_value=1,
    max_value=200,
    value=10,
    step=1,
    label_visibility="collapsed"
)
st.sidebar.markdown(
    '<div class="sidebar-info">📝 <b>n</b> — How many trials total?<br>Example: 10 questions, 5 throws</div>',
    unsafe_allow_html=True
)

# p - probability
st.sidebar.markdown("### 2️⃣ Success probability (p)")
p = st.sidebar.slider(
    "p:",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.01,
    label_visibility="collapsed"
)
st.sidebar.markdown(
    '<div class="sidebar-info">🎯 <b>p</b> — Success probability per trial (0-1)<br>Example: 0.6 = 60%</div>',
    unsafe_allow_html=True
)

# k - number of successes
st.sidebar.markdown("### 3️⃣ Number of successes (k)")
k = st.sidebar.number_input(
    "k:",
    min_value=0,
    max_value=n,
    value=min(6, n),
    step=1,
    label_visibility="collapsed"
)
st.sidebar.markdown(
    '<div class="sidebar-info">🎲 <b>k</b> — Required number of successes<br>Example: at least 6</div>',
    unsafe_allow_html=True
)

# Mode
st.sidebar.markdown("### 4️⃣ Calculation type")
mode = st.sidebar.radio(
    "Mode:",
    options=["P(X = k)", "P(X ≥ k)", "P(X ≤ k)"],
    index=1,
    label_visibility="collapsed"
)

# Mode description
mode_desc = {
    "P(X = k)": "🎯 <b>Exactly k</b> — Probability of exactly k successes",
    "P(X ≥ k)": "⬆️ <b>At least k</b> — k or more successes",
    "P(X ≤ k)": "⬇️ <b>At most k</b> — k or fewer successes"
}
st.sidebar.markdown(f'<div class="sidebar-info">{mode_desc[mode]}</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# ==================== CALCULATE ====================
dist = binom(n, p)

if mode == "P(X = k)":
    result = dist.pmf(k)
    label = f"P(X = {k})"
    explanation = f"Probability of exactly {k} successes"
elif mode == "P(X ≥ k)":
    result = dist.sf(k - 1)
    label = f"P(X ≥ {k})"
    explanation = f"Probability of at least {k} successes"
else:
    result = dist.cdf(k)
    label = f"P(X ≤ {k})"
    explanation = f"Probability of at most {k} successes"

# ==================== RESULT CARD ====================
st.markdown(f"""
<div class="result-card">
    <div class="result-label">📊 {label}</div>
    <div class="result-value">{result*100:.2f}%</div>
    <div class="result-desc">
        {explanation}<br>
        In about <b>{round(result*100)} out of 100 trials</b>, this result will occur
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== STATISTICS ====================
st.markdown("### 📐 Statistical Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-label">E[X] — Mean</div>
        <div class="metric-value">{n*p:.2f}</div>
        <div class="metric-desc">
            Expected number of successes<br>
            <small>n × p = {n} × {p} = {n*p:.2f}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-label">Var(X) — Variance</div>
        <div class="metric-value">{n*p*(1-p):.2f}</div>
        <div class="metric-desc">
            Spread of results<br>
            <small>n × p × (1-p)</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📉</div>
        <div class="metric-label">σ — Std Dev</div>
        <div class="metric-value">{np.sqrt(n*p*(1-p)):.2f}</div>
        <div class="metric-desc">
            Typical deviation from mean<br>
            <small>√Var(X)</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== EXPLANATION BLOCK ====================
st.markdown("### 💡 Explanation")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="info-card">
        <h4>📝 n = {n} — Number of trials</h4>
        <p>You perform <b>{n} trials</b> total. Example: answering {n} questions, throwing {n} times.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>🎯 p = {p:.2f} — Probability</h4>
        <p>Success probability per trial is <b>{p*100:.0f}%</b>. Each trial has {p*100:.0f}% chance of success.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card">
        <h4>🎲 k = {k} — Number of successes</h4>
        <p>Required number of successes is <b>{k}</b>. Calculating in "{mode}" mode.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-card">
        <h4>📊 {label} = {result*100:.2f}%</h4>
        <p>{explanation}. In <b>{round(result*100)} out of 100</b> trials, this result will occur.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CHART ====================
st.markdown("### 📈 Distribution Chart")

fig, ax = plt.subplots(figsize=(12, 5))

x = np.arange(0, n + 1)
y = dist.pmf(x) * 100

# Colors
colors = []
for i in x:
    highlight = False
    if mode == "P(X = k)" and i == k:
        highlight = True
    elif mode == "P(X ≥ k)" and i >= k:
        highlight = True
    elif mode == "P(X ≤ k)" and i <= k:
        highlight = True
    colors.append('#764ba2' if highlight else '#c5cae9')

bars = ax.bar(x, y, color=colors, edgecolor='white', linewidth=1.5)

# Add values above bars
for bar, val in zip(bars, y):
    if val > 0.5:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f'{val:.1f}%',
            ha='center',
            fontsize=9,
            fontweight='bold',
            color='#333'
        )

# Add E[X] line
ax.axvline(x=n*p, color='red', linestyle='--', alpha=0.7, label=f'E[X] = {n*p:.2f}')

ax.set_xlabel('k — Number of successes', fontsize=12, fontweight='bold')
ax.set_ylabel('Probability (%)', fontsize=12, fontweight='bold')
ax.set_title(f'Binomial Distribution (n={n}, p={p})', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.legend()
ax.set_xticks(range(0, n + 1, max(1, n // 20)))

st.pyplot(fig)

st.markdown("---")

# ==================== TABLE ====================
st.markdown("### 📋 Full Table")

# Explanation
st.markdown("""
<div class="explanation-box">
<b>📖 How to read the table:</b><br>
• <b>k</b> — Number of successes (from 0 to n)<br>
• <b>P(X = k)</b> — Probability of exactly k successes<br>
• <b>P(X ≤ k)</b> — Probability of k or fewer<br>
• <b>P(X ≥ k)</b> — Probability of k or more
</div>
""", unsafe_allow_html=True)

# Data
table_data = []
for i in range(n + 1):
    table_data.append({
        "k": i,
        "P(X = k)": f"{dist.pmf(i)*100:.2f}%",
        "P(X ≤ k)": f"{dist.cdf(i)*100:.2f}%",
        "P(X ≥ k)": f"{dist.sf(i-1)*100:.2f}%"
    })

df = pd.DataFrame(table_data)

# Display table
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    height=400
)

st.markdown("---")

# ==================== FORMULA ====================
with st.expander("📐 Mathematical Formula"):
    st.latex(r"P(X = k) = \binom{n}{k} \cdot p^k \cdot (1-p)^{n-k}")
    st.markdown(f"""
    **Where:**
    - $n = {n}$ — Number of trials
    - $p = {p:.2f}$ — Success probability
    - $k = {k}$ — Number of successes
    - $\\binom{{n}}{{k}} = \\frac{{n!}}{{k!(n-k)!}}$ — Combination
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #999; font-size: 13px; padding: 20px;">
        🎲 <b>BinomPlay</b> — Streamlit App | Binomial Distribution Calculator<br>
        <small>Made with ❤️ using Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)
