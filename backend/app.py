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

# Configuración
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/questions'
app.config['UPLOAD_FOLDER'] = 'static/employees'
db = SQLAlchemy(app)
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
        industriousness = request.json.get('industriousness')


        worker = Worker(first_name, last_name, job_title, industriousness)

        worker.calculate_ind_score()

        db.session.add(worker)
        db.session.commit()
        
        return jsonify({'success': True, 'id': worker.id, 'message': 'Worker created successfully'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSIONS


# Start server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5006)
else:
    print('Importing {}'.format(__name__))
