from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from supabase_py import create_client

load_dotenv()

app = FastAPI()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

@app.post("/insertar")
def insertar_dato(industriosidad: str):
    data = {'industriousness': industriosidad}
    response = supabase.table('Preguntas_chamba').insert(data)
    if response['status_code'] == 201:
        return {'message': 'Dato insertado correctamente.'}
    else:
        raise HTTPException(status_code=500, detail=f'Error al insertar dato: {response["error"]}')

@app.delete("/eliminar/{id}")
def eliminar_dato(id: int):
    response = supabase.table('Preguntas_chamba').delete().eq('id', id)
    if response['status_code'] == 200:
        return {'message': 'Dato eliminado correctamente.'}
    else:
        raise HTTPException(status_code=500, detail=f'Error al eliminar dato: {response["error"]}')

@app.put("/actualizar/{id}")
def actualizar_dato(id: int, nueva_industriosidad: str):
    data = {'industriousness': nueva_industriosidad}
    response = supabase.table('Preguntas_chamba').update(data).eq('id', id)
    if response['status_code'] == 200:
        return {'message': 'Dato actualizado correctamente.'}
    else:
        raise HTTPException(status_code=500, detail=f'Error al actualizar dato: {response["error"]}')


