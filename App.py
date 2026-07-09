import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Estación Maestra PRO", layout="centered")

def analizar_macro_texto(precio, techo, suelo, bono, dxy):
    tendencia = "ALCISTA" if precio > (techo + suelo)/2 else "BAJISTA"
    return f"""
    **Resumen Macro:** El mercado muestra una tendencia {tendencia}. 
    El bono US10Y en {bono} y el DXY en {dxy} sugieren un flujo de capital {'hacia refugio' if 'positive' in str(bono) else 'hacia riesgo'}.
    **Análisis Técnico:** El precio actual (${precio}) se encuentra operando entre el soporte diario de ${suelo} y la resistencia de ${techo}.
    Si el nivel de ${techo} es superado con volumen, se invalidaría la estructura correctiva diaria.
    """

def ejecutar_analisis():
    try:
        oro = yf.Ticker("GC=F")
        bono = yf.Ticker("^TNX")
        dxy = yf.Ticker("DX-Y.NYB")
        d, s = oro.history(period="1d"), oro.history(period="1wk")
        
        # Datos básicos
        p = round(float(d['Close'].iloc[-1]), 2)
        mx_d, mn_d = round(float(d['High'].max()), 2), round(float(d['Low'].min()), 2)
        mx_s, mn_s = round(float(s['High'].max()), 2), round(float(s['Low'].min()), 2)
        
        # Macro
        macro_b = f"{bono.fast_info['last_price']:.2f}"
        macro_d = f"{dxy.fast_info['last_price']:.2f}"
        
        return p, macro_b, macro_d, mx_d, mn_d, mx_s, mn_s
    except: return None

st.title("🚀 ESTACIÓN MAESTRA PRO")

res = ejecutar_analisis()
if res:
    p, b, d, mx_d, mn_d, mx_s, mn_s = res
    
    st.text_input("Precio Oro", value=f"${p}")
    
    st.subheader("📅 ANÁLISIS DIARIO")
    st.text_input("Resistencia Diaria (Techo)", value=f"${mx_d}")
    st.text_input("Soporte Diario (Suelo)", value=f"${mn_d}")
    st.write(analizar_macro_texto(p, mx_d, mn_d, b, d))
    
    st.subheader("🗓️ ANÁLISIS SEMANAL")
    st.text_input("Resistencia Semanal", value=f"${mx_s}")
    st.text_input("Soporte Semanal", value=f"${mn_s}")
    st.write(f"**Resumen Semanal:** La estructura semanal mantiene un rango operativo entre ${mn_s} y ${mx_s}. La ruptura de estos niveles confirmará la tendencia de fondo para los próximos días.")
    
    st.write("---")
    st.write("⏳ Auto-actualización en 60s...")
    time.sleep(60)
    st.rerun()
else:
    st.write("Cargando datos...")
    time.sleep(5)
    st.rerun()
    
