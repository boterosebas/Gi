from flask import Flask, request, render_template, jsonify
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_PATH = 'database/consultas.db'

def init_db():
    """Inicializa la base de datos con algunas tablas de ejemplo"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Crear tabla de usuarios de ejemplo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento INTEGER UNIQUE NOT NULL,     
            email TEXT UNIQUE NOT NULL,
            telefono INTEGER UNIQUE,
            pais TEXT,
            ciudad TEXT,
            rol TEXT NOT NULL,
            fecha_registro DATE DEFAULT CURRENT_DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            categoria TEXT,
            talla TEXT,
            color TEXT,
            precio REAL NOT NULL,
            marca TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
           id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha_actualizacion TEXT
        )
    ''')



  
    # Insertar datos de ejemplo si no existen
    cursor.execute('SELECT COUNT(*) FROM Usuario')
    if cursor.fetchone()[0] == 0:
        usuarios_ejemplo = [
            ("Alexis", 13364758, "aguilanocturna@gmail.com", 3124456, "Rusia", "Moscu", 1),
            ("María", 24875932, "maria.lopez@mail.com", 3159874, "España", "Madrid", 2),
            ("John", 98765432, "john.smith@gmail.com", 4123678, "EEUU", "Nueva York", 2),
            ("Lucía", 45321687, "lucia.mendez@hotmail.com", 3178456, "México", "Guadalajara", 2),
            ("Carlos", 76234981, "carlos.ruiz@mail.com", 3201987, "Colombia", "Bogotá", 1),
            ("Anna", 33451298, "anna.petrov@rambler.ru", 4987632, "Rusia", "San Petersburgo", 2),
            ("Taro", 11324567, "taro.yamamoto@yahoo.jp", 5609823, "Japón", "Tokio", 1),
            ("Laura", 85236974, "laura.gomez@gmail.com", 3187654, "Argentina", "Buenos Aires", 2),
            ("Pierre", 98741236, "pierre.dupont@orange.fr", 4456123, "Francia", "París", 1),
            ("Fatima", 67549812, "fatima.hassan@gmail.com", 5541098, "Marruecos", "Casablanca", 2),
            ("Hans", 74123659, "hans.muller@web.de", 4412987, "Alemania", "Berlín", 1),
            ("Giulia", 56413287, "giulia.rossi@mail.it", 4823761, "Italia", "Roma", 2),
            ("David", 95231478, "david.brown@gmail.com", 4032159, "EEUU", "Los Ángeles", 2),
            ("Sofía", 31245987, "sofia.diaz@hotmail.com", 3167542, "Chile", "Santiago", 2),
            ("Ahmed", 86543219, "ahmed.farouk@outlook.com", 5092381, "Egipto", "El Cairo", 1),
            ("Ingrid", 74129536, "ingrid.olsen@mail.no", 4523876, "Noruega", "Oslo", 2),
            ("Pedro", 65478912, "pedro.alvarez@gmail.com", 3198476, "Perú", "Lima", 1),
            ("Olga", 23147896, "olga.kuznetsova@rambler.ru", 4992134, "Rusia", "Ekaterimburgo",1),
            ("Chen", 87654321, "chen.li@mail.cn", 5321498, "China", "Pekín", 1),
            ("Elena", 49563217, "elena.popescu@yahoo.ro", 4762398, "Rumanía", "Bucarest", 2),
            ("Miguel", 52147893, "miguel.hernandez@gmail.com", 3148597, "México", "Monterrey", 1),
            ("Nina", 64321985, "nina.schmidt@web.de", 4420198, "Alemania", "Múnich", 2),
            ("Omar", 74213589, "omar.khan@mail.pk", 5076312, "Pakistán", "Lahore", 1),
            ("Camila", 33451267, "camila.fernandez@hotmail.com", 3128974, "Chile", "Valparaíso", 2),
            ("Yuri", 99874563, "yuri.ivanov@gmail.com", 4987321, "Rusia", "Moscu", 1)
        ]
        cursor.executemany('INSERT INTO Usuario (nombre, documento, email, telefono, pais, ciudad, rol) VALUES (?, ?, ?, ?, ?, ?, ?)', usuarios_ejemplo)
        

    cursor.execute('SELECT COUNT(*) FROM Producto')
    if cursor.fetchone()[0] == 0:
        productos_ejemplo = [
            ("Ultraboost Light", "Zapatillas", 42, "Blanco", 749000, "Adidas"),
            ("Superstar Classic", "Zapatillas", 40, "Negro", 499000, "Adidas"),
            ("Stan Smith", "Zapatillas", 41, "Verde", 459000, "Adidas"),
            ("Forum Low", "Zapatillas", 43, "Azul", 539000, "Adidas"),
            ("Gazelle Retro", "Zapatillas", 39, "Rojo", 479000, "Adidas"),
            ("NMD_R1", "Zapatillas", 42, "Gris", 689000, "Adidas"),
            ("Adilette Aqua", "Sandalias", 44, "Azul", 179000, "Adidas"),
            ("Tiro 23 Pants", "Pantalón Deportivo", "M", "Negro", 249000, "Adidas"),
            ("Essentials Hoodie", "Buzo", "L", "Gris", 289000, "Adidas"),
            ("Adicolor Tee", "Camiseta", "S", "Blanco", 139000, "Adidas"),
            ("4DFWD 3", "Zapatillas", 43, "Negro", 999000, "Adidas"),
            ("Predator Elite FG", "Botines", 42, "Negro/Rojo", 829000, "Adidas"),
            ("X Crazyfast", "Botines", 41, "Amarillo", 749000, "Adidas"),
            ("Copa Pure II", "Botines", 44, "Blanco/Dorado", 819000, "Adidas"),
            ("Response CL", "Zapatillas", 40, "Beige", 599000, "Adidas"),
            ("Terrex Free Hiker 2", "Botas de Senderismo", 42, "Marrón", 849000, "Adidas"),
            ("Run It Shorts", "Pantaloneta", "M", "Negro", 129000, "Adidas"),
            ("Aeroready Tank", "Camiseta", "L", "Celeste", 119000, "Adidas"),
            ("Adilette Comfort", "Sandalias", 43, "Blanco/Azul", 199000, "Adidas"),
            ("Essentials Track Jacket", "Chaqueta", "M", "Negro", 319000, "Adidas"),
            ("Trefoil Cap", "Accesorio", "Única", "Negro", 99000, "Adidas"),
            ("Performance Backpack", "Accesorio", "Única", "Gris", 199000, "Adidas"),
            ("Own the Run Jacket", "Chaqueta", "L", "Azul Marino", 349000, "Adidas"),
            ("Powerlift 5", "Zapatillas", 42, "Rojo/Negro", 659000, "Adidas"),
            ("Adicolor Cargo Pants", "Pantalón", "M", "Verde Oliva", 299000, "Adidas")
        ]
        cursor.executemany('INSERT INTO Producto (nombre_producto, categoria, talla, color, precio, marca) VALUES (?, ?, ?, ?, ?, ?)', productos_ejemplo)

    cursor.execute('SELECT COUNT(*) FROM Inventario')
    if cursor.fetchone()[0] == 0:
        inventarios_ejemplo = [
            (25, "2025-01-15"),
            (48, "2025-02-02"),
            (10, "2025-02-17"),
            (32, "2025-03-05"),
            (60, "2025-03-21"),
            (15, "2025-04-03"),
            (80, "2025-04-19"),
            (42, "2025-05-01"),
            (70, "2025-05-12"),
            (55, "2025-05-27"),
            (12, "2025-06-04"),
            (65, "2025-06-20"),
            (30, "2025-07-02"),
            (50, "2025-07-15"),
            (77, "2025-08-01"),
            (18, "2025-08-18"),
            (90, "2025-09-03"),
            (22, "2025-09-14"),
            (68, "2025-09-29"),
            (33, "2025-10-05"),
            (47, "2025-10-12"),
            (53, "2025-10-20"),
            (19, "2025-11-02"),
            (84, "2025-11-10"),
            (26, "2025-12-01")
           
        ]
        cursor.executemany('INSERT INTO Inventario (id_producto, cantidad) VALUES (?, ?)', inventarios_ejemplo)    
    
    conn.commit()
    conn.close()

def execute_query(query, params=None):
    """Ejecuta una consulta SQL y retorna los resultados"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Determinar si es una consulta SELECT o una operación de modificación
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
            columns = [description[0] for description in cursor.description]
        else:
            conn.commit()
            results = {"affected_rows": cursor.rowcount, "message": "Query executed successfully"}
            columns = []
        
        conn.close()
        return {"success": True, "data": results, "columns": columns}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    """Página principal con el formulario para consultas SQL"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_sql():
    """Endpoint para ejecutar consultas SQL"""
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({"success": False, "error": "Query cannot be empty"})
    
    result = execute_query(query)
    return jsonify(result)

@app.route('/schema')
def get_schema():
    """Endpoint para obtener el esquema de la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema[table_name] = [{"name": col[1], "type": col[2], "nullable": not col[3], "primary_key": bool(col[5])} for col in columns]
        
        conn.close()
        return jsonify({"success": True, "schema": schema})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/examples')
def get_examples():
    """Endpoint que retorna consultas SQL de ejemplo"""
    examples = [
        {
            "title": "Listar todos los usuarios",
            "query": "SELECT * FROM usuarios;"
        },
        {
            "title": "Productos con precio mayor a 100",
            "query": "SELECT * FROM productos WHERE precio > 100;"
        },
        {
            "title": "Contar usuarios por edad",
            "query": "SELECT edad, COUNT(*) as cantidad FROM usuarios GROUP BY edad ORDER BY edad;"
        },
        {
            "title": "Ventas con información de usuarios y productos",
            "query": """SELECT 
                v.id as venta_id,
                u.nombre as usuario,
                p.nombre as producto,
                v.cantidad,
                v.fecha_venta
            FROM ventas v
            JOIN usuarios u ON v.usuario_id = u.id
            JOIN productos p ON v.producto_id = p.id
            ORDER BY v.fecha_venta DESC;"""
        },
        {
            "title": "Insertar nuevo usuario",
            "query": "INSERT INTO usuarios (nombre, email, edad) VALUES ('Nuevo Usuario', 'nuevo@email.com', 25);"
        },
        {
            "title": "Actualizar precio de producto",
            "query": "UPDATE productos SET precio = 899.99 WHERE nombre = 'Laptop';"
        }
    ]
    return jsonify({"examples": examples})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)