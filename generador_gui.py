import secrets
import string
import tkinter as tk
from tkinter import messagebox, Toplevel

def generar_contrasena(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos):
    """Genera una contraseña segura basada en las opciones seleccionadas."""
    caracteres = string.ascii_lowercase
    if incluir_mayusculas:
        caracteres += string.ascii_uppercase
    if incluir_numeros:
        caracteres += string.digits
    if incluir_simbolos:
        caracteres += string.punctuation
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena

def evaluar_fuerza_contrasena(contrasena):
    """Evalúa la fuerza de la contraseña y devuelve una descripción y color."""
    if len(contrasena) < 8:
        return "Débil", "#FF0000"  
    elif any(char.isdigit() for char in contrasena) and any(char.isupper() for char in contrasena) and any(char in string.punctuation for char in contrasena):
        return "Fuerte", "#00FF00"  
    else:
        return "Media", "#FFFF00"  

def mostrar_contrasena():
    """Muestra la contraseña generada en el área de texto y actualiza el historial."""
    try:
        longitud = int(entry_longitud.get())
        if longitud < 8:
            messagebox.showwarning("Advertencia", "La longitud mínima es 8 caracteres.")
            return
        incluir_mayusculas = var_mayusculas.get()
        incluir_numeros = var_numeros.get()
        incluir_simbolos = var_simbolos.get()
        contrasena = generar_contrasena(longitud, incluir_mayusculas, incluir_numeros, incluir_simbolos)
        entry_resultado.config(state=tk.NORMAL)
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(tk.END, contrasena)
        entry_resultado.config(state=tk.DISABLED)

        historial.insert(0, contrasena)
        actualizar_historial()

        fuerza, color = evaluar_fuerza_contrasena(contrasena)
        etiqueta_fuerza.config(text=f"Fuerza: {fuerza}", bg=color)
        barra_fuerza.config(bg=color)
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número entero válido.")

def copiar_al_portapapeles():
    """Copia la contraseña al portapapeles."""
    ventana.clipboard_clear()
    ventana.clipboard_append(entry_resultado.get())
    messagebox.showinfo("Copiado", "La contraseña ha sido copiada al portapapeles.")

def mostrar_ocultar_contrasena():
    """Muestra u oculta la contraseña en el área de texto."""
    if entry_resultado.cget("show") == "*":
        entry_resultado.config(show="") 
        boton_mostrar.config(text="Ocultar Contraseña")
    else:
        entry_resultado.config(show="*") 
        boton_mostrar.config(text="Mostrar Contraseña")

def seleccionar_contrasena(e):
    """Selecciona una contraseña del historial para mostrarla."""
    seleccion = listbox_historial.curselection()
    if seleccion:
        contrasena = listbox_historial.get(seleccion[0])
        entry_resultado.config(state=tk.NORMAL)
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(tk.END, contrasena)
        entry_resultado.config(state=tk.DISABLED)

        fuerza, color = evaluar_fuerza_contrasena(contrasena)
        etiqueta_fuerza.config(text=f"Fuerza: {fuerza}", bg=color)
        barra_fuerza.config(bg=color)

def actualizar_historial():
    """Actualiza el historial mostrado en la lista."""
    if 'listbox_historial' in globals():
        listbox_historial.delete(0, tk.END)
        for contrasena in historial:
            listbox_historial.insert(tk.END, contrasena)

def mostrar_historial():
    """Muestra el historial de contraseñas en una nueva ventana emergente."""
    historial_ventana = Toplevel(ventana)
    historial_ventana.title("Historial de Contraseñas")
    historial_ventana.geometry("400x300")
    historial_ventana.configure(bg="#e0f7fa")
    
    etiqueta_historial = tk.Label(historial_ventana, text="Historial de Contraseñas:", font=fuente_texto, bg="#e0f7fa", fg="#00796b")
    etiqueta_historial.pack(pady=5)
    
    global listbox_historial
    listbox_historial = tk.Listbox(historial_ventana, width=50, height=10, font=fuente_entrada, bg="#ffffff", fg="#000000")
    listbox_historial.pack(side=tk.LEFT, padx=10, pady=10)
    listbox_historial.bind("<<ListboxSelect>>", seleccionar_contrasena)
    
    scrollbar = tk.Scrollbar(historial_ventana)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox_historial.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox_historial.yview)
    
    actualizar_historial() 

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Contraseñas Seguras")
ventana.geometry("800x600") 
ventana.configure(bg="#e0f7fa")

fuente_titulo = ("Helvetica", 18, "bold")
fuente_texto = ("Helvetica", 12)
fuente_entrada = ("Helvetica", 12)

def crear_widget_redondeado(parent, widget_type, **kwargs):
    """Crea un widget con bordes redondeados (simulado)."""
    widget = widget_type(parent, **kwargs)
    widget.pack(padx=20, pady=10, fill=tk.X)
    return widget

titulo = crear_widget_redondeado(ventana, tk.Label, text="Generador de Contraseñas Seguras", font=fuente_titulo, bg="#e0f7fa", fg="#004d40")

etiqueta = crear_widget_redondeado(ventana, tk.Label, text="Introduce la longitud deseada para la contraseña (mínimo 8):", font=fuente_texto, bg="#e0f7fa", fg="#00796b")

entry_longitud = crear_widget_redondeado(ventana, tk.Entry, font=fuente_entrada, width=50)

# Opciones de configuración
frame_opciones = tk.Frame(ventana, bg="#e0f7fa")
frame_opciones.pack(pady=10)

var_mayusculas = tk.BooleanVar()
var_numeros = tk.BooleanVar()
var_simbolos = tk.BooleanVar()

check_mayusculas = tk.Checkbutton(frame_opciones, text="Incluir Mayúsculas", variable=var_mayusculas, bg="#e0f7fa", font=fuente_texto, selectcolor="#a5d6a7", activebackground="#b2dfdb")
check_mayusculas.pack(side=tk.LEFT, padx=5)

check_numeros = tk.Checkbutton(frame_opciones, text="Incluir Números", variable=var_numeros, bg="#e0f7fa", font=fuente_texto, selectcolor="#a5d6a7", activebackground="#b2dfdb")
check_numeros.pack(side=tk.LEFT, padx=5)

check_simbolos = tk.Checkbutton(frame_opciones, text="Incluir Símbolos", variable=var_simbolos, bg="#e0f7fa", font=fuente_texto, selectcolor="#a5d6a7", activebackground="#b2dfdb")
check_simbolos.pack(side=tk.LEFT, padx=5)

boton_generar = crear_widget_redondeado(ventana, tk.Button, text="Generar Contraseña", font=fuente_entrada, bg="#004d40", fg="white", relief=tk.RAISED, command=mostrar_contrasena)

boton_copiar = crear_widget_redondeado(ventana, tk.Button, text="Copiar al Portapapeles", font=fuente_entrada, bg="#00796b", fg="white", relief=tk.RAISED, command=copiar_al_portapapeles)

boton_mostrar = crear_widget_redondeado(ventana, tk.Button, text="Mostrar Contraseña", font=fuente_entrada, bg="#004d40", fg="white", relief=tk.RAISED, command=mostrar_ocultar_contrasena)

entry_resultado = tk.Entry(ventana, font=fuente_entrada, width=60, bg="#ffffff", fg="#000000", borderwidth=2, relief=tk.GROOVE, show="*")
entry_resultado.pack(padx=20, pady=10)

etiqueta_fuerza = tk.Label(ventana, text="Fuerza: ", font=fuente_texto, bg="#e0f7fa", fg="#004d40")
etiqueta_fuerza.pack(pady=5)

barra_fuerza = tk.Label(ventana, height=2, width=60, bg="#FF0000")
barra_fuerza.pack(pady=5)

historial = []

boton_historial = crear_widget_redondeado(ventana, tk.Button, text="Mostrar Historial", font=fuente_entrada, bg="#004d40", fg="white", relief=tk.RAISED, command=mostrar_historial)

ventana.mainloop()
