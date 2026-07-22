import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Punto de Equilibrio", layout="centered")

st.title("📊 Aplicativo Punto de Equilibrio")

# Formulario de entrada
st.sidebar.header("Datos de la Empresa")
usuario = st.sidebar.text_input("Nombre del Usuario")
empresa = st.sidebar.text_input("Nombre de la Empresa")
rubro = st.sidebar.selectbox("Rubro", ["Comercial", "Industrial", "Servicios", "Otro"])

st.subheader("Datos Financieros")
costos_fijos = st.number_input("Costos Fijos Totales (S/.)", min_value=0.0, value=1000.0)
precio_venta = st.number_input("Precio de Venta por Unidad (S/.)", min_value=0.01, value=50.0)
costo_variable = st.number_input("Costo Variable por Unidad (S/.)", min_value=0.0, value=30.0)

if st.button("Calcular Punto de Equilibrio"):
    if precio_venta <= costo_variable:
        st.error("El precio de venta debe ser mayor al costo variable unitario.")
    else:
        # Cálculos
        margen_contribucion = precio_venta - costo_variable
        punto_equilibrio_q = costos_fijos / margen_contribucion
        punto_equilibrio_v = punto_equilibrio_q * precio_venta

        # Resultados
        st.success(f"**Punto de Equilibrio (Unidades):** {punto_equilibrio_q:,.2f} u.")
        st.info(f"**Punto de Equilibrio (Ventas):** S/. {punto_equilibrio_v:,.2f}")

        # Gráfico
        unidades = [0, punto_equilibrio_q * 2]
        ventas_totales = [0, (punto_equilibrio_q * 2) * precio_venta]
        costos_totales = [costos_fijos, costos_fijos + (punto_equilibrio_q * 2 * costo_variable)]

        fig, ax = plt.subplots()
        ax.plot(unidades, ventas_totales, label="Ingresos Totales", color="green")
        ax.plot(unidades, costos_totales, label="Costos Totales", color="red")
        ax.axhline(y=costos_fijos, color="gray", linestyle="--", label="Costos Fijos")
        ax.plot(punto_equilibrio_q, punto_equilibrio_v, "ro", label="Punto de Equilibrio")

        ax.set_xlabel("Unidades")
        ax.set_ylabel("Monto (S/.)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)