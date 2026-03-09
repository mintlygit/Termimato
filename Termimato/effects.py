"""
Модуль с эффектами анимации.
"""

import sys
import asyncio
import random
import math
from typing import List, Optional, Tuple, Union, Callable
from dataclasses import dataclass
from enum import Enum

from .exceptions import ColorNotSupportedError

class Colors:
    """ANSI escape-последовательности для стилизации текста."""
    
    # Основные цвета
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Яркие цвета
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Фоны
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Стили
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    
    # Сброс
    RESET = '\033[0m'
    RESET_COLOR = '\033[39m'
    RESET_BG = '\033[49m'
    
    @classmethod
    def rgb(cls, r: int, g: int, b: int) -> str:
        """Получить цвет в формате True Color (24-bit)."""
        return f'\033[38;2;{r};{g};{b}m'
    
    @classmethod
    def bg_rgb(cls, r: int, g: int, b: int) -> str:
        """Получить цвет фона в формате True Color (24-bit)."""
        return f'\033[48;2;{r};{g};{b}m'
    
    @classmethod
    def gradient(
        cls, 
        text: str, 
        start_color: Tuple[int, int, int], 
        end_color: Tuple[int, int, int]
    ) -> str:
        """Применить градиент к тексту."""
        if not text:
            return ""
        
        result = []
        r1, g1, b1 = start_color
        r2, g2, b2 = end_color
        
        for i, char in enumerate(text):
            ratio = i / max(len(text) - 1, 1)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            result.append(f"{cls.rgb(r, g, b)}{char}")
        
        return "".join(result) + cls.RESET

@dataclass
class ColorTheme:
    """Тема цветов для анимаций."""
    primary: str = Colors.CYAN
    secondary: str = Colors.GREEN
    accent: str = Colors.YELLOW
    error: str = Colors.RED
    success: str = Colors.GREEN
    warning: str = Colors.YELLOW
    info: str = Colors.BLUE
    
    @classmethod
    def dark(cls):
        """Темная тема."""
        return cls(
            primary=Colors.BRIGHT_CYAN,
            secondary=Colors.BRIGHT_GREEN,
            accent=Colors.BRIGHT_YELLOW,
            error=Colors.BRIGHT_RED,
            success=Colors.BRIGHT_GREEN,
            warning=Colors.BRIGHT_YELLOW,
            info=Colors.BRIGHT_BLUE
        )
    
    @classmethod
    def light(cls):
        """Светлая тема."""
        return cls(
            primary=Colors.BLUE,
            secondary=Colors.GREEN,
            accent=Colors.MAGENTA,
            error=Colors.RED,
            success=Colors.GREEN,
            warning=Colors.YELLOW,
            info=Colors.CYAN
        )
    
    @classmethod
    def rainbow(cls):
        """Радужная тема."""
        return cls(
            primary=Colors.RED,
            secondary=Colors.YELLOW,
            accent=Colors.GREEN,
            error=Colors.MAGENTA,
            success=Colors.CYAN,
            warning=Colors.YELLOW,
            info=Colors.BLUE
        )

async def type_writer(
    text: str, 
    speed: float = 0.05, 
    color: Union[str, ColorTheme] = Colors.RESET,
    jitter: float = 0.5,
    sound_effect: bool = False,
    on_char: Optional[Callable[[str], None]] = None
) -> None:
    """
    Эффект печатающей машинки.
    
    Args:
        text: Текст для печати
        speed: Базовая скорость печати (секунды на символ)
        color: Цвет или тема
        jitter: Коэффициент случайности (0-1)
        sound_effect: Имитировать звук печати (вывод в stderr)
        on_char: Колбэк, вызываемый при печати каждого символа
    """
    if isinstance(color, ColorTheme):
        color = color.primary
    
    for i, char in enumerate(text):
        sys.stdout.write(f"{color}{char}{Colors.RESET}")
        sys.stdout.flush()
        
        if sound_effect:
            sys.stderr.write('\a')  # Звуковой сигнал
            sys.stderr.flush()
        
        if on_char:
            on_char(char)
        
        # Умная задержка: разные паузы для разных символов
        if char in '.,!?;:':
            delay = speed * 3 * random.uniform(1 - jitter, 1 + jitter)
        elif char == ' ':
            delay = speed * 0.5 * random.uniform(1 - jitter, 1 + jitter)
        elif char == '\n':
            delay = speed * 5 * random.uniform(1 - jitter, 1 + jitter)
        else:
            delay = speed * random.uniform(1 - jitter, 1 + jitter)
        
        await asyncio.sleep(delay)
    
    sys.stdout.write("\n")
    sys.stdout.flush()

async def scanner(
    text: str, 
    speed: float = 0.08, 
    color: Union[str, ColorTheme] = Colors.GREEN,
    width: int = 3,
    bounce: bool = False
) -> None:
    """
    Эффект сканирующей линии.
    
    Args:
        text: Текст для сканирования
        speed: Скорость движения сканера
        color: Цвет или тема
        width: Ширина подсветки
        bounce: Движение туда-обратно
    """
    if isinstance(color, ColorTheme):
        color = color.primary
    
    positions = list(range(len(text)))
    if bounce:
        positions += list(reversed(positions))
    
    for pos in positions:
        # Определяем диапазон подсветки
        start = max(0, pos - width // 2)
        end = min(len(text), pos + width // 2 + 1)
        
        # Собираем строку с подсветкой
        result = []
        result.append(text[:start])
        result.append(f"{Colors.BOLD}{color}{text[start:end]}{Colors.RESET}")
        result.append(text[end:])
        
        sys.stdout.write(f"\r{''.join(result)}")
        sys.stdout.flush()
        await asyncio.sleep(speed)
    
    sys.stdout.write(f"\r{text}\n")
    sys.stdout.flush()

async def glitch(
    text: str, 
    duration: float = 2.0, 
    intensity: float = 0.1,
    color: Union[str, ColorTheme] = Colors.RED,
    charset: str = "X#&%$@*!?<>/\\",
    preserve_spaces: bool = True
) -> None:
    """
    Эффект цифрового глитча.
    
    Args:
        text: Текст для искажения
        duration: Длительность эффекта
        intensity: Интенсивность помех (0-1)
        color: Цвет или тема
        charset: Набор символов для помех
        preserve_spaces: Сохранять пробелы
    """
    if isinstance(color, ColorTheme):
        color = color.primary
    
    start_time = asyncio.get_event_loop().time()
    chars = list(text)
    
    while asyncio.get_event_loop().time() - start_time < duration:
        # Вычисляем прогресс для плавного изменения интенсивности
        progress = (asyncio.get_event_loop().time() - start_time) / duration
        current_intensity = intensity * (1 - progress * 0.5)  # Уменьшаем к концу
        
        glitched = []
        for i, char in enumerate(chars):
            if preserve_spaces and char == ' ':
                glitched.append(' ')
            elif random.random() < current_intensity:
                glitched.append(random.choice(charset))
            else:
                glitched.append(char)
        
        # Иногда добавляем смещение
        if random.random() < 0.1:
            offset = random.randint(-2, 2)
            if offset > 0:
                glitched = [' '] * offset + glitched[:-offset]
            elif offset < 0:
                glitched = glitched[-offset:] + [' '] * (-offset)
        
        sys.stdout.write(f"\r{color}{''.join(glitched)}{Colors.RESET}")
        sys.stdout.flush()
        await asyncio.sleep(0.05)
    
    sys.stdout.write(f"\r{text}\n")
    sys.stdout.flush()

async def fade_out(
    text: str, 
    speed: float = 0.05,
    effect: str = "dots",  # dots, fade, dissolve, vaporize
    color: Union[str, ColorTheme] = Colors.RESET
) -> None:
    """
    Эффект исчезновения текста.
    
    Args:
        text: Текст для исчезновения
        speed: Скорость исчезновения
        effect: Тип эффекта
        color: Цвет или тема
    """
    if isinstance(color, ColorTheme):
        color = color.primary
    
    chars = list(text)
    indices = list(range(len(text)))
    
    if effect == "dots":
        # Исчезновение в точки
        random.shuffle(indices)
        for idx in indices:
            chars[idx] = random.choice(['.', '·', ' ', ' '])
            sys.stdout.write(f"\r{color}{''.join(chars)}{Colors.RESET}")
            sys.stdout.flush()
            await asyncio.sleep(speed * random.uniform(0.5, 1.5))
    
    elif effect == "fade":
        # Постепенное исчезновение
        steps = 10
        for step in range(steps, -1, -1):
            alpha = step / steps
            sys.stdout.write(f"\r{color}{text}{Colors.RESET}")
            sys.stdout.flush()
            await asyncio.sleep(speed * 2)
    
    elif effect == "dissolve":
        # Эффект растворения
        positions = [(i, random.random()) for i in range(len(text))]
        positions.sort(key=lambda x: x[1])
        
        for i, _ in positions:
            chars[i] = ' '
            sys.stdout.write(f"\r{color}{''.join(chars)}{Colors.RESET}")
            sys.stdout.flush()
            await asyncio.sleep(speed)
    
    elif effect == "vaporize":
        # Эффект испарения (символы поднимаются вверх)
        for i in range(len(text) + 3):
            line = []
            for j, char in enumerate(text):
                if i - j > 0:
                    line.append(' ')
                else:
                    line.append(char)
            sys.stdout.write(f"\r{color}{''.join(line)}{Colors.RESET}")
            sys.stdout.flush()
            await asyncio.sleep(speed)
    
    sys.stdout.write("\r" + " " * len(text) + "\r")
    sys.stdout.flush()

async def progress_bar(
    total: int,
    prefix: str = "",
    suffix: str = "",
    length: int = 30,
    fill: str = "█",
    empty: str = "░",
    color: Union[str, ColorTheme] = Colors.GREEN,
    show_percentage: bool = True,
    show_count: bool = True
):
    """
    Анимированный прогресс-бар.
    
    Args:
        total: Общее количество шагов
        prefix: Текст перед баром
        suffix: Текст после бара
        length: Длина бара в символах
        fill: Символ заполнения
        empty: Символ пустоты
        color: Цвет или тема
        show_percentage: Показывать процент
        show_count: Показывать счетчик
    """
    if isinstance(color, ColorTheme):
        color = color.primary
    
    for i in range(total + 1):
        percent = 100 * (i / float(total))
        filled_length = int(length * i // total)
        bar = fill * filled_length + empty * (length - filled_length)
        
        line_parts = []
        if prefix:
            line_parts.append(prefix)
        
        line_parts.append(f"{color}[{bar}]{Colors.RESET}")
        
        if show_percentage:
            line_parts.append(f"{percent:.1f}%")
        
        if show_count:
            line_parts.append(f"({i}/{total})")
        
        if suffix:
            line_parts.append(suffix)
        
        sys.stdout.write("\r" + " ".join(line_parts))
        sys.stdout.flush()
        
        if i < total:
            await asyncio.sleep(0.1)
        else:
            sys.stdout.write("\n")
            sys.stdout.flush()

async def rainbow_text(
    text: str,
    speed: float = 0.1,
    cycle: bool = True
) -> None:
    """
    Радужный текст с анимацией.
    
    Args:
        text: Текст для анимации
        speed: Скорость смены цветов
        cycle: Зациклить анимацию
    """
    hues = [i / 12 for i in range(12)]  # 12 оттенков
    
    def hue_to_rgb(hue: float) -> Tuple[int, int, int]:
        """Конвертировать hue в RGB."""
        r = int(255 * (1 - abs((hue * 6) % 2 - 1)))
        g = int(255 * (1 - abs((hue * 6 + 4) % 2 - 1)))
        b = int(255 * (1 - abs((hue * 6 + 2) % 2 - 1)))
        return r, g, b
    
    frame = 0
    try:
        while True:
            colored_text = []
            for i, char in enumerate(text):
                hue = (frame / 60 + i / len(text)) % 1 if len(text) > 0 else 0
                r, g, b = hue_to_rgb(hue)
                colored_text.append(Colors.rgb(r, g, b) + char)
            
            sys.stdout.write(f"\r{''.join(colored_text)}{Colors.RESET}")
            sys.stdout.flush()
            
            frame += 1
            await asyncio.sleep(speed)
            
            if not cycle and frame >= 60:
                break
    except asyncio.CancelledError:
        sys.stdout.write(f"\r{text}\n")
        sys.stdout.flush()

async def particle_explosion(
    text: str,
    duration: float = 1.5,
    particle_count: int = 50
) -> None:
    """
    Эффект взрыва текста на частицы.
    
    Args:
        text: Текст для взрыва
        duration: Длительность анимации
        particle_count: Количество частиц
    """
    import math
    
    class Particle:
        def __init__(self, char: str, x: float, y: float):
            self.char = char
            self.x = x
            self.y = y
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(-3, 0)
            self.gravity = 0.1
            self.life = 1.0
            self.decay = random.uniform(0.02, 0.05)
    
    # Создаем частицы из каждого символа
    particles = []
    for i, char in enumerate(text):
        if char != ' ':
            for _ in range(max(1, particle_count // len(text))):
                particles.append(Particle(
                    char=char,
                    x=i,
                    y=0
                ))
    
    start_time = asyncio.get_event_loop().time()
    
    while asyncio.get_event_loop().time() - start_time < duration:
        # Очищаем экран
        sys.stdout.write("\033[2J\033[H")
        
        # Обновляем и рисуем частицы
        for p in particles[:]:
            p.x += p.vx
            p.y += p.vy
            p.vy += p.gravity
            p.life -= p.decay
            
            if p.life <= 0:
                particles.remove(p)
                continue
            
            # Рисуем частицу
            x_pos = int(p.x)
            y_pos = int(p.y)
            
            if 0 <= x_pos < 80 and 0 <= y_pos < 24:  # Примерные границы
                color_intensity = int(255 * p.life)
                color = Colors.rgb(
                    color_intensity,
                    color_intensity // 2,
                    max(0, color_intensity - 100)
                )
                sys.stdout.write(f"\033[{y_pos + 1};{x_pos + 1}H{color}{p.char}")
        
        sys.stdout.write(Colors.RESET)
        sys.stdout.flush()
        await asyncio.sleep(0.05)
    
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
