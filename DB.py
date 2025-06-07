from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime
from os import getenv

load_dotenv()
DB = create_client(getenv("SUPABASE_URL"), getenv("SUPABASE_KEY"))

def insert(nome: str, turma: str, tipo: str) -> dict:
    now = datetime.now()
    dados = {
        "nome": nome, 
        "turma": turma, 
        "tipo": tipo, 
        "data": now.date().strftime("%Y-%m-%d"), 
        "hora": now.time().strftime("%H:%M:%S")
    }

    try:
        response = DB.table("registros").insert(dados).execute()
        
        return {
            "success": bool(response.data),
            "data": response.data,
            "error": None if response.data else "Nenhum dado retornado"
        }
        
    except Exception as e:
        return {"success": False, "data": None, "error": str(e)}

def get_all(datas: list, horas: list) -> list:
    try:
        response = DB.rpc("consulta_registros", {"data_inicio": datas[0], "hora_inicio": horas[0], "data_fim": datas[1], "hora_fim": horas[1]}).execute()
        return response.data
    except Exception as e:
        print(f"Erro: {e}")
        return []
