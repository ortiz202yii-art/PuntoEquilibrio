import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt


def calcular_punto_equilibrio():
  try:
    # 1. Obtener datos de la Empresa y Usuario
    usuario = txt_usuario.get().strip()
    empresa = txt_empresa.get().strip()
    rubro = combo_rubro.get()

    if not usuario or not empresa:
      messagebox.showwarning(
          "Campos Vacíos",
          "Por favor, ingresa el nombre del usuario y de la empresa.",
      )
      return

    # 2. Obtener datos financieros
    cf = float(txt_cf.get())
    pv = float(txt_pv.get())
    cvu = float(txt_cvu.get())
    q_planeadas = float(txt_q.get())

    # 3. Validación de margen
    mc = pv - cvu
    if mc <= 0:
      messagebox.showwarning(
          "Atención",
          "El Precio de Venta (PV) debe ser mayor al CVu para generar"
          " margen.",
      )
      return

    # 4. Fórmulas de Ingeniería de Costos
    pe_uf = cf / mc
    pe_mon = pe_uf * pv
    ms = (
        ((q_planeadas - pe_uf) / q_planeadas) * 100 if q_planeadas > 0 else 0
    )
    utilidad_planeada = (q_planeadas * mc) - cf

    # 5. Generar Reporte Personalizado
    reporte = (
      f"--- INFORMACIÓN DE LA ORGANIZACIÓN ---\n"
      f"• Elaborado por: {usuario}\n"
      f"• Empresa: {empresa}\n"
      f"• Sector / Rubro: {rubro}\n\n"
      f"--- RESULTADOS DEL PUNTO DE EQUILIBRIO ---\n"
      f"• Margen de Contribución (MC): S/. {mc:.2f}\n"
      f"• PE (Unidades Físicas): {pe_uf:,.2f} u.\n"
      f"• PE (Unidades Monetarias): S/. {pe_mon:,.2f}\n"
      f"• Margen de Seguridad (MS): {ms:.2f}%\n"
      f"• Utilidad estimada ({q_planeadas:,.0f} u.): S/."
      f" {utilidad_planeada:,.2f}\n\n"
      f"--- ANÁLISIS DE SENSIBILIDAD (-10%) ---\n"
      f"• Reduciendo CF 10%: Nuevo PE = {(cf * 0.9) / mc:,.2f} u.\n"
      f"• Reduciendo CVu 10%: Nuevo PE = {cf / (pv - (cvu * 0.9)):,.2f} u.\n"
      f"• Subiendo PV 10%: Nuevo PE = {cf / ((pv * 1.1) - cvu):,.2f} u."
  )

    lbl_resultado.config(text=reporte)

    # 6. Generar Gráfico Personalizado con el Nombre de la Empresa
    q_max = int(max(pe_uf * 2, q_planeadas * 1.2))
    cantidades = list(range(0, q_max + 1, max(1, q_max // 30)))

    ingresos = [pv * q for q in cantidades]
    costos_totales = [cf + (cvu * q) for q in cantidades]

    plt.figure(figsize=(8, 5))
    plt.plot(
        cantidades,
        ingresos,
        label="Ingresos Totales (IT)",
        color="blue",
        linewidth=2,
    )
    plt.plot(
        cantidades,
        costos_totales,
        label="Costos Totales (CT)",
        color="red",
        linewidth=2,
    )
    plt.axhline(
        y=cf,
        color="gray",
        linestyle="--",
        label="Costos Fijos (CF)",
        alpha=0.7,
    )
    plt.plot(
        pe_uf, pe_mon, "ro", markersize=8, label=f"PE ({pe_uf:,.1f} u.)"
    )

    plt.title(
        f"Punto de Equilibrio - {empresa.upper()}\nAnalista: {usuario} |"
        f" Sector: {rubro}"
    )
    plt.xlabel("Nivel de Actividad / Unidades (Q)")
    plt.ylabel("Soles (S/.)")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.show()

  except ValueError:
    messagebox.showerror(
        "Error", "Ingresa números válidos en los campos financieros."
    )


# --- INTERFAZ GRÁFICA ---
root = tk.Tk()
root.title("Sistema de Costos - Punto de Equilibrio")
root.geometry("480x680")
root.resizable(False, False)

# Encabezado
title_label = tk.Label(
    root,
    text="Ingeniería de Costos y Presupuestos\nAnálisis de Punto de"
    " Equilibrio",
    font=("Arial", 11, "bold"),
    fg="#1F4E78",
)
title_label.pack(pady=8)

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=5)

# 1. Datos de la Empresa y Usuario
tk.Label(
    frame_inputs, text="Nombre del Usuario / Analista:", font=("Arial", 9)
).grid(row=0, column=0, sticky="w", pady=2, padx=5)
txt_usuario = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_usuario.insert(0, "Estudiante")
txt_usuario.grid(row=0, column=1, pady=2, padx=5)

tk.Label(frame_inputs, text="Empresa / Razón Social:", font=("Arial", 9)).grid(
    row=1, column=0, sticky="w", pady=2, padx=5
)
txt_empresa = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_empresa.insert(0, "Consultora de Ingeniería")
txt_empresa.grid(row=1, column=1, pady=2, padx=5)

tk.Label(frame_inputs, text="Sector / Rubro:", font=("Arial", 9)).grid(
    row=2, column=0, sticky="w", pady=2, padx=5
)
combo_rubro = ttk.Combobox(
    frame_inputs,
    values=["Servicios", "Comercialización", "Manufactura / Industrial"],
    state="readonly",
    width=17,
)
combo_rubro.set("Servicios")
combo_rubro.grid(row=2, column=1, pady=2, padx=5)

# Separador visual
ttk.Separator(frame_inputs, orient="horizontal").grid(
    row=3, column=0, columnspan=2, sticky="ew", pady=8
)

# 2. Datos Financieros
tk.Label(
    frame_inputs, text="Costos Fijos Totales (CF) [S/.]:", font=("Arial", 9)
).grid(row=4, column=0, sticky="w", pady=2, padx=5)
txt_cf = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_cf.insert(0, "60000")
txt_cf.grid(row=4, column=1, pady=2, padx=5)

tk.Label(
    frame_inputs, text="Precio de Venta Unitario (PV) [S/.]:", font=("Arial", 9)
).grid(row=5, column=0, sticky="w", pady=2, padx=5)
txt_pv = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_pv.insert(0, "120")
txt_pv.grid(row=5, column=1, pady=2, padx=5)

tk.Label(
    frame_inputs, text="Costo Variable Unitario (CVu) [S/.]:", font=("Arial", 9)
).grid(row=6, column=0, sticky="w", pady=2, padx=5)
txt_cvu = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_cvu.insert(0, "70")
txt_cvu.grid(row=6, column=1, pady=2, padx=5)

tk.Label(
    frame_inputs, text="Ventas Planeadas [Unidades]:", font=("Arial", 9)
).grid(row=7, column=0, sticky="w", pady=2, padx=5)
txt_q = tk.Entry(frame_inputs, font=("Arial", 9), width=20)
txt_q.insert(0, "2000")
txt_q.grid(row=7, column=1, pady=2, padx=5)

# Botón
btn_calcular = tk.Button(
    root,
    text="Calcular y Generar Informe",
    font=("Arial", 10, "bold"),
    bg="#007ACC",
    fg="white",
    padx=10,
    pady=4,
    command=calcular_punto_equilibrio,
)
btn_calcular.pack(pady=10)

# Caja de Salida
lbl_resultado = tk.Label(
    root,
    text="Ingresa los datos para generar el reporte.",
    font=("Consolas", 8),
    justify="left",
    bg="#F8F9FA",
    relief="sunken",
    width=58,
    height=16,
    anchor="nw",
    padx=8,
    pady=8,
)
lbl_resultado.pack(pady=5)

root.mainloop()
