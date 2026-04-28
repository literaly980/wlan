#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║         NETWORK LEARNING LAB  v2.0                      ║
║  Интерактивный симулятор компьютерных сетей              ║
║  Предмет: Компьютерные системы                           ║
║  Темы: Модель OSI  •  VLAN 802.1Q  •  Протокол STP      ║
║  Требования: Python 3.6+  (только tkinter, встроен)     ║
╚══════════════════════════════════════════════════════════╝
  Запуск:  python network_learning_lab.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import heapq

# ─────────────────────────────────────────────────────────
#  ЦВЕТА
# ─────────────────────────────────────────────────────────
BG       = '#0d1117'
SURF     = '#161b22'
SURF2    = '#21262d'
BORDER   = '#30363d'
ACCENT   = '#58a6ff'
GREEN    = '#3fb950'
YELLOW   = '#d29922'
RED      = '#f85149'
PURPLE   = '#bc8cff'
ORANGE   = '#ffa657'
TEXT     = '#c9d1d9'
DIM      = '#8b949e'
GOLD     = '#e3b341'
TEAL     = '#39d353'

# ─────────────────────────────────────────────────────────
#  ДАННЫЕ — OSI
# ─────────────────────────────────────────────────────────
OSI_LAYERS = [
    {
        'num': 7, 'name': 'Прикладной', 'en': 'Application Layer',
        'color': '#b91c1c', 'pdu': 'Данные (Data)',
        'protocols': 'HTTP, HTTPS, FTP, SMTP, POP3, DNS, DHCP, SSH, Telnet, SNMP',
        'function': (
            '• Предоставляет сетевые сервисы пользователям и приложениям.\n'
            '• Интерфейс между программами и сетевым стеком.\n'
            '• Управляет аутентификацией и конфиденциальностью.'
        ),
        'devices': 'Прокси-серверы, WAF, шлюзы приложений',
        'tcpip': 'Прикладной',
        'example': 'Браузер загружает страницу по HTTPS (порт 443)',
    },
    {
        'num': 6, 'name': 'Представления', 'en': 'Presentation Layer',
        'color': '#c2410c', 'pdu': 'Данные (Data)',
        'protocols': 'SSL/TLS, JPEG, GIF, MPEG, ASCII, Unicode, XDR',
        'function': (
            '• Преобразование форматов данных (кодирование/декодирование).\n'
            '• Шифрование и дешифрование данных (SSL/TLS).\n'
            '• Сжатие и распаковка трафика.'
        ),
        'devices': 'SSL-ускорители, шлюзы шифрования',
        'tcpip': 'Прикладной',
        'example': 'TLS шифрует HTTP-данные → получается HTTPS',
    },
    {
        'num': 5, 'name': 'Сеансовый', 'en': 'Session Layer',
        'color': '#a16207', 'pdu': 'Данные (Data)',
        'protocols': 'NetBIOS, PPTP, RPC, SIP, SAP, NFS',
        'function': (
            '• Установка, поддержание, завершение сеансов.\n'
            '• Синхронизация диалога (кто когда говорит).\n'
            '• Восстановление сеанса после сбоя (checkpoint).'
        ),
        'devices': 'Шлюзы уровня сеансов',
        'tcpip': 'Прикладной',
        'example': 'Сессия входа на сайт сохраняется после перехода между страницами',
    },
    {
        'num': 4, 'name': 'Транспортный', 'en': 'Transport Layer',
        'color': '#15803d', 'pdu': 'Сегмент / Датаграмма',
        'protocols': 'TCP, UDP, SCTP, DCCP',
        'function': (
            '• Надёжная доставка (TCP) или быстрая без гарантий (UDP).\n'
            '• Мультиплексирование — порты 0..65535.\n'
            '• Управление потоком, контроль перегрузки.\n'
            '• Сегментация данных и сборка сегментов.'
        ),
        'devices': 'Файрволы L4, балансировщики нагрузки',
        'tcpip': 'Транспортный',
        'example': 'TCP: скачивание файла с подтверждениями. UDP: онлайн-игры.',
    },
    {
        'num': 3, 'name': 'Сетевой', 'en': 'Network Layer',
        'color': '#1d4ed8', 'pdu': 'Пакет (Packet)',
        'protocols': 'IPv4, IPv6, ICMP, ICMPv6, OSPF, BGP, RIP, IGMP',
        'function': (
            '• Логическая IP-адресация (IPv4: 32 бит, IPv6: 128 бит).\n'
            '• Маршрутизация пакетов между разными сетями.\n'
            '• Фрагментация пакетов при необходимости.\n'
            '• TTL — ограничивает время жизни пакета.'
        ),
        'devices': 'Маршрутизаторы, Layer 3 коммутаторы, файрволы',
        'tcpip': 'Интернет',
        'example': 'Роутер направляет пакет от 192.168.1.1 к 8.8.8.8 через интернет',
    },
    {
        'num': 2, 'name': 'Канальный', 'en': 'Data Link Layer',
        'color': '#6d28d9', 'pdu': 'Кадр (Frame)',
        'protocols': 'Ethernet 802.3, Wi-Fi 802.11, STP 802.1D, VLAN 802.1Q, PPP, HDLC',
        'function': (
            '• MAC-адресация (48 бит = 6 байт, уникальный адрес NIC).\n'
            '• Обнаружение ошибок через FCS/CRC в конце кадра.\n'
            '• MAC-подуровень: управление доступом к среде.\n'
            '• LLC-подуровень: логическое управление каналом.\n'
            '★ Именно здесь работают протоколы STP и VLAN!'
        ),
        'devices': 'Коммутаторы L2, мосты, Wi-Fi точки доступа',
        'tcpip': 'Канальный',
        'example': 'Коммутатор читает MAC-адрес назначения и перенаправляет кадр',
    },
    {
        'num': 1, 'name': 'Физический', 'en': 'Physical Layer',
        'color': '#0e7490', 'pdu': 'Биты (Bits)',
        'protocols': 'Ethernet (физ.), DSL, ISDN, USB, Bluetooth, Wi-Fi (физ.)',
        'function': (
            '• Передача необработанных битов по физической среде.\n'
            '• Электрические сигналы, оптика, радиоволны.\n'
            '• Разъёмы, кабели, частоты, скорости передачи.\n'
            '• Режимы: дуплекс / полудуплекс / симплекс.'
        ),
        'devices': 'Хабы, репитеры, кабели (UTP/STP/оптика), NIC',
        'tcpip': 'Канальный',
        'example': 'UTP Cat5e передаёт 100 Мбит/с на расстояние до 100 метров',
    },
]

# ─────────────────────────────────────────────────────────
#  ДАННЫЕ — ТЕСТ
# ─────────────────────────────────────────────────────────
QUIZ = [
    {
        'q': 'На каком уровне модели OSI работает протокол STP (Spanning Tree Protocol)?',
        'opts': [
            'Физический (L1) — передача битов по кабелю',
            'Канальный (L2) — работа с MAC-адресами и кадрами',
            'Сетевой (L3) — маршрутизация IP-пакетов',
            'Транспортный (L4) — сегменты TCP/UDP',
        ],
        'ans': 1,
        'expl': (
            'STP работает на 2-м уровне OSI — Канальном (Data Link).\n'
            'Он использует MAC-адреса для выбора Root Bridge и управляет\n'
            'топологией Ethernet-сети, блокируя избыточные порты.'
        ),
    },
    {
        'q': 'Что такое VLAN и для чего он используется?',
        'opts': [
            'Физическая кабельная сеть нового стандарта',
            'Виртуальная локальная сеть — логически разделяет физическую инфраструктуру',
            'Протокол шифрования данных на канальном уровне',
            'Стандарт беспроводной передачи данных IEEE 802.11',
        ],
        'ans': 1,
        'expl': (
            'VLAN (Virtual LAN) позволяет логически разделить физическую\n'
            'сеть на изолированные сегменты без прокладки новых кабелей.\n'
            'Повышает безопасность, снижает broadcast-домены.'
        ),
    },
    {
        'q': 'Какой стандарт IEEE используется для тегирования VLAN?',
        'opts': [
            'IEEE 802.1X — аутентификация в сети',
            'IEEE 802.1Q — VLAN тегирование Ethernet кадров',
            'IEEE 802.3 — стандарт проводного Ethernet',
            'IEEE 802.11 — беспроводная сеть Wi-Fi',
        ],
        'ans': 1,
        'expl': (
            'IEEE 802.1Q добавляет 4-байтный тег в Ethernet кадр:\n'
            'TPID (0x8100) + PCP (приоритет) + DEI + VLAN ID (12 бит).\n'
            'VLAN ID от 1 до 4094 (4096 значений за вычетом 0 и 4095).'
        ),
    },
    {
        'q': 'Как STP определяет, какой коммутатор будет Root Bridge?',
        'opts': [
            'Выбирается коммутатор с наибольшим количеством портов',
            'Выбирается коммутатор с наименьшим Bridge ID (Priority + MAC)',
            'Root Bridge выбирается случайно при первом запуске',
            'Root Bridge — коммутатор с наибольшим MAC-адресом',
        ],
        'ans': 1,
        'expl': (
            'Bridge ID = Priority (2 байта, по умолчанию 32768) + MAC (6 байт).\n'
            'Root Bridge = коммутатор с НАИМЕНЬШИМ Bridge ID.\n'
            'Чтобы задать Root, уменьшают Priority, например, до 4096.'
        ),
    },
    {
        'q': 'Сколько уровней в модели OSI?',
        'opts': [
            '4 уровня (как в модели TCP/IP)',
            '5 уровней',
            '6 уровней',
            '7 уровней',
        ],
        'ans': 3,
        'expl': (
            'Модель OSI (ISO 7498) содержит 7 уровней:\n'
            '1-Физический, 2-Канальный, 3-Сетевой, 4-Транспортный,\n'
            '5-Сеансовый, 6-Представления, 7-Прикладной.'
        ),
    },
    {
        'q': 'Какой транспортный протокол гарантирует доставку данных?',
        'opts': [
            'UDP — быстрый, без подтверждений',
            'ICMP — диагностика (ping)',
            'TCP — надёжный, с подтверждениями ACK',
            'IP — адресация и маршрутизация',
        ],
        'ans': 2,
        'expl': (
            'TCP: трёхстороннее рукопожатие (SYN→SYN-ACK→ACK),\n'
            'номера последовательностей, подтверждения (ACK),\n'
            'повторная передача при потере, контроль потока.'
        ),
    },
    {
        'q': 'Что происходит с портом коммутатора в состоянии STP "Blocking"?',
        'opts': [
            'Порт пересылает кадры данных и обновляет MAC-таблицу',
            'Порт не пересылает кадры, но принимает BPDU сообщения',
            'Порт полностью выключен и не принимает никаких пакетов',
            'Порт работает в режиме только broadcast трафика',
        ],
        'ans': 1,
        'expl': (
            'Blocking: порт НЕ пересылает кадры данных, НЕ учит MAC,\n'
            'но ПОЛУЧАЕТ BPDU — сообщения управления STP.\n'
            'Переходы: Blocking→Listening→Learning→Forwarding.'
        ),
    },
    {
        'q': 'Чем отличается Access порт от Trunk порта?',
        'opts': [
            'Access порты быстрее, Trunk порты медленнее',
            'Access — один VLAN без тегов, Trunk — несколько VLAN с тегами 802.1Q',
            'Access только для серверов, Trunk только для маршрутизаторов',
            'Access шифрует данные, Trunk — нет',
        ],
        'ans': 1,
        'expl': (
            'Access порт: принадлежит одному VLAN, кадры без тегов.\n'
            'Подключаются: ПК, принтеры, IP-телефоны.\n'
            'Trunk порт: несёт трафик нескольких VLAN с 802.1Q тегами.\n'
            'Используется между коммутаторами и маршрутизаторами.'
        ),
    },
    {
        'q': 'Какой уровень OSI отвечает за IP-адресацию и маршрутизацию?',
        'opts': [
            'Канальный (L2) — MAC-адреса и кадры',
            'Транспортный (L4) — порты и сегменты',
            'Сетевой (L3) — IP-адреса и маршрутизация пакетов',
            'Прикладной (L7) — пользовательские приложения',
        ],
        'ans': 2,
        'expl': (
            'Сетевой уровень L3: IP-адресация, маршрутизация.\n'
            'PDU = Пакет (Packet).\n'
            'Устройства: маршрутизаторы, L3 коммутаторы.'
        ),
    },
    {
        'q': 'Какой диапазон допустимых VLAN ID по стандарту 802.1Q?',
        'opts': [
            'VLAN ID от 1 до 255',
            'VLAN ID от 0 до 4095',
            'VLAN ID от 1 до 4094',
            'VLAN ID от 10 до 4000',
        ],
        'ans': 2,
        'expl': (
            'Поле VLAN ID = 12 бит → 4096 значений (0..4095).\n'
            'VLAN 0 зарезервирован (только приоритет).\n'
            'VLAN 4095 зарезервирован.\n'
            'Пользовательские VLAN: 1..4094. VLAN 1 = Default (нельзя удалить).'
        ),
    },
]

# ─────────────────────────────────────────────────────────
#  ЗАСТАВКА (SPLASH SCREEN)
# ─────────────────────────────────────────────────────────
class SplashScreen:
    def __init__(self, parent):
        W, H = 640, 400
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.configure(bg=BG)
        sw = self.win.winfo_screenwidth()
        sh = self.win.winfo_screenheight()
        self.win.geometry(f'{W}x{H}+{(sw-W)//2}+{(sh-H)//2}')
        self.win.lift()
        self.win.focus_force()

        c = tk.Canvas(self.win, width=W, height=H, bg=BG,
                      bd=0, highlightthickness=0)
        c.pack(fill='both', expand=True)
        self.c = c
        self.W, self.H = W, H

        # Decorative grid
        for x in range(0, W, 28):
            c.create_line(x, 0, x, H, fill='#12191f', width=1)
        for y in range(0, H, 28):
            c.create_line(0, y, W, y, fill='#12191f', width=1)

        # Outer border
        c.create_rectangle(3, 3, W-3, H-3, outline=ACCENT, width=2)
        c.create_rectangle(6, 6, W-6, H-6, outline='#1c2840', width=1)

        # Corner accents
        sz = 16
        for px, py in [(3,3), (W-3,3), (3,H-3), (W-3,H-3)]:
            c.create_rectangle(px-sz, py-sz, px+sz, py+sz,
                               outline=ACCENT, width=1, fill='#0d1f35')

        # Logo
        c.create_text(W//2, 88,
                      text='NETWORK  LEARNING  LAB',
                      fill=ACCENT, font=('Consolas', 26, 'bold'),
                      anchor='center')
        c.create_text(W//2, 128,
                      text='v 2.0',
                      fill=DIM, font=('Consolas', 11),
                      anchor='center')

        # Divider
        c.create_line(80, 150, W-80, 150, fill=BORDER, width=1)

        # Subject info
        c.create_text(W//2, 176,
                      text='Предмет:  Компьютерные системы',
                      fill=TEXT, font=('Consolas', 14),
                      anchor='center')
        c.create_text(W//2, 208,
                      text='Темы:  Модель OSI  •  VLAN 802.1Q  •  Протокол STP',
                      fill=DIM, font=('Consolas', 11),
                      anchor='center')

        # Icons row
        icons = [('📋', 'OSI\n7 уровней', ACCENT),
                 ('🔀', 'VLAN\n802.1Q', GREEN),
                 ('🌳', 'STP\nПетли', ORANGE),
                 ('📝', 'Тест\n10 вопр.', PURPLE)]
        xs = [W//5, 2*W//5, 3*W//5, 4*W//5]
        for (icon, lbl, col), x in zip(icons, xs):
            c.create_text(x, 260, text=icon, font=('Segoe UI Emoji', 20),
                          fill=col, anchor='center')
            c.create_text(x, 294, text=lbl, font=('Consolas', 9),
                          fill=DIM, anchor='center', justify='center')

        # Progress bar
        c.create_rectangle(80, 340, W-80, 356,
                           outline=BORDER, fill=SURF, width=1)
        self.bar = c.create_rectangle(80, 340, 80, 356,
                                      outline='', fill='#1f6feb')
        c.create_text(W//2, 374,
                      text='Загрузка...',
                      fill=DIM, font=('Consolas', 9), anchor='center')

        self.step = 0
        self.bar_max = W - 80 - 80   # 480 px
        self._tick()

    def _tick(self):
        self.step += 6
        if self.step <= self.bar_max:
            x2 = 80 + self.step
            self.c.coords(self.bar, 80, 340, x2, 356)
            self.win.after(12, self._tick)
        else:
            self.win.after(200, self.win.destroy)


# ─────────────────────────────────────────────────────────
#  ГЛАВНОЕ ОКНО
# ─────────────────────────────────────────────────────────
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Network Learning Lab  —  Компьютерные системы')
        self.root.geometry('1360x860')
        self.root.minsize(1060, 680)
        self.root.configure(bg=BG)

        self._style()
        self._header()
        self._notebook()

    # ── СТИЛЬ ────────────────────────────────────────────
    def _style(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Main.TNotebook', background=BG, borderwidth=0)
        s.configure('Main.TNotebook.Tab',
                    background=SURF, foreground=DIM,
                    padding=[20, 9], font=('Consolas', 10, 'bold'))
        s.map('Main.TNotebook.Tab',
              background=[('selected', SURF2), ('active', '#1c2128')],
              foreground=[('selected', ACCENT), ('active', TEXT)])
        s.configure('Treeview',
                    background=SURF, foreground=TEXT,
                    fieldbackground=SURF, rowheight=30,
                    font=('Consolas', 10))
        s.configure('Treeview.Heading',
                    background=SURF2, foreground=ACCENT,
                    font=('Consolas', 10, 'bold'))
        s.map('Treeview',
              background=[('selected', '#1f6feb')],
              foreground=[('selected', 'white')])

    # ── ШАПКА ────────────────────────────────────────────
    def _header(self):
        c = tk.Canvas(self.root, height=60, bg=SURF, bd=0,
                      highlightthickness=1, highlightbackground=BORDER)
        c.pack(fill='x', padx=10, pady=(10, 2))
        c.bind('<Configure>', lambda e: self._draw_header(c))
        self._hdr_canvas = c

    def _draw_header(self, c):
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 2: return

        # Subtle grid dots
        for x in range(0, w, 22):
            for y in range(0, h, 22):
                c.create_oval(x, y, x+2, y+2, fill='#1a2233', outline='')

        # Left accent bar
        c.create_rectangle(0, 0, 4, h, fill=ACCENT, outline='')

        # Title
        c.create_text(22, h//2, text='NETWORK LEARNING LAB',
                      fill=ACCENT, font=('Consolas', 15, 'bold'), anchor='w')
        c.create_text(278, h//2, text='|',
                      fill=BORDER, font=('Consolas', 15), anchor='w')
        c.create_text(296, h//2, text='Предмет: Компьютерные системы',
                      fill=TEXT, font=('Consolas', 11), anchor='w')

        # Right badge
        bx = w - 10
        c.create_rectangle(bx - 200, 12, bx, h - 12,
                           fill='#0d2040', outline=ACCENT, width=1)
        c.create_text(bx - 100, h//2,
                      text='OSI  •  VLAN  •  STP',
                      fill=ACCENT, font=('Consolas', 10, 'bold'), anchor='center')

        # Bottom accent line
        c.create_line(0, h-1, w, h-1, fill='#1a3a6a', width=1)

    # ── ВКЛАДКИ ──────────────────────────────────────────
    def _notebook(self):
        nb = ttk.Notebook(self.root, style='Main.TNotebook')
        nb.pack(fill='both', expand=True, padx=10, pady=(2, 10))
        self.nb = nb

        self._osi_tab()
        self._vlan_tab()
        self._stp_tab()
        self._quiz_tab()
        self._about_tab()

    # ╔═══════════════════════════════════════════════════╗
    # ║  ВКЛАДКА 1 — МОДЕЛЬ OSI                          ║
    # ╚═══════════════════════════════════════════════════╝
    def _osi_tab(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text='  📋 Модель OSI  ')

        # Intro banner
        intro = tk.Frame(frame, bg='#0c1f3a', height=34)
        intro.pack(fill='x', padx=10, pady=(8, 0))
        intro.pack_propagate(False)
        tk.Label(intro,
                 text='  Модель OSI — эталонная 7-уровневая архитектура сети (ISO 7498).  '
                      '|  Нажмите на уровень слева для просмотра протоколов и PDU.',
                 bg='#0c1f3a', fg=ACCENT, font=('Consolas', 9)).pack(side='left', pady=6)

        left  = tk.Frame(frame, bg=BG, width=290)
        left.pack(side='left', fill='y', padx=(10, 3), pady=(6, 10))
        left.pack_propagate(False)

        center = tk.Frame(frame, bg=BG)
        center.pack(side='left', fill='both', expand=True, padx=3, pady=(6, 10))

        right = tk.Frame(frame, bg=BG, width=260)
        right.pack(side='left', fill='y', padx=(3, 10), pady=(6, 10))
        right.pack_propagate(False)

        # Left column: layer buttons
        tk.Label(left, text='7 уровней модели OSI',
                 bg=BG, fg=ACCENT, font=('Consolas', 11, 'bold')).pack(pady=(0, 3))

        # Click hint — colored info badge
        hint_box = tk.Frame(left, bg='#0c2040', highlightthickness=1,
                            highlightbackground=ACCENT)
        hint_box.pack(fill='x', pady=(0, 8))
        tk.Label(hint_box,
                 text='  👆 Нажмите на уровень  \n  чтобы увидеть подробности',
                 bg='#0c2040', fg=ACCENT, font=('Consolas', 8),
                 justify='center').pack(pady=4)

        for layer in OSI_LAYERS:
            self._osi_btn(left, layer)

        # Encapsulation arrow
        arr = tk.Frame(left, bg=SURF)
        arr.pack(fill='x', pady=(10, 0))
        tk.Label(arr, text='  Отправитель  →  Инкапсуляция  →',
                 bg=SURF, fg=DIM, font=('Consolas', 8)).pack(anchor='w', pady=(5, 1))
        tk.Label(arr, text='  7→6→5→4→3→2→1',
                 bg=SURF, fg=GREEN, font=('Consolas', 9, 'bold')).pack(anchor='w')
        tk.Label(arr, text='  Получатель   →  Декапсуляция  →',
                 bg=SURF, fg=DIM, font=('Consolas', 8)).pack(anchor='w', pady=(4, 1))
        tk.Label(arr, text='  1→2→3→4→5→6→7',
                 bg=SURF, fg=ACCENT, font=('Consolas', 9, 'bold')).pack(anchor='w', pady=(0, 6))

        self._osi_center = center
        self._osi_right  = right

        # Right column: OSI vs TCP/IP comparison
        self._osi_tcpip_panel()

        # Default: show L2 (most relevant)
        self._osi_show(OSI_LAYERS[5])

    def _osi_btn(self, parent, layer):
        c = layer['color']
        wrap = tk.Frame(parent, bg=c, cursor='hand2')
        wrap.pack(fill='x', pady=2)

        num_lbl = tk.Label(wrap, text=f' L{layer["num"]} ',
                           bg=self._dk(c), fg='white',
                           font=('Consolas', 11, 'bold'), width=5)
        num_lbl.pack(side='left', ipady=9)

        info = tk.Frame(wrap, bg=c)
        info.pack(side='left', fill='both', expand=True, ipady=7, padx=5)
        tk.Label(info, text=layer['name'], bg=c, fg='white',
                 font=('Consolas', 11, 'bold'), anchor='w').pack(fill='x')
        tk.Label(info, text=layer['en'], bg=c, fg='#cccccc',
                 font=('Consolas', 8), anchor='w').pack(fill='x')

        pdu = tk.Label(wrap, text=f' {layer["pdu"].split("(")[0].strip()} ',
                       bg=self._dk(c), fg='white', font=('Consolas', 8))
        pdu.pack(side='right', padx=3, ipady=9)

        all_w = [wrap, info, num_lbl, pdu] + list(info.winfo_children())
        for w in all_w:
            w.bind('<Button-1>', lambda e, l=layer: self._osi_show(l))

    def _osi_tcpip_panel(self):
        p = self._osi_right
        tk.Label(p, text='OSI  vs  TCP/IP',
                 bg=BG, fg=GOLD, font=('Consolas', 11, 'bold')).pack(pady=(0, 6))

        data = [
            ('L7 Прикладной',   '#b91c1c', 'Прикладной',   ORANGE),
            ('L6 Представления','#c2410c', 'Прикладной',   ORANGE),
            ('L5 Сеансовый',    '#a16207', 'Прикладной',   ORANGE),
            ('L4 Транспортный', '#15803d', 'Транспортный', GREEN),
            ('L3 Сетевой',      '#1d4ed8', 'Интернет',     ACCENT),
            ('L2 Канальный',    '#6d28d9', 'Канальный',    PURPLE),
            ('L1 Физический',   '#0e7490', 'Канальный',    PURPLE),
        ]

        for osi_name, osi_col, tcp_name, tcp_col in data:
            row = tk.Frame(p, bg=BG)
            row.pack(fill='x', pady=1)

            ok = tk.Frame(row, bg=osi_col, width=136, height=28)
            ok.pack(side='left')
            ok.pack_propagate(False)
            tk.Label(ok, text=osi_name, bg=osi_col, fg='white',
                     font=('Consolas', 8, 'bold')).pack(expand=True)

            tk.Label(row, text='→', bg=BG, fg=DIM,
                     font=('Consolas', 10)).pack(side='left', padx=2)

            tk.Frame(row, bg=tcp_col, width=90, height=28).pack(side='left')
            tk.Label(row, text=tcp_name, bg=BG, fg=tcp_col,
                     font=('Consolas', 8, 'bold')).pack(side='left', padx=4)

        tk.Frame(p, bg=BORDER, height=1).pack(fill='x', pady=8)

        # Quick ref
        tk.Label(p, text='Быстрая справка:',
                 bg=BG, fg=DIM, font=('Consolas', 9, 'bold')).pack(anchor='w')
        refs = [
            ('MAC-адрес', 'L2  48 бит', PURPLE),
            ('IP-адрес',  'L3  32/128 бит', ACCENT),
            ('Порт',      'L4  0..65535', GREEN),
            ('STP',       'L2  802.1D', ORANGE),
            ('VLAN',      'L2  802.1Q', YELLOW),
        ]
        for name, info, col in refs:
            r = tk.Frame(p, bg=SURF)
            r.pack(fill='x', pady=1)
            tk.Label(r, text=f'  {name}', bg=SURF, fg=col,
                     font=('Consolas', 9, 'bold'), width=14, anchor='w').pack(side='left', pady=3)
            tk.Label(r, text=info, bg=SURF, fg=TEXT,
                     font=('Consolas', 9)).pack(side='left', pady=3)

    def _osi_show(self, layer):
        for w in self._osi_center.winfo_children():
            w.destroy()
        p = self._osi_center

        # Header bar
        hdr = tk.Canvas(p, height=64, bg=layer['color'],
                        bd=0, highlightthickness=0)
        hdr.pack(fill='x')
        hdr.bind('<Configure>', lambda e, c=hdr, l=layer: self._draw_osi_hdr(c, l))

        # Cards
        cards = [
            ('PDU — единица данных', layer['pdu'],       ACCENT,  '#0d2040'),
            ('Протоколы',            layer['protocols'],  GREEN,   '#0d2a0d'),
            ('Оборудование',         layer['devices'],    YELLOW,  '#2a1e00'),
            ('Пример из жизни',      layer['example'],    ORANGE,  '#2a1600'),
        ]
        for title, content, fg, bg in cards:
            self._card(p, title, content, fg, bg)

        # Function card with left border
        func = tk.Frame(p, bg=SURF)
        func.pack(fill='x', pady=4, padx=2)
        accent_bar = tk.Frame(func, bg=PURPLE, width=4)
        accent_bar.pack(side='left', fill='y')
        inner = tk.Frame(func, bg=SURF)
        inner.pack(side='left', fill='both', expand=True, padx=10, pady=8)
        tk.Label(inner, text='Функции уровня',
                 bg=SURF, fg=PURPLE, font=('Consolas', 10, 'bold'),
                 anchor='w').pack(fill='x')
        tk.Label(inner, text=layer['function'],
                 bg=SURF, fg=TEXT, font=('Consolas', 10),
                 anchor='w', justify='left', wraplength=560).pack(fill='x', pady=(4, 0))

        # Frame structure for L1/L2/L3/L4
        if layer['num'] <= 4:
            self._frame_diagram(p, layer['num'])

    def _draw_osi_hdr(self, c, layer):
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        c.create_rectangle(0, 0, w, h, fill=layer['color'], outline='')
        # Stripe pattern
        stripe_col = self._dk(layer['color'], 0.85)
        for i in range(0, w, 40):
            c.create_line(i, 0, i+h, h, fill=stripe_col, width=8)
        c.create_text(16, h//2,
                      text=f'Уровень {layer["num"]}  —  {layer["name"]}',
                      fill='white', font=('Consolas', 16, 'bold'), anchor='w')
        c.create_text(16, h//2 + 18,
                      text=layer['en'],
                      fill='#cccccc', font=('Consolas', 10), anchor='w')
        # TCP/IP badge
        badge_col = self._dk(layer['color'], 0.55)
        c.create_rectangle(w-160, 12, w-10, h-12,
                           fill=badge_col, outline='#888888', width=1)
        c.create_text(w-85, h//2,
                      text=f'TCP/IP: {layer["tcpip"]}',
                      fill='white', font=('Consolas', 9), anchor='center')

    def _card(self, parent, title, content, fg, bg):
        f = tk.Frame(parent, bg=SURF)
        f.pack(fill='x', pady=3, padx=2)
        bar = tk.Frame(f, bg=fg, width=4)
        bar.pack(side='left', fill='y')
        inner = tk.Frame(f, bg=SURF)
        inner.pack(side='left', fill='both', expand=True, padx=10, pady=6)
        tk.Label(inner, text=title, bg=SURF, fg=fg,
                 font=('Consolas', 9, 'bold'), anchor='w').pack(fill='x')
        tk.Label(inner, text=content, bg=SURF, fg=TEXT,
                 font=('Consolas', 10), anchor='w', wraplength=560,
                 justify='left').pack(fill='x', pady=(2, 0))

    def _frame_diagram(self, parent, num):
        f = tk.Frame(parent, bg=SURF)
        f.pack(fill='x', pady=4, padx=2)
        bar = tk.Frame(f, bg=RED, width=4)
        bar.pack(side='left', fill='y')
        inner = tk.Frame(f, bg=SURF)
        inner.pack(side='left', fill='both', expand=True, padx=10, pady=8)

        if num == 2:
            title = 'Структура Ethernet кадра (с VLAN тегом 802.1Q):'
            fields = [('Преамбула\n8 байт','#2a2a4a'),('DST MAC\n6 байт','#1a3a1a'),
                      ('SRC MAC\n6 байт','#1a3a1a'),('VLAN Tag\n4 байта','#4a1a1a'),
                      ('EtherType\n2 байта','#1a2a3a'),('Данные\n46-1500 байт','#0a1a3a'),
                      ('FCS\n4 байта','#3a2a1a')]
        elif num == 3:
            title = 'Структура IPv4 пакета (основные поля):'
            fields = [('Version\n1 байт','#2a2a4a'),('TTL\n1 байт','#3a1a1a'),
                      ('Protocol\n1 байт','#2a1a3a'),('SRC IP\n4 байта','#1a3a1a'),
                      ('DST IP\n4 байта','#1a3a1a'),('Данные\n...','#0a1a3a')]
        elif num == 4:
            title = 'Структура TCP сегмента (основные поля):'
            fields = [('SRC Port\n2 байта','#2a2a4a'),('DST Port\n2 байта','#2a2a4a'),
                      ('Seq Num\n4 байта','#1a3a1a'),('Ack Num\n4 байта','#3a1a1a'),
                      ('Flags\n2 байта','#2a1a3a'),('Данные\n...','#0a1a3a')]
        else:
            title = 'Физический уровень — биты по кабелю:'
            fields = [('0','#1a3a1a'),('1','#3a1a1a'),('0','#1a3a1a'),
                      ('0','#3a1a1a'),('1','#1a3a1a'),('1','#3a1a1a'),('...','#2a2a2a')]

        tk.Label(inner, text=title, bg=SURF, fg=RED,
                 font=('Consolas', 9, 'bold'), anchor='w').pack(fill='x')
        row = tk.Frame(inner, bg=SURF)
        row.pack(anchor='w', pady=(4, 0))
        for name, col in fields:
            cell = tk.Frame(row, bg=col, relief='ridge', bd=1)
            cell.pack(side='left', padx=2)
            tk.Label(cell, text=name, bg=col, fg='#cccccc',
                     font=('Consolas', 8), justify='center').pack(padx=5, pady=5)

    # ╔═══════════════════════════════════════════════════╗
    # ║  ВКЛАДКА 2 — VLAN МЕНЕДЖЕР                       ║
    # ╚═══════════════════════════════════════════════════╝
    def _vlan_tab(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text='  🔀 VLAN 802.1Q  ')

        self._vlans = {
            1:  {'name': 'Default',     'ports': ['Fa0/1','Fa0/2'],           'type': 'default'},
            10: {'name': 'Management',  'ports': ['Fa0/3','Fa0/4'],           'type': 'access'},
            20: {'name': 'Sales',       'ports': ['Fa0/5','Fa0/6','Fa0/7'],   'type': 'access'},
            30: {'name': 'Engineering', 'ports': ['Fa0/8','Fa0/9'],           'type': 'access'},
            99: {'name': 'Native',      'ports': ['Gi0/1'],                   'type': 'native'},
        }
        self._trunk_ports = ['Gi0/1', 'Gi0/2']

        # Banner
        banner = tk.Frame(frame, bg='#0c1f3a', height=38)
        banner.pack(fill='x', padx=10, pady=(10, 4))
        banner.pack_propagate(False)
        tk.Label(banner,
                 text='  VLAN (IEEE 802.1Q) — логически разделяет физическую сеть на изолированные сегменты.  '
                      '|  Access = один VLAN без тегов  |  Trunk = несколько VLAN с тегами 0x8100',
                 bg='#0c1f3a', fg=ACCENT, font=('Consolas', 9)).pack(side='left', pady=6)

        # Main area
        left   = tk.Frame(frame, bg=BG)
        left.pack(side='left', fill='both', expand=True, padx=(10, 4), pady=(4, 10))
        center = tk.Frame(frame, bg=BG, width=280)
        center.pack(side='left', fill='y', padx=4, pady=(4, 10))
        center.pack_propagate(False)
        right  = tk.Frame(frame, bg=BG, width=320)
        right.pack(side='left', fill='y', padx=(4, 10), pady=(4, 10))
        right.pack_propagate(False)

        self._vlan_table_area(left)
        self._vlan_diagram(center)
        self._vlan_controls(right)

    def _vlan_table_area(self, parent):
        tk.Label(parent, text='Таблица VLAN коммутатора',
                 bg=BG, fg=ACCENT, font=('Consolas', 11, 'bold')).pack(anchor='w', pady=(0, 6))

        tf = tk.Frame(parent, bg=BG)
        tf.pack(fill='both', expand=True)

        cols = ('VLAN ID', 'Название', 'Порты', 'Тип', 'Статус')
        self._vt = ttk.Treeview(tf, columns=cols, show='headings', height=13)
        for col, w in zip(cols, [80, 130, 260, 100, 90]):
            self._vt.heading(col, text=col)
            self._vt.column(col, width=w, anchor='center')
        sb = ttk.Scrollbar(tf, orient='vertical', command=self._vt.yview)
        self._vt.configure(yscrollcommand=sb.set)
        self._vt.pack(side='left', fill='both', expand=True)
        sb.pack(side='left', fill='y')

        self._vt.tag_configure('default', foreground=DIM)
        self._vt.tag_configure('access',  foreground=GREEN)
        self._vt.tag_configure('trunk',   foreground=ACCENT)
        self._vt.tag_configure('native',  foreground=YELLOW)
        self._vlan_refresh()

        tk.Frame(parent, bg=BORDER, height=1).pack(fill='x', pady=(8, 4))
        row = tk.Frame(parent, bg=SURF)
        row.pack(fill='x')
        tk.Label(row, text='  Trunk порты (802.1Q):',
                 bg=SURF, fg=ACCENT, font=('Consolas', 10, 'bold')).pack(side='left', pady=6)
        self._trunk_lbl = tk.Label(row, text=', '.join(self._trunk_ports),
                                   bg=SURF, fg=GREEN, font=('Consolas', 10))
        self._trunk_lbl.pack(side='left', pady=6, padx=6)

    def _vlan_refresh(self):
        for i in self._vt.get_children():
            self._vt.delete(i)
        for vid, d in sorted(self._vlans.items()):
            self._vt.insert('', 'end',
                values=(vid, d['name'], ', '.join(d['ports']) or '—',
                        d['type'].upper(), 'active'),
                tags=(d['type'],))

    def _vlan_diagram(self, parent):
        tk.Label(parent, text='Схема коммутатора',
                 bg=BG, fg=GOLD, font=('Consolas', 11, 'bold')).pack(pady=(0, 6))

        c = tk.Canvas(parent, bg=SURF, bd=0,
                      highlightthickness=1, highlightbackground=BORDER)
        c.pack(fill='both', expand=True)
        c.bind('<Configure>', lambda e: self._draw_vlan_diagram(c))
        self._vlan_canvas = c

    def _draw_vlan_diagram(self, c):
        c.delete('all')
        W = c.winfo_width()
        H = c.winfo_height()
        if W < 10: return

        # Switch body
        sx, sy = W//2, H//2 - 20
        sw, sh = W - 40, 60
        c.create_rectangle(sx-sw//2, sy-sh//2, sx+sw//2, sy+sh//2,
                           fill='#1c2840', outline=ACCENT, width=2)
        c.create_text(sx, sy-4, text='SW-Core  (Cisco Catalyst)',
                      fill=ACCENT, font=('Consolas', 9, 'bold'))
        c.create_text(sx, sy+10, text='24 порта  FastEthernet + 2 GigabitEthernet',
                      fill=DIM, font=('Consolas', 8))

        port_data = [
            ('Fa0/1-2',  'VLAN 1\nDefault', DIM,    0.14),
            ('Fa0/3-4',  'VLAN 10\nManagement', ACCENT, 0.32),
            ('Fa0/5-7',  'VLAN 20\nSales',      GREEN,  0.50),
            ('Fa0/8-9',  'VLAN 30\nEngineering', PURPLE, 0.68),
            ('Gi0/1-2',  'Trunk\n802.1Q', ORANGE, 0.86),
        ]

        top_y = sy - sh//2
        for port_name, vlan_label, col, xr in port_data:
            px = int(xr * W)
            # Port box
            c.create_rectangle(px-24, top_y-38, px+24, top_y-8,
                               fill=self._dk2(col), outline=col, width=1)
            c.create_text(px, top_y-23, text=port_name,
                          fill='white', font=('Consolas', 8, 'bold'))
            # Connector line
            c.create_line(px, top_y-8, px, top_y, fill=col, width=2)
            # Label below switch
            c.create_rectangle(px-32, sy+sh//2+8, px+32, sy+sh//2+54,
                               fill=self._dk2(col), outline=col, width=1)
            c.create_text(px, sy+sh//2+31, text=vlan_label,
                          fill='white', font=('Consolas', 8),
                          justify='center')
            c.create_line(px, sy+sh//2, px, sy+sh//2+8, fill=col, width=2)

        # Legend
        lx, ly = 10, H - 60
        c.create_text(lx, ly, text='Типы портов:', fill=DIM,
                      font=('Consolas', 8, 'bold'), anchor='w')
        legend = [('Access порт', GREEN), ('Trunk порт', ORANGE), ('Native VLAN', YELLOW)]
        for i, (txt, col) in enumerate(legend):
            c.create_rectangle(lx, ly+12+i*14, lx+10, ly+22+i*14, fill=col, outline='')
            c.create_text(lx+14, ly+17+i*14, text=txt, fill=col,
                          font=('Consolas', 8), anchor='w')

    def _vlan_controls(self, parent):
        tk.Label(parent, text='Управление VLAN',
                 bg=BG, fg=ACCENT, font=('Consolas', 11, 'bold')).pack(pady=(0, 4))

        # Usage guide
        guide = tk.Frame(parent, bg='#0c1f3a', highlightthickness=1,
                         highlightbackground=ACCENT)
        guide.pack(fill='x', pady=(0, 8))
        tk.Frame(guide, bg=ACCENT, width=4).pack(side='left', fill='y')
        gin = tk.Frame(guide, bg='#0c1f3a')
        gin.pack(side='left', fill='both', expand=True, padx=8, pady=6)
        tk.Label(gin, text='Как пользоваться:', bg='#0c1f3a', fg=ACCENT,
                 font=('Consolas', 9, 'bold')).pack(anchor='w')
        for step in [
            '1. Введите VLAN ID (число 2-4094)',
            '2. Укажите название и порты',
            '3. Выберите тип: ACCESS или TRUNK',
            '4. Нажмите  + Добавить VLAN',
            '   Схема обновится автоматически',
        ]:
            tk.Label(gin, text=step, bg='#0c1f3a', fg=TEXT,
                     font=('Consolas', 8), anchor='w').pack(fill='x')

        # Add
        add = tk.Frame(parent, bg=SURF)
        add.pack(fill='x', pady=3)
        tk.Frame(add, bg=GREEN, width=4).pack(side='left', fill='y')
        inner = tk.Frame(add, bg=SURF)
        inner.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        tk.Label(inner, text='Создать новый VLAN',
                 bg=SURF, fg=GREEN, font=('Consolas', 10, 'bold')).pack(anchor='w', pady=(0, 6))

        self._vi = self._fentry(inner, 'VLAN ID (2–4094):')
        self._vn = self._fentry(inner, 'Название VLAN:')
        self._vp = self._fentry(inner, 'Порты (Fa0/1, Fa0/2, ...):')

        tk.Label(inner, text='Тип порта:', bg=SURF, fg=DIM,
                 font=('Consolas', 9)).pack(anchor='w')
        self._vtype = tk.StringVar(value='access')
        tr = tk.Frame(inner, bg=SURF)
        tr.pack(anchor='w', pady=(2, 6))
        for t in ('access', 'trunk', 'native'):
            col = {'access': GREEN, 'trunk': ACCENT, 'native': YELLOW}[t]
            tk.Radiobutton(tr, text=t.upper(), variable=self._vtype, value=t,
                           bg=SURF, fg=col, selectcolor=SURF2,
                           activebackground=SURF, font=('Consolas', 9)).pack(side='left', padx=4)

        self._btn(inner, '+ Добавить VLAN', '#1f6feb', self._vlan_add)

        # Delete
        delf = tk.Frame(parent, bg=SURF)
        delf.pack(fill='x', pady=8)
        tk.Frame(delf, bg=RED, width=4).pack(side='left', fill='y')
        inner2 = tk.Frame(delf, bg=SURF)
        inner2.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        tk.Label(inner2, text='Удалить VLAN',
                 bg=SURF, fg=RED, font=('Consolas', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self._vd = self._fentry(inner2, 'VLAN ID:')
        self._btn(inner2, '× Удалить', '#da3633', self._vlan_del)

        # CLI
        tk.Label(parent, text='CLI (Cisco IOS симуляция):',
                 bg=BG, fg=DIM, font=('Consolas', 9)).pack(anchor='w', pady=(8, 2))
        self._cli = tk.Text(parent, height=10, bg='#010409', fg=GREEN,
                            font=('Consolas', 9), bd=0, insertbackground=GREEN,
                            highlightthickness=1, highlightbackground=BORDER,
                            state='disabled', wrap='word')
        self._cli.pack(fill='x')

        self._cliw('Switch# show vlan brief\n\n')
        self._cliw('VLAN  Name                 Status    Ports\n')
        self._cliw('----  -------------------- --------- ------------------\n')
        for vid, d in sorted(self._vlans.items()):
            ports = ', '.join(d['ports'][:3])
            self._cliw(f'{vid:<5} {d["name"]:<20} {"active":<9} {ports}\n')

    def _fentry(self, parent, label):
        tk.Label(parent, text=label, bg=SURF, fg=DIM,
                 font=('Consolas', 9)).pack(anchor='w')
        var = tk.StringVar()
        tk.Entry(parent, textvariable=var, bg=SURF2, fg=TEXT,
                 insertbackground=TEXT, font=('Consolas', 10), bd=0,
                 highlightthickness=1, highlightcolor=ACCENT,
                 highlightbackground=BORDER).pack(fill='x', pady=(0, 5))
        return var

    def _btn(self, parent, text, bg, cmd):
        tk.Button(parent, text=text, bg=bg, fg='white',
                  font=('Consolas', 10, 'bold'), bd=0, pady=7,
                  cursor='hand2', command=cmd).pack(fill='x', pady=(2, 0))

    def _cliw(self, text):
        self._cli.configure(state='normal')
        self._cli.insert('end', text)
        self._cli.see('end')
        self._cli.configure(state='disabled')

    def _vlan_add(self):
        try:
            vid   = int(self._vi.get())
            name  = self._vn.get().strip()
            pstr  = self._vp.get().strip()
            vtype = self._vtype.get()
            if not (2 <= vid <= 4094):
                messagebox.showerror('Ошибка', 'VLAN ID должен быть 2..4094'); return
            if not name:
                messagebox.showerror('Ошибка', 'Введите название VLAN'); return
            if vid in self._vlans:
                messagebox.showerror('Ошибка', f'VLAN {vid} уже существует'); return
            ports = [p.strip() for p in pstr.split(',') if p.strip()]
            self._vlans[vid] = {'name': name, 'ports': ports, 'type': vtype}
            self._vlan_refresh()
            self._cliw(f'\nSwitch# conf t\nSwitch(config)# vlan {vid}\n')
            self._cliw(f'Switch(config-vlan)# name {name}\nSwitch(config-vlan)# exit\n')
            for port in ports:
                self._cliw(f'Switch(config)# interface {port}\n')
                self._cliw(f'Switch(config-if)# switchport mode {vtype}\n')
                if vtype == 'access':
                    self._cliw(f'Switch(config-if)# switchport access vlan {vid}\n')
                elif vtype == 'trunk':
                    self._cliw(f'Switch(config-if)# switchport trunk allowed vlan add {vid}\n')
            self._cliw(f'%VLAN {vid} added to VLAN database.\n')
            self._vi.set(''); self._vn.set(''); self._vp.set('')
            self._draw_vlan_diagram(self._vlan_canvas)
            messagebox.showinfo('Готово', f'VLAN {vid} ({name}) создан!')
        except ValueError:
            messagebox.showerror('Ошибка', 'VLAN ID должен быть числом')

    def _vlan_del(self):
        try:
            vid = int(self._vd.get())
            if vid == 1:
                messagebox.showerror('Ошибка', 'VLAN 1 (Default) нельзя удалить!'); return
            if vid not in self._vlans:
                messagebox.showerror('Ошибка', f'VLAN {vid} не существует'); return
            name = self._vlans.pop(vid)['name']
            self._vlan_refresh()
            self._cliw(f'\nSwitch(config)# no vlan {vid}\n')
            self._cliw(f'%VLAN {vid} removed from VLAN database.\n')
            self._vd.set('')
            self._draw_vlan_diagram(self._vlan_canvas)
            messagebox.showinfo('Готово', f'VLAN {vid} ({name}) удалён')
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректный VLAN ID')

    # ╔═══════════════════════════════════════════════════╗
    # ║  ВКЛАДКА 3 — STP СИМУЛЯТОР                       ║
    # ╚═══════════════════════════════════════════════════╝
    def _stp_tab(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text='  🌳 STP Симулятор  ')

        self._stp_nodes = {
            'SW-1': {'priority': 32768, 'mac': '00:1A:2B:00:00:01', 'is_root': False, 'dist': 0},
            'SW-2': {'priority': 32768, 'mac': '00:1A:2B:00:00:02', 'is_root': False, 'dist': 0},
            'SW-3': {'priority': 32768, 'mac': '00:1A:2B:00:00:03', 'is_root': False, 'dist': 0},
            'SW-4': {'priority': 32768, 'mac': '00:1A:2B:00:00:04', 'is_root': False, 'dist': 0},
        }
        self._stp_edges = [
            ('SW-1','SW-2', 19, None),
            ('SW-1','SW-3', 19, None),
            ('SW-2','SW-3', 19, None),  # loop!
            ('SW-2','SW-4', 19, None),
            ('SW-3','SW-4', 19, None),  # loop!
        ]

        left = tk.Frame(frame, bg=BG, width=300)
        left.pack(side='left', fill='y', padx=(10, 0), pady=10)
        left.pack_propagate(False)
        right = tk.Frame(frame, bg=BG)
        right.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        self._stp_controls(left)
        self._stp_canvas_area(right)

    def _stp_controls(self, parent):
        tk.Label(parent, text='STP — Spanning Tree Protocol',
                 bg=BG, fg=ACCENT, font=('Consolas', 11, 'bold')).pack(pady=(0, 4))

        # Theory block
        theory = tk.Frame(parent, bg=SURF)
        theory.pack(fill='x', pady=4)
        tk.Frame(theory, bg=ACCENT, width=4).pack(side='left', fill='y')
        inner = tk.Frame(theory, bg=SURF)
        inner.pack(side='left', fill='both', expand=True, padx=8, pady=8)
        tk.Label(inner, text='Зачем нужен STP?', bg=SURF, fg=ACCENT,
                 font=('Consolas', 9, 'bold')).pack(anchor='w')
        tk.Label(inner,
                 text=(
                     'Без STP петли в сети вызывают\n'
                     '"broadcast storm" — бесконечную\n'
                     'пересылку одних и тех же кадров.\n'
                     'STP блокирует лишние порты,\n'
                     'создавая дерево без петель.'
                 ),
                 bg=SURF, fg=TEXT, font=('Consolas', 9), justify='left').pack(anchor='w')

        # Step-by-step guide
        guide = tk.Frame(parent, bg='#0c2a0c', highlightthickness=1,
                         highlightbackground=GREEN)
        guide.pack(fill='x', pady=(6, 4))
        tk.Frame(guide, bg=GREEN, width=4).pack(side='left', fill='y')
        gin = tk.Frame(guide, bg='#0c2a0c')
        gin.pack(side='left', fill='both', expand=True, padx=8, pady=6)
        tk.Label(gin, text='Как пользоваться:', bg='#0c2a0c', fg=GREEN,
                 font=('Consolas', 9, 'bold')).pack(anchor='w')
        for step in [
            '1. Смените Priority у одного SW',
            '   (например SW-1 → 4096)',
            '2. Нажмите  ▶ Run STP',
            '3. Root Bridge — коммутатор с',
            '   наименьшим Priority',
            '4. Зелёные линии — Forwarding',
            '   Красные пунктир — Blocked',
        ]:
            tk.Label(gin, text=step, bg='#0c2a0c', fg=TEXT,
                     font=('Consolas', 8), anchor='w').pack(fill='x')

        # Priority settings
        tk.Label(parent, text='Bridge Priority (меньше = Root):',
                 bg=BG, fg=GREEN, font=('Consolas', 9, 'bold')).pack(anchor='w', pady=(10, 3))

        self._prio_vars = {}
        opts = ['4096','8192','16384','24576','32768','40960','49152']
        for sw in ('SW-1','SW-2','SW-3','SW-4'):
            row = tk.Frame(parent, bg=SURF)
            row.pack(fill='x', pady=2)
            tk.Label(row, text=f'  {sw}:', bg=SURF, fg=TEXT,
                     font=('Consolas', 10), width=8).pack(side='left', pady=5)
            var = tk.StringVar(value='32768')
            self._prio_vars[sw] = var
            ttk.Combobox(row, textvariable=var, values=opts,
                         width=8, state='readonly',
                         font=('Consolas', 9)).pack(side='left', padx=6, pady=5)

        tk.Frame(parent, bg=BG, height=6).pack()

        # Buttons
        self._btn_plain(parent, '▶  Run STP  —  Запустить алгоритм', '#1f6feb', self._stp_run)
        self._btn_plain(parent, '↺  Reset  —  Сбросить топологию', SURF2, self._stp_reset)

        # Legend
        tk.Frame(parent, bg=BORDER, height=1).pack(fill='x', pady=(10, 4))
        tk.Label(parent, text='Легенда:', bg=BG, fg=DIM,
                 font=('Consolas', 9, 'bold')).pack(anchor='w')
        for txt, col in [
            ('★  ROOT BRIDGE — корневой коммутатор', GOLD),
            ('━━  Forwarding — передаёт данные',     GREEN),
            ('╌╌  Blocked — заблокирован STP',        RED),
        ]:
            tk.Label(parent, text=f'  {txt}', bg=BG, fg=col,
                     font=('Consolas', 8)).pack(anchor='w')

        # Port states table
        tk.Frame(parent, bg=BORDER, height=1).pack(fill='x', pady=(8, 4))
        tk.Label(parent, text='Состояния портов STP:', bg=BG, fg=YELLOW,
                 font=('Consolas', 9, 'bold')).pack(anchor='w')
        states = [
            ('Blocking',   'Принимает BPDU. Нет пересылки.',   RED),
            ('Listening',  'Слушает BPDU. Нет MAC-обучения.',   YELLOW),
            ('Learning',   'Изучает MAC-адреса.',                ORANGE),
            ('Forwarding', 'Полная работа.',                     GREEN),
            ('Disabled',   'Порт выключен.',                     DIM),
        ]
        for state, desc, col in states:
            r = tk.Frame(parent, bg=SURF)
            r.pack(fill='x', pady=1)
            tk.Label(r, text=f'  {state:<12}', bg=SURF, fg=col,
                     font=('Consolas', 8, 'bold'), width=14, anchor='w').pack(side='left', pady=3)
            tk.Label(r, text=desc, bg=SURF, fg=TEXT,
                     font=('Consolas', 8)).pack(side='left', pady=3)

    def _btn_plain(self, parent, text, bg, cmd):
        tk.Button(parent, text=text, bg=bg, fg='white',
                  font=('Consolas', 10, 'bold'), bd=0, pady=8,
                  cursor='hand2', command=cmd).pack(fill='x', pady=2)

    def _stp_canvas_area(self, parent):
        # Warning banner
        warn = tk.Frame(parent, bg='#2a1500', height=32)
        warn.pack(fill='x', pady=(0, 4))
        warn.pack_propagate(False)
        tk.Label(warn,
                 text='  ⚠  Топология содержит петли (loops)!  '
                      'Без STP это вызвало бы "broadcast storm".  '
                      'Нажмите ▶ Run STP для устранения.',
                 bg='#2a1500', fg=ORANGE, font=('Consolas', 9)).pack(side='left', pady=6)

        cf = tk.Frame(parent, bg=SURF, highlightthickness=1,
                      highlightbackground=BORDER)
        cf.pack(fill='both', expand=True)
        self._sc = tk.Canvas(cf, bg='#010409', bd=0, highlightthickness=0)
        self._sc.pack(fill='both', expand=True)
        self._sc.bind('<Configure>', lambda e: self._stp_draw())

        tk.Label(parent, text='Лог алгоритма STP:',
                 bg=BG, fg=DIM, font=('Consolas', 9)).pack(anchor='w', pady=(6, 2))
        self._slog = tk.Text(parent, height=6, bg='#010409', fg=GREEN,
                             font=('Consolas', 9), bd=0,
                             highlightthickness=1, highlightbackground=BORDER,
                             state='disabled', wrap='word')
        self._slog.pack(fill='x')
        self._slogw('Нажмите "Run STP" для запуска алгоритма Spanning Tree.\n')
        self._slogw('Попробуйте изменить Priority у SW-1 на 4096 — он станет Root Bridge.\n')
        self._stp_draw()

    def _slogw(self, text):
        self._slog.configure(state='normal')
        self._slog.insert('end', text)
        self._slog.see('end')
        self._slog.configure(state='disabled')

    def _stp_positions(self):
        W = max(self._sc.winfo_width(),  100)
        H = max(self._sc.winfo_height(), 100)
        return {
            'SW-1': (W*0.50, H*0.14),
            'SW-2': (W*0.18, H*0.52),
            'SW-3': (W*0.82, H*0.52),
            'SW-4': (W*0.50, H*0.86),
        }

    def _stp_draw(self):
        c = self._sc
        c.delete('all')
        pos = self._stp_positions()
        W = c.winfo_width()
        H = c.winfo_height()

        # Background grid
        for x in range(0, W, 30):
            c.create_line(x, 0, x, H, fill='#0c1018', width=1)
        for y in range(0, H, 30):
            c.create_line(0, y, W, y, fill='#0c1018', width=1)

        # Edges
        for (a, b, cost, state) in self._stp_edges:
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            if state == 'forwarding':
                col, dash, width = GREEN, (), 3
            elif state == 'blocked':
                col, dash, width = RED, (6, 4), 2
            else:
                col, dash, width = '#2a3a4a', (), 2
            c.create_line(x1, y1, x2, y2, fill=col, width=width, dash=dash)
            mx, my = (x1+x2)/2, (y1+y2)/2
            c.create_text(mx+1, my-12+1, text=f'cost {cost}', fill='#000000',
                          font=('Consolas', 8))
            c.create_text(mx, my-12, text=f'cost {cost}', fill=DIM,
                          font=('Consolas', 8))
            if state:
                lc = GREEN if state == 'forwarding' else RED
                c.create_text(mx, my+12, text=state.upper(), fill=lc,
                              font=('Consolas', 8, 'bold'))

        # Nodes
        SW, SH = 52, 28
        for name, data in self._stp_nodes.items():
            x, y = pos[name]
            is_root = data.get('is_root', False)

            # Shadow
            c.create_rectangle(x-SW+3, y-SH+3, x+SW+3, y+SH+3,
                               fill='#000000', outline='')
            # Body
            fill = '#2a2000' if is_root else SURF2
            border = GOLD if is_root else ACCENT
            bw = 3 if is_root else 1
            c.create_rectangle(x-SW, y-SH, x+SW, y+SH,
                               fill=fill, outline=border, width=bw)

            # Port indicators (decorative)
            for i, px in enumerate([x-SW+8, x-SW+16, x+SW-16, x+SW-8]):
                col = GREEN if data.get('is_root') else DIM
                c.create_rectangle(px-4, y+SH-8, px+4, y+SH,
                                   fill=col, outline='')

            # Text
            c.create_text(x, y-8, text=name, fill='white',
                          font=('Consolas', 12, 'bold'))
            prio = self._prio_vars[name].get()
            c.create_text(x, y+8, text=f'Priority: {prio}',
                          fill=GOLD if is_root else DIM,
                          font=('Consolas', 8))

            # Root crown
            if is_root:
                c.create_text(x, y-SH-18, text='★  ROOT BRIDGE  ★',
                              fill=GOLD, font=('Consolas', 10, 'bold'))

    def _stp_run(self):
        for sw, var in self._prio_vars.items():
            self._stp_nodes[sw]['priority'] = int(var.get())
        for n in self._stp_nodes.values():
            n['is_root'] = False

        log = self._slogw
        log('\n' + '═'*52 + '\n')
        log('[STP] Запуск алгоритма Spanning Tree Protocol\n')

        # 1. Elect Root Bridge
        def bid(name):
            n = self._stp_nodes[name]
            return (n['priority'], n['mac'])
        root = min(self._stp_nodes.keys(), key=bid)
        self._stp_nodes[root]['is_root'] = True

        log('\n[1] Bridge ID всех коммутаторов:\n')
        for n in sorted(self._stp_nodes):
            nd = self._stp_nodes[n]
            m = '  ← ROOT (min BID)' if n == root else ''
            log(f'    {n}: Priority={nd["priority"]}  MAC={nd["mac"]}{m}\n')
        log(f'\n    Root Bridge: {root}\n')

        # 2. Dijkstra from root
        adj = {n: {} for n in self._stp_nodes}
        for a, b, cost, _ in self._stp_edges:
            adj[a][b] = cost
            adj[b][a] = cost
        dist = {n: float('inf') for n in self._stp_nodes}
        prev = {n: None for n in self._stp_nodes}
        dist[root] = 0
        pq = [(0, root)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]: continue
            for v, w in adj[u].items():
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))

        for n, d in dist.items():
            self._stp_nodes[n]['dist'] = d

        log('\n[2] Root Cost (расстояние до Root Bridge):\n')
        for n in sorted(dist):
            if n != root:
                log(f'    {n}: cost={dist[n]}  (Root Port → {prev[n]})\n')

        # 3. Determine port states
        root_ports = {sw: prev[sw] for sw in self._stp_nodes if sw != root and prev[sw]}
        new_edges = []
        blocked = []

        for (a, b, cost, _) in self._stp_edges:
            is_rp = ((a != root and root_ports.get(a) == b) or
                     (b != root and root_ports.get(b) == a))
            if is_rp:
                new_edges.append((a, b, cost, 'forwarding'))
                continue
            a_ok = (a == root) or (a in root_ports)
            b_ok = (b == root) or (b in root_ports)
            if a_ok and b_ok:
                # Tiebreak: block port of switch farther from root
                if dist[a] > dist[b]:
                    new_edges.append((a, b, cost, 'blocked'))
                    blocked.append(f'{a}—{b}')
                elif dist[b] > dist[a]:
                    new_edges.append((a, b, cost, 'blocked'))
                    blocked.append(f'{a}—{b}')
                else:
                    if self._stp_nodes[a]['mac'] > self._stp_nodes[b]['mac']:
                        new_edges.append((a, b, cost, 'blocked'))
                        blocked.append(f'{a}—{b}')
                    else:
                        new_edges.append((a, b, cost, 'forwarding'))
            else:
                new_edges.append((a, b, cost, 'forwarding'))

        self._stp_edges = new_edges
        fwd = sum(1 for e in self._stp_edges if e[3] == 'forwarding')
        blk = sum(1 for e in self._stp_edges if e[3] == 'blocked')

        log('\n[3] Результат:\n')
        for b in blocked:
            log(f'    BLOCKED: {b}  (петля устранена)\n')
        log(f'\n    Forwarding: {fwd} линков   Blocked: {blk} линков\n')
        log('    STP завершил работу. Петли устранены!\n')
        log('═'*52 + '\n')

        self._stp_draw()

    def _stp_reset(self):
        self._stp_edges = [
            ('SW-1','SW-2', 19, None), ('SW-1','SW-3', 19, None),
            ('SW-2','SW-3', 19, None), ('SW-2','SW-4', 19, None),
            ('SW-3','SW-4', 19, None),
        ]
        for n in self._stp_nodes.values():
            n['is_root'] = False
        for v in self._prio_vars.values():
            v.set('32768')
        self._slog.configure(state='normal')
        self._slog.delete('1.0', 'end')
        self._slog.configure(state='disabled')
        self._slogw('Сброс выполнен. Нажмите "Run STP".\n')
        self._stp_draw()

    # ╔═══════════════════════════════════════════════════╗
    # ║  ВКЛАДКА 4 — ТЕСТ ЗНАНИЙ                         ║
    # ╚═══════════════════════════════════════════════════╝
    def _quiz_tab(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text='  📝 Тест знаний  ')

        self._ql      = QUIZ[:]
        self._qi      = 0
        self._qs      = 0
        self._qstreak = 0
        self._qmax    = 0
        self._qanswered = False
        random.shuffle(self._ql)

        # Header
        hdr = tk.Frame(frame, bg=SURF)
        hdr.pack(fill='x', padx=10, pady=10)
        title_f = tk.Frame(hdr, bg=SURF)
        title_f.pack(side='left', padx=14, pady=10)
        tk.Label(title_f, text='Тест знаний: OSI / VLAN / STP',
                 bg=SURF, fg=ACCENT, font=('Consolas', 13, 'bold'),
                 anchor='w').pack(anchor='w')
        tk.Label(title_f,
                 text='10 вопросов — выберите правильный ответ и читайте пояснение',
                 bg=SURF, fg=DIM, font=('Consolas', 9),
                 anchor='w').pack(anchor='w')
        self._slbl = tk.Label(hdr, text='0 / 0', bg=SURF, fg=GREEN,
                              font=('Consolas', 13, 'bold'))
        self._slbl.pack(side='right', padx=20)
        self._streak_lbl = tk.Label(hdr, text='Серия: 0 🔥', bg=SURF, fg=ORANGE,
                                    font=('Consolas', 10))
        self._streak_lbl.pack(side='right', padx=10)
        tk.Label(hdr, text='Очки / Всего', bg=SURF, fg=DIM,
                 font=('Consolas', 8)).pack(side='right')

        # Progress bar
        self._pbg = tk.Canvas(frame, height=8, bg=SURF2,
                              bd=0, highlightthickness=0)
        self._pbg.pack(fill='x', padx=10)
        self._pbar = self._pbg.create_rectangle(0, 0, 0, 8, fill='#1f6feb', outline='')

        # Question area
        qw = tk.Frame(frame, bg=SURF)
        qw.pack(fill='x', padx=10, pady=6)
        qnum_row = tk.Frame(qw, bg=SURF)
        qnum_row.pack(fill='x', padx=14, pady=(8, 0))
        self._qnum  = tk.Label(qnum_row, text='', bg=SURF, fg=DIM, font=('Consolas', 9))
        self._qnum.pack(side='left')
        tk.Label(qnum_row, text='  •  Нажмите на вариант ответа ниже',
                 bg=SURF, fg='#3a4a5a', font=('Consolas', 9)).pack(side='left')
        self._qtxt  = tk.Label(qw, text='', bg=SURF, fg=TEXT, font=('Consolas', 12),
                               wraplength=980, justify='left')
        self._qtxt.pack(anchor='w', padx=14, pady=(4, 12))

        # Options
        self._obts = []
        ow = tk.Frame(frame, bg=BG)
        ow.pack(fill='x', padx=10, pady=2)
        for i in range(4):
            btn = tk.Button(ow, text='', bg=SURF, fg=TEXT,
                            font=('Consolas', 11), bd=0, pady=13, padx=22,
                            anchor='w', cursor='hand2',
                            highlightthickness=2, highlightbackground=BORDER,
                            command=lambda idx=i: self._qanswer(idx))
            btn.pack(fill='x', pady=3)
            self._obts.append(btn)

        # Explanation
        self._exf = tk.Frame(frame, bg='#0d2a0d')
        self._exl = tk.Label(self._exf, text='', bg='#0d2a0d', fg=GREEN,
                             font=('Consolas', 10), wraplength=980, justify='left')
        self._exl.pack(padx=14, pady=10, anchor='w')

        # Nav
        nav = tk.Frame(frame, bg=BG)
        nav.pack(fill='x', padx=10, pady=6)
        self._restbtn = tk.Button(nav, text='  Начать заново  ',
                                  bg=SURF2, fg=TEXT, font=('Consolas', 10),
                                  bd=0, pady=9, cursor='hand2',
                                  command=self._qrestart)
        self._restbtn.pack(side='right', padx=8)
        self._nxtbtn  = tk.Button(nav, text='  Следующий  →  ',
                                  bg='#1f6feb', fg='white',
                                  font=('Consolas', 11, 'bold'), bd=0, pady=9,
                                  cursor='hand2', state='disabled',
                                  command=self._qnext)
        self._nxtbtn.pack(side='right')

        # Result (hidden)
        self._resf = tk.Frame(frame, bg=BG)
        self._resl = tk.Label(self._resf, text='', bg=BG, fg=GOLD,
                              font=('Consolas', 16, 'bold'))
        self._resl.pack(pady=20)

        self._qshow()

    def _qshow(self):
        if self._qi >= len(self._ql):
            self._qfinal(); return
        q = self._ql[self._qi]
        total = len(self._ql)
        self._qnum.configure(text=f'Вопрос {self._qi+1} из {total}')
        self._qtxt.configure(text=q['q'])

        self._pbg.update_idletasks()
        pw = self._pbg.winfo_width()
        self._pbg.coords(self._pbar, 0, 0, int(pw * self._qi / total), 8)

        for i, btn in enumerate(self._obts):
            btn.configure(text=f'  {"ABCD"[i]})  {q["opts"][i]}',
                          bg=SURF, fg=TEXT, state='normal',
                          highlightbackground=BORDER)
        self._exf.pack_forget()
        self._resf.pack_forget()
        self._qanswered = False
        self._nxtbtn.configure(state='disabled', text='  Следующий  →  ')

    def _qanswer(self, idx):
        if self._qanswered: return
        self._qanswered = True
        q       = self._ql[self._qi]
        correct = q['ans']
        for btn in self._obts:
            btn.configure(state='disabled')
        for i, btn in enumerate(self._obts):
            if i == correct:
                btn.configure(bg='#0d3a0d', fg=GREEN,
                              highlightbackground=GREEN)
            elif i == idx:
                btn.configure(bg='#3a0d0d', fg=RED,
                              highlightbackground=RED)
            else:
                btn.configure(fg='#3a4050')

        if idx == correct:
            self._qs      += 1
            self._qstreak += 1
            self._qmax     = max(self._qmax, self._qstreak)
            expl_bg, expl_fg = '#0d2a0d', GREEN
            prefix = '✔  ПРАВИЛЬНО!'
        else:
            self._qstreak = 0
            expl_bg, expl_fg = '#2a0d0d', RED
            prefix = f'✘  НЕВЕРНО.  Правильный ответ:  {q["opts"][correct]}'

        done = self._qi + 1
        pct  = self._qs / done * 100
        self._slbl.configure(text=f'{self._qs} / {done}',
                             fg=GREEN if pct >= 60 else RED)
        self._streak_lbl.configure(text=f'Серия: {self._qstreak} 🔥')

        self._exf.configure(bg=expl_bg)
        self._exl.configure(bg=expl_bg, fg=expl_fg,
                            text=f'{prefix}\n\n{q["expl"]}')
        self._exf.pack(fill='x', padx=10, pady=4)

        if self._qi + 1 >= len(self._ql):
            self._nxtbtn.configure(state='normal', text='  Результат  →  ')
        else:
            self._nxtbtn.configure(state='normal')

    def _qnext(self):
        self._qi += 1
        self._qshow()

    def _qfinal(self):
        self._exf.pack_forget()
        for btn in self._obts: btn.pack_forget()
        self._qtxt.configure(text='')
        self._qnum.configure(text='Тест завершён!')

        total = len(self._ql)
        pct   = self._qs / total * 100

        self._pbg.update_idletasks()
        pw = self._pbg.winfo_width()
        self._pbg.coords(self._pbar, 0, 0, pw, 8)
        self._pbg.itemconfigure(self._pbar,
                                fill=GREEN if pct >= 55 else RED)

        if pct >= 90:
            grade, col = 'Отлично! Превосходные знания!', GOLD
        elif pct >= 75:
            grade, col = 'Хорошо! Уверенные знания.', GREEN
        elif pct >= 55:
            grade, col = 'Удовлетворительно. Есть пробелы.', YELLOW
        else:
            grade, col = 'Нужно повторить материал.', RED

        self._resl.configure(fg=col,
            text=(f'{grade}\n\n'
                  f'Результат: {self._qs} из {total}  ({pct:.0f}%)\n'
                  f'Лучшая серия правильных ответов: {self._qmax}'))
        self._resf.pack(fill='x', padx=10, pady=10)
        self._slbl.configure(text=f'{self._qs}/{total}')
        self._nxtbtn.configure(state='disabled', text='  Тест завершён  ')

    def _qrestart(self):
        self._qi = 0; self._qs = 0; self._qstreak = 0; self._qmax = 0
        self._qanswered = False
        random.shuffle(self._ql)
        for btn in self._obts: btn.pack(fill='x', pady=3)
        self._resf.pack_forget()
        self._pbg.itemconfigure(self._pbar, fill='#1f6feb')
        self._slbl.configure(text='0 / 0', fg=GREEN)
        self._streak_lbl.configure(text='Серия: 0 🔥')
        self._nxtbtn.configure(text='  Следующий  →  ')
        self._qshow()

    # ╔═══════════════════════════════════════════════════╗
    # ║  ВКЛАДКА 5 — О ПРОГРАММЕ                         ║
    # ╚═══════════════════════════════════════════════════╝
    def _about_tab(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text='  ℹ О программе  ')

        canvas = tk.Canvas(frame, bg=BG, bd=0, highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        inner = tk.Frame(canvas, bg=BG)
        canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind('<Configure>',
                   lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        self._about_content(inner)

    def _about_content(self, p):
        # Title block
        title_frame = tk.Canvas(p, height=100, bg='#0d2040', bd=0,
                                highlightthickness=0)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.bind('<Configure>',
                         lambda e, c=title_frame: self._about_hdr(c))

        sections = [
            # (heading, color, lines)
            ('О программе', ACCENT, [
                'Network Learning Lab — интерактивный образовательный симулятор',
                'компьютерных сетей, созданный для изучения ключевых тем курса',
                '"Компьютерные системы".',
                '',
                'Программа позволяет наглядно изучить протоколы и стандарты,',
                'которые лежат в основе работы любой современной сети.',
                'Все разделы интерактивны — можно кликать, запускать алгоритмы',
                'и проверять знания в режиме теста.',
            ]),
            ('Разработчики', GOLD, [
                'Медведев Б.А.',
                'Шик А.В.',
                '',
                'Предмет:  Компьютерные системы',
            ]),
            ('Как пользоваться программой', TEAL, [
                'Программа содержит 4 рабочих раздела (вкладки вверху экрана):',
                '',
                '  📋  Вкладка «Модель OSI»',
                '      Нажмите на любой из 7 уровней слева — справа появятся',
                '      подробности: протоколы, PDU (единица данных), устройства,',
                '      пример из жизни, структура кадра/пакета.',
                '      Справа — сравнение OSI с моделью TCP/IP.',
                '',
                '  🔀  Вкладка «VLAN 802.1Q»',
                '      Таблица слева — все VLAN на коммутаторе.',
                '      Схема в центре — визуальные порты коммутатора.',
                '      Справа — форма для создания нового VLAN:',
                '        введите ID (например 40), название (например "HR"),',
                '        порты (Fa0/10, Fa0/11) и нажмите «+ Добавить VLAN».',
                '      Внизу справа — Cisco IOS CLI лог всех команд.',
                '',
                '  🌳  Вкладка «STP Симулятор»',
                '      Слева — 4 коммутатора с настройкой Bridge Priority.',
                '      Топология содержит петли (loops) — это специально!',
                '      Шаг 1: смените Priority у SW-1 с 32768 на 4096.',
                '      Шаг 2: нажмите «▶ Run STP».',
                '      Шаг 3: алгоритм выберет Root Bridge и заблокирует',
                '             лишние порты (красные пунктирные линии).',
                '      Лог снизу объясняет каждый шаг алгоритма.',
                '',
                '  📝  Вкладка «Тест знаний»',
                '      10 вопросов по темам OSI, VLAN и STP.',
                '      Нажмите на один из 4 вариантов ответа.',
                '      После ответа — пояснение почему ответ верный/неверный.',
                '      Нажмите «Следующий →» для перехода к следующему вопросу.',
                '      В конце — итоговый результат и оценка знаний.',
            ]),
            ('Изученные темы', GREEN, [
                '1. Модель OSI (Open Systems Interconnection, ISO 7498)',
                '   7 уровней: Физический → Канальный → Сетевой → Транспортный',
                '              → Сеансовый → Представления → Прикладной',
                '   Принципы инкапсуляции и декапсуляции данных.',
                '',
                '2. VLAN — Virtual Local Area Network (IEEE 802.1Q)',
                '   Логическое разделение физической сети на сегменты.',
                '   Тегирование кадров: TPID + PCP + DEI + VLAN ID (12 бит).',
                '   Access порты (1 VLAN) и Trunk порты (несколько VLAN).',
                '',
                '3. STP — Spanning Tree Protocol (IEEE 802.1D)',
                '   Предотвращение петель в коммутируемых Ethernet-сетях.',
                '   Алгоритм: выбор Root Bridge → Root Ports → Designated Ports',
                '             → блокировка лишних портов.',
                '   Состояния портов: Blocking → Listening → Learning → Forwarding.',
            ]),
            ('Технические сведения', YELLOW, [
                'Язык:          Python 3.6+',
                'GUI:           tkinter (встроен в Python, не требует установки)',
                'Алгоритм STP:  Dijkstra (поиск кратчайшего пути до Root Bridge)',
                'Зависимости:   отсутствуют — только стандартная библиотека',
                'Платформы:     Windows 10/11,  macOS,  Linux',
                'Запуск:        python network_learning_lab.py',
                '',
                'Запуск EXE (без Python):',
                '   Открыть файл  NetworkLearningLab.exe  — Python внутри.',
            ]),
            ('Ключевые стандарты', ORANGE, [
                'ISO/IEC 7498-1   —  Модель взаимодействия открытых систем (OSI)',
                'IEEE 802.3       —  Стандарт Ethernet (проводная сеть)',
                'IEEE 802.11      —  Стандарт Wi-Fi (беспроводная сеть)',
                'IEEE 802.1Q      —  Тегирование VLAN',
                'IEEE 802.1D      —  Spanning Tree Protocol (STP)',
                'IEEE 802.1W      —  Rapid STP (RSTP — ускоренная версия)',
                'RFC 793          —  TCP (Transmission Control Protocol)',
                'RFC 791          —  IP версии 4 (IPv4)',
                'RFC 2460         —  IP версии 6 (IPv6)',
            ]),
        ]

        for heading, col, lines in sections:
            block = tk.Frame(p, bg=SURF)
            block.pack(fill='x', padx=10, pady=6)
            tk.Frame(block, bg=col, width=4).pack(side='left', fill='y')
            inner = tk.Frame(block, bg=SURF)
            inner.pack(side='left', fill='both', expand=True, padx=12, pady=10)
            tk.Label(inner, text=heading, bg=SURF, fg=col,
                     font=('Consolas', 12, 'bold'), anchor='w').pack(fill='x', pady=(0, 6))
            for line in lines:
                tk.Label(inner, text=line, bg=SURF, fg=TEXT if line.strip() else DIM,
                         font=('Consolas', 10), anchor='w',
                         justify='left').pack(fill='x')

        # Footer
        ft = tk.Frame(p, bg='#0c1f3a')
        ft.pack(fill='x', padx=10, pady=(6, 20))
        tk.Label(ft,
                 text='  Разработчики: Медведев Б.А., Шик А.В.  |  '
                      'Предмет: Компьютерные системы  ',
                 bg='#0c1f3a', fg=GOLD, font=('Consolas', 10, 'bold')).pack(pady=6)
        tk.Label(ft,
                 text='  Программа создана в рамках курса "Компьютерные системы"  ',
                 bg='#0c1f3a', fg=DIM, font=('Consolas', 9)).pack(pady=(0, 8))

    def _about_hdr(self, c):
        c.delete('all')
        w = c.winfo_width()
        h = c.winfo_height()
        for x in range(0, w, 22):
            for y in range(0, h, 22):
                c.create_oval(x, y, x+2, y+2, fill='#1a3050', outline='')
        c.create_rectangle(0, 0, 4, h, fill=ACCENT, outline='')
        c.create_text(22, h//2-14, text='NETWORK LEARNING LAB',
                      fill=ACCENT, font=('Consolas', 18, 'bold'), anchor='w')
        c.create_text(22, h//2+12, text='Компьютерные системы  |  OSI • VLAN 802.1Q • STP 802.1D',
                      fill=TEXT, font=('Consolas', 11), anchor='w')

    # ── ВСПОМОГАТЕЛЬНЫЕ ──────────────────────────────────
    def _dk(self, hex_color, f=0.72):
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return '#{:02x}{:02x}{:02x}'.format(int(r*f), int(g*f), int(b*f))

    def _dk2(self, hex_color, f=0.25):
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return '#{:02x}{:02x}{:02x}'.format(int(r*f), int(g*f), int(b*f))


# ─────────────────────────────────────────────────────────
#  ТОЧКА ВХОДА
# ─────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.withdraw()          # hide until splash is done

    splash = SplashScreen(root)
    root.wait_window(splash.win)

    root.deiconify()
    app = App(root)

    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = root.winfo_width()
    wh = root.winfo_height()
    root.geometry(f'+{(sw-ww)//2}+{(sh-wh)//2}')

    root.mainloop()


if __name__ == '__main__':
    main()
