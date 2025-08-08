-- Esquema para catálogo de ecommerce
-- Optimizado para Supabase PostgreSQL

-- Tabla de categorías
CREATE TABLE categories (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    slug VARCHAR(255) UNIQUE NOT NULL,
    image_url TEXT,
    parent_id UUID REFERENCES categories(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla de productos
CREATE TABLE products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    short_description VARCHAR(500),
    price DECIMAL(10,2) NOT NULL,
    compare_price DECIMAL(10,2),
    cost DECIMAL(10,2),
    sku VARCHAR(100) UNIQUE,
    barcode VARCHAR(100),
    stock_quantity INTEGER DEFAULT 0,
    min_stock_level INTEGER DEFAULT 0,
    weight DECIMAL(8,3),
    dimensions JSONB,
    images JSONB DEFAULT '[]',
    category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    brand VARCHAR(100),
    tags TEXT[],
    attributes JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    is_taxable BOOLEAN DEFAULT TRUE,
    meta_title VARCHAR(60),
    meta_description VARCHAR(160),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);

-- Función para actualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_categories_updated_at BEFORE UPDATE ON categories
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Datos de ejemplo
INSERT INTO categories (name, description, slug) VALUES
('Proteínas', 'Suplementos proteicos en polvo y listos para consumir', 'proteinas'),
('Snacks Saludables', 'Snacks bajos en azúcar y ricos en nutrientes', 'snacks-saludables'),
('Bebidas Saludables', 'Jugos naturales, aguas infundidas y bebidas funcionales', 'bebidas-saludables'),
('Panadería Saludable', 'Panes, galletas y productos horneados saludables', 'panaderia-saludable'),
('Frutas y Verduras', 'Productos frescos y pre-listos para consumo', 'frutas-verduras');

INSERT INTO products (name, slug, description, price, stock_quantity, category_id, images, attributes) VALUES
('Proteína Whey 100% Natural', 'proteina-whey-natural', 'Proteína whey de alta calidad sin aditivos artificiales', 45000.00, 50, (SELECT id FROM categories WHERE slug = 'proteinas'), '[{"url": "https://example.com/proteina.jpg", "alt": "Proteína Whey"}]', '{"sabor": "vainilla", "peso": "1kg", "marca": "NaturePro"}'),
('Barra de Proteína Casera', 'barra-proteina-casera', 'Barra energética con 15g de proteína por porción', 3500.00, 100, (SELECT id FROM categories WHERE slug = 'snacks-saludables'), '[{"url": "https://example.com/barra.jpg", "alt": "Barra de Proteína"}]', '{"proteina": "15g", "calorias": "180", "sin_gluten": true}'),
('Jugo Verde Detox', 'jugo-verde-detox', 'Jugo natural con espinaca, pepino y manzana verde', 8000.00, 30, (SELECT id FROM categories WHERE slug = 'bebidas-saludables'), '[{"url": "https://example.com/jugo.jpg", "alt": "Jugo Verde"}]', '{"tamaño": "500ml", "calorias": "120", "ingredientes": ["espinaca", "pepino", "manzana"]}'),
('Pan Integral de Semillas', 'pan-integral-semillas', 'Pan artesanal con semillas de chía y lino', 12000.00, 25, (SELECT id FROM categories WHERE slug = 'panaderia-saludable'), '[{"url": "https://example.com/pan.jpg", "alt": "Pan Integral"}]', '{"tipo": "integral", "semillas": ["chia", "lino", "girasol"], "sin_azucar": true}'),
('Ensalada Proteica Pre-armada', 'ensalada-proteica-prearmada', 'Ensalada lista con pollo, quinoa y vegetales frescos', 18000.00, 20, (SELECT id FROM categories WHERE slug = 'frutas-verduras'), '[{"url": "https://example.com/ensalada.jpg", "alt": "Ensalada Proteica"}]', '{"proteina": "25g", "calorias": "350", "tiempo_preparacion": "3 min"}');

-- Vista para productos con categoría
CREATE VIEW products_with_category AS
SELECT 
    p.id,
    p.name,
    p.slug,
    p.description,
    p.price,
    p.stock_quantity,
    p.images,
    p.attributes,
    p.is_active,
    p.created_at,
    c.name as category_name,
    c.slug as category_slug
FROM products p
JOIN categories c ON p.category_id = c.id;
