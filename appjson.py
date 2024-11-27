from flask import Flask, request, jsonify, flash, redirect
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

# Rutas para CRUD de Proveedores
@app.route('/proveedores', methods=['GET'])
def listar_proveedores():
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    return jsonify(proveedores)

@app.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    try:
        nombre = request.json.get('nombre')
        telefono = request.json.get('telefono')
        correo = request.json.get('correo')
        direccion = request.json.get('direccion')
        cursor.execute(
            "INSERT INTO Proveedores (Nombre, Telefono, Correo, Direccion) VALUES (%s, %s, %s, %s)",
            (nombre, telefono, correo, direccion)
        )
        database.commit()
        return jsonify({"message": "Proveedor agregado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/editar_proveedor/<int:id>', methods=['PUT'])
def editar_proveedor(id):
    try:
        nombre = request.json.get('nombre')
        telefono = request.json.get('telefono')
        correo = request.json.get('correo')
        direccion = request.json.get('direccion')
        cursor.execute("""
            UPDATE Proveedores 
            SET Nombre = %s, Telefono = %s, Correo = %s, Direccion = %s 
            WHERE ProveedorID = %s
        """, (nombre, telefono, correo, direccion, id))
        database.commit()
        return jsonify({"message": "Proveedor actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/eliminar_proveedor/<int:id>', methods=['DELETE'])
def eliminar_proveedor(id):
    try:
        cursor.execute("DELETE FROM Proveedores WHERE ProveedorID = %s", (id,))
        database.commit()
        return jsonify({"message": "Proveedor eliminado con éxito"}), 200
    except mysql.connector.errors.IntegrityError:
        return jsonify({"error": "No se puede eliminar el proveedor porque tiene productos asociados"}), 400

# Rutas para CRUD de Productos
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

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    try:
        data = request.json
        cursor.execute("""
            INSERT INTO Productos (Nombre, Categoria, Precio, UnidadMedida, Cantidad, Disponible, ProveedorID) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre'], data['categoria'], data['precio'],
            data['unidad_medida'], data['cantidad'], data['disponible'], data['proveedor_id']
        ))
        database.commit()
        return jsonify({"message": "Producto agregado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/editar_producto/<int:id>', methods=['PUT'])
def editar_producto(id):
    try:
        data = request.json
        cursor.execute("""
            UPDATE Productos 
            SET Nombre = %s, Categoria = %s, Precio = %s, UnidadMedida = %s, Cantidad = %s, Disponible = %s, ProveedorID = %s
            WHERE ProductoID = %s
        """, (
            data['nombre'], data['categoria'], data['precio'],
            data['unidad_medida'], data['cantidad'], data['disponible'], data['proveedor_id'], id
        ))
        database.commit()
        return jsonify({"message": "Producto actualizado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/eliminar_producto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        cursor.execute("DELETE FROM Productos WHERE ProductoID = %s", (id,))
        database.commit()
        return jsonify({"message": "Producto eliminado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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
    return jsonify({"message": "Bienvenido a la API del Mercado2"}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    app.run(host="0.0.0.0", port=port, debug=True)
