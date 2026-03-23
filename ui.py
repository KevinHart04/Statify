import customtkinter as ctk
import pandas as pd
import subprocess
import threading
import os
from tkinter import filedialog, messagebox
from PIL import Image
from tksheet import Sheet

# Configuración visual AMOLED Orange
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class InfoStatKillerApp(ctk.CTk):
    """
    Aplicación GUI principal que envuelve el script CLI frecuencia.R.
    Maneja la carga de datos, visualización en grilla y orquestación de comandos.
    """
    def __init__(self):
        super().__init__()

        self.title("Estadística Descriptiva - El Killer de InfoStat")
        self.geometry("1200x700")

        # Variables de estado
        self.df = None
        self.ruta_archivo = None
        self.r_script_path = "./frecuencia.R"

        # Layout Principal
        self.grid_columnconfigure(0, weight=3) # Área de datos más ancha
        self.grid_columnconfigure(1, weight=1) # Panel lateral
        self.grid_rowconfigure(1, weight=1)

        # ==========================================
        # 1. Barra de Herramientas
        # ==========================================
        self.toolbar_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        self.toolbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.btn_open = ctk.CTkButton(self.toolbar_frame, text="📂 Abrir Archivo", width=140, 
                                      fg_color="#CC6600", hover_color="#FF8C00", text_color="white",
                                      command=self.abrir_archivo)
        self.btn_open.pack(side="left", padx=15, pady=10)

        self.btn_analizar = ctk.CTkButton(self.toolbar_frame, text="⚙️ Analizar Variable", width=140,
                                          fg_color="#CC6600", hover_color="#FF8C00", text_color="white",
                                          command=self.abrir_panel_analisis, state="disabled")
        self.btn_analizar.pack(side="left", padx=10, pady=10)

        # ==========================================
        # 2. Visualizador de Datos (tksheet)
        # ==========================================
        self.data_viewer_frame = ctk.CTkFrame(self, corner_radius=5)
        self.data_viewer_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lbl_no_data = ctk.CTkLabel(self.data_viewer_frame, text="Abre un dataset (.csv o .xlsx) para comenzar", font=("Arial", 16))
        self.lbl_no_data.pack(expand=True)
        
        self.sheet_data = None 

        # ==========================================
        # 3. Panel de Resultados
        # ==========================================
        self.results_frame = ctk.CTkFrame(self, corner_radius=5)
        self.results_frame.grid(row=1, column=1, padx=(0,10), pady=10, sticky="nsew")
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        self.lbl_results = ctk.CTkLabel(self.results_frame, text="Resultados del Análisis", font=("Arial", 14, "bold"))
        self.lbl_results.grid(row=0, column=0, pady=10)

        self.txt_output = ctk.CTkTextbox(self.results_frame, font=("Consolas", 12), fg_color="#1e1e1e")
        self.txt_output.grid(row=1, column=0, pady=5, padx=10, sticky="nsew")

        self.lbl_image_result = ctk.CTkLabel(self.results_frame, text="Gráfico (Esperando...)", height=250, fg_color="#2b2b2b", corner_radius=5)
        self.lbl_image_result.grid(row=2, column=0, pady=(5, 10), padx=10, sticky="nsew")

        # Barra de estado
        self.status_label = ctk.CTkLabel(self, text="  Listo.", anchor="w")
        self.status_label.grid(row=2, column=0, columnspan=2, sticky="ew")

    def abrir_archivo(self):
        """
        Abre un cuadro de diálogo para seleccionar el archivo, lo procesa con pandas
        y actualiza la grilla de visualización interactiva.
        """
        filename = filedialog.askopenfilename(title="Seleccionar Dataset",
                                              filetypes=[("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx *.xls")])
        if not filename: return

        self.status_label.configure(text=f"  Cargando {os.path.basename(filename)}...")
        self.update() 

        try:
            ext = filename.split('.')[-1].lower()
            if ext == 'csv':
                self.df = pd.read_csv(filename)
            else:
                self.df = pd.read_excel(filename)
            
            # Limpiar nombres de columnas
            self.df.columns = self.df.columns.str.strip()
            self.ruta_archivo = filename

            self.visualizar_datos_en_planilla()
            self.btn_analizar.configure(state="normal")
            self.status_label.configure(text=f"  Dataset cargado: {os.path.basename(filename)} | Filas: {len(self.df)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
            self.status_label.configure(text="  Error al cargar archivo.")

    def visualizar_datos_en_planilla(self):
        """
        Toma el DataFrame cargado y lo inyecta en el widget tksheet para 
        navegación y visualización estilo Excel.
        """
        if self.lbl_no_data:
            self.lbl_no_data.destroy()
            self.lbl_no_data = None

        if self.sheet_data:
            self.sheet_data.destroy()

        self.sheet_data = Sheet(self.data_viewer_frame, 
                                data = self.df.values.tolist(),
                                headers=list(self.df.columns),
                                theme="dark")
        self.sheet_data.enable_bindings() 
        self.sheet_data.pack(expand=True, fill="both", padx=5, pady=5)

    def abrir_panel_analisis(self):
        """
        Despliega una ventana modal (Toplevel) para configurar el análisis:
        selección de variable y selección de gráficos a generar.
        """
        popup = ctk.CTkToplevel(self)
        popup.title("Configurar Análisis")
        popup.geometry("350x300")
        popup.attributes("-topmost", True)

# Le decimos a la app que espere a que el OS dibuje la ventana
        popup.wait_visibility() 
        popup.grab_set() # Ahora sí, secuestramos el foco
        ctk.CTkLabel(popup, text="Selecciona la Variable:", font=("Arial", 14)).pack(pady=(20, 5))
        
        var_seleccionada = ctk.StringVar(value=self.df.columns[0])
        combo = ctk.CTkComboBox(popup, values=list(self.df.columns), variable=var_seleccionada, width=200)
        combo.pack(pady=5)

        ctk.CTkLabel(popup, text="Gráficos a generar:", font=("Arial", 14)).pack(pady=(20, 5))
        
        check_hist = ctk.StringVar(value="")
        cb_hist = ctk.CTkCheckBox(popup, text="Histograma", variable=check_hist, onvalue="histograma", offvalue="", fg_color="#FF8C00", hover_color="#CC6600")
        cb_hist.pack(pady=5)

        check_bar = ctk.StringVar(value="")
        cb_bar = ctk.CTkCheckBox(popup, text="Gráfico de Barras", variable=check_bar, onvalue="barras", offvalue="", fg_color="#FF8C00", hover_color="#CC6600")
        cb_bar.pack(pady=5)

        def confirmar():
            graficos = [g for g in [check_hist.get(), check_bar.get()] if g]
            str_graficos = ",".join(graficos) if graficos else None
            
            popup.destroy()
            
            # Ejecutar el puente en un hilo separado para no congelar la app
            threading.Thread(target=self.ejecutar_frecuencia_r, 
                             args=(var_seleccionada.get(), str_graficos), 
                             daemon=True).start()

        ctk.CTkButton(popup, text="Ejecutar", fg_color="#FF8C00", hover_color="#CC6600", command=confirmar).pack(pady=30)

    def ejecutar_frecuencia_r(self, variable, flag_graficos):
        """
        Ejecuta el script R en un subproceso de terminal. 
        Captura el stdout para la tabla Markdown y carga las imágenes PNG generadas.
        
        Args:
            variable (str): Nombre de la variable a analizar.
            flag_graficos (str): String separado por comas con los gráficos deseados (ej: "histograma,barras").
        """
        self.status_label.configure(text="  Ejecutando motor estadístico R... (Por favor espera)")
        self.txt_output.delete("1.0", "end")
        self.lbl_image_result.configure(image=None, text="Procesando gráfico...")
        
        comando = ["Rscript", self.r_script_path, "-b", self.ruta_archivo, "-v", variable]
        if flag_graficos:
            comando.extend(["-g", flag_graficos])

        try:
            # MAGIA NEGRA: Ejecutar consola invisible
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
            
            # Limpiar ANSI Escape Codes (colores de la consola) para que el texto se vea bien
            import re
            texto_limpio = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', resultado.stdout)
            
            # Mostrar resultado en texto
            self.txt_output.insert("end", texto_limpio)
            
            # Intentar cargar la imagen si se pidió (cargamos la primera que encuentre)
            imagen_mostrada = False
            if flag_graficos:
                for tipo in flag_graficos.split(','):
                    img_name = f"{tipo}_{variable}.png"
                    if os.path.exists(img_name):
                        img = Image.open(img_name)
                        # Resize manteniendo la proporción
                        img.thumbnail((350, 250), Image.Resampling.LANCZOS)
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                        
                        self.lbl_image_result.configure(image=ctk_img, text="")
                        imagen_mostrada = True
                        break # Solo mostramos una en el panel por ahora
            
            if not imagen_mostrada:
                self.lbl_image_result.configure(text="Sin gráfico para mostrar.")

            self.status_label.configure(text="  Análisis finalizado exitosamente.")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else "Error desconocido al ejecutar R."
            self.txt_output.insert("end", f"ERROR FATAL:\n{error_msg}")
            self.lbl_image_result.configure(text="Error.")
            self.status_label.configure(text="  Falló la ejecución del análisis.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró 'Rscript' en tu sistema. Asegúrate de tener R instalado.")
            self.status_label.configure(text="  Error: Rscript no encontrado.")

if __name__ == "__main__":
    app = InfoStatKillerApp()
    app.mainloop()
