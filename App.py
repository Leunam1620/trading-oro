import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Estación Maestra PRO", layout="centered")

# --- AJUSTE DE PRECIO ---
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
        
        p = round(float(d['Close'].iloc[-1]), 2) - AJUSTE
        mx_d = round(float(d['High'].max()), 2) - AJUSTE
        mn_d = round(float(d['Low'].min()), 2) - AJUSTE
        mx_s = round(float(s['High'].max()), 2) - AJUSTE
        mn_s = round(float(s['Low'].min()), 2) - AJUSTE
        
        f23_d, f61_d = mx_d - ((mx_d - mn_d) * 0.236), mx_d - ((mx_d - mn_d) * 0.618)
        f23_s, f61_s = mx_s - ((mx_s - mn_s) * 0.236), mx_s - ((mx_s - mn_s) * 0.618)
        
        return p, obtener_macro(bono), obtener_macro(dxy), mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s
    except: return None

st.title("🚀 ESTACIÓN MAESTRA PRO")

res = ejecutar_analisis()
if res:
    p, b, d, mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s = res
    
    st.text_input("Precio Oro", value=f"${p:.2f}")
    st.text_input("Bono US10Y", value=b)
    st.text_input("Dólar DXY", value=d)
    
    st.subheader("📅 ANÁLISIS DIARIO")
    st.text_input("Resistencia (Techo)", value=f"${mx_d:.2f}")
    st.text_input("Soporte (Suelo)", value=f"${mn_d:.2f}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_d:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_d:.2f}")
    st.text_input("SEMÁFORO DIARIO", value=get_estado(p, f23_d, f61_d))
    st.write("**Análisis fundamental:** Tendencias marcadas por la correlación entre bonos y divisa. Niveles técnicos ajustados.")
    
    st.subheader("🗓️ ANÁLISIS SEMANAL")
    st.text_input("Resistencia Semanal", value=f"${mx_s:.2f}")
    st.text_input("Soporte Semanal", value=f"${mn_s:.2f}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_s:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_s:.2f}")
    st.write("**Análisis Semanal:** Estructura macro en fase de consolidación técnica sobre soportes clave.")
    
    st.write("---")
    st.write("⏳ Auto-actualización en 60s...")
    time.sleep(60)
    st.rerun()
else:
    st.write("Cargando datos...")
    time.sleep(5)
    st.rerun()
    
