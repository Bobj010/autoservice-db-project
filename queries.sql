-- ====================================================================
-- ТИПОВЫЕ SQL-ЗАПРОСЫ ПОЛЬЗОВАТЕЛЕЙ ИНФОРМАЦИОННОЙ СИСТЕМЫ АВТОСЕРВИСА
-- (К разделу 5 аналитического отчета)
-- ====================================================================

-- --------------------------------------------------------------------
-- РОЛЬ 1: МАСТЕР-ПРИЕМЩИК
-- --------------------------------------------------------------------

-- Запрос 1.1: Поиск клиента и автомобиля по госномеру
-- Назначение: Быстро идентифицировать клиента и машину при въезде в автосервис
SELECT 
    c.id AS car_id,
    c.brand || ' ' || c.model AS car_model,
    c.license_plate,
    c.vin,
    c.year,
    c.mileage,
    cl.full_name AS owner_name,
    cl.phone AS owner_phone
FROM cars c
JOIN clients cl ON c.client_id = cl.id
WHERE c.license_plate = 'А123ВС777';

-- Запрос 1.2: Список всех активных заказ-нарядов со статусами 'В работе', 'Ожидает запчастей', 'Новый'
-- Назначение: Мониторинг загруженности ремзоны и контроля сроков
SELECT 
    wo.order_number,
    wo.status,
    wo.created_at,
    c.license_plate,
    c.brand || ' ' || c.model AS car_model,
    cl.full_name AS client_name,
    cl.phone AS client_phone,
    e.full_name AS manager_name,
    wo.description
FROM work_orders wo
JOIN cars c ON wo.car_id = c.id
JOIN clients cl ON c.client_id = cl.id
JOIN employees e ON wo.manager_id = e.id
WHERE wo.status IN ('Новый', 'В работе', 'Ожидает запчастей')
ORDER BY wo.created_at DESC;

-- Запрос 1.3: Полная детализация конкретного заказ-наряда (услуги + запчасти + итог)
-- Назначение: Формирование печатного заказ-наряда для выдачи клиенту
SELECT 
    'Услуга' AS item_type,
    s.name AS item_name,
    os.quantity,
    os.unit_price,
    os.subtotal,
    e.full_name AS performer
FROM order_services os
JOIN services s ON os.service_id = s.id
JOIN employees e ON os.mechanic_id = e.id
WHERE os.work_order_id = 1
UNION ALL
SELECT 
    'Запчасть' AS item_type,
    sp.name AS item_name,
    op.quantity,
    op.unit_price,
    op.subtotal,
    sp.manufacturer AS performer
FROM order_parts op
JOIN spare_parts sp ON op.spare_part_id = sp.id
WHERE op.work_order_id = 1;


-- --------------------------------------------------------------------
-- РОЛЬ 2: АВТОМЕХАНИК
-- --------------------------------------------------------------------

-- Запрос 2.1: Список назначенных работ конкретному механику на сегодня/в работе
-- Назначение: Механик видит свои задачи и автомобили, над которыми нужно работать
SELECT 
    wo.order_number,
    c.brand || ' ' || c.model AS car,
    c.license_plate,
    s.name AS service_name,
    s.standard_hours,
    wo.status AS order_status
FROM order_services os
JOIN work_orders wo ON os.work_order_id = wo.id
JOIN cars c ON wo.car_id = c.id
JOIN services s ON os.service_id = s.id
WHERE os.mechanic_id = 4 AND wo.status IN ('Новый', 'В работе');

-- Запрос 2.2: Проверка наличия запчастей на складе под задачи
-- Назначение: Механик проверяет перед началом разборки узла, есть ли деталь на складе
SELECT 
    sku,
    name,
    manufacturer,
    stock_quantity
FROM spare_parts
WHERE stock_quantity > 0
ORDER BY name;


-- --------------------------------------------------------------------
-- РОЛЬ 3: КЛАДОВЩИК
-- --------------------------------------------------------------------

-- Запрос 3.1: Запчасти с критическим остатком (меньше или равно минимального уровня)
-- Назначение: Формирование заявки поставщику на пополнение склада
SELECT 
    sku,
    name,
    manufacturer,
    stock_quantity,
    min_stock_level,
    (min_stock_level - stock_quantity + 5) AS recommended_order_qty,
    cost_price,
    (min_stock_level - stock_quantity + 5) * cost_price AS estimated_cost
FROM spare_parts
WHERE stock_quantity <= min_stock_level;

-- Запрос 3.2: Общая инвентаризационная стоимость склада в закупочных и розничных ценах
-- Назначение: Инвентаризация и финансовая оценка остатков
SELECT 
    COUNT(*) AS total_positions,
    SUM(stock_quantity) AS total_items_count,
    ROUND(SUM(stock_quantity * cost_price), 2) AS total_cost_value,
    ROUND(SUM(stock_quantity * selling_price), 2) AS total_retail_value,
    ROUND(SUM(stock_quantity * (selling_price - cost_price)), 2) AS potential_profit
FROM spare_parts;


-- --------------------------------------------------------------------
-- РОЛЬ 4: ДИРЕКТОР / УПРАВЛЯЮЩИЙ
-- --------------------------------------------------------------------

-- Запрос 4.1: Финансовый отчет по закрытым заказ-нарядам (выручка, затраты, прибыль)
-- Назначение: Оценка рентабельности и финансового состояния предприятия
SELECT 
    COUNT(DISTINCT wo.id) AS completed_orders_count,
    ROUND(SUM(wo.total_amount), 2) AS total_revenue,
    ROUND(SUM(services_total.revenue), 2) AS services_revenue,
    ROUND(SUM(parts_total.revenue), 2) AS parts_revenue
FROM work_orders wo
LEFT JOIN (
    SELECT work_order_id, SUM(subtotal) AS revenue 
    FROM order_services GROUP BY work_order_id
) services_total ON wo.id = services_total.work_order_id
LEFT JOIN (
    SELECT work_order_id, SUM(subtotal) AS revenue 
    FROM order_parts GROUP BY work_order_id
) parts_total ON wo.id = parts_total.work_order_id
WHERE wo.status IN ('Завершен', 'Оплачен');

-- Запрос 4.2: Рейтинг автомехаников по сумме выполненных работ и нормо-часам
-- Назначение: Расчет премиального фонда и оценка производительности труда
SELECT 
    e.id AS employee_id,
    e.full_name,
    e.position,
    COUNT(os.id) AS jobs_count,
    ROUND(SUM(s.standard_hours * os.quantity), 1) AS total_hours_worked,
    ROUND(SUM(os.subtotal), 2) AS total_service_revenue
FROM employees e
JOIN order_services os ON e.id = os.mechanic_id
JOIN services s ON os.service_id = s.id
JOIN work_orders wo ON os.work_order_id = wo.id
WHERE wo.status IN ('Завершен', 'Оплачен')
GROUP BY e.id, e.full_name, e.position
ORDER BY total_service_revenue DESC;

-- Запрос 4.3: ТОП-5 самых востребованных услуг автосервиса
-- Назначение: Анализ спроса и оптимизация прайс-листа
SELECT 
    s.name AS service_name,
    s.category,
    COUNT(os.id) AS orders_count,
    SUM(os.quantity) AS total_quantity,
    ROUND(SUM(os.subtotal), 2) AS total_sales
FROM services s
JOIN order_services os ON s.id = os.service_id
GROUP BY s.id, s.name, s.category
ORDER BY total_sales DESC
LIMIT 5;

-- Запрос 4.4: Рейтинг лояльности клиентов (сумма заказов и количество обращений)
-- Назначение: Программа лояльности и выявление ключевых клиентов
SELECT 
    cl.id AS client_id,
    cl.full_name,
    cl.phone,
    COUNT(DISTINCT wo.id) AS orders_count,
    ROUND(SUM(wo.total_amount), 2) AS total_spent
FROM clients cl
JOIN cars c ON cl.id = c.client_id
JOIN work_orders wo ON c.id = wo.car_id
WHERE wo.status IN ('Завершен', 'Оплачен')
GROUP BY cl.id, cl.full_name, cl.phone
ORDER BY total_spent DESC;
