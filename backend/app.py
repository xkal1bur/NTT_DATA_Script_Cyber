# Imports
from flask import (
    Flask, 
    request, 
    render_template,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

client_ai = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/ntt_data'
app.config['UPLOAD_FOLDER'] = 'static/employees'
db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "*"}})
ALLOW_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

ind_coef = [.59, -.60, -.56, -.55, .52, -.54, .49, .49, -.53, -.52] # industriousness
ind_min_max = [-14.41, 7.15]

"""
industriousness_questions = [
    0: "Llevar a cabo mis planes.",
    1: "Perder mi tiempo.",
    2: "Encontrar difícil ponerme a trabajar.",
    3: "Desordenar las cosas.",
    4: "Terminar lo que empiezo.",
    5: "No concentrar mi mente en la tarea en cuestión.",
    6: "Hacer las cosas rápidamente.",
    7: "Siempre saber lo que estoy haciendo.",
    8: "Posponer decisiones.",
    9: "Distraerme fácilmente."
]
"""
# Ejemplo de alguien máximo en industriousness
# [5,1,1,1,5,1,5,5,1,1]


# lista = [first_name, last_name, job_title, industriousness]
def creation_call(lista):
    completion = client_ai.chat.completions.create(
        model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "Te voy a pasar el first_name, last_name, job_title y industriousness. Vas a escribir una descripción de un párrafo para promocionar al trabajador basandote en los datos que te di y en indicador entre 0 y 1 de industriousness. Tómalo como un porcentaje, si es menos de 50 es peor para el trabajo. Menciona el industriousness en porcentaje."},
            {"role": "user", "content": f"first_name: {lista[0]}, last_name: {lista[1]}, job_title: {lista[2]}, industriousness: {lista[3]}"}
        ]
    )

    descripcion = completion.choices[0].message.content
    print(descripcion)

    return descripcion




# Modelos
class Worker(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), server_default=db.text('uuid_generate_v4()'))
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text('now()'))
    description = db.Column(db.Text, nullable=True)
    ind = db.Column(db.JSON, nullable=True) # industriousness
    ind_score = db.Column(db.Float, nullable=True)
    

    def __init__(self, first_name, last_name, job_title, ind=None):
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.ind = ind

    def __repr__(self):
        return '<Employee %r %r>' % (self.first_name, self.last_name)

    def calculate_ind_score(self):
        if self.ind:
            score_sum = 0
            for i in range(10):
                score_sum += ind_coef[i] * self.ind[i]
            self.ind_score = (score_sum - ind_min_max[0]) / (ind_min_max[1] - ind_min_max[0])
        else:
            self.ind_score = None
    
    def generate_description(self):
        if self.ind_score:
            self.description = creation_call([self.first_name, self.last_name, self.job_title, self.ind_score])
        else:
            self.description = None

@app.route('/worker', methods=['GET'])
def get_worker():
    workers = Worker.query.all()
    return jsonify([worker.__dict__ for worker in workers])


@app.route('/worker', methods=['POST'])
def create_worker():
    try: 
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        job_title = request.json.get('job_title')
        industriousness_all = request.json.get('industriousness')
        ind = {}
        for i in range(10):
            ind[i] = int(industriousness_all[i]['option'])
        print(ind)



        worker = Worker(first_name, last_name, job_title, ind)

        worker.calculate_ind_score()

        worker.generate_description()

        db.session.add(worker)
        db.session.commit()
        
        return jsonify({'success': True, 'id': worker.id, 'message': 'Worker created successfully'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/worker/<id>', methods=['GET'])
def get_worker_by_id(id):
    worker = Worker.query.get(id)
    return jsonify(worker.__dict__)

# Start server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
else:
    print('Importing {}'.format(__name__))
