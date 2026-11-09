# -*- coding: utf-8 -*-
"""
Скрипт генерации профессиональных диаграмм для курсового проекта
«База данных и ИС автосервиса»
1. org_structure.png — Организационная структура ООО «АвтоМастер-Сервис»
2. idef0_a0.png — Контекстная диаграмма бизнес-процесса IDEF0 (A0)
3. dfd_order_flow.png — Диаграмма потоков данных DFD (Обслуживание клиента и заказ-наряд)
4. is_architecture.png — Архитектура ИС, администрирование и безопасность БД
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import os

# Настройка шрифтов для корректного отображения кириллицы
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'diagrams'))

def create_org_structure():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Заголовок
    ax.text(7, 8.5, 'ОРГАНИЗАЦИОННАЯ СТРУКТУРА АВТОСЕРВИСА\nООО «АвтоМастер-Сервис»',
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1A202C')

    # Стили боксов
    def draw_box(x, y, w, h, title, subtitle, bg_color='#EDF2F7', border_color='#2B6CB0'):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                             facecolor=bg_color, edgecolor=border_color, linewidth=1.8, zorder=2)
        ax.add_patch(box)
        ax.text(x + w/2, y + h*0.65, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color='#1A365D', zorder=3)
        ax.text(x + w/2, y + h*0.3, subtitle, ha='center', va='center',
                fontsize=8.5, color='#4A5568', zorder=3, multialignment='center')

    # Генеральный директор
    draw_box(4.5, 6.8, 5.0, 1.2, 'Генеральный директор',
             'Стратегическое планирование, общий финансовый контроль,\nутверждение штатного расписания и регламентов',
             bg_color='#EBF8FF', border_color='#2B6CB0')

    # Линия вниз от директора
    ax.plot([7, 7], [6.8, 5.6], color='#4A5568', lw=2, zorder=1)
    ax.plot([1.8, 12.2], [5.6, 5.6], color='#4A5568', lw=2, zorder=1)

    # 4 подразделения
    # 1. Администрация / Бухгалтерия
    ax.plot([1.8, 1.8], [5.6, 4.8], color='#4A5568', lw=2, zorder=1)
    draw_box(0.5, 3.6, 2.6, 1.2, 'Бухгалтерия',
             'Финансовый учет, налоги,\nрасчет заработной платы,\nрасчеты с контрагентами',
             bg_color='#F7FAFC', border_color='#4A5568')

    # 2. Сервисный отдел (Клиентская зона)
    ax.plot([5.0, 5.0], [5.6, 4.8], color='#4A5568', lw=2, zorder=1)
    draw_box(3.7, 3.6, 2.6, 1.2, 'Сервисный отдел\n(Приемка)',
             'Мастера-приемщики:\nприем клиентов, дефектовка,\nоткрытие и закрытие заказов',
             bg_color='#EBF8FF', border_color='#3182CE')

    # 3. Производственный цех (Ремзона)
    ax.plot([8.7, 8.7], [5.6, 4.8], color='#4A5568', lw=2, zorder=1)
    draw_box(7.4, 3.6, 2.6, 1.2, 'Ремонтная зона\n(Производство)',
             'Начальник цеха / Мастера:\nавтомеханики, слесари,\nэлектрики-диагносты, мотористы',
             bg_color='#F0FFF4', border_color='#38A169')

    # 4. Складской сектор
    ax.plot([12.2, 12.2], [5.6, 4.8], color='#4A5568', lw=2, zorder=1)
    draw_box(10.9, 3.6, 2.6, 1.2, 'Складской сектор',
             'Кладовщик / Снабженец:\nприемка запчастей, учет остатков,\nвыдача под заказ-наряды',
             bg_color='#FFFAF0', border_color='#DD6B20')

    # Нижний уровень должностей
    # Детализация ролей
    def draw_subrole(x, y, w, h, text, color='#718096'):
        b = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.05",
                           facecolor='#FFFFFF', edgecolor=color, linewidth=1.2, linestyle='--', zorder=2)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8, color='#2D3748', zorder=3)

    # Вертикальные связки к нижним должностям
    ax.plot([1.8, 1.8], [3.6, 2.8], color='#CBD5E0', lw=1.5, zorder=1)
    draw_subrole(0.5, 2.0, 2.6, 0.8, 'Главный бухгалтер\n(1 чел.)')

    ax.plot([5.0, 5.0], [3.6, 2.8], color='#CBD5E0', lw=1.5, zorder=1)
    draw_subrole(3.7, 1.8, 2.6, 1.0, 'Старший мастер-приемщик\nМастера-консультанты\n(2 чел.)')

    ax.plot([8.7, 8.7], [3.6, 2.8], color='#CBD5E0', lw=1.5, zorder=1)
    draw_subrole(7.4, 1.6, 2.6, 1.2, 'Автомеханики-слесари (3 чел.)\nАвтоэлектрик-диагност (1 чел.)\nМастер сход-развала (1 чел.)')

    ax.plot([12.2, 12.2], [3.6, 2.8], color='#CBD5E0', lw=1.5, zorder=1)
    draw_subrole(10.9, 2.0, 2.6, 0.8, 'Кладовщик-учетчик\n(1 чел.)')

    # Подвал
    ax.text(7, 0.6, 'Тип структуры: Линейно-функциональная. Штатная численность: 10 человек.',
            ha='center', va='center', fontsize=9.5, fontstyle='italic', color='#718096')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'org_structure.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print('Created:', out_path)


def create_idef0_a0():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Заголовок
    ax.text(7, 8.6, 'КОНТЕКСТНАЯ ДИАГРАММА IDEF0 (БЛОК A0)\nТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ И РЕМОНТ АВТОМОБИЛЕЙ',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A202C')

    # Центральный блок А0
    bx, by, bw, bh = 4.2, 3.2, 5.6, 2.6
    box = FancyBboxPatch((bx, by), bw, bh, boxstyle="square,pad=0.1",
                         facecolor='#EBF8FF', edgecolor='#2B6CB0', linewidth=2.5, zorder=2)
    ax.add_patch(box)
    ax.text(bx + bw/2, by + bh/2 + 0.3,
            'Выполнение технического\nобслуживания и ремонта\nавтомобилей клиентов',
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1A365D', zorder=3)
    ax.text(bx + bw - 0.4, by + 0.3, 'A0', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#2B6CB0', zorder=3)

    # Стрелки:
    # 1. ВХОДЫ (Inputs - слева)
    # Стрелка 1: Неисправный автомобиль
    ax.annotate('', xy=(bx, by + 1.9), xytext=(0.5, by + 1.9),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(0.7, by + 2.1, 'Неисправный автомобиль\n(объект обслуживания)', fontsize=9, color='#2D3748', fontweight='bold')

    # Стрелка 2: Заявка / жалоба клиента
    ax.annotate('', xy=(bx, by + 1.1), xytext=(0.5, by + 1.1),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(0.7, by + 1.3, 'Заявка и обращение клиента\n(симптомы неисправности)', fontsize=9, color='#2D3748', fontweight='bold')

    # Стрелка 3: Запчасти и расходные материалы
    ax.annotate('', xy=(bx, by + 0.4), xytext=(0.5, by + 0.4),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(0.7, by + 0.55, 'Автозапчасти и расходники\nот поставщиков', fontsize=9, color='#2D3748', fontweight='bold')

    # 2. УПРАВЛЕНИЕ (Controls - сверху)
    # Стрелка C1: Технологические карты и регламенты
    ax.annotate('', xy=(bx + 1.5, by + bh), xytext=(bx + 1.5, 7.8),
                arrowprops=dict(arrowstyle="-|>", color='#744210', lw=2, mutation_scale=15))
    ax.text(bx + 1.6, 7.5, 'Регламенты автопроизводителей,\nтехнологические карты ТО', fontsize=8.5, color='#744210', fontweight='bold')

    # Стрелка C2: Законодательство и Прейскурант
    ax.annotate('', xy=(bx + 4.2, by + bh), xytext=(bx + 4.2, 7.8),
                arrowprops=dict(arrowstyle="-|>", color='#744210', lw=2, mutation_scale=15))
    ax.text(bx + 4.3, 7.5, 'Законодательство РФ (ЗоЗПП),\nпрайс-лист и нормо-часы', fontsize=8.5, color='#744210', fontweight='bold')

    # 3. МЕХАНИЗМЫ (Mechanisms - снизу)
    # Стрелка M1: Персонал
    ax.annotate('', xy=(bx + 1.5, by), xytext=(bx + 1.5, 1.2),
                arrowprops=dict(arrowstyle="-|>", color='#276749', lw=2, mutation_scale=15))
    ax.text(bx + 0.2, 1.5, 'Персонал сервиса\n(мастера-приемщики,\nмеханики, кладовщик)', fontsize=8.5, color='#276749', fontweight='bold')

    # Стрелка M2: Оборудование и ИС
    ax.annotate('', xy=(bx + 4.2, by), xytext=(bx + 4.2, 1.2),
                arrowprops=dict(arrowstyle="-|>", color='#276749', lw=2, mutation_scale=15))
    ax.text(bx + 4.3, 1.5, 'Оборудование сервиса и\nИС «АвтоСервис-Экспресс»\n(СУБД SQLite 3)', fontsize=8.5, color='#276749', fontweight='bold')

    # 4. ВЫХОДЫ (Outputs - справа)
    # Стрелка O1: Исправный автомобиль
    ax.annotate('', xy=(13.5, by + 2.0), xytext=(bx + bw, by + 2.0),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(bx + bw + 0.3, by + 2.15, 'Исправный автомобиль\n(прошедший ОТК)', fontsize=9, color='#2D3748', fontweight='bold')

    # Стрелка O2: Закрытый заказ-наряд и гарантия
    ax.annotate('', xy=(13.5, by + 1.3), xytext=(bx + bw, by + 1.3),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(bx + bw + 0.3, by + 1.45, 'Закрытый заказ-наряд,\nакт работ и гарантийный талон', fontsize=9, color='#2D3748', fontweight='bold')

    # Стрелка O3: Финансовая оплата
    ax.annotate('', xy=(13.5, by + 0.5), xytext=(bx + bw, by + 0.5),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=2, mutation_scale=15))
    ax.text(bx + bw + 0.3, by + 0.65, 'Денежные средства\n(оплата заказ-наряда)', fontsize=9, color='#2D3748', fontweight='bold')

    # Легенда IDEF0 внизу
    ax.text(7, 0.4, 'Нотация IDEF0: Вход (слева) | Управление (сверху) | Механизм (снизу) | Выход (справа)',
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#718096')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'idef0_a0.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print('Created:', out_path)


def create_dfd_order_flow():
    fig, ax = plt.subplots(figsize=(15, 9.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    # Заголовок
    ax.text(7.5, 9.0, 'DFD-ДИАГРАММА ПОТОКОВ ДАННЫХ (УРОВЕНЬ 1)\nПРОЦЕСС ОБСЛУЖИВАНИЯ КЛИЕНТА И ЖИЗНЕННЫЙ ЦИКЛ ЗАКАЗ-НАРЯДА',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1A202C')

    # Вспомогательные функции
    def draw_external(x, y, w, h, text):
        b = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0.05",
                           facecolor='#ED8936', edgecolor='#C05621', linewidth=2, zorder=2)
        ax.add_patch(b)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=3, multialignment='center')

    def draw_process(x, y, r, num, text):
        circle = patches.Circle((x, y), r, facecolor='#3182CE', edgecolor='#2B6CB0', linewidth=2, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y + 0.22, num, ha='center', va='center',
                fontsize=10, fontweight='bold', color='#FFFFFF', zorder=3)
        ax.text(x, y - 0.2, text, ha='center', va='center',
                fontsize=7.8, color='#FFFFFF', fontweight='bold', zorder=3, multialignment='center')

    def draw_store(x, y, w, h, num, text):
        ax.plot([x+w, x, x, x+w], [y+h, y+h, y, y], color='#2C5282', lw=2, zorder=2)
        ax.plot([x+0.8, x+0.8], [y, y+h], color='#2C5282', lw=1.5, zorder=2)
        ax.fill_between([x, x+w], y, y+h, color='#EBF8FF', zorder=1)
        ax.text(x + 0.4, y + h/2, num, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color='#2B6CB0', zorder=3)
        ax.text(x + 0.9 + (w-0.9)/2, y + h/2, text, ha='center', va='center',
                fontsize=8, color='#1A365D', fontweight='bold', zorder=3)

    # Внешние сущности (слева и справа)
    draw_external(0.4, 4.0, 2.1, 1.5, 'Внешняя сущность:\nКЛИЕНТ\n(Автовладелец)')
    draw_external(12.5, 4.0, 2.1, 1.5, 'Внешняя сущность:\nПОСТАВЩИК\nЗАПЧАСТЕЙ')

    # Верхний ряд процессов (1.0, 2.0, 3.0)
    draw_process(3.8, 7.0, 0.85, '1.0', 'Прием и\nзапись')
    draw_process(7.5, 7.0, 0.85, '2.0', 'Дефектовка\nи расчет')
    draw_process(11.2, 7.0, 0.85, '3.0', 'Заказ-наряд\nи ремзона')

    # Накопители данных (в центре, компактно)
    draw_store(5.5, 5.0, 4.0, 0.65, 'D1', 'База клиентов и автомобилей (clients, cars)')
    draw_store(5.5, 4.0, 4.0, 0.65, 'D2', 'Журнал заказ-нарядов (work_orders)')
    draw_store(5.5, 3.0, 4.0, 0.65, 'D3', 'Склад запасных частей (spare_parts)')

    # Нижний ряд процессов (6.0, 5.0, 4.0)
    draw_process(11.2, 1.5, 0.85, '4.0', 'Складской\nучет')
    draw_process(7.5, 1.5, 0.85, '5.0', 'Ремонтные\nработы')
    draw_process(3.8, 1.5, 0.85, '6.0', 'Оплата\nи выдача')

    # Стрелки потоков данных
    # Клиент -> 1.0
    ax.annotate('', xy=(3.0, 6.8), xytext=(1.5, 5.5),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(1.2, 6.5, 'Заявка, ФИО,\nгосномер', fontsize=7.5, color='#2D3748')

    # 1.0 -> 2.0
    ax.annotate('', xy=(6.65, 7.0), xytext=(4.65, 7.0),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(5.1, 7.2, 'Карточка осмотра', fontsize=7.5, color='#2D3748')

    # 2.0 -> 3.0
    ax.annotate('', xy=(10.35, 7.0), xytext=(8.35, 7.0),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(8.8, 7.2, 'Смета и состав работ', fontsize=7.5, color='#2D3748')

    # 1.0 -> D1
    ax.annotate('', xy=(5.5, 5.3), xytext=(4.2, 6.2),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=1.4, mutation_scale=12))
    ax.text(4.2, 5.5, 'Регистрация', fontsize=7, color='#2B6CB0')

    # 2.0 -> D2
    ax.annotate('', xy=(7.5, 4.65), xytext=(7.5, 6.15),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=1.4, mutation_scale=12))
    ax.text(7.6, 5.4, 'Создание заказа', fontsize=7, color='#2B6CB0')

    # 3.0 -> 4.0
    ax.annotate('', xy=(11.2, 2.35), xytext=(11.2, 6.15),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(11.3, 4.3, 'Резервирование\nдеталей', fontsize=7.5, color='#2D3748')

    # Поставщик -> 4.0
    ax.annotate('', xy=(12.05, 1.5), xytext=(12.8, 4.0),
                arrowprops=dict(arrowstyle="-|>", color='#C05621', lw=1.5, mutation_scale=12))
    ax.text(12.6, 2.6, 'Приход деталей\n(накладные)', fontsize=7.5, color='#C05621')

    # 4.0 -> D3
    ax.annotate('', xy=(9.5, 3.3), xytext=(10.5, 2.1),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=1.4, mutation_scale=12))
    ax.text(9.8, 2.8, 'Списание', fontsize=7, color='#2B6CB0')

    # 4.0 -> 5.0
    ax.annotate('', xy=(8.35, 1.5), xytext=(10.35, 1.5),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(8.7, 1.7, 'Выдача деталей', fontsize=7.5, color='#2D3748')

    # 5.0 -> 6.0
    ax.annotate('', xy=(4.65, 1.5), xytext=(6.65, 1.5),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(4.9, 1.7, 'Завершенный ремонт', fontsize=7.5, color='#2D3748')

    # 6.0 -> D2 (закрытие заказа)
    ax.annotate('', xy=(6.5, 4.0), xytext=(4.3, 2.2),
                arrowprops=dict(arrowstyle="-|>", color='#2B6CB0', lw=1.4, mutation_scale=12))
    ax.text(4.7, 3.3, 'Статус: Оплачен', fontsize=7, color='#2B6CB0')

    # 6.0 -> Клиент
    ax.annotate('', xy=(1.5, 4.0), xytext=(3.2, 2.1),
                arrowprops=dict(arrowstyle="-|>", color='#2D3748', lw=1.5, mutation_scale=12))
    ax.text(1.3, 2.8, 'Акт, чек, гарантия,\nисправное авто', fontsize=7.5, color='#2D3748')

    # Легенда
    ax.text(7.5, 0.4, 'Нотация DFD: Прямоугольник — Внешняя сущность | Круг — Процесс | Двойная линия — Накопитель данных',
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#718096')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'dfd_order_flow.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print('Created:', out_path)


def create_is_architecture():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Заголовок
    ax.text(7, 8.6, 'АРХИТЕКТУРА ИНФОРМАЦИОННОЙ СИСТЕМЫ И БЕЗОПАСНОСТЬ БАЗЫ ДАННЫХ\n«АвтоСервис-Экспресс» (СУБД SQLite 3)',
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#1A202C')

    # Центральное ядро
    cx, cy, cw, ch = 5.0, 3.6, 4.0, 2.0
    core = FancyBboxPatch((cx, cy), cw, ch, boxstyle="round,pad=0.1,rounding_size=0.2",
                          facecolor='#EBF8FF', edgecolor='#2B6CB0', linewidth=2.5, zorder=2)
    ax.add_patch(core)
    ax.text(cx + cw/2, cy + ch*0.65, 'ЯДРО ИС И БАЗА ДАННЫХ\n«АвтоСервис-Экспресс»',
            ha='center', va='center', fontsize=11, fontweight='bold', color='#1A365D', zorder=3)
    ax.text(cx + cw/2, cy + ch*0.25, 'Файл: autoservice.db (SQLite 3)\nWAL-режим, ACID, Foreign Keys = ON',
            ha='center', va='center', fontsize=8.5, color='#2C5282', zorder=3)

    # 4 рабочих места вокруг ядра (АРМ)
    def draw_terminal(x, y, w, h, title, subtitle, color='#2B6CB0'):
        b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                           facecolor='#FFFFFF', edgecolor=color, linewidth=1.8, zorder=2)
        ax.add_patch(b)
        ax.text(x + w/2, y + h*0.68, title, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color='#1A365D', zorder=3)
        ax.text(x + w/2, y + h*0.3, subtitle, ha='center', va='center',
                fontsize=8, color='#4A5568', zorder=3, multialignment='center')

    # Сверху: АРМ Мастера-приемщика
    draw_terminal(4.7, 6.7, 4.6, 1.4, 'Терминал Мастера-приемщика\n(Настольное рабочее место)',
                  'Прием клиентов, карточки ТС, дефектовка,\nрасчет стоимости, закрытие заказ-нарядов', color='#3182CE')
    # Двусторонняя стрелка
    ax.annotate('', xy=(7.0, 5.7), xytext=(7.0, 6.6),
                arrowprops=dict(arrowstyle="<|-|>", color='#3182CE', lw=2.5, mutation_scale=15))

    # Снизу: Резервное копирование и Администрирование
    draw_terminal(4.7, 1.1, 4.6, 1.4, 'Контур администрирования и бэкапа\n(Служба безопасности и резервирования)',
                  'Ежесуточный дамп базы (Backup),\nшифрование ПДн (ФЗ-152), журнал транзакций', color='#38A169')
    ax.annotate('', xy=(7.0, 3.5), xytext=(7.0, 2.6),
                arrowprops=dict(arrowstyle="<|-|>", color='#38A169', lw=2.5, mutation_scale=15))

    # Слева: Веб-клиент / Онлайн-запись
    draw_terminal(0.5, 3.9, 3.5, 1.4, 'Веб-сервис онлайн-записи\n(Клиентский портал)',
                  'Запись клиентов через сайт / Telegram-бот,\nпредварительный выбор удобного времени', color='#DD6B20')
    ax.annotate('', xy=(4.9, 4.6), xytext=(4.1, 4.6),
                arrowprops=dict(arrowstyle="<|-|>", color='#DD6B20', lw=2.5, mutation_scale=15))

    # Справа вверху: Планшет механика
    draw_terminal(10.0, 5.3, 3.5, 1.4, 'Мобильный терминал Механика\n(Планшет в ремзоне)',
                  'Список назначенных работ, нормы времени,\nзапрос запчастей со склада, отметка выполнения', color='#805AD5')
    ax.annotate('', xy=(9.1, 4.9), xytext=(9.9, 5.6),
                arrowprops=dict(arrowstyle="<|-|>", color='#805AD5', lw=2.5, mutation_scale=15))

    # Справа внизу: АРМ Кладовщика
    draw_terminal(10.0, 2.5, 3.5, 1.4, 'Терминал Кладовщика\n(АРМ Складской учет)',
                  'Приход/списание автозапчастей,\nконтроль неснижаемого остатка, сканер штрихкодов', color='#D69E2E')
    ax.annotate('', xy=(9.1, 4.3), xytext=(9.9, 3.6),
                arrowprops=dict(arrowstyle="<|-|>", color='#D69E2E', lw=2.5, mutation_scale=15))

    # Подвал
    ax.text(7, 0.4, 'Архитектура: Клиент-серверное взаимодействие / Локальная сеть автосервиса. Защита: RBAC + ФЗ-152.',
            ha='center', va='center', fontsize=9, fontstyle='italic', color='#718096')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'is_architecture.png')
    plt.savefig(out_path, dpi=300)
    plt.close()
    print('Created:', out_path)

if __name__ == '__main__':
    create_org_structure()
    create_idef0_a0()
    create_dfd_order_flow()
    create_is_architecture()
    print('All 4 diagrams generated successfully!')
