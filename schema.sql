-- ========================================================
-- СХЕМА БАЗЫ ДАННЫХ АВТОСЕРВИСА (SQLite 3)
-- Проект: Информационная система управления автосервисом
-- Соответствие 3-й нормальной форме (3NF)
-- ========================================================

PRAGMA foreign_keys = ON;

-- 1. Таблица клиентов
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE,
    email TEXT,
    address TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 2. Таблица автомобилей клиентов
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    license_plate TEXT NOT NULL UNIQUE,
    vin TEXT NOT NULL UNIQUE,
    year INTEGER NOT NULL CHECK(year >= 1970 AND year <= 2030),
    mileage INTEGER NOT NULL CHECK(mileage >= 0),
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);

-- 3. Таблица сотрудников автосервиса
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    position TEXT NOT NULL,
    specialization TEXT,
    phone TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    salary_rate REAL NOT NULL CHECK(salary_rate >= 0)
);

-- 4. Справочник услуг автосервиса
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    standard_hours REAL NOT NULL CHECK(standard_hours > 0),
    price REAL NOT NULL CHECK(price >= 0)
);

-- 5. Каталог запасных частей и склад
CREATE TABLE IF NOT EXISTS spare_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    cost_price REAL NOT NULL CHECK(cost_price >= 0),
    selling_price REAL NOT NULL CHECK(selling_price >= cost_price),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
    min_stock_level INTEGER NOT NULL DEFAULT 2 CHECK(min_stock_level >= 0)
);

-- 6. Таблица заказ-нарядов
CREATE TABLE IF NOT EXISTS work_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT NOT NULL UNIQUE,
    car_id INTEGER NOT NULL,
    manager_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Новый' CHECK(status IN ('Новый', 'В работе', 'Ожидает запчастей', 'Завершен', 'Оплачен', 'Отменен')),
    description TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    closed_at TEXT,
    total_amount REAL NOT NULL DEFAULT 0.0 CHECK(total_amount >= 0),
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE RESTRICT,
    FOREIGN KEY (manager_id) REFERENCES employees(id) ON DELETE RESTRICT
);

-- 7. Оказанные услуги в заказ-наряде
CREATE TABLE IF NOT EXISTS order_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_order_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    mechanic_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE RESTRICT,
    FOREIGN KEY (mechanic_id) REFERENCES employees(id) ON DELETE RESTRICT
);

-- 8. Использованные запчасти в заказ-наряде
CREATE TABLE IF NOT EXISTS order_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_order_id INTEGER NOT NULL,
    spare_part_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    subtotal REAL NOT NULL CHECK(subtotal >= 0),
    FOREIGN KEY (work_order_id) REFERENCES work_orders(id) ON DELETE CASCADE,
    FOREIGN KEY (spare_part_id) REFERENCES spare_parts(id) ON DELETE RESTRICT
);

-- Индексы для ускорения поиска
CREATE INDEX IF NOT EXISTS idx_cars_client_id ON cars(client_id);
CREATE INDEX IF NOT EXISTS idx_cars_license_plate ON cars(license_plate);
CREATE INDEX IF NOT EXISTS idx_work_orders_status ON work_orders(status);
CREATE INDEX IF NOT EXISTS idx_work_orders_car_id ON work_orders(car_id);
CREATE INDEX IF NOT EXISTS idx_spare_parts_sku ON spare_parts(sku);
