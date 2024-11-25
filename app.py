import os
from functools import wraps
from cs50 import SQL
from flask import (Flask, redirect, render_template, request, session, jsonify, make_response)
from flask_session import Session
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np

categorias = ["agriculturaGanaderia", "agropecuaria", "pescaAcuicultura", "automotriz", "aviacionAeronaves", "bancaFinanzas", "comercioMayorista", "comercioMinorista", "retail", "construccion", "materialesConstruccion", "cosmeticaBelleza", "disenoDecoracion", "educacion", "consultoriaRRHH", "serviciosSocialesSalud", "farmaceuticas", "fabricacionProductosQuimicos", "fabricacionVehiculosMaquinaria", "produccionAlimentosBebidas", "produccionMaderaProductos", "logisticaDistribucion", "mineriaHidrocarburos", "telecomunicaciones", "textil", "defensa", "gobierno", "ong", "siderurgia"]


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["DEBUG"] = True
Session(app)

db = SQL("sqlite:///registros.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
# @login_required
def index():
    return render_template("index.html")

@app.route("/feed")
def fedd():
    return render_template("feed.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Limpiar cualquier sesión activa
    if request.method == "POST":
        # Obtener DNI y contraseña del formulario
        dni = request.form.get("dni")
        password = request.form.get("password")

        # Validar que ambos campos fueron proporcionados
        if not dni or not password:
            return "Error: DNI y contraseña son obligatorios.", 400

        # Buscar en la base de datos al usuario por DNI y contraseña
        rows = db.execute(
            "SELECT * FROM usuarios WHERE dni = ? AND contraseña = ?", dni, password
        ) 

        # Verificar si existe exactamente un usuario con esos datos
        if len(rows) != 1:
            return "Error: Contraseña o DNI incorrectos.", 400

        # Iniciar sesión guardando el ID del usuario en la sesión
        session["user_id"] = rows[0]["id"]
        print("que paso?")

        # Redirigir a la página principal
        return redirect("/perfil")
    
    # Si el método es GET, mostrar el formulario de inicio de sesión
    return render_template("login.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Obtener los datos del formulario
        username = request.form.get("username")
        dni = request.form.get("dni")
        celular = request.form.get("celular")
        password = request.form.get("password")

        # Guardar el username en la sesión
        session["username"] = username
        session["dni"] = dni
        session["celular"] = celular
        session["password"] = password

        # Redirigir a la página de empezar

        # print(username)
        return redirect("/empezar")

    return render_template("signin.html")

@app.route("/empezar", methods=["GET", "POST"])
def empezar():
    username = session.get("username")  # Recupera el username de la sesión SESSION RECUPERADO
    # print(username)
    if not username:
        return redirect("/signin")  # Redirige si no hay username en la sesión
    return render_template("empezar.html", username=username)

@app.route("/p1", methods=["GET", "POST"])
def p1():
    if request.method == "POST":
        # Capturar los datos del formulario
        work_schedules = request.form.getlist("workSchedule")
        # Imprimir en la consola del servidor
        session["horario"] = int(work_schedules[0])
        print("AAAAAA")
        print(work_schedules[0])
        return redirect("/p2")

    # Renderizar la plantilla como respuesta (puedes personalizarla si lo deseas)
    return render_template("1.html")


@app.route("/p2", methods=["GET", "POST"])
def p2():
    if request.method == "POST":
        # Capturar el valor seleccionado en el formulario
        nivelEducacion1 = request.form.get("nivelEducacion")
        
        # Imprimir el valor seleccionado en la consola del servidor
        print("Nivel educativo seleccionado:", nivelEducacion1)
        
        session["nivelEducacion"] = int(nivelEducacion1)
        
        # Redirigir a la siguiente página o mostrar un mensaje
        return redirect("/p3")
    
    # Renderizar el formulario por defecto si se accede con GET
    return render_template("2.html")


@app.route("/p3", methods=["GET", "POST"])
def p3():
    if request.method == "POST":
        # Capturar el valor ingresado en el campo "Pago Deseado"
        pago_deseado = request.form.get("pago-deseado")
        
        # Validar si el valor es numérico antes de procesarlo
        try:
            monto = float(pago_deseado)
            session["pago"] = int(monto)
            print(f"El pago deseado ingresado es: S/ {monto:.2f}")
        except ValueError:
            print("El valor ingresado no es válido.")
            return "Error: Debes ingresar un monto válido.", 400
        
        # Redirigir a la siguiente página
        return redirect("/p4")
    
    # Renderizar el formulario si se accede por método GET
    return render_template("3.html")


@app.route("/p4", methods=["GET", "POST"])
def p4():
    if request.method == "POST":
        modalidad = request.form.get("modalidad")
        print(f"Modalidad recibida en /p4: {modalidad}")
        if modalidad:
            session["modalidad"] = int(modalidad)
            return redirect("/p5")
    return render_template("4.html")

@app.route("/p5", methods=["GET", "POST"])
def p5():
    # Captura la respuesta pasada como parámetro en la URL
    response2 = request.args.get('response2')

    # Verifica si 'response' tiene un valor válido (no es None ni cadena vacía)
    if response2:
        session["experiencia"] = int(response2)
        print(f"Respuesta recibida: {response2}")  # Imprime la respuesta en consola para depurar
        return redirect("/p6")  # Redirige a p6
    
    # Si no hay respuesta, solo renderiza la página 5
    return render_template("5.html")



@app.route("/p6", methods=["GET", "POST"])
def p6():
    # Captura la respuesta pasada como parámetro en la URL
    response = request.args.get('response')  # Asegúrate de que el nombre sea 'response', como en el JavaScript
    
    # Si la respuesta no está vacía, imprime la respuesta y redirige
    if response:
        session["situacion"] = int(response)
        print(f"Respuesta recibida: {response}")  # Ahora sí debería imprimir correctamente
        return redirect("/p7")  # Redirige a p7
    
    # Si no se recibe respuesta, simplemente renderiza la página p6
    return render_template("6.html")

@app.route("/p7", methods=["GET", "POST"])
def p7():
    # Captura la respuesta pasada como parámetro en la URL
    response = request.args.get('respuesta', None)  # Obtiene el valor de 'respuesta'

    # Si se ha recibido respuesta, muestra la respuesta en la consola
    if response:
        session["dependencia"] = int(response)
        print(f"respuesta 7: {response}")
        return redirect("/p8")  # Redirige a la página p8 si hay una respuesta

    # Si no se recibe respuesta, simplemente renderiza la página p7
    return render_template("7.html")


@app.route("/p8", methods=["GET", "POST"])
def p8():
    # Captura el valor de la respuesta desde la URL
    response = request.args.get('respuesta', None)
    if response:
        session["habilidades"] = int(response)
        print(f"respuesta 8: {response}")
        return redirect("/p9") 
    
    return render_template("8.html")


@app.route("/p9", methods=["GET", "POST"])
def p9():
    if request.method == "POST":
        # Capturar los sectores seleccionados
        sectores = request.form.getlist("sectores[]")
        
        if sectores:
            session["sectores"] = sectores
            
            print(type(sectores))
            print(f"Sectores seleccionados: {sectores}")
            # Puedes hacer algo con los sectores seleccionados, como almacenarlos o procesarlos.
            return redirect("/p10")  # Redirige a la siguiente página (ajusta esto según sea necesario)
        else:
            # Si no se seleccionaron sectores, mostrar mensaje de error
            return "Error: No seleccionaste ningún sector.", 400

    # Si el método es GET, simplemente renderiza la página
    return render_template("9.html")


@app.route("/p10", methods=["GET", "POST"])
def p10():
    if request.method == "POST":
        trabajo_deseado = request.form.get("trabajo")
        # Aquí puedes procesar el trabajo deseado, como guardarlo en una base de datos
        # O hacer algo con él antes de redirigir al login
        session["deseado"] = trabajo_deseado
        print(f"respuesta 10: {trabajo_deseado}")

        nombre = session.get("username")
        dni = session.get("dni")
        celular = session.get("celular")
        contraseña = session.get("password")
        horario = session.get("horario")
        nivelEducacion = session.get("nivelEducacion")
        pago = session.get("pago")
        modalidad = session.get("modalidad")
        experiencia = session.get("experiencia")
        situacion = session.get("situacion")
        dependencia = session.get("dependencia")
        habilidades = session.get("habilidades")
        sectores = session.get("sectores")
        deseado = session.get("deseado")

        c = [1 if categoria in sectores else 0 for categoria in categorias]
        print(len(c))
        # Combinar todos los datos en una lista
        data_to_insert = [
            nombre, dni, celular, contraseña, horario, nivelEducacion, pago, modalidad, 
            experiencia, situacion, dependencia, habilidades, *c, deseado
        ]

        # Verifica que la longitud de 'data_to_insert' sea 42
        print(len(data_to_insert))  # Debería ser 42

        db.execute(
            """
            INSERT INTO usuarios (
                nombre, dni, celular, contraseña, horario, nivelEducacion, pago, modalidad,
                experiencia, situacion, dependencia, habilidades, agriculturaGanaderia, agropecuaria,
                pescaAcuicultura, automotriz, aviacionAeronaves, bancaFinanzas, comercioMayorista,
                comercioMinorista, retail, construccion, materialesConstruccion, cosmeticaBelleza,
                disenoDecoracion, educacion, consultoriaRRHH, serviciosSocialesSalud, farmaceuticas,
                fabricacionProductosQuimicos, fabricacionVehiculosMaquinaria, produccionAlimentosBebidas,
                produccionMaderaProductos, logisticaDistribucion, mineriaHidrocarburos, telecomunicaciones,
                textil, defensa, gobierno, ong, siderurgia, deseado
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            );
            """, *data_to_insert
        )



        return redirect('/perfil')  # Redirige después de recibir el formulario
    return render_template("10.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/perfil")
@login_required
def perfil():
    # Obtener el ID del usuario desde la sesión
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")  # Si no hay usuario en sesión, redirige al login

    # Obtener los datos del usuario desde la base de datos usando el ID
    user_data = db.execute("SELECT nombre, dni, celular FROM usuarios WHERE id = ?", user_id)

    if len(user_data) != 1:
        session.clear()  # Limpiar la sesión si no se puede acceder al perfil
        return redirect("/login")  # Redirigir al login si no se encuentra el usuario

    # Extraer la información del usuario
    user = user_data[0]
    username = user["nombre"]
    dni = user["dni"]
    celular = user["celular"]

    # Obtener los datos del usuario desde la tabla 'usuarios'
    user_data_query = db.execute("""
        SELECT modalidad, experiencia, situacion, dependencia, habilidades,
               agriculturaGanaderia, agropecuaria, pescaAcuicultura, automotriz,
               aviacionAeronaves, bancaFinanzas, comercioMayorista, comercioMinorista,
               retail, construccion, materialesConstruccion, cosmeticaBelleza,
               disenoDecoracion, educacion, consultoriaRRHH, serviciosSocialesSalud,
               farmaceuticas, fabricacionProductosQuimicos, fabricacionVehiculosMaquinaria,
               produccionAlimentosBebidas, produccionMaderaProductos, logisticaDistribucion,
               mineriaHidrocarburos, telecomunicaciones, textil, defensa, gobierno,
               ong, siderurgia
        FROM usuarios
        WHERE id = ?
    """, user_id)

    if len(user_data_query) != 1:
        session.clear()  # Limpiar la sesión si no se puede acceder al perfil
        return redirect("/login")  # Redirigir al login si no se encuentra el usuario

    # Obtener datos del usuario
    user_data = user_data_query[0]

    # Obtener los datos de todos los empleados
    empleados_data = db.execute("""
        SELECT modalidad, experiencia, situacion, dependencia, habilidades,
               agriculturaGanaderia, agropecuaria, pescaAcuicultura, automotriz,
               aviacionAeronaves, bancaFinanzas, comercioMayorista, comercioMinorista,
               retail, construccion, materialesConstruccion, cosmeticaBelleza,
               disenoDecoracion, educacion, consultoriaRRHH, serviciosSocialesSalud,
               farmaceuticas, fabricacionProductosQuimicos, fabricacionVehiculosMaquinaria,
               produccionAlimentosBebidas, produccionMaderaProductos, logisticaDistribucion,
               mineriaHidrocarburos, telecomunicaciones, textil, defensa, gobierno,
               ong, siderurgia
        FROM empleadosModelo
    """)

    categorias = list(user_data.keys())
    valores_user = list(user_data.values())
    valores_empleados = [list(emp.values()) for emp in empleados_data]

    # Unir los datos del usuario y empleados
    columnas = ["user_data"] + [f"empleado_{i+1}" for i in range(len(empleados_data))]
    datos = [valores_user] + valores_empleados
    df = pd.DataFrame(datos, columns=categorias).T
    df.columns = columnas

    # Transponer el DataFrame para que cada columna represente un punto
    df_transpuesto = df.T

    # Normalizar los datos transpuestos
    escalador = MinMaxScaler().fit(df_transpuesto)
    df_normalizadas = pd.DataFrame(escalador.transform(df_transpuesto), columns=df_transpuesto.columns)

    # Función para obtener grupo y orden de puntos
    def obtener_grupo_y_orden(data, punto_referencia, n_clusters):
        """
        Agrupa los datos en n_clusters y encuentra los puntos en el mismo grupo que el punto de referencia,
        ordenados por distancia.
        """
        # Crear una copia del DataFrame para evitar modificar el original
        data_copia = data.copy()

        # Aplicar KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(data_copia)
        data_copia['cluster'] = kmeans.labels_

        # Convertir el punto de referencia a un DataFrame
        punto_df = pd.DataFrame([punto_referencia], columns=data.columns)

        # Identificar el cluster del punto de referencia
        cluster_referencia = kmeans.predict(punto_df)[0]

        # Filtrar puntos del mismo grupo
        puntos_mismo_grupo = data_copia[data_copia['cluster'] == cluster_referencia].drop(columns=['cluster'])

        # Calcular distancias al punto de referencia
        puntos_mismo_grupo['distancia'] = puntos_mismo_grupo.apply(
            lambda fila: np.linalg.norm(fila.values - punto_referencia), axis=1
        )

        # Ordenar por distancia
        puntos_ordenados = puntos_mismo_grupo.sort_values(by='distancia')

        return cluster_referencia, puntos_ordenados

    # Función jerarquia
    def jerarquia(n_clusters_inicial):
        """
        Realiza el proceso iterativo de jerarquía y muestra los resultados.
        """
        # Seleccionar el primer punto como punto de referencia
        punto_referencia = df_normalizadas.iloc[0].values

        # Inicializar una lista para almacenar los resultados
        resultados_por_nivel = []

        for n_clusters in range(n_clusters_inicial, 0, -1):
            cluster_referencia, puntos_ordenados = obtener_grupo_y_orden(df_normalizadas, punto_referencia, n_clusters)

            resultados_por_nivel.append({
                'clusters': n_clusters,
                'cluster_referencia': cluster_referencia,
                'puntos_ordenados': puntos_ordenados
            })

        # Inicializar un conjunto para almacenar los índices ya mostrados
        indices_mostrados = set()

        # Imprimir resultados
        for resultado in resultados_por_nivel:
            print(f"\nNúmero de clusters: {resultado['clusters']}")
            print(f"Grupo del punto de referencia: {resultado['cluster_referencia']}")
            print("Puntos en el mismo grupo ordenados por distancia:")

            # Filtrar los puntos que no hayan sido mostrados en niveles anteriores
            puntos_nivel_actual = resultado['puntos_ordenados'].index.tolist()
            puntos_no_mostrados = [idx for idx in puntos_nivel_actual if idx not in indices_mostrados]

            # Agregar los índices mostrados a `indices_mostrados`
            indices_mostrados.update(puntos_no_mostrados)

            # Imprimir los índices sin duplicados
            print(", ".join(map(str, puntos_no_mostrados)))

    # Llamada a la función jerarquia con el número de clusters inicial
    jerarquia(2)

    return render_template("perfil.html", username=username, dni=dni, celular=celular)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)