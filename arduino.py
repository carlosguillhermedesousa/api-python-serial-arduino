import threading
import time
import sqlite3
from datetime import datetime
from flask import Flask, render_template, jsonify
import serial

app = Flask(__name__)

# Configurações da porta serial
PORTA = "COM7"   # ajuste conforme necessário
BAUD = 9600
DB_PATH = "led_status.db"

# Banco de dados SQLite
def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS led_inteligente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT,
            data_hora TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_led(descricao, data_hora, status):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO led_inteligente (descricao, data_hora, status) VALUES (?, ?, ?)",
                (descricao, data_hora.isoformat(), status))
    conn.commit()
    conn.close()

def ultimos_registros(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT descricao, data_hora, status FROM led_inteligente ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

# Gerenciador da porta serial
class SerialManager:
    def __init__(self):
        self.ser = None
        self.status = "Arduino Desconectado"
        self.rodando = False

    def conectar(self):
        try:
            self.ser = serial.Serial(PORTA, BAUD, timeout=1)
            self.status = "Porta aberta com sucesso!"
            self.rodando = True
            threading.Thread(target=self._ouvir, daemon=True).start()
            return True
        except Exception as e:
            self.status = f"Falha ao abrir porta: {e}"
            return False

    def desconectar(self):
        self.rodando = False
        if self.ser:
            self.ser.close()
        self.status = "Arduino Desconectado"

    def enviar(self, comando):
        if not self.ser or not self.ser.is_open:
            return False, "Arduino Desconectado"
        try:
            if not comando.endswith("\n"):
                comando += "\n"
            self.ser.write(comando.encode())
            self.ser.flush()
            return True, "Comando enviado"
        except Exception as e:
            return False, f"Erro: {e}"

    def _ouvir(self):
        buffer = bytearray()
        while self.rodando:
            try:
                if self.ser.in_waiting > 0:
                    dados = self.ser.read(self.ser.in_waiting)
                    buffer.extend(dados)
                    while b"\n" in buffer:
                        linha, _, resto = buffer.partition(b"\n")
                        buffer = resto
                        msg = linha.decode().strip()
                        self.status = msg
                        try:
                            partes = msg.split(" ", 2)
                            if len(partes) == 3 and partes[0] == "LED":
                                descricao, status, dataHora = partes
                                dt = datetime.strptime(dataHora, "%d/%m/%Y %H:%M:%S")
                                salvar_led(descricao, dt, status)
                        except:
                            pass
                time.sleep(0.05)
            except:
                time.sleep(0.05)

serial_mgr = SerialManager()
inicializar_db()

# Rotas Flask   
@app.route("/")
def index():
    return render_template("index.html",
                           status=serial_mgr.status,
                           conectado=(serial_mgr.ser and serial_mgr.ser.is_open),
                           registros=ultimos_registros())

@app.route("/conectar", methods=["POST"])
def conectar():
    ok = serial_mgr.conectar()
    return jsonify({"ok": ok, "status": serial_mgr.status})

@app.route("/desconectar", methods=["POST"])
def desconectar():
    serial_mgr.desconectar()
    return jsonify({"ok": True, "status": serial_mgr.status})

@app.route("/ligar", methods=["POST","GET"])
def ligar():
    ok, msg = serial_mgr.enviar("ligar")
    return jsonify({"ok": ok, "msg": msg, "status": serial_mgr.status})

@app.route("/desligar", methods=["POST"])
def desligar():
    ok, msg = serial_mgr.enviar("desligar")
    return jsonify({"ok": ok, "msg": msg, "status": serial_mgr.status})

@app.route("/atualiza_datahora", methods=["POST"])
def atualiza_datahora():
    agora = datetime.now()
    comando = f"atualiza {agora.strftime('%y %m %d %H %M %S')}"
    ok, msg = serial_mgr.enviar(comando)
    return jsonify({"ok": ok, "msg": msg, "status": serial_mgr.status})

@app.route("/status")
def status():
    return jsonify({
        "status": serial_mgr.status,
        "conectado": (serial_mgr.ser and serial_mgr.ser.is_open),
        "registros": ultimos_registros()
    })
'''
@app.route('/api/dados')
def api_dados():
    con = get_db_connection()
    # Pega TODOS os registros
    cursor = con.execute('SELECT descricao, data_hora, status FROM logs ORDER BY id DESC')
    dados = cursor.fetchall()
    con.close()
    
    # Converte para lista simples para o JSON
    lista_registros = []
    for linha in dados:
        lista_registros.append([
            linha['descricao'], 
            linha['data_hora'], 
            linha['status']
        ])
    
    # Retorna JSON com status atual e a lista completa
    return jsonify({
        "status": status_atual_global, # Sua variável global de status
        "registros": lista_registros
    })
'''
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
