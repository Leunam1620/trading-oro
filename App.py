import streamlit as st
import yfinance as yf
import gradio as gr

# Definimos tu función maestra
def ejecutar_analisis_maestro():
    try:
        oro = yf.Ticker("GC=F")
        bono = yf.Ticker("^TNX")
        dxy = yf.Ticker("DX-Y.NYB")
        
        d = oro.history(period="1d")
        s = oro.history(period="1wk")
        
        def get_macro(tk):
            info = tk.fast_info
            cambio = ((info['last_price'] - info['previous_close']) / info['previous_close']) * 100
            return f"{info['last_price']:.2f} ({cambio:+.2f}%)"
            
        p = round(float(d['Close'].iloc[-1]), 2)
        mx_d, mn_d = round(float(d['High'].max()), 2), round(float(d['Low'].min()), 2)
        mx_s, mn_s = round(float(s['High'].max()), 2), round(float(s['Low'].min()), 2)
        
        f23_d, f61_d = mx_d - ((mx_d - mn_d) * 0.236), mx_d - ((mx_d - mn_d) * 0.618)
        f23_s, f61_s = mx_s - ((mx_s - mn_s) * 0.236), mx_s - ((mx_s - mn_s) * 0.618)
        
        return p, get_macro(bono), get_macro(dxy), mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s
    except: return None

# Interfaz Streamlit (para que funcione en el móvil sin bloqueos)
st.title("🚀 ESTACIÓN DE ANÁLISIS MAESTRA")
if st.button("🚀 EJECUTAR ESCANEO REAL"):
    res = ejecutar_analisis_maestro()
    if res:
        p, b, d, mx_d, mn_d, f23_d, f61_d, mx_s, mn_s, f23_s, f61_s = res
        st.metric("Precio Oro", f"${p}")
        col1, col2 = st.columns(2)
        col1.metric("Bono US10Y", b)
        col2.metric("Dólar DXY", d)
        
        st.subheader("📅 ANÁLISIS DIARIO")
        st.write(f"Venta > {f23_d:.2f} | Compra < {f61_d:.2f}")
        
        st.subheader("🗓️ ANÁLISIS SEMANAL")
        st.write(f"Venta > {f23_s:.2f} | Compra < {f61_s:.2f}")
    else: st.error("Error en la conexión.")
        
