import os
import re
import sqlite3
import unicodedata

from flask import Flask, jsonify, request, send_from_directory

BASE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.abspath(os.path.join(BASE, "..", "frontend", "dist"))
DB = os.environ.get("DB_PATH", os.path.join(BASE, "ranking.db"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
MAX_SCORE = 100  # 10 palavras x 10 pontos

app = Flask(__name__, static_folder=None)


def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with conn() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS ranking (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                secs INTEGER NOT NULL,
                created TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )


def slug(nome):
    s = unicodedata.normalize("NFD", nome)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s.lower())


@app.get("/api/ranking")
def listar():
    with conn() as c:
        rows = c.execute(
            "SELECT name, score, secs FROM ranking ORDER BY score DESC, secs ASC LIMIT 30"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.post("/api/ranking")
def salvar():
    d = request.get_json(silent=True) or {}
    nome = str(d.get("name", "")).strip()[:16]
    try:
        score, secs = int(d.get("score")), int(d.get("secs"))
    except (TypeError, ValueError):
        return jsonify(error="dados inválidos"), 400
    key = slug(nome)
    if not key or not (0 <= score <= MAX_SCORE) or secs < 0:
        return jsonify(error="dados inválidos"), 400
    with conn() as c:
        # só substitui se o novo resultado for melhor
        c.execute(
            """INSERT INTO ranking (id, name, score, secs) VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 name = excluded.name, score = excluded.score, secs = excluded.secs
               WHERE excluded.score > ranking.score
                  OR (excluded.score = ranking.score AND excluded.secs < ranking.secs)""",
            (key, nome, score, secs),
        )
    return jsonify(ok=True)


@app.delete("/api/ranking")
def zerar():
    if not ADMIN_TOKEN or request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify(error="não autorizado"), 403
    with conn() as c:
        c.execute("DELETE FROM ranking")
    return jsonify(ok=True)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def site(path):
    if path and os.path.isfile(os.path.join(DIST, path)):
        return send_from_directory(DIST, path)
    return send_from_directory(DIST, "index.html")


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
