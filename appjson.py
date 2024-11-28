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
app.secret_key = "supersecretkey"

# Rutas para listar proveedores
@app.route('/proveedores', methods=['GET'])
def listar_proveedores():
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    return jsonify(proveedores)

# Ruta para búsqueda específica en proveedores por nombre
@app.route('/proveedores/buscar/<string:nombre>', methods=['GET'])
def buscar_proveedor(nombre):
    try:
        sql = """
            SELECT * 
            FROM Proveedores 
            WHERE Nombre LIKE %s
        """
        cursor.execute(sql, (f"%{nombre}%",))
        proveedores = cursor.fetchall()

        if proveedores:
            return jsonify({"proveedores": proveedores, "mensaje": "Proveedores encontrados"}), 200
        else:
            return jsonify({"mensaje": "No se encontraron proveedores"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para listar productos
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

# Ruta para búsqueda específica en productos por nombre
@app.route('/productos/buscar/<string:nombre>', methods=['GET'])
def buscar_producto(nombre):
    try:
        sql = """
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
            WHERE p.Nombre LIKE %s
        """
        cursor.execute(sql, (f"%{nombre}%",))
        productos = cursor.fetchall()

        if productos:
            return jsonify({"productos": productos, "mensaje": "Productos encontrados"}), 200
        else:
            return jsonify({"mensaje": "No se encontraron productos"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rutas para listar historial
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

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a la API del Mercado Agrícola"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 1000))  # Cambié el puerto predeterminado a 3000
    app.run(host="0.0.0.0", port=port, debug=True)
