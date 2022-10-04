from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from datetime import datetime
import time

app = FastAPI()

class Entrada(BaseModel):
    id: int
    nome: str
    unix_timestamp_chegada: datetime = int(time.time())
    prioridade: bool


fila = {0: Entrada(id=0,nome='gerson',prioridade=False)}
atendidos = []
proxima_posicao = 0


@app.get('/fila')
def mostrar_fila():
    if len(fila) == 0:
        return {}
    return fila;

@app.get('/fila/{id}')
def mostra_entrada(id: int):
    try:
        return fila[id]
    except:
        raise HTTPException(status_code=404, detail="Não encontrado na fila")

@app.post('/fila')
def adiciona_entrada(entrada: Entrada):
    return entrada
