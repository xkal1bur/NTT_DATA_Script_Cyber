from app import app,db
from flask import render_template
from flask import Flask
import json
from flask_cors import cross_origin,CORS
from flask import request
import datetime
from app.models import Usuario,Tarea,Tipo_tarea
from conexion_WhatsApp import notificacion
from conexion_Gmail import correo


#ventana principal
#registro
#perfil
#tareas pendientes
#crear tareas
#configuraciones
#papelera

#pagina de prueba
@app.route('/')
def main():
    return "Main"

#papelera asociada con las tareas borradas por el usuario
@app.route("/papelera/<usuario_nombre>",methods=['POST'])
@cross_origin()
def papelera(usuario_nombre): #retorna todas las tareas correspondientes al usuario  
    tareas=Tarea.query.filter(Tarea.usuario_nombre==usuario_nombre).all()

    
    tareas_usuario=[]

    for tarea in tareas:
        if tarea.eliminada==True or tarea.fecha_entrega<datetime.date.today():
            this={"nombre":tarea.nombre,"fecha_inicio":tarea.fecha_inicio,"fecha_limite":tarea.fecha_entrega,"tipo":tarea.tipo}

            tareas_usuario.append(this)


    #print(result)
    return {"tareas":tareas_usuario}


@app.route("/login/async",methods=['POST'])
@cross_origin()
def login_asincrono():
    body = request.get_json() #se obtiene el body pasado por fetch
    
    nombre=body["username"]
    clave=body["password"]

    #se obtiene a un usuario asociado a traves del nombre
    usuario=Usuario.query.filter(Usuario.nombre_usuario==nombre).first()

    if usuario==None or usuario.clave!=clave:
        result={"success":False}

    else:
        result={"success":True}

    return json.dumps(result)

#funcion para visualizar usuarios
@app.route("/usersjson",methods=['GET','POST'])
@cross_origin()
def all_users():
    result=[]

    usuarios=Usuario.query.all()
    print(usuarios)
    for usuario in usuarios:
        result.append(usuario.nombre_usuario)

    return json.dumps(result)


@app.route("/configuraciones",methods = ['POST'])
@cross_origin()
def configuraciones():
    body = request.get_json() #se obtiene el body pasado por fetch
    
    #obtiene parametros de body
    correo=body["email"]
    clave=body["password"]
    nuevo_nombre=body["newName"]
    nuevo_correo=body["newEmail"]
    nuevo_telefono=body["newPhone"]
    nueva_clave=body["newPassword"]

    if correo=='' or  clave=='': #verifica si el correo o la clave son vacios
        result={'success':False}
    
    elif nuevo_nombre=='' and nuevo_correo=='' and nueva_clave=='' and nuevo_telefono=='':
        #verifica si todos los atributos están vacios
        result={'success':False}

    else: #cuando se pasó el valor de al menos un atributo

        #se obtiene al usuario
        usuario=Usuario.query.filter(Usuario.correo_electronico==correo).first()

        if (usuario==None or usuario.clave!=clave):
            result={'success':False}
        
        else: 
            #se actualiza valores de atributos enviados
            if nuevo_nombre!='':
                usuario.nombre_usuario=nuevo_nombre

            if nuevo_correo!='':
                usuario.correo_electronico=nuevo_correo

            if nuevo_telefono!='':
                usuario.numero_whatsapp=nuevo_telefono
            
            if nueva_clave!='':
                usuario.clave=nueva_clave
        

            result={'success':True}

    db.session.commit()
    return json.dumps(result)


@app.route("/agregar/tarea/<usuario>/<tipo>/<tarea>",methods=['POST'])
@cross_origin()
def agregar_tarea(usuario,tipo,tarea):
   #obtiene todas las tareas con ese nombre
   tareas=Tarea.query.filter(Tarea.nombre==tarea).all()
   #busca al tipo de Tarea especifico
   for t in tareas:
    if t.tipo==tipo and t.    usuario_nombre==usuario:
            t.eliminada=False 
            print(t)  

    db.session.commit()
    return json.dumps({'success':True})



@app.route("/borrar/tarea/<usuario>/<tipo>/<tarea>",methods=['POST','GET'])
@cross_origin()
def borrar_tarea(usuario,tipo,tarea):
    
    #obtiene todas las tareas con ese nombre
    tareas=Tarea.query.filter(Tarea.nombre==tarea).all()

    #busca al tipo de Tarea especifico
    for t in tareas:
        if t.tipo==tipo and t.usuario_nombre==usuario:
            t.eliminada=True   

    db.session.commit()
    return json.dumps({'success':True})


@app.route("/crear_tarea/<nombre_usuario>",methods = ['POST', 'GET'])
@cross_origin()
def crear_tareas(nombre_usuario):
    body = request.get_json() #se obtiene el body pasado por fetch

    #obtiene atributos pasados por el fetch
    nombre=body["descripcion"]

    fecha_entrega=body["fecha_limite"]

   
    #notificacion
    notificacion_dia=body["RecordatorioDia"]

    notificacion_hora=body["RecordatorioHora"]

    #notificacion
    whatsapp=body["notificacion"]
    correo=body["notificacion1"]
    no_notificacion=body["notificacion2"]


    #tipo de Tarea
    academica=body["tareaAcademica"]
    trabajo=body["tareaTrabajo"] 
    hogar=body["tareaHogar"]
    otro=body["tareaOtro"]

    #obtiene la fecha actual
    fecha_inicio=datetime.date.today()

    #para notificaciones
    notificacion=''

    if whatsapp==True:
        notificacion="Whatsapp"
    
    elif correo==True:
        notificacion="Correo"
    
    elif no_notificacion==True:
        notificacion="Sin notificación"

    
    
    #para el tipo de Tarea
    tipo=''
    if academica==True:
        tipo='Tarea Académica'

    elif hogar==True:
        tipo='Tarea del Hogar'

    elif trabajo==True:
        tipo='Tarea de Trabajo'

    elif otro==True:
        tipo='Otro tipo de Tarea'


    #transormando la fecha 
    recordatorio=datetime.datetime.strptime(notificacion_dia,'%Y-%m-%d') 

    #obteniendo horas y minutos (notificacion_hora = 19:50 )
    horas=int(notificacion_hora[0:2])
    minutos=int(notificacion_hora[3:])

    #se suma la hora brindada a la fecha  (para generar recordatorio)
    recordatorio+=datetime.timedelta(hours=horas,minutes=minutos)

    #print("Recordatorio: ",recordatorio)

    #se crea la tarea
    tarea=Tarea(nombre=nombre,fecha_inicio=fecha_inicio,fecha_entrega=fecha_entrega,eliminada=False,notificacion=recordatorio,recordatorio=notificacion,usuario_nombre=nombre_usuario,tipo=tipo)


    try:
        #se intenta añadir la tarea
        db.session.add(tarea)
        db.session.commit()
        result={'success':True}
    except KeyError:
        #se reporta el error
        result={'success':False}

    return json.dumps(result)

@app.route("/tareas_pendientes/<usuario_nombre>",methods=['GET','POST'])
@cross_origin()
def tareas_pendientes(usuario_nombre):

    tareas=Tarea.query.filter(Tarea.usuario_nombre==usuario_nombre).all()

    
    tareas_usuario=[]

    for tarea in tareas:
        if tarea.eliminada==False and tarea.fecha_entrega>=datetime.date.today():
            this={"nombre":tarea.nombre,"fecha_inicio":tarea.fecha_inicio,"fecha_limite":tarea.fecha_entrega,"tipo":tarea.tipo}

            tareas_usuario.append(this)


    #print(result)
    return {"tareas":tareas_usuario}
    #return json.dumps(result)


@app.route("/login/register",methods = ['POST'])
@cross_origin()
def registrar_usuario():
    print('a')    
    body = request.get_json() #se obtiene el body pasado por fetch

    nuevoNombre=body["newUsername"]
    nuevaClave=body["newPassword"]
    nuevoCorreo=body["newEmail"]
    nuevoTelefono=body["newPhone"]
    nuevaFechadeNacimiento=body["newDate"]
    
    print(nuevoNombre,nuevoCorreo,nuevoTelefono,nuevaFechadeNacimiento,nuevaClave)
    
    nuevoUsuario=Usuario(nombre_usuario=nuevoNombre,numero_whatsapp=nuevoTelefono,correo_electronico=nuevoCorreo,clave=nuevaClave,fecha_nacimiento=nuevaFechadeNacimiento)

    print(nuevoUsuario)

    try:    
        db.session.add(nuevoUsuario)
        db.session.commit()

        result={"success":True}
    except:
        result={"success":False}

    return json.dumps(result)
    

@app.route('/recuperar/celular/<celular>',methods=['POST'])
@cross_origin()
def escribir_por_celular(celular):

    #se obtiene la clave asociada con el numero de celular
    usuario=Usuario.query.filter(Usuario.numero_whatsapp==celular).first()

    if usuario==None:
        result={"success":False}
    
    else:
        try:
            #se envia la clave (por WhatsApp)
            notificacion("+51"+str(celular),"Su usuario en la App🐮 es:"+ usuario.nombre_usuario+"\nSu clave en la App🐮 es: "+usuario.clave) 
            result={"success":True}

        except KeyError:
            result={"success":False}
    return json.dumps(result)


@app.route('/recuperar/correo/<correo_usuario>',methods=['POST'])
@cross_origin()
def escribir_por_correo(correo_usuario):

    #se obtiene la clave asociada con el numero de celular
    usuario=Usuario.query.filter(Usuario.correo_electronico==correo_usuario).first()

 
    mensaje="Su usuario en la App🐮 es:"+ usuario.nombre_usuario+"\nSu clave en la App🐮 es: "+usuario.clave
    email=str(usuario.correo_electronico)

    #print(mensaje,email)
    
    try:
        #se envia la clave (por WhatsApp)
        correo(email,mensaje) 

        #correo("mariana.capunay@utec.edu.pe","Desde Python")
        result={"success":True}

    except KeyError:
        result={"success":False}
    return json.dumps(result)
