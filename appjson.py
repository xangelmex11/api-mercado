from flask import Flask, jsonify
import mysql.connector
import os
import random

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

# Ruta para obtener un proveedor aleatorio
@app.route('/proveedores', methods=['GET'])
def listar_proveedor_aleatorio():
    try:
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()
        if proveedores:
            proveedor_aleatorio = random.choice(proveedores)
            return jsonify({"proveedor": proveedor_aleatorio}), 200
        else:
            return jsonify({"mensaje": "No hay proveedores registrados"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para buscar proveedores por nombre
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

# Ruta para obtener un producto aleatorio
@app.route('/productos', methods=['GET'])
def listar_producto_aleatorio():
    try:
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
        if productos:
            producto_aleatorio = random.choice(productos)
            return jsonify({"producto": producto_aleatorio}), 200
        else:
            return jsonify({"mensaje": "No hay productos registrados"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Ruta para buscar productos por nombre
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

@app.route('/')
def index():
    return jsonify({"message": "Bienvenido a la API del Mercado Agrícola"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # Cambié el puerto predeterminado a 3000
    app.run(host="0.0.0.0", port=port, debug=True)
