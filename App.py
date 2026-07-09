import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="Estación Maestra PRO", layout="centered")

def obtener_macro(tk):
    i = tk.fast_info
    cambio = ((i['last_price'] - i['previous_close']) / i['previous_close']) * 100
    return f"{i['last_price']:.2f} ({cambio:+.2f}%)"

def generar_analisis_fundamental(precio, mx, mn, bono_val, dxy_val):
    # Lógica de análisis fundamental simplificada basada en correlaciones
    tendencia_dxy = "Fuerte" if float(dxy_val.split('(')[0]) > 102 else "Débil"
    sentimiento = "Aversión al riesgo" if float(bono_val.split('(')[0]) > 4.5 else "Búsqueda de riesgo"
    
    return f"""
    **Análisis Fundamental:** - El dólar (DXY) se encuentra en una posición {tendencia_dxy}, lo que ejerce presión directa sobre el Oro. 
    - El mercado muestra un sentimiento de {sentimiento} (Bono 10Y: {bono_val}).
    - La correlación actual indica que si el bono sigue subiendo, el Oro podría testear el soporte de ${mn}.
    """

def ejecutar_analisis():
    try:
        oro, bono, dxy = yf.Ticker("GC=F"), yf.Ticker("^TNX"), yf.Ticker("DX-Y.NYB")
        d, s = oro.history(period="1d"), oro.history(period="1wk")
        
        p = round(float(d['Close'].iloc[-1]), 2)
        mx_d, mn_d = round(float(d['High'].max()), 2), round(float(d['Low'].min()), 2)
        mx_s, mn_s = round(float(s['High'].max()), 2), round(float(s['Low'].min()), 2)
        
        f23_d, f61_d = mx_d - ((mx_d - mn_d) * 0.236), mx_d - ((mx_d - mn_d) * 0.618)
        f23_s, f61_s = mx_s - ((mx_s - mn_s) * 0.236), mx_s - ((mx_s - mn_s) * 0.618)
        
        return p, obtener_macro(bono), obtener_macro(dxy), mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s
    except: return None

st.title("🚀 ESTACIÓN MAESTRA PRO")

res = ejecutar_analisis()
if res:
    p, b, d, mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s = res
    
    st.text_input("Precio Oro", value=f"${p}")
    st.text_input("Bono US10Y", value=b)
    st.text_input("Dólar DXY", value=d)
    
    st.subheader("📅 ANÁLISIS DIARIO")
    st.text_input("Resistencia", value=f"${mx_d}")
    st.text_input("Soporte", value=f"${mn_d}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_d:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_d:.2f}")
    st.write(generar_analisis_fundamental(p, mx_d, mn_d, b, d))
    
    st.subheader("🗓️ ANÁLISIS SEMANAL")
    st.text_input("Resistencia Semanal", value=f"${mx_s}")
    st.text_input("Soporte Semanal", value=f"${mn_s}")
    st.text_input("Venta Fib (23.6%)", value=f"${f23_s:.2f}")
    st.text_input("Compra Fib (61.8%)", value=f"${f61_s:.2f}")
    st.write("**Análisis Semanal:** La tendencia macro semanal está condicionada por la inflación implícita en los bonos. Mientras el soporte semanal en ${mn_s} no sea vulnerado, la estructura de compras se mantiene vigente.")
    
    time.sleep(60)
    st.rerun()
    
