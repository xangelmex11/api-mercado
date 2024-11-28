from flask import Flask, request, jsonify
import mysql.connector
import os

# Configuración de la base de datos
database = mysql.connector.connect(
    host="apimercadoagricola.cp0m2uu08onk.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Efdade1146",
    database="api_mercado_agricola"
)
cursor = database.cursor(dictionary=True)

app = Flask(__name__)

# Ruta para listar proveedores
@app.route('/proveedores', methods=['GET'])
def listar_proveedores():
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    return jsonify(proveedores)

# Ruta para listar productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    cursor.execute("""
        SELECT 
            p.ProductoID,
            p.Nombre,
            p.Categoria,
            p.Precio,
            p.UnidadMedida,
            p.Cantidad,
            p.Disponible,
            p.FechaAgregado,
            pr.Nombre AS Proveedor
        FROM Productos p
        JOIN Proveedores pr ON p.ProveedorID = pr.ProveedorID
    """)
    productos = cursor.fetchall()
    return jsonify(productos)

# Ruta para listar historial
@app.route('/historial', methods=['GET'])
def listar_historial():
    cursor.execute("""
        SELECT 
            h.HistorialID AS ID,
            h.Cantidad,
            h.Fecha,
            COALESCE(p.Nombre, 'Producto desconocido') AS Producto,
            pr.Nombre AS Proveedor
        FROM Historial h
        LEFT JOIN Productos p ON h.ProductoID = p.ProductoID
        LEFT JOIN Proveedores pr ON h.ProveedorID = pr.ProveedorID
    """)
    historial = cursor.fetchall()
    return jsonify(historial)

# Ruta para búsqueda filtrada de eventos
@app.route('/evento/<nombreEvento>', methods=['GET'])
def listas_evento(nombreEvento):
    try:
        sql = """
            SELECT nombreEvento, lugar, fecha, artista, clasificacion, historia 
            FROM eventos 
            WHERE nombreEvento = %s
        """
        cursor.execute(sql, (nombreEvento,))
        datos = cursor.fetchone()
        
        if datos:
            evento = {
                'Nombre_del_evento': datos['nombreEvento'],
                'Lugar': datos['lugar'],
                'Fecha': datos['fecha'],
                'Artista': datos['artista'],
                'Clasificacion': datos['clasificacion'],
                'Historia': datos['historia']
            }
            return jsonify({'Estado': evento, 'mensaje': 'Evento encontrado'})
        else:
            return jsonify({'mensaje': 'Evento no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'ERROR', 'error': str(ex)})

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a la API del Mercado"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Puerto predeterminado: 3000
    app.run(host="0.0.0.0", port=port, debug=True)
