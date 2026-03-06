import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. إعدادات الإمبراطورية (الواجهة المظلمة)
st.set_page_config(page_title="Quant Empire", layout="wide", page_icon="🌍", initial_sidebar_state="expanded")

st.title("🌍 مركز القيادة السيادي (Quant Empire)")
st.markdown("---")

# 2. القائمة الجانبية (أجهزة الاستشعار)
st.sidebar.header("🎛️ لوحة التحكم")
market = st.sidebar.selectbox("اختر السوق:", ["العملات الرقمية (Crypto)", "المعادن (Metals)", "الفوركس (Forex)"])

assets = {
    "العملات الرقمية (Crypto)": {"البتكوين (BTC)": "BTC-USD", "الإيثريوم (ETH)": "ETH-USD"},
    "المعادن (Metals)": {"الذهب (Gold)": "GC=F", "الفضة (Silver)": "SI=F"},
    "الفوركس (Forex)": {"يورو/دولار (EUR/USD)": "EURUSD=X", "باوند/دولار (GBP/USD)": "GBPUSD=X"}
}

selected_asset = st.sidebar.selectbox("اختر الأصل المالي:", list(assets[market].keys()))
ticker = assets[market][selected_asset]

# 3. محرك اختراق البيانات (الذاكرة المؤقتة لمنع الحظر)
@st.cache_data(ttl=60)
def get_data(symbol):
    end = datetime.now()
    start = end - timedelta(days=7) # سحب بيانات آخر 7 أيام
    df = yf.download(symbol, start=start, end=end, interval="15m")
    return df

with st.spinner('جاري الاتصال بالأقمار الصناعية وسحب البيانات الحية...'):
    df = get_data(ticker)

# 4. رسم الشموع اليابانية الحية
if not df.empty:
    current_price = df['Close'].iloc[-1].item()
    st.sidebar.markdown("---")
    st.sidebar.metric(label=f"السعر اللحظي", value=f"{current_price:,.2f} $")
    st.sidebar.success("الرادار متصل: البيانات مشفرة وآمنة 🟢")

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'].squeeze(),
                    high=df['High'].squeeze(),
                    low=df['Low'].squeeze(),
                    close=df['Close'].squeeze(),
                    name="Market Data")])

    fig.update_layout(
        title=f"الرسم البياني اللحظي: {selected_asset} (إطار 15 دقيقة)",
        yaxis_title="السعر (دولار)",
        xaxis_title="الوقت",
        template="plotly_dark",
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ فشل في جلب البيانات، السوق قد يكون مغلقاً أو السيرفر محظور.")
