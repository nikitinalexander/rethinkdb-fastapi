from fastapi import FastAPI
from rethinkdb import RethinkDB
import os

r = RethinkDB()
admin_password = os.getenv('RETHINKDB_PASSWORD').strip()
admin_user = os.getenv('RETHINKDB_USER').strip()
host = os.getenv('RETHINKDB_HOST').strip()

conn = r.connect(host=host,
                 db="rethinkdb",
                 user=admin_user,
                 password=admin_password)             
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/create_client/{client}/{client_password}")
def read_item(client: str, client_password: str):
    return r.table("users").insert({"id": client, "password": client_password}).run(conn)

@app.get("/update_client/{client}/{client_password}")
def read_item(client: str, client_password: str):
    return r.table("users").get(client).update({"password": client_password}).run(conn)

@app.get("/create_db/{db_name}")
def read_item(db_name: str):
    return r.db_create(db_name).run(conn)

@app.get("/create_table/{db_name}/{table_name}")
def read_item(db_name: str, table_name: str):
    return r.db(db_name).table_create(table_name).run(conn)

@app.get("/create_match")
def read_item():
    current_match_info = {
        "team1":"manchester",
        "team2":"chelsea",
        "score":[0, 0],
        "timestamp": r.now()}
    return r.db("test").table("scores").insert(current_match_info).run(conn)['generated_keys'][0]

@app.get("/score_goal/{match_id}")
def read_item(match_id: str):
    current_match_info = r.db("test").table("scores").get(match_id).run(conn)
    new_score = [current_match_info["score"][0] + 1, current_match_info["score"][1]]
    new_match_info = {
        "team1":current_match_info["team1"],
        "team2":current_match_info["team2"],
        "score":new_score,
        "timestamp": r.now()}
    return r.db("test").table("scores").get(match_id).update(new_match_info).run(conn)