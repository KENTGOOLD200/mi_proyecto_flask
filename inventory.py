import json
import os

from models import db, Producto

import json
import os
from models import db, Producto

class Inventario:
    """
    Clase que gestiona el inventario en memoria.
    - Usa un diccionario {id: Producto} para accesos rápidos.
    - Usa un set con nombres en minúsculas para evitar duplicados.
    """

    def __init__(self, productos_dict=None):
        self.productos = productos_dict or {}  # Diccionario de productos
        self.nombres = set(p.nombre.lower() for p in self.productos.values())  # Set de nombres únicos

    @classmethod
    def cargar_desde_bd(cls):
        productos = Producto.query.all()  # Consulta todos los productos
        productos_dict = {p.id: p for p in productos}  # Crea diccionario por ID
        return cls(productos_dict)

    def agregar(self, nombre: str, cantidad: int, precio: float) -> Producto:
        if nombre.lower() in self.nombres:
            raise ValueError('Ya existe un producto con ese nombre.')
        p = Producto(nombre=nombre.strip(), cantidad=int(cantidad), precio=float(precio))
        db.session.add(p)
        db.session.commit()
        self.productos[p.id] = p
        self.nombres.add(p.nombre.lower())
        self._guardar_en_json(p)
        return p

    def eliminar(self, id: int) -> bool:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        self.productos.pop(id, None)
        self.nombres.discard(p.nombre.lower())
        return True

    def actualizar(self, id: int, nombre=None, cantidad=None, precio=None) -> Producto | None:
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return None
        if nombre is not None:
            nuevo = nombre.strip()
            if nuevo.lower() != p.nombre.lower() and nuevo.lower() in self.nombres:
                raise ValueError('Ya existe otro producto con ese nombre.')
            self.nombres.discard(p.nombre.lower())
            p.nombre = nuevo
            self.nombres.add(p.nombre.lower())
        if cantidad is not None:
            p.cantidad = int(cantidad)
        if precio is not None:
            p.precio = float(precio)
        db.session.commit()
        self.productos[p.id] = p
        return p

    def buscar_por_nombre(self, q: str):
        q = q.lower()
        return sorted([p for p in self.productos.values() if q in p.nombre.lower()], key=lambda x: x.nombre)

    def listar_todos(self):
        return sorted(self.productos.values(), key=lambda x: x.nombre)

    def _guardar_en_json(self, producto):
        ruta = os.path.join('datos', 'datos.json')
        datos = []
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                try:
                    datos = json.load(f)
                except json.JSONDecodeError:
                    datos = []
        datos.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'cantidad': producto.cantidad,
            'precio': producto.precio
        })
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
