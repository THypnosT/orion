import re
import secrets, os
import dbConnect
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

import enviarEmail
from email_inventario import create_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = './static/images/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
Session(app)

# Instanciar módulo de conexión a la base de datos
conn = dbConnect

# SECCION PARA LOS COMPRADORES


@app.route('/')
def Index2():
    listaProductos = conn.listaProductos()
    if not session.get("comprador"):
        session["comprador"] = "no"
    
    if not session.get("username"):
        return render_template('IndexShop.html',listaProductos=listaProductos,comprador=session["comprador"])
    elif session["userType"] == "empleado" or session["userType"] == "superAdmin":
        return redirect("/Home")
    else:
        return render_template('IndexShop.html',listaProductos=listaProductos,comprador=session["comprador"])

@app.route('/singleProduct', methods=['GET', 'POST'])
def singleProduct():
    if request.method == 'POST':
        codigoProducto = request.form['codigo_producto']
        idProveedor = request.form['id_proveedor']
        print("-----------------------------------------------------------")
        print(codigoProducto)
        print(idProveedor)
        # producto=conn.getProducto(codigoProducto)       #crear una funcion para obtener el producto
        producto=conn.obtenerProductoPorID(idProveedor,codigoProducto)
        comentarios=conn.obtenerComentariosProductos(codigoProducto)
        print(comentarios)
        if not session.get("username"):
            return render_template('singleProduct.html',producto=producto,comentarios=comentarios)
        elif session["userType"] == "empleado" or session["userType"] == "superAdmin":
            return redirect("/Home")
        else:
            return render_template('singleProduct.html',producto=producto)
    else:
        return redirect("/")

@app.route('/iniciarSeccion', methods=['GET', 'POST'])
def iniciarSeccion():
    if not session.get("username"):
        return render_template('Login.html')
    else:
        return redirect("/")

@app.route('/registro', methods=['GET'])
def registro():
    if not session.get("username"):
        return render_template('Registrarse.html')
    else:
        return redirect("/")

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        if request.form['sign-in'] == 'Registrarse':
            username = request.form['username']
            email = request.form['email']
            nombre = request.form['nombre_user']
            apellido = request.form['apellido_user']
            tipoUser='usuario'
            # sexo= request.form['sexo_user']
            sexo = request.form['selectedSearch']
            cedula= request.form['cedula_user']
            ciudad= request.form['ciudad_user']
            direccion= request.form['direccion_user']
            telefono= request.form['telefono_user']
            image_src="/static/images/avatar.png"                  


            resultado=conn.insertarPersona(nombre, apellido, sexo, None, direccion, ciudad, 
                                            image_src, tipoUser, email, cedula, None, telefono)
            if resultado==True:
                flash("Usuario creado correctamente")
                return redirect('/iniciarSeccion')
       
            
        # contrasena = request.form['newpw']
        # contrasena2 = request.form['confirmpw']
        # if contrasena != contrasena2:
        #     flash("Las contraseñas no coinciden")
        #     return redirect("/registro")
        # contrasena = generate_password_hash(contrasena)
        # if conn.registrar(nombre, apellido, email, contrasena):
        #     flash("Registro exitoso")
        #     return redirect("/iniciarSeccion")
        # else:
        #     flash("Error al registrarse")
        #     return redirect("/registro")]
    

@app.route('/anadir/AddCarrito', methods=['GET', 'POST'])
def AddCarrito():
    if not session.get("username"):
        return redirect("/") 
    elif session["userType"] == "usuario":
        if request.method == 'POST':
            id_producto = request.form['codigo_producto']
            cantidad = request.form['cantidad']
            # conn.addCarrito(id_producto, cantidad)
            return redirect("/Carrito")
        else:
            return redirect("/")   
    else:
        return render_template('AccessDenied.html')

@app.route('/Carrito', methods=['GET', 'POST'])
def Carrito():
    # return render_template('Carrito.html')
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] == "usuario":
        return render_template('Carrito.html')
    else:
        return render_template('AccessDenied.html')

@app.route('/addComentario', methods=['GET', 'POST'])
def addComentario():
    if request.method == 'POST':
        codigo_producto = request.form['codigo_producto']
        comentario = request.form['newComentario']
        id_usuario = session["id_usuario"]
        calificacion = request.form['newCalificacion']
        conn.insertarComentarioCalificacionProducto(comentario,calificacion,codigo_producto,id_usuario)
        return redirect("/singleProduct")
    else:
        return redirect("/")

# SECCION PARA LOS SUPERAMINISTRADORES Y USUARIOS INTERNOS

# @app.route('/')
# def login():
#     if not session.get("username"):
#         return render_template('Login.html')
#     else:
#         return redirect("/Home")

@app.route('/Index', methods=['GET', 'POST'])
def Index():
    if request.method == 'POST':
        if conn.validarContrasena(request.form["email"], request.form["password"]) is not False:
            
            # Verificar si el usuario solicitó recuperación de contraseña o es primera vez que inicia sesión
            if conn.comprobarEstatusUsuario(conn.obtenerIDUsuario(request.form["email"])) == 0:
                flash("Bienvenido a la aplicación, por favor cambia tu contraseña", "success")
                session["cambiarPass"]=True
                return redirect('/CambiarContrasena')
            else:
                session["username"] = request.form["email"]
                session["userType"] = conn.validarTipoUsuario(request.form["email"])
                datosusuarios=conn.obtenerDatosUsuario(request.form["email"])
                
                session["usuario"] = (datosusuarios['id_persona'],datosusuarios['nombre_persona'],datosusuarios['apellido_persona'],
                                    datosusuarios['imagen_src']) 
                consultaProductos=conn.listaProductos()
                consultaProveedor=conn.listaProveedores()
                session['autocompletarProductos'] = conn.autocompletarListaProductos()
                session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
                
                if session["userType"] == "usuario":
                    session["comprador"]="activo"
                    return redirect("/")
                else:
                    return render_template('Index.html', userType=session["userType"],usuario=session["usuario"],consultaProductos=consultaProductos,
                                        consultaProveedor=consultaProveedor,autocompletarProductos=session['autocompletarProductos'], 
                                        autoCompletarProveedores=session['autoCompletarProveedores'])
        else:
            session["username"] = None
            flash("Correo o contraseña incorrectos")
            return redirect('/iniciarSeccion')
    else:
        return redirect('/Home')
    
@app.route('/CambiarContrasena', methods=['GET', 'POST'])
def CambiarContrasena():
    if session.get("cambiarPass") is True:
        return render_template('CambiarContrasena.html')
    session["cambiarPass"]=False
    return redirect("/")
    

@app.route('/Home')
def Home():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        # Consulta para el index, aqui se realizaran dos consultas, Productos y proveedores.
        # La consulta productos retorna: 'nombre producto', 'Proveedor', 'disponibles', 'imagen_src','fecha_creado
        # La consulta proveedores retorna: 'nombre proveedor', 'imagen_src','fecha_creado'
        # Cada consulta se guarda en una variable distinta
        consultaProductos=conn.listaProductos()
        consultaProveedor=conn.listaProveedores()


        # return render_template('Index.html', userType=session["userType"],consultaProductos=consultaProductos,consultaProveedor=consultaProveedor)
        return render_template('Index.html', userType=session["userType"],usuario=session["usuario"],consultaProductos=consultaProductos,
                               consultaProveedor=consultaProveedor, autocompletarProductos=session['autocompletarProductos'], 
                               autoCompletarProveedores=session['autoCompletarProveedores'])
    else:
        return render_template('AccessDenied.html')


@app.route('/Productos', methods=['POST', 'GET'])
def Productos():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        # Consulta para productos retorna:(id,nombre_producto,proveedor,disponibles,descripcion,calificacion,imagen_src)
        lista=conn.listaProductos()
        session['autocompletarProductos'] = conn.autocompletarListaProductos()
        session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
        return render_template('Productos.html',lista=lista)
    else:
        return render_template('AccessDenied.html')

@app.route('/Lotes', methods=['POST', 'GET'])
def Lotes():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        # Consulta para lotes retorna:(id,nombre_lote,producto,disponibles,fecha_creado)
        # lista=conn.listaLotes()
        lista=""    #Borrar luego de crear la consulta
        return render_template('Lotes.html',lista=lista)
    else:
        return render_template('AccessDenied.html')

@app.route('/Lote.add', methods=['POST', 'GET'])
def LoteAdd():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            if request.form.get('submit_button') == 'editar':
                # Consulta para lotes retorna:(id,nombre_lote,producto,disponibles,fecha_creado)
                # lista=conn.listaLotes()
                lista=""    #Borrar luego de crear la consulta
                return render_template('AgregarLote.html',lista=lista)
            elif request.form.get('submit_button') == 'eliminar':
                flash("Eliminado")
                lista=""    #Borrar luego de crear la consulta
                return render_template('Lotes.html',lista=lista)
            elif request.form.get('submit_button') == 'Añadir lote +':

                lista=""
                return render_template('AgregarLote.html',lista=lista)
        

    else:
        return render_template('AccessDenied.html')

@app.route('/Listas', methods=['POST', 'GET'])
def Listas():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        #session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
        session['autoCompletarEmail'] = conn.autocompletarListaEmail()
        lista=conn.obtenerProductosMinimosDiponible()
        return render_template('Listas.html',lista=lista, autoCompletarEmail=session['autoCompletarEmail'],)
    else:
        return render_template('AccessDenied.html')

@app.route('/EnviarCorreo', methods=['POST', 'GET'])
def EnviarCorreo():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            if request.form["correo"] == "":
                flash("El campo email no puede estar vacío")
                return redirect("/Listas")
            else:
                # Consulta para enviar correo
                if conn.validarUsuario(request.form["correo"]) is not False:
                    usuario = conn.obtenerDatosUsuario(request.form["correo"])["nombre_persona"] +" "+ conn.obtenerDatosUsuario(request.form["correo"])["apellido_persona"]
                else:
                    usuario = "Usuario"
                correo = request.form["correo"]
                create_pdf(usuario, correo)
                flash("Se ha enviado un correo a: "+request.form["correo"])
        return redirect("/Listas")
    else:
        return render_template('AccessDenied.html')

@app.route('/Configuracion', methods=['POST', 'GET'])
def Configuracion():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            
            datosusuarios=conn.obtenerDatosUsuarioById(request.form["id-user"])
            if(datosusuarios['descripcion_rol']=="empleado"):
                datosusuarios['descripcion_rol']="Empleado"
            elif(datosusuarios['descripcion_rol']=="superAdmin"):
                datosusuarios['descripcion_rol']="Super administrador"
            else:
                datosusuarios['descripcion_rol']="Usuario"
                    
            return render_template('User.html',datosusuarios=datosusuarios)
        else:
            return render_template('AccessDenied.html')

@app.route('/Proveedores', methods=['POST', 'GET'])
def Proveedores():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        # Consulta para productos retorna:(id,nombre_proveedor,descripcion,imagen_src)
        lista=conn.listaProveedores()
        session['autocompletarProductos'] = conn.autocompletarListaProductos()
        session['autoCompletarProveedores'] = conn.autocompletarListaProveedores()
        return render_template('Proveedores.html',lista=lista)
    else:
        return render_template('AccessDenied.html')

@app.route('/Usuarios', methods=['POST', 'GET'])
def Usuarios():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        
        if session.get("userType")=='empleado' or session.get("userType")=='superAdmin':
            ListaUsuarios = conn.obtenerListaDeUsuarios()
            
            for x in range(len(ListaUsuarios)):
                if(ListaUsuarios[x]['descripcion_rol']=="empleado"):
                    ListaUsuarios[x]['descripcion_rol']="Empleado"
                elif(ListaUsuarios[x]['descripcion_rol']=="superAdmin"):
                    ListaUsuarios[x]['descripcion_rol']="Super administrador"
                else:
                    ListaUsuarios[x]['descripcion_rol']="Usuario";
                
            return render_template('Usuarios.html',ListaUsuarios=ListaUsuarios)
        else:
            return render_template('AccessDenied.html')
    else:
        return render_template('AccessDenied.html')

@app.route('/Logout', methods=['POST', 'GET'])
def Logout():
    session.pop('username', None)
    session.pop('userType', None)
    session.pop('usuario', None)
    session.pop('cambiarPass', None)
    session.pop('autocompletarProductos', None)
    session.pop('autoCompletarProveedores', None)
    session.pop('autoCompletarEmail', None)
    session.pop('comprador', None)
    flash(" ")
    return redirect('/')


@app.route('/Editarproducto', methods=['POST', 'GET'])
def Editarproducto():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        
        if request.method == 'POST':
            
            
            if request.form['submit_button'] == 'editar':
                idProducto=request.form['id']
                idproveedor=request.form['idproveedor']
                # Aqui se recibe el id del producto para su busqueda en la base de datos, esta retorna los datos
                # del producto
                datosProducto = conn.obtenerProductoPorID(idproveedor, idProducto)
                proveedores=conn.listaProveedores()
                
                return render_template('EditarProducto.html',datosProducto=datosProducto,proveedores=proveedores, listaLote=conn.obtenerListaLote(idProducto))
            
            elif request.form['submit_button'] == 'eliminar':
                
                # consulta para eliminar producto
                conn.eliminarRegistroAlmacen(request.form['id'], request.form['idproveedor'])
                flash("Prodcuto eliminado correctamente")
                return redirect('/Productos')
                
            elif request.form['submit_button']=='Añadir +':
                # Formulario en blanco para añadir producto
                
                return redirect('/AnadirProductos')
                
            elif request.form['submit_button'] == 'Disponible':
                
                textoBuscar='productos'
                buscarPor='Disponibles'
                #Consulta para Disponibles. 
                resultadobusqueda=conn.productosDisponibles()        
                                             
                
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
                
                
            elif request.form['submit_button'] == 'No Disponible':
                textoBuscar='productos'
                buscarPor='No Disponibles'
                # Consulta para No disponible, se considera no disponible cuando la cantiada de productos es 0
                resultadobusqueda=conn.productosNoDisponibles()
                                         
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
    else:
        return render_template('AccessDenied.html')

@app.route('/AnadirProductos', methods=['POST', 'GET'])
def AnadirProductos():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        proveedores=conn.listaProveedores()               
        datosProducto={'codigo_producto':'0','id_proveedor':'','nombre_proveedor': 'Proveedor','calificacion':1,'src_imagen':'/static/images/Producto.png'}
        return render_template('AnadirProducto.html',datosProducto=datosProducto,proveedores=proveedores)
    else:
        return render_template('AccessDenied.html')

@app.route('/AdminUser', methods=['POST', 'GET'])
def AdminUser():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            
            if request.form.get('submit_button') == 'editar':
                
                # Aqui se recibe el id del usuario para su busqueda en la base de datos, esta retorna los datos
                # del usuario
                datosusuarios=conn.obtenerDatosUsuarioById(request.form["id"])
                
                if(datosusuarios['descripcion_rol']=="empleado"):
                    datosusuarios['descripcion_rol']="Empleado"
                elif(datosusuarios['descripcion_rol']=="superAdmin"):
                    datosusuarios['descripcion_rol']="Super administrador"
                else:
                    datosusuarios['descripcion_rol']="Usuario";
                
                
                return render_template('AdminUser.html',datosusuarios=datosusuarios)
            
            elif request.form.get('submit_button') == 'eliminar':
                # Consulta para eliminar usuarios
                # consulta para obtner el tipo de usuario del que se quiere borrar
                datosusuarios=conn.obtenerDatosUsuarioById(request.form["id"])
                tipoUSuario=datosusuarios['descripcion_rol']
                if session['userType']=='empleado':
                   
                    if tipoUSuario=="usuario":
                        conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])  
                       
                        flash("Usuario eliminado correctamente")
                    else: 
                        flash("No posees los permisos para borrar un usuario de tipo administrador y super administrador")
                else:
                    if session['userType']=='superAdmin':
                        if tipoUSuario=="usuario" or tipoUSuario=="empleado":
                            # Puede borrar un usuario de tipo usuario y empleado, pero no super administrador
                            conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])
                            flash("Usuario eliminado correctamente")
                        else:
                            if datosusuarios['email']==session['username']:
                                flash("No puedes borrar tu propio usuario")
                            flash("No se puede borrar un usuario de tipo Super administrador")
                        # conn.eliminarUsuario(conn.obtenerIDUsuarioDesdePersona(request.form["id"]), request.form["id"])
                        
                return redirect('/Usuarios')
            elif request.form.get('submit_button')=='Añadir usuario +':
                                          
                datosusuarios={'id_persona': 0, 'nombre_persona': '', 'apellido_persona': '', 'cedula_persona': '',
                               'descripcion_rol': 'Empleado', 'sexo_persona': 'Femenino', 'descripcion_cargo' : "Comercial",
                               'direccion_persona': '', 'ciudad_persona': '', 'email': '','telefono_persona': '',
                               'imagen_src': '/static/images/avatar.png'}
                
                return render_template('AdminUser.html',datosusuarios=datosusuarios)
    # return render_template('AdminUser.html')
    else:
        return render_template('AccessDenied.html')


@app.route('/EditarLista', methods=['POST', 'GET'])
def EditarLista():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        return render_template('EditarListas.html')
    else:
        return render_template('AccessDenied.html')

@app.route('/EditarProveedores', methods=['POST', 'GET'])
def EditarProveedores():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        
        if request.method == 'POST':
            
            if request.form['submit_button'] == 'editar':
                
                # Aqui se recibe el id del proveedor para su busqueda en la base de datos, esta retorna los datos
                # del usuario
                datosProveedor=conn.obtenerProveedorById(request.form['id'])
                
                
                return render_template('EditarProveedor.html',datosProveedor=datosProveedor)
            
            elif request.form['submit_button'] == 'eliminar':
                
                # consulta para eliminar proveedor
                conn.borrarRegistrosProveedorTdAlmacen(request.form['id'])
                flash("Proveedor eliminado")
                return redirect('/Proveedores')
                
            elif request.form['submit_button']=='Añadir proveedor +':
                # Formulario en blanco para añadir proveedor
 
                datosProveedor={'id_proveedor': 0, 'nombre_proveedor': '', 'descripcion_proveedor': '', 'src_imagen': '/static/images/proveedores.png'}
                return render_template('EditarProveedor.html',datosProveedor=datosProveedor)
    else:
        return render_template('AccessDenied.html')    

@app.route('/RecuperarPass', methods=['POST', 'GET'])
def RecuperarPass():
    if conn.validarUsuario(request.form["recuperarEmail"]) is not False:
        datosUsuario = conn.obtenerDatosUsuario(request.form['recuperarEmail'])
        nombreApellido = datosUsuario['nombre_persona'] + " " + datosUsuario['apellido_persona']
        datosEmail = enviarEmail.emailRestablecerCuenta(datosUsuario['email'], nombreApellido, datosUsuario['id_usuario'])
        response = enviarEmail.enviarCorreo(datosEmail)
        flash("Se ha enviado un correo a su cuenta de email con las instrucciones para restablecer su contraseña")
    else:
        flash("El email ingresado no se encuentra registrado")
    return redirect('/')

@app.route('/ConfirmacionNewPass', methods=['POST', 'GET'])
def ConfirmacionNewPass():

    if request.method == 'POST':
        if request.form['sign-in'] == 'Guardar':
            contrasenaActual = request.form['actualpw']
            contrasenaNueva = request.form['newpw']
            nuevaContrasena = request.form['confirmpw']
            if contrasenaNueva != nuevaContrasena:
                flash("Las contraseñas no coinciden")
                return redirect('/CambiarContrasena')

            if conn.validarContrasena(request.form['email'], contrasenaActual) is not False:
                datos=conn.obtenerDatosUsuario(request.form['email'])
                conn.cambiarContrasena(datos['id_persona'], generate_password_hash(nuevaContrasena))
                conn.cambiarEstatusUsuario(1, datos['id_persona'])
                flash("Contraseña cambiada correctamente")
                return redirect('/')
            else:
                return "Error"
        return render_template('Login.html')

@app.route('/CambiarPass', methods=['POST', 'GET'])
def CambiarPass():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            if request.form['submit_button'] == 'Cambiar contraseña':
                contrasenaActual = request.form['actualpw']
                nuevaContrasena = request.form['confirnpw']
                if conn.validarContrasena(session['username'], contrasenaActual) is not False:
                    conn.cambiarContrasena(request.form['id'], generate_password_hash(nuevaContrasena))
                    conn.cambiarEstatusUsuario(1, (request.form['id']))
                    flash("Contraseña cambiada correctamente")
                    return redirect('/')
                else:
                    return "Error"
        return redirect("/Home")

# Guardar datos de los usuarios. Llega desde la pagina adminUser
@app.route('/GuardarUser', methods=['POST', 'GET'])
def GuardarUser():
    
    if not session.get("username"):
        return redirect("/")
    else:
        if session.get("userType")=='empleado' or session.get("userType")=='superAdmin':
            if request.method == 'POST':
                if request.form['submit_button'] == 'Guardar':
                    
                    id=request.form['id']
                    nombre=request.form['nombre']
                    apellido=request.form['apellido']
                    tipoUser=request.form['selectedUsuario']   
                    if (tipoUser == "Empleado"):
                        tipoUser="empleado"
                    elif(tipoUser=="Super administrador"):
                        tipoUser="superAdmin"
                    else:
                        tipoUser="usuario"
                    
                    sexo = request.form['selectedSexo']
                    fnacimiento = request.form['fnacimiento']
                    direccion = request.form['direccion']
                    ciudad = request.form['ciudad']
                    cedula = request.form['cedula']
                    cargo = request.form['selectedCargo']
                
                    email=request.form['email']
                    telefono=request.form['telefono']
                    
                    image_src=request.files['archivo']                    
                    
                    if id=="0":
                        
                        if image_src.filename !="":
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                            
                        else:
                            image_src="/static/images/avatar.png"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                        #Consulta para insert en la base de datos
                        resultado=conn.insertarPersona(nombre, apellido, sexo, fnacimiento, direccion, ciudad, 
                                                    image_src, tipoUser, email, cedula, cargo, telefono)
                        if resultado==True:
                            flash("Usuario creado correctamente")
                            return redirect('/Usuarios')
                    else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.actualizarPersona(id,nombre, apellido, sexo, fnacimiento, direccion, ciudad, 
                                                    image_src, tipoUser, email, cedula, cargo, telefono)
                            conn.actualizarRolUsuario(conn.obtenerIDUsuarioDesdePersona(id), conn.buscarIdRol(tipoUser.strip()))
                            flash("Usuario actualizado correctamente")
                        else:
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            image_src = conn.obtenerImagenPersona(id)
                            conn.actualizarPersona(id,nombre, apellido, sexo, fnacimiento, direccion, ciudad, 
                                                    image_src, tipoUser, email, cedula, cargo, telefono)
                            conn.actualizarRolUsuario(conn.obtenerIDUsuarioDesdePersona(id), conn.buscarIdRol(tipoUser.strip()))
                            flash("Usuario actualizado correctamente")
                
                    # Despues de realizar la query regresa a la pagina de usuarios 
                    return redirect('/Usuarios')
                

                elif request.form['submit_button'] == 'Cancelar':
                    return redirect('/Usuarios')
        else:
            return render_template('AccessDenied.html')
        
# Guardar datos del productos. Llega des la pagina Editar productos
@app.route('/GuardarProducto', methods=['POST', 'GET'])
def GuardarProducto():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            if request.form['submit_button'] == 'Guardar':
                id_usuario = conn.obtenerIDUsuario(session.get("username"))
                id=request.form['id_producto']
                nombreProducto = request.form["nombre_producto"]
                proveedor = request.form['selectedProveedor']
                proveedor= proveedor.strip()
                descripcion =request.form["descripcion"]
                disponible=request.form["cantidad_disponible"]
                cantidad_minima=request.form["cantidad_minima"]
                bono=request.form["selectedCalificacion"]
                tipoUnidad=request.form["selectedUnidad"]
                precio=request.form["precio_producto"]
                descuento=request.form["descuento_producto"]
                lote=request.form["lote_producto"]
                image_src=request.files['archivo']

                if bono == "Si":
                    bono = 1
                else:
                    bono = 0
                unidad = request.form["selectedCalificacion"]
                image_src=request.files['archivo']
                if id=="0":
                    
                    if image_src.filename !="":
                        image_src=uploader()
                        image_src="/static/images/upload/"+image_src
                        
                    else:
                            image_src="/static/images/Producto.png"   # Si no se selecciona ninguna imagen, establece la imagen por defecto

                    conn.insertarProducto(nombreProducto, descripcion, precio, image_src, bono, descuento, proveedor,
                                          cantidad_minima, disponible, lote, tipoUnidad, id_usuario)
                    flash("Producto guardado correctamente")
                else:
                    if image_src.filename !="":
                        
                        image_src=uploader()            #Retorna Foto.png
                        image_src="/static/images/upload/"+image_src
                    
                        #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                        conn.actualizarProducto(id, nombreProducto, descripcion, precio, image_src, bono, descuento, proveedor, cantidad_minima, disponible, descripcion, unidad)
                        flash("Producto guardado correctamente")
                    else:
                        image_src = conn.obtenerImagenProducto(id)
                        #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                        conn.actualizarProducto(id, nombreProducto, descripcion, image_src, cantidad_minima, disponible, proveedor)
                        flash("Producto guardado correctamente","success")
                            
                return redirect('/Productos')
            elif request.form['submit_button'] == 'Cancelar':
                return redirect('/Productos')
    else:
        return render_template('AccessDenied.html')

# Guardar datos del proveedor. Llega des la pagina Editar proveedor
@app.route('/GuardarProveedor', methods=['POST', 'GET'])
def GuardarProveedor():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
            if request.form['submit_button'] == 'Guardar':
                id=request.form['id_proveedor']
                nombre_proveedor=request.form['nombre_proveedor']
                descripcion_proveedor=request.form['descripcion_proveedor']
                image_src=request.files['archivo']  
                if id=="0":
                    
                    if image_src.filename !="":
                        image_src=uploader()
                        image_src="/static/images/upload/"+image_src
                        
                    else:
                        image_src="/static/images/proveedores.png"   # Si no se selecciona ninguna imagen, establece la imagen por defecto
                        
                    #Consulta para insert en la base de datos
                    conn.insertarProveedor(nombre_proveedor,descripcion_proveedor,image_src)
                    flash("Proveedor guardado correctamente")
                else:
                        if image_src.filename !="":
                            
                            image_src=uploader()            #Retorna Foto.png
                            image_src="/static/images/upload/"+image_src
                        
                            #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento
                            conn.actualizarProveedor(id, nombre_proveedor, descripcion_proveedor, image_src)
                            flash("Proveedor guardado correctamente")
                        else:
                            image_src = conn.obtenerImagenProveedor(id)
                            #Consulta para update en la base de datos sin incluir imagen, permanece la actual
                            conn.actualizarProveedor(id, nombre_proveedor, descripcion_proveedor, image_src)
                            flash("Proveedor guardado correctamente")

                return redirect('/Proveedores')
            
            elif request.form['submit_button'] == 'Cancelar':
                return redirect('/Proveedores')
    else:
        return render_template('AccessDenied.html')

# Guardar configuracion de usuario. Llega desde la pagina User
@app.route('/Guardarconfiguracion', methods=['POST', 'GET'])
def Guardarconfiguracion():
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
        if request.method == 'POST':
        
            
            if request.form['submit_button'] == 'Guardar':
                id=request.form['id']
                telefono=request.form['telefono']
                image_src=request.files['archivo']
                if image_src.filename !="":
                    image_src=uploader()            #Retorna Foto.png
                    image_src="/static/images/upload/"+image_src
                    #Consulta para update en la base de datos cambiando la imagen por la seleccionada en el momento. Busqueda por id
                    conn.editarConfiguracionUsuario(image_src,id,telefono)
                    
                else:
                    #Consulta para update en la base de datos sin cambiar la imagen. Busqueda por id
                    conn.editarConfiguracionUsuarioSinImagen(id,telefono)
                        
                datosusuarios=conn.obtenerDatosUsuario(request.form["email"])
                
                session["usuario"] = (datosusuarios['id_persona'],datosusuarios['nombre_persona'],datosusuarios['apellido_persona'],
                                    datosusuarios['imagen_src'])
                return redirect('/Home')
            elif request.form['submit_button'] == 'Cancelar':
                
                return redirect('/Home')
           
            else:
                return ('ok')
        else:
            return redirect('/Home')
    else:
        return render_template('AccessDenied.html')

def uploader():
    """Funcion para subir la imagen en el servidor
        
    """
    if not session.get("username"):
        return redirect("/")
    elif session["userType"] != "usuario":
    # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        if f and allowed_file(f.filename):

            filename = secure_filename(f.filename)
            # Guardamos el archivo en el directorio 
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retornamos una respuesta satisfactoria
        return (filename)
    else:
        return render_template('AccessDenied.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
@app.route('/Search', methods=['POST', 'GET'])
def Search():
    if not session.get("username"):
        return redirect("/")
    else:
        if request.method == 'POST':
            textoBuscar=request.form['txtsearch']
            buscarPor=request.form['selectedSearch']
            
            if buscarPor=='Productos':
                resultadobusqueda=conn.buscarPorProducto(textoBuscar)
                if resultadobusqueda==[]:
                    flash("No se encontraron resultados")
                    return redirect('/Productos')
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)
            elif buscarPor=='Proveedores':
                resultadobusqueda=conn.buscarPorProveedor(textoBuscar)
                if resultadobusqueda==[]:
                    flash("No se encontraron resultados")
                    return redirect('/Proveedores')
                return render_template('Search.html',textoBuscar=textoBuscar,buscarPor=buscarPor,
                                       resultadobusqueda=resultadobusqueda)

 