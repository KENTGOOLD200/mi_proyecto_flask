from models import db, Producto

class Inventario:
    """
    - Usa un diccionario {id: Producto} para accesos O(1).
    - Mantiene un set con nombres en minúsculas para validar duplicados rápidamente.
    - Devuelve listas ordenadas usando list/tuplas según convenga.
    """
    def __init__(self, productos_dict=None):
        # Inicializa el inventario con un diccionario de productos (id: Producto)
        self.productos = productos_dict or {}  # dict[int, Producto]
        # Set de nombres en minúsculas para evitar duplicados rápidamente
        self.nombres = set(p.nombre.lower() for p in self.productos.values())

    @classmethod
    def cargar_desde_bd(cls):
        # Carga todos los productos desde la base de datos
        productos = Producto.query.all()              # -> list[Producto]
        productos_dict = {p.id: p for p in productos} # Crea dict por id
        return cls(productos_dict)

    # --- CRUD ---
    def agregar(self, nombre: str, cantidad: int, precio: float) -> Producto:
        # Agrega un nuevo producto al inventario y a la base de datos
        if nombre.lower() in self.nombres:
            raise ValueError('Ya existe un producto con ese nombre.')
        p = Producto(nombre=nombre.strip(), cantidad=int(cantidad), precio=float(precio))
        db.session.add(p)
        db.session.commit()
        self.productos[p.id] = p
        self.nombres.add(p.nombre.lower())
        return p

    def eliminar(self, id: int) -> bool:
        # Elimina un producto por id del inventario y la base de datos
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return False
        db.session.delete(p)
        db.session.commit()
        self.productos.pop(id, None)
        self.nombres.discard(p.nombre.lower())
        return True

    def actualizar(self, id: int, nombre=None, cantidad=None, precio=None) -> Producto | None:
        # Actualiza los datos de un producto existente
        p = self.productos.get(id) or Producto.query.get(id)
        if not p:
            return None
        if nombre is not None:
            nuevo = nombre.strip()
            # Verifica si el nuevo nombre ya existe en el inventario
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

    # --- Consultas con colecciones ---
    def buscar_por_nombre(self, q: str):
        # Busca productos cuyo nombre contenga el texto 'q' (insensible a mayúsculas)
        q = q.lower()
        # Filtra productos y los ordena por nombre
        return sorted([p for p in self.productos.values() if q in p.nombre.lower()],
                      key=lambda x: x.nombre)

    def listar_todos(self):
        # Devuelve todos los productos ordenados por nombre
        return sorted(self.productos.values(), key=lambda x: x.nombre)
