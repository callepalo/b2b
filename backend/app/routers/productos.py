from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional, Union
from app.models import ProductoBase, ProductoCreate, Producto
from config.supabase import get_supabase

router = APIRouter(tags=["productos"])

# Endpoints
@router.get("", response_model=List[Producto], response_model_exclude_none=True)
async def obtener_productos(
    categoria_id: Optional[str] = Query(None, description="Filtrar por ID de categoría")
):
    """Obtener todos los productos, opcionalmente filtrados por categoría"""
    try:
        print("Obteniendo cliente de Supabase...")
        supabase = get_supabase()
        print("Cliente de Supabase obtenido")
        
        print("Preparando consulta a la tabla 'productos'...")
        # Incluir la relación con categorías en la consulta
        query = supabase.table('productos').select('*, categorias(*)')
        
        if categoria_id:
            print(f"Filtrando por categoría_id: {categoria_id}")
            query = query.eq('categoria_id', categoria_id)
        
        print("Ejecutando consulta...")
        response = query.execute()
        print(f"Respuesta de Supabase: {response}")
        
        # Asegurarse de que siempre devolvemos una lista
        if not response.data:
            print("No se encontraron productos")
            return []
        
        # Formatear la respuesta para incluir la categoría
        productos_formateados = []
        for producto in response.data:
            if 'categorias' in producto and producto['categorias']:
                producto['categoria'] = producto.pop('categorias')
            productos_formateados.append(producto)
            
        print(f"Productos encontrados: {len(productos_formateados)}")
        return productos_formateados
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error en obtener_productos: {str(e)}")
        print(f"Detalles del error: {error_details}")
        
        # Intentar obtener más detalles del error de Supabase si está disponible
        error_msg = str(e)
        if hasattr(e, 'message'):
            error_msg = e.message
        elif hasattr(e, 'args') and e.args:
            error_msg = str(e.args[0])
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Error al obtener los productos",
                "error": error_msg,
                "type": type(e).__name__
            }
        )

@router.get("/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: str):  # Cambiado de int a str
    """Obtener un producto por ID con su categoría"""
    supabase = get_supabase()
    
    # Obtener el producto con la relación de categoría
    response = supabase.table('productos')\
        .select('*, categorias(*)')\
        .eq('id', producto_id)\
        .execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Formatear la respuesta para incluir la categoría
    producto = response.data[0]
    if 'categorias' in producto and producto['categorias']:
        producto['categoria'] = producto.pop('categorias')
    
    return producto

@router.post("", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto"""
    supabase = get_supabase()
    
    # Verificar si ya existe un producto con el mismo nombre
    existing = supabase.table('productos').select('id').eq('nombre', producto.nombre).execute()
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con este nombre"
        )
    
    # Verificar que la categoría exista
    categoria = supabase.table('categorias').select('id').eq('id', producto.categoria_id).execute()
    if not categoria.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No existe una categoría con ID {producto.categoria_id}"
        )
    
    # Crear el producto
    response = supabase.table('productos').insert(producto.model_dump()).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear el producto"
        )
    
    # Obtener el producto recién creado con sus relaciones
    nuevo_producto = supabase.table('productos')\
        .select('*, categorias!inner(*)')\
        .eq('id', response.data[0]['id'])\
        .execute()
    
    if not nuevo_producto.data:
        # Si no se pudo obtener con la relación, devolver solo los datos básicos
        return response.data[0]
        
    # Asegurarse de que la categoría esté en el formato esperado
    producto_con_categoria = nuevo_producto.data[0]
    if 'categorias' in producto_con_categoria and producto_con_categoria['categorias']:
        producto_con_categoria['categoria'] = producto_con_categoria.pop('categorias')
    
    return producto_con_categoria

@router.put("/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: str, producto: ProductoCreate):  # Cambiado de int a str
    """Actualizar un producto existente"""
    supabase = get_supabase()
    
    # Verificar si el producto existe
    existing = supabase.table('productos').select('*').eq('id', producto_id).execute()
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    # Verificar si hay otro producto con el mismo nombre
    same_name = supabase.table('productos') \
        .select('id') \
        .eq('nombre', producto.nombre) \
        .neq('id', producto_id) \
        .execute()
    
    if same_name.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe otro producto con este nombre"
        )
    
    response = supabase.table('productos').update(producto.model_dump()).eq('id', producto_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el producto"
        )
    
    return response.data[0]

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: str):  # Cambiado de int a str
    """Eliminar un producto"""
    supabase = get_supabase()
    
    # Verificar si el producto existe
    existing = supabase.table('productos').select('id').eq('id', producto_id).execute()
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    response = supabase.table('productos').delete().eq('id', producto_id).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el producto"
        )
    
    return None
