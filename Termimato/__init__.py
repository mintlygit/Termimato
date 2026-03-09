"""
Termimato - Асинхронная библиотека для создания анимаций в терминале.
Поддерживает Linux, macOS, Windows Terminal и Termux.
"""

from .animator import Termimato, AnimationController
from .effects import (
    Colors, 
    ColorTheme,
    type_writer, 
    scanner, 
    glitch, 
    fade_out,
    progress_bar,
    rainbow_text,
    particle_explosion
)
from .exceptions import TerminalError, AnimationError, ColorNotSupportedError
from .config import DEFAULT_CONFIG, get_config, set_config

__version__ = "2.0.0"
__author__ = "minthly"
__license__ = "MIT"

__all__ = [
    # Основные классы
    "Termimato",
    "AnimationController",
    
    # Эффекты
    "type_writer",
    "scanner", 
    "glitch",
    "fade_out",
    "progress_bar",
    "rainbow_text",
    "particle_explosion",
    
    # Цвета и темы
    "Colors",
    "ColorTheme",
    
    # Исключения
    "TerminalError",
    "AnimationError", 
    "ColorNotSupportedError",
    
    # Конфигурация
    "DEFAULT_CONFIG",
    "get_config",
    "set_config",
]
