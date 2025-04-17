import tkinter as tk

# Datos a mostrar
datos = [
    ["Nombre", "Edad", "Ciudad"],
    ["Ana", 25, "Madrid"],
    ["Luis", 30, "Barcelona"],
    ["Carlos", 22, "Valencia"]
]

# Crear la ventana
ventana = tk.Tk()
ventana.title("Tabla de datos")

# Recorrer filas y columnas para crear el grid
for fila in range(len(datos)):
    for col in range(len(datos[0])):
        valor = datos[fila][col]
        etiqueta = tk.Label(ventana, text=valor, borderwidth=1, relief="solid", padx=10, pady=5)
        etiqueta.grid(row=fila, column=col, sticky="nsew")

# Ajustar columnas para que se expandan
for col in range(len(datos[0])):
    ventana.grid_columnconfigure(col, weight=1)

ventana.mainloop()
