from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.responses import JSONResponse
from datetime import datetime
import time

app = FastAPI()


class Entrada(BaseModel):
    id: Optional[int]
    nome: str = Field(..., max_length=20)
    unix_timestamp_chegada: datetime = int(time.time())
    prioridade: str = Field(..., max_length=1)
    atendido: bool = False


fila = {
    "N": [],
    "P": []
}

atendidos = []

def passa_fila(modo: str):
    substituto = fila[modo][0]
    del fila[modo][0]
    substituto.atendido = True
    atendidos.append(substituto)

def remove_da_fila(modo: str, id: int):
   for item in fila[modo]:
       if(item.id == id):
           fila[modo].remove(item)
           return True


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
    entrada.id = len(fila['N']) + len(fila['P'])
    if entrada.prioridade is not 'N' and entrada.prioridade is not 'P':
        raise HTTPException(status_code=400, detail="Prioridade deve ser apenas N para normal e P para prioritario")
    fila[entrada.prioridade].append(entrada)
    return True

@app.put('/fila')
def andar_filas():
    if len(fila["P"]) > 0:
        passa_fila("P")
        return {"fila": fila, "atendidos": atendidos}
    elif len(fila["N"]) > 0:
        passa_fila("N")
        return {"fila": fila, "atendidos": atendidos}
    else:
        return "Filas vazias"

@app.delete('/fila/{id}')
def remover_cliente(id: int):
    for item in fila["N"]:
        if item.id == id:
            remove_da_fila("N",id)
            return True
    for item in fila["P"]:
        if item.id == id:
            remove_da_fila("P",id)
            return True
    return HTTPException(status_code=404, detail="Cliente não encontrado")

uvicorn.run("main:app", port=443, log_level="info")
