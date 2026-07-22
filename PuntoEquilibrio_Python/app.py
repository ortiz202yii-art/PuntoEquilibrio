import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Punto de Equilibrio - Costos", layout="wide")

st.title("📊 Aplicativo de Punto de Equilibrio y Análisis de Sensibilidad")
st.caption("Basado en el modelo de Ingeniería de Costos y Presupuestos - Ing. José Alvarado")

# Sidebar - Datos Generales
st.sidebar.header("🏢 Datos de la Empresa")
usuario = st.sidebar.text_input("Usuario", "James Ortiz")
empresa = st.sidebar.text_input("Empresa / Proyecto", "Consultora Ing.")
rubro = st.sidebar.selectbox("Rubro", ["Servicios", "Comercial", "Industrial", "Otro"])

# Definición de Pestañas
tab1, tab2, tab3 = st.tabs(["📌 Punto de Equilibrio Base", "⚡ Análisis de Sensibilidad (10%)", "🎯 Utilidad & Punto de Cierre"])

# ==========================================
# TAB 1: PE BÁSICO Y GRÁFICO
# ==========================================
with tab1:
    st.subheader("1. Cálculo Básicos del Punto de Equilibrio")
    col1, col2 = st.columns(2)

    with col1:
        costos_fijos = st.number_input("Costos Fijos Totales (S/.)", min_value=0.0, value=2024000.0, step=1000.0)
        precio_venta = st.number_input("Precio de Venta Unitario - PV (S/.)", min_value=0.01, value=85.56, step=1.0)
        costo_variable = st.number_input("Costo Variable Unitario - CVu (S/.)", min_value=0.0, value=62.0, step=1.0)
        capacidad_max = st.number_input("Capacidad Máxima de Producción (Unidades/Horas)", min_value=1.0, value=160000.0, step=1000.0)

    if precio_venta <= costo_variable:
        st.error("⚠️ El precio de venta debe ser mayor al costo variable unitario para tener margen de contribución.")
    else:
        mc = precio_venta - costo_variable
        pe_q = costos_fijos / mc
        pe_v = pe_q * precio_venta
        pct_capacidad = (pe_q / capacidad_max) * 100
        margen_seguridad = ((capacidad_max - pe_q) / capacidad_max) * 100

        with col2:
            st.markdown("### 📋 Resultados Principales")
            st.success(f"**Punto de Equilibrio (Unidades):** {pe_q:,.2f} u.")
            st.info(f"**Punto de Equilibrio (Ventas):** S/. {pe_v:,.2f}")
            st.metric("Margen de Contribución Unitario (MC)", f"S/. {mc:,.2f}")
            st.metric("Uso de Capacidad en PE", f"{pct_capacidad:.2f} %")
            st.metric("Margen de Seguridad (al 100% de cap.)", f"{margen_seguridad:.2f} %")

        st.divider()
        st.subheader("📈 Gráfica del Punto de Equilibrio")
        
        # Gráfica
        max_x = max(capacidad_max, pe_q * 1.5)
        unidades = [0, max_x]
        ingresos = [0, max_x * precio_venta]
        costos_t = [costos_fijos, costos_fijos + (max_x * costo_variable)]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(unidades, ingresos, label="Ingresos Totales (V)", color="green", linewidth=2)
        ax.plot(unidades, costos_t, label="Costos Totales (CT)", color="red", linewidth=2)
        ax.axhline(y=costos_fijos, color="gray", linestyle="--", label="Costos Fijos (CF)")
        ax.plot(pe_q, pe_v, "ro", markersize=8, label=f"PE ({pe_q:,.0f} u.)")

        ax.set_xlabel("Nivel de Actividad / Unidades")
        ax.set_ylabel("Monto (S/.)")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

# ==========================================
# TAB 2: ANÁLISIS DE SENSIBILIDAD (PDF)
# ==========================================
with tab2:
    st.subheader("2. Análisis de Sensibilidad (Escenarios al ±10%)")
    st.write("Evaluación del impacto de variaciones en Costos y Precios sobre el Punto de Equilibrio:")

    if precio_venta > costo_variable:
        pe_base = costos_fijos / (precio_venta - costo_variable)

        # Escenario b1: -10% CF
        cf_b1 = costos_fijos * 0.9
        pe_b1 = cf_b1 / (precio_venta - costo_variable)
        red_b1 = ((pe_base - pe_b1) / pe_base) * 100

        # Escenario b2: -10% CVu
        cv_b2 = costo_variable * 0.9
        pe_b2 = costos_fijos / (precio_venta - cv_b2)
        red_b2 = ((pe_base - pe_b2) / pe_base) * 100

        # Escenario b3: -10% CF y -10% CVu
        pe_b3 = cf_b1 / (precio_venta - cv_b2)
        red_b3 = ((pe_base - pe_b3) / pe_base) * 100

        # Escenario b4: +10% PV
        pv_b4 = precio_venta * 1.10
        pe_b4 = costos_fijos / (pv_b4 - costo_variable)
        red_b4 = ((pe_base - pe_b4) / pe_base) * 100

        data_sensibilidad = {
            "Escenario": [
                "Base (Sin cambios)",
                "b1: Reducción del 10% en CF",
                "b2: Reducción del 10% en CVu",
                "b3: Reducción del 10% en CF y CVu",
                "b4: Incremento del 10% en PV"
            ],
            "Nuevo PE (Unidades)": [pe_base, pe_b1, pe_b2, pe_b3, pe_b4],
            "Reducción del PE (%)": [0.0, red_b1, red_b2, red_b3, red_b4]
        }

        df_sens = pd.DataFrame(data_sensibilidad)
        st.dataframe(df_sens.style.format({
            "Nuevo PE (Unidades)": "{:,.2f}",
            "Reducción del PE (%)": "{:.2f}%"
        }), use_container_width=True)

        st.info("💡 **Conclusión del Análisis:** Las reducciones simultáneas de costos o los aumentos de precio generan los impactos más altos en la optimización del Punto de Equilibrio.")

# ==========================================
# TAB 3: UTILIDAD DESEADA Y PUNTO DE CIERRE
# ==========================================
with tab3:
    st.subheader("3. Modulos Complementarios")
    col_u, col_c = st.columns(2)

    with col_u:
        st.markdown("### 🎯 Unidades para Utilidad Deseada")
        utilidad_deseada = st.number_input("Utilidad Neta Deseada (S/.)", min_value=0.0, value=500000.0, step=10000.0)
        if precio_venta > costo_variable:
            q_utilidad = (costos_fijos + utilidad_deseada) / (precio_venta - costo_variable)
            v_utilidad = q_utilidad * precio_venta
            st.success(f"**Unidades a vender:** {q_utilidad:,.2f} u.")
            st.info(f"**Facturación necesaria:** S/. {v_utilidad:,.2f}")

    with col_c:
        st.markdown("### 🛑 Punto de Cierre de Negocio (PC)")
        cf_vivo = st.number_input("Costo Fijo Vivo (Efectivo Real) (S/.)", min_value=0.0, value=costos_fijos * 0.85, step=1000.0)
        if precio_venta > costo_variable:
            pc_q = cf_vivo / (precio_venta - costo_variable)
            st.warning(f"**Punto de Cierre:** {pc_q:,.2f} u.")
            st.caption("Si las ventas caen por debajo de este nivel, la empresa no puede cubrir sus costos fijos operativos inmediatos.")
