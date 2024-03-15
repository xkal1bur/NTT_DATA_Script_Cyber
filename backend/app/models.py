from app import db


class Usuario(db.Model): 
    nombre_usuario = db.Column(db.String(30), primary_key = True)
    numero_whatsapp = db.Column(db.String(9), index=True,unique=True)
    correo_electronico = db.Column(db.String(40), nullable=False,index=True,unique=True)
    clave=db.Column(db.String(50),nullable=False,index=True)
    fecha_nacimiento=db.Column(db.Date,nullable=False,index=True)
    #tabla Padre de Tarea
    tareas = db.relationship('Tarea',backref='usuario',lazy='joined')

    def __repr__(self):
        return '<Usuario {}>'.format(self.nombre_usuario)



class Tarea(db.Model):
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre = db.Column(db.String(30),index=True,nullable=False)
    fecha_inicio = db.Column(db.Date,index=True)
    fecha_entrega = db.Column(db.Date,index=True)
    eliminada=db.Column(db.Boolean,index=True)
    notificacion=db.Column(db.Date,index=True)
    recordatorio=db.Column(db.String(30),index=True)
    #Tabla Hijo de Usuario (Foreign Key)
    usuario_nombre= db.Column(db.String(30),db.ForeignKey('usuario.nombre_usuario'),nullable=False)
    
    #Tabla Hijo de Tipo_Tarea (Foreign Key)
    tipo = db.Column(db.String(30),db.ForeignKey('tipo_tarea.nombre'),nullable=False)

    def __repr__(self):
        return 'Tarea <{}> , Tipo <{}>'.format(self.nombre,self.tipo)


class Tipo_tarea(db.Model):
    nombre = db.Column(db.String(30),primary_key=True)

    #Tabla Padre de Tarea
    tareas = db.relationship('Tarea',backref='tipo_tarea',lazy='joined')

    def __repr__(self):
        return 'Tipo de tarea <{}>'.format(self.nombre)