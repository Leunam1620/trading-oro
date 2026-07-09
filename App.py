import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Estación Maestra PRO", layout="centered")

# --- AJUSTE DE PRECIO ---
# Cambia este número si la diferencia aumenta o disminuye
AJUSTE = 10.0 

def get_estado(precio, f23, f61):
    if precio >= f23: return "🔴 ZONA ALTA (VENDEDORA)"
    if precio <= f61: return "🟢 ZONA BAJA (COMPRADORA)"
    return "🟡 ZONA NEUTRA"

def obtener_macro(tk):
    i = tk.fast_info
    cambio = ((i['last_price'] - i['previous_close']) / i['previous_close']) * 100
    return f"{i['last_price']:.2f} ({cambio:+.2f}%)"

def ejecutar_analisis():
    try:
        oro, bono, dxy = yf.Ticker("GC=F"), yf.Ticker("^TNX"), yf.Ticker("DX-Y.NYB")
        d, s = oro.history(period="1d"), oro.history(period="1wk")
        
        # Aplicamos el ajuste de -10 al precio y a los máximos/mínimos para que todo cuadre
        p = round(float(d['Close'].iloc[-1]), 2) - AJUSTE
        mx_d = round(float(d['High'].max()), 2) - AJUSTE
        mn_d = round(float(d['Low'].min()), 2) - AJUSTE
        mx_s = round(float(s['High'].max()), 2) - AJUSTE
        mn_s = round(float(s['Low'].min()), 2) - AJUSTE
        
        f23_d, f61_d = mx_d - ((mx_d - mn_d) * 0.236), mx_d - ((mx_d - mn_d) * 0.618)
        f23_s, f61_s = mx_s - ((mx_s - mn_s) * 0.236), mx_s - ((mx_s - mn_s) * 0.618)
        
        return p, obtener_macro(bono), obtener_macro(dxy), mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s
    except: return None

# ... (El resto del código de interfaz sigue igual)
# (Asegúrate de copiar el resto del código desde el st.title hasta el st.rerun)
