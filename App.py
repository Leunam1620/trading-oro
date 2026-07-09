import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Estación Maestra PRO", layout="centered")

def get_estado(precio, f23, f61):
    if precio >= f23: return "🔴 ZONA ALTA (VENDEDORA)"
    if precio <= f61: return "🟢 ZONA BAJA (COMPRADORA)"
    return "🟡 ZONA NEUTRA"

def ejecutar_analisis():
    try:
        oro = yf.Ticker("GC=F")
        bono = yf.Ticker("^TNX")
        dxy = yf.Ticker("DX-Y.NYB")
        d, s = oro.history(period="1d"), oro.history(period="1wk")
        
        p = round(float(d['Close'].iloc[-1]), 2)
        mx_d, mn_d = round(float(d['High'].max()), 2), round(float(d['Low'].min()), 2)
        mx_s, mn_s = round(float(s['High'].max()), 2), round(float(s['Low'].min()), 2)
        
        f23_d, f61_d = mx_d - ((mx_d - mn_d) * 0.236), mx_d - ((mx_d - mn_d) * 0.618)
        f23_s, f61_s = mx_s - ((mx_s - mn_s) * 0.236), mx_s - ((mx_s - mn_s) * 0.618)
        
        b = f"{bono.fast_info['last_price']:.2f}"
        dxy_val = f"{dxy.fast_info['last_price']:.2f}"
        
        return p, b, dxy_val, mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s
    except: return None

st.title("🚀 ESTACIÓN MAESTRA PRO")

res = ejecutar_analisis()
if res:
    p, b, dxy_val, mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s = res
    
    st.text_input("Precio Oro", value=f"${p}")
    st.text_input("Bono US10Y", value=b)
    st.text_input("Dólar DXY", value=dxy_val)
    
    st.subheader("📅 ANÁLISIS DIARIO")
    st.text_input("Resistencia (Techo)", value=f"${mx_d}")
    st.text_input("Soporte (Suelo)", value=f"${mn_d}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_d:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_d:.2f}")
    st.text_input("Semáforo Diario", value=get_estado(p, f23_d, f61_d))
    st.write("**Resumen Macro Diario:** Análisis técnico basado en niveles institucionales. El precio actual opera bajo la influencia de la correlación con bonos y dólar.")
    
    st.subheader("🗓️ ANÁLISIS SEMANAL")
    st.text_input("Resistencia Semanal", value=f"${mx_s}")
    st.text_input("Soporte Semanal", value=f"${mn_s}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_s:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_s:.2f}")
    st.write("**Resumen Macro Semanal:** Estructura de mercado definida por rangos operativos amplios. La gestión de niveles clave en resistencias y soportes semanales determinará la tendencia de medio plazo.")
    
    st.write("---")
    st.write("⏳ Auto-actualización en 60s...")
    time.sleep(60)
    st.rerun()
else:
    st.write("Cargando datos...")
    time.sleep(5)
    st.rerun()
