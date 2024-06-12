import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# Datos de ejemplo para horarios y películas
horarios = ["10:00 AM - 12:00 PM", "1:00 PM - 3:00 PM", "4:00 PM - 6:00 PM", "7:00 PM - 9:00 PM"]
peliculas = ["Dune part 2", "El club de la lucha", "Pinocho", "El Guason", "Intensamente", "Batman", "The Truman show", "Dune part 1"]
rutas_imagenes = ["SegundoSemestre/semana9/imagenes/Dune_2.png",
                  "SegundoSemestre/semana9/imagenes/club.png",
                  "SegundoSemestre/semana9/imagenes/pinocho.jpg",
                  "SegundoSemestre/semana9/imagenes/joker.jpeg",
                  "SegundoSemestre/semana9/imagenes/intensamente.jpg",
                  "SegundoSemestre/semana9/imagenes/señor_noche.jpg",
                  "SegundoSemestre/semana9/imagenes/show_truman.jpg",
                  "SegundoSemestre/semana9/imagenes/dune1.jpg"]

# Diccionario para almacenar el estado de los asientos
estado_asientos = {}
asientos_seleccionados = []

def crear_frame(raiz):
    return ctk.CTkFrame(master=raiz, fg_color="transparent")

# Función para actualizar el estado del asiento
def seleccionar_asiento(boton, horario, pelicula, sala_numero, fila, columna):
    clave = (pelicula, horario, sala_numero)
    
    if estado_asientos[clave][fila][columna] == "O":
        messagebox.showwarning("Asiento ocupado", "Este asiento ya está ocupado.")
        return
    elif estado_asientos[clave][fila][columna] is None:  
        boton.configure(text="S", fg_color="#2D7B75", text_color="white")
        estado_asientos[clave][fila][columna] = "S"
    elif estado_asientos[clave][fila][columna] == "S":
        boton.configure(text="L", fg_color="#1c6ca4", text_color="white")
        estado_asientos[clave][fila][columna] = None

# Función para resaltar los asientos disponibles
def resaltar_asientos_disponibles(sala_numero, horario, pelicula, botones):
    fila_del_medio = 2
    fila_siguiente = fila_del_medio + 1
    clave = (pelicula, horario, sala_numero)
    # Verificar si la fila del medio está completamente ocupada
    fila_completamente_ocupada = all(estado_asientos[clave][fila_del_medio][j] is not None for j in range(10))

    for i in range(6):  # filas 
        for j in range(10):  # columnas
            if fila_completamente_ocupada and i == fila_siguiente:
                if estado_asientos[clave][i][j] is None:  # Asiento disponible en la fila siguiente
                    botones[i][j].configure(fg_color="#D7B82B")
                    
            elif not fila_completamente_ocupada and i == fila_del_medio:
                if estado_asientos[clave][i][j] is None:  #Asiento disponible en la fila del medio
                    botones[i][j].configure(fg_color="#D7B82B")
                elif estado_asientos[clave][i][j] is not None:  #Asiento ocupado en la fila del medio
                    botones[i + 1][j].configure(fg_color="#D7B82B")
                    if estado_asientos[clave][i + 1][j] == "S": #Si el boton tiene S, se colocara el color de seleccion
                        botones[i + 1][j].configure(fg_color="#2D7B75")
                    elif estado_asientos[clave][i + 1][j] == "O": #Si el boton tiene O, se colocara el color de ocupado
                        botones[i + 1][j].configure(fg_color="green")


def seleccionar_horario_sala(pelicula):
    # Limpiar el contenido existente en el frame principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    # Etiqueta para seleccionar un horario
    ctk.CTkLabel(contenido_principal, text="Seleccione un Horario:", text_color="white").pack(pady=5)
    horario_var = ctk.StringVar()
    
    # Crear botones de opción para cada horario disponible
    for horario in horarios:
        ctk.CTkRadioButton(contenido_principal, text=horario, variable=horario_var, value=horario).pack()

    # Función para confirmar la selección de horario y sala
    def confirmar_seleccion():
        horario_seleccionado = horario_var.get()
        sala_seleccionado = sala_var.get()
        if horario_seleccionado and sala_seleccionado:
            # Si se han seleccionado tanto el horario como la sala, muestra los asientos disponibles
            mostrar_asientos(pelicula, horario_seleccionado, sala_seleccionado)
            cartelera()
        else:
            # Si falta alguna selección, muestra un mensaje de advertencia
            messagebox.showwarning("Selección incompleta", "Por favor seleccione tanto el horario como la película.")

    # Etiqueta para seleccionar una sala de cine
    ctk.CTkLabel(contenido_principal, text="Seleccione una sala de Cine:", text_color="white").pack(pady=10)
    sala_var = ctk.StringVar()
    
    # Crear botones de opción para cada sala de cine disponible
    for i in range(1, 4):
        ctk.CTkRadioButton(contenido_principal, text=f"Sala de Cines {i}", variable=sala_var, value=i).pack(pady=5)

    # Botón para confirmar la selección de horario y sala
    ctk.CTkButton(contenido_principal, text="Confirmar", command=confirmar_seleccion).pack(pady=10)



# Función para mostrar la disposición de asientos
def mostrar_asientos(pelicula, horario, sala_numero):
    """
    :param pelicula: El nombre de la película.
    :param horario: El horario de la función.
    :param sala_numero: El número de la sala de cine.
    """
    # Limpiar el contenido existente en el frame principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()
        
    # Crear una nueva ventana para la selección de asientos
    sala_ventana = ctk.CTkToplevel()
    sala_ventana.title(f"{pelicula} - Sala de Cines {sala_numero} - {horario}")
    sala_ventana.geometry("750x550")

    # Cargar una imagen para representar la pantalla del cine
    imagen = Image.open("SegundoSemestre/semana9/imagenes/linea.png")
    imagen = imagen.resize((600, 50))
    linea_pantalla = ImageTk.PhotoImage(imagen)

    # Mostrar un mensaje y crear un frame para los asientos
    ctk.CTkLabel(sala_ventana, text="Seleccione los asientos que desea ocupar:").pack(pady=10)
    clave = (pelicula, horario, sala_numero)
    #confirma si estan todas las claves en el diccionario
    if clave not in estado_asientos:
        estado_asientos[clave] = [[None for _ in range(10)] for _ in range(6)]
    frame_asientos = ctk.CTkFrame(sala_ventana, fg_color="transparent")
    frame_asientos.pack()

    # Crear botones para representar cada asiento en la sala
    botones = []
    for i in range(6): #filas
        fila_botones = []
        for j in range(10): #columnas
            estado = estado_asientos[clave][i][j]
            texto = "O" if estado == "O" else "L"
            color = "green" if estado == "O" else None

            boton = ctk.CTkButton(frame_asientos, text=texto, width=50, height=20, corner_radius=30, fg_color=color)
            boton.grid(row=i, column=j, padx=5, pady=5)
            fila_botones.append(boton)

            boton.configure(command=lambda b=boton, i=i, j=j: seleccionar_asiento(b, horario, pelicula, sala_numero, i, j))

        botones.append(fila_botones)

    #funcion para confirmar las reservas de asientos
    def confirmar_reservas():
        asientos_seleccionados = []
        for i in range(6): #filas
            for j in range(10):#columnas
                if estado_asientos[clave][i][j] == "S":
                    asientos_seleccionados.append((i, j))
        if asientos_seleccionados:
            for fila, columna in asientos_seleccionados:
                estado_asientos[clave][fila][columna] = "O"
            messagebox.showinfo("Reserva", "Asientos reservados con éxito!")
        else:
            messagebox.showwarning("No hay asientos seleccionados", "Por favor, seleccione al menos un asiento.")
        sala_ventana.destroy()

    # Mostrar la pantalla y agregar botones para confirmar reservas y resaltar asientos disponibles
    pantalla = ctk.CTkLabel(master=sala_ventana, image=linea_pantalla, text="")
    pantalla.place(x=136, y=250)

    ctk.CTkLabel(sala_ventana, text="Pantalla", font=ctk.CTkFont(size=14)).pack(pady=35)
    ctk.CTkButton(sala_ventana, text="Confirmar Reservas", command=confirmar_reservas).pack(pady=10)
    ctk.CTkButton(sala_ventana, text="Resaltar Asientos Disponibles",
                  command=lambda: resaltar_asientos_disponibles(sala_numero, horario, pelicula, botones)).pack(pady=10)

    # Mostrar leyendas para los estados de los asientos
    ctk.CTkLabel(sala_ventana, text="L = Asientos Libres").pack(pady=5)
    ctk.CTkLabel(sala_ventana, text="O = Asientos Ocupados").pack(pady=5)
    ctk.CTkLabel(sala_ventana, text="S = Asiento Seleccionado").pack(pady=5)




def cartelera():
    """
    Muestra la cartelera de películas disponibles en la interfaz gráfica.

    Esta función limpia el contenido existente en el frame principal y luego crea un canvas
    y un frame desplazable para mostrar las películas disponibles. Cada película se muestra
    con una imagen y un botón que permite al usuario seleccionar el horario y la sala de cine.
    """

    # Limpiar el contenido existente en el frame principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()

    # Crear un canvas y un frame desplazable
    canvas = ctk.CTkCanvas(contenido_principal, width=600, height=350, bg="#2c2c2c", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(contenido_principal, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = ctk.CTkFrame(canvas, fg_color="#2c2c2c")

    scrollable_frame.bind(
        "<Configure>", #vincula una función al evento de configuración
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    #Muestra el frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") #anchor="nw" hace que barra deslizante se enclaje al noroeste
    canvas.configure(yscrollcommand=scrollbar.set)

    #Etiqueta que indica que se muestran películas disponibles en la cartelera
    ctk.CTkLabel(scrollable_frame, text="Películas Disponibles en nuestra cartelera").pack()

    #Crear un frame para mostrar las imagenes de las películas y los botones de seleccion
    frame_peliculas = crear_frame(scrollable_frame)
    frame_peliculas.pack(pady=5)

    #Mostrar cada película con su imagen y botón de selección de horario y sala
    for i, (pelicula, ruta_imagen) in enumerate(zip(peliculas, rutas_imagenes)):
        #Cargar la imagen de la pelicula y ajustar su tamaño
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((120, 140))
        imagen_tk = ImageTk.PhotoImage(imagen)

        #Mostrar la imagen de la película
        label_imagen = ctk.CTkLabel(frame_peliculas, image=imagen_tk, text="")
        label_imagen.image = imagen_tk
        #Posiciona el widget label_imagen en una cuadrícula dentro del contenedor.
        #calcula dinámicamente la fila y la columna en función del índice 'i' del bucle
        #y la distribución deseada. El widget se coloca en filas impares para evitar
        #la superposición con los botones. Se establece un relleno horizontal y vertical
        #alrededor del widget para proporcionar espacio entre las imágenes y los elementos circundantes.
        label_imagen.grid(row=(i // 4) * 2 + 1, column=(i % 4), padx=14, pady=10)

        #Crear un botón para seleccionar el horario y la sala de la película
        boton = ctk.CTkButton(master=frame_peliculas, text=pelicula, 
                              width=100, height=25, corner_radius=20, 
                              command=lambda p=pelicula: seleccionar_horario_sala(p))
        boton.grid(row=(i // 4) * 2 + 2, column=(i % 4), padx=14, pady=10)


def quienes_somos():
    #Limpiar el contenido existente en el frame principal
    for widget in contenido_principal.winfo_children():
        widget.destroy()
    #carga la imagen del logo de intercine y la modifica
    imagen = Image.open("SegundoSemestre/semana9/imagenes/intercine.png")
    imagen = imagen.resize((300, 200))
    imagen_fondo = ImageTk.PhotoImage(imagen)
    #Titulo
    label_bienvenida = ctk.CTkLabel(contenido_principal, text="Somos InterCine, Cine de calidad", font=ctk.CTkFont(size=25, weight="bold"))
    label_bienvenida.pack(pady=20)
    #descripcion
    label_instrucciones = ctk.CTkLabel(contenido_principal, text="¡Descubre la magia del cine en InterCine, donde la emoción cobra vida en la gran pantalla!\nSumérgete en una experiencia cinematográfica sin igual", font=ctk.CTkFont(size=14))
    label_instrucciones.pack(pady=10)
    #muestra la imagen
    logo = ctk.CTkLabel(master=contenido_principal, image=imagen_fondo, text="")
    logo.pack()
    
#Actualiza el contenido principal, mostrado un perfil del usuario
def perfil():
    #Elimina todos los widgets hijos del widget contenido_principal.
    #Esto asegura que el contenido anterior se limpie antes de agregar nuevos widgets,
    #evitando así cualquier superposición o conflicto con los nuevos elementos que se agregarán.
    for widget in contenido_principal.winfo_children():#El método winfo_children() devuelve una lista de todos los widgets secundarios (hijos). Esto incluye cualquier tipo de widget, como botones,
        widget.destroy() #Elimina los widgets
    #Carga la imagen y la modifica
    imagen = Image.open("SegundoSemestre\semana9\imagenes\perfil.png")
    imagen = imagen.resize((250, 250))
    imagen_fondo = ImageTk.PhotoImage(imagen)
    #texto de bienvenida
    label_bienvenida_nombre = ctk.CTkLabel(contenido_principal, text="¡Bienvenido de vuelta!", font=ctk.CTkFont(size=25, weight="bold"))
    label_bienvenida_nombre.pack(pady=20)
    #Muestra la imagen anteriormente cargada
    foto_perfil = ctk.CTkLabel(master=contenido_principal, image=imagen_fondo, text="")
    foto_perfil.pack()
    #texto de descripcion
    label_bienvenida_texto = ctk.CTkLabel(contenido_principal, text="Esperamos que le agrade nuestra app", font=ctk.CTkFont(size=14))
    label_bienvenida_texto.pack(pady=10)

#Funcion para salir de la aplicacion
def salir():
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
        root.destroy()
        
#Sera la ventana principal donde el usuario selecciona la opcion
def ventana_principal():
    #Estas variables seran globales para poner y quitar contenido con otras funciones
    global root, contenido_principal
    root = ctk.CTk()
    root.title("Intercine")
    root.geometry("600x400")

    # Crear un frame para la barra de opciones
    barra_opciones = ctk.CTkFrame(root, fg_color="gray")
    barra_opciones.pack(side="top")

    # Botones para la barra de opciones
    btn_nuevo = ctk.CTkButton(barra_opciones, text="¿Quienes somos?", command=quienes_somos)#Crea el boton
    btn_nuevo.pack(side="left", padx=5, pady=5)#muestra el boton

    btn_abrir = ctk.CTkButton(barra_opciones, text="Cartelera", command=cartelera)
    btn_abrir.pack(side="left", padx=5, pady=5)

    btn_guardar = ctk.CTkButton(barra_opciones, text="Perfil", command=perfil)  
    btn_guardar.pack(side="left", padx=5, pady=5)

    btn_salir = ctk.CTkButton(barra_opciones, text="Salir", command=salir)
    btn_salir.pack(side="left", padx=5, pady=5)

    # Contenido principal y que va a ir cambiando dependiendo de las opcion seleccionada
    contenido_principal = crear_frame(root)
    # = ctk.CTkFrame(root)
    
    contenido_principal.pack(fill="both", expand=True, padx=10, pady=10)
    
    perfil()

    root.mainloop()

ventana_principal()
