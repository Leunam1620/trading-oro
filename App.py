import streamlit as st
import yfinance as yf
import requests

TOKEN = "8816994018:AAFitwF_XmNdnTb_S2nF8faN8GAv-DQKmac"
CHAT_ID = "1642337232"

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
        requests.get(url, timeout=5)
    except: pass

st.title("🚀 ESTACIÓN DE ORO MAESTRA")

if st.button("🚀 ANALIZAR MERCADO AHORA"):
    oro = yf.Ticker("GC=F")
    d = oro.history(period="1d")
    p = round(float(d['Close'].iloc[-1]), 2)
    mx = round(float(d['High'].max()), 2)
    mn = round(float(d['Low'].min()), 2)
    
    f23 = mx - ((mx - mn) * 0.236)
    f61 = mx - ((mx - mn) * 0.618)
    
    st.metric("Precio Actual", f"${p}")
    
    col1, col2 = st.columns(2)
    col1.metric("Techo Diario", f"${mx}")
    col2.metric("Suelo Diario", f"${mn}")
    
    st.divider()
    st.subheader("🎯 ZONAS DE GATILLO")
    st.info(f"🔴 VENTA (Fib 23.6%): **${f23:.2f}**")
    st.warning(f"🟢 COMPRA (Fib 61.8%): **${f61:.2f}**")
    
    if p >= f23:
        st.error("¡PRECIO EN ZONA DE VENTA!")
        enviar_telegram(f"🔔 ALERTA DE VENTA: Oro en {p}")
    elif p <= f61:
        st.success("¡PRECIO EN ZONA DE COMPRA!")
        enviar_telegram(f"🔔 ALERTA DE COMPRA: Oro en {p}")
    else:
        st.write("Precio en zona neutral.")
      
