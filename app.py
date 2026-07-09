import streamlit as st
import yfinance as yf
import requests

# Tus datos
TOKEN = "8816994018:AAFitwF_XmNdnTb_S2nF8faN8GAv-DQKmac"
CHAT_ID = "1642337232"

def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={mensaje}"
        requests.get(url, timeout=5)
    except: pass

st.title("🚀 ESTACIÓN DE ORO")

if st.button("🚀 ACTUALIZAR Y ANALIZAR"):
    oro = yf.Ticker("GC=F")
    d = oro.history(period="1d")
    p = round(float(d['Close'].iloc[-1]), 2)
    mx = round(float(d['High'].max()), 2)
    mn = round(float(d['Low'].min()), 2)
    
    f23 = mx - ((mx - mn) * 0.236)
    f61 = mx - ((mx - mn) * 0.618)
    
    st.metric("Precio Actual", f"${p}")
    st.write(f"Zona Venta: {f23:.2f}")
    st.write(f"Zona Compra: {f61:.2f}")
    
    if p >= f23 or p <= f61:
        enviar_telegram(f"🔔 Alerta: El Oro está en nivel clave: {p}")
        st.success("¡Alerta enviada a tu Telegram!")
      
