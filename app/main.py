import datetime
from typing import Any, Dict, Optional
import pymysql
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from fastapi.responses import PlainTextResponse

from pydantic import BaseModel

class Pessoa(BaseModel):
    id_pessoa:Optional[int]
    nome: str
    rg: str
    cpf: str
    data_nascimento: str
    data_admissao: str



# setup logging as early as possible


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/")
def index(request: Request) -> Any:
    message = {
        "Name": "API VISIE",
        "Developed by": "Kalil Kabiam Vasconcelos Junior",
        "Status": "Online",
        "Documentation": ""
    }
    return message



@app.get("/consulta-pessoas")
async def consultar(search:str):

    db = pymysql.connect(host="jobs.visie.com.br",user="kalilkabiam",password="a2FsaWxrYWJp",database="kalilkabiam",charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()

    sql_query = " SELECT id_pessoa,SUBSTRING_INDEX(nome, ' ',1) as nome,DATE_FORMAT(data_admissao,'%d/%m/%Y') as data_admissao FROM pessoas WHERE 1=1"

    if(search):
        sql_query += " and nome like '%"+search+"%'"

    cursor.execute(sql_query)

    results = cursor.fetchall()

    return results




@app.post("/pessoas")
async def post_pessoas(pessoa: Pessoa):
    db = pymysql.connect(host="jobs.visie.com.br", user="kalilkabiam", password="a2FsaWxrYWJp", database="kalilkabiam",
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    cursor = db.cursor()

    sql_query = " INSERT INTO pessoas (nome,rg,cpf,data_nascimento,data_admissao) " \
                " values ('"\
                 +pessoa.nome+"','"\
                 +pessoa.rg+"','"\
                 +pessoa.cpf+"','"\
                 +pessoa.data_nascimento+"','"\
                 +pessoa.data_admissao \
                +"')"


    cursor.execute(sql_query)

    return pessoa


@app.get("/pessoas/{id}")
async def consultar_uma_pessoa(id:str):

    db = pymysql.connect(host="jobs.visie.com.br",user="kalilkabiam",password="a2FsaWxrYWJp",database="kalilkabiam",charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

    cursor = db.cursor()

    sql_query = " SELECT * FROM pessoas WHERE id_pessoa=" +id

    cursor.execute(sql_query)

    results = cursor.fetchone()

    return results


@app.put("/pessoas/{id}")
async def put_pessoas(id:str, pessoa: Pessoa):
    db = pymysql.connect(host="jobs.visie.com.br", user="kalilkabiam", password="a2FsaWxrYWJp", database="kalilkabiam",
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    cursor = db.cursor()

    sql_query = " UPDATE pessoas set  nome = '"\
                 +pessoa.nome+"', rg = '"\
                 +pessoa.rg+"',cpf ='"\
                 +pessoa.cpf+"',data_nascimento='"\
                 +pessoa.data_nascimento+"',data_admissao='"\
                 +pessoa.data_admissao \
                +"' where id_pessoa=" + id


    cursor.execute(sql_query)

    return pessoa



@app.delete("/pessoas/{id}")
async def delete_pessoas(id:str):
    db = pymysql.connect(host="jobs.visie.com.br", user="kalilkabiam", password="a2FsaWxrYWJp", database="kalilkabiam",
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
    cursor = db.cursor()

    sql_query = " DELETE FROM pessoas  where id_pessoa=" + id


    cursor.execute(sql_query)

    return id


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
