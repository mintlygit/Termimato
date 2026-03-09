"""
Конфигурация библиотеки Termimato.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict, field

from .exceptions import ConfigurationError

@dataclass
class TermimatoConfig:
    
    #Основа
    auto_restore_cursor: bool = True
    check_terminal_support: bool = True
    default_speed: float = 0.05
    max_concurrent_animations: int = 10
    
    #Цветики
    enable_true_color: bool = True
    fallback_to_8bit: bool = True
    default_theme: str = "dark"  # dark, light, rainbow
    
    #Эфектики
    type_writer_jitter: float = 0.5
    scanner_width: int = 3
    glitch_charset: str = "X#&%$@*!?<>/\\"
    fade_out_effect: str = "dots"
    
    #Вывод
    buffer_output: bool = True
    flush_threshold: int = 1024
    enable_sound_effects: bool = False
    
    enable_signal_handlers: bool = True
    debug_mode: bool = False
    log_file: Optional[str] = None
    
    custom_themes: Dict[str, Dict[str, str]] = field(default_factory=dict)

#Стандарт
DEFAULT_CONFIG = TermimatoConfig()

#Глобалка
_current_config: Optional[TermimatoConfig] = None

def get_config() -> TermimatoConfig:
    global _current_config
    if _current_config is None:
        _current_config = _load_config()
    return _current_config

def set_config(config: TermimatoConfig):
    global _current_config
    _current_config = config

def update_config(**kwargs):
    config = get_config()
    
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
        else:
            raise ConfigurationError(f"Неизвестный параметр конфигурации: {key}")
    
    set_config(config)

def reset_config():
    global _current_config
    _current_config = TermimatoConfig()

def save_config(path: Optional[str] = None):
    config = get_config()
    
    if path is None:
        config_dir = Path.home() / ".config" / "termimato"
        config_dir.mkdir(parents=True, exist_ok=True)
        path = config_dir / "config.json"
    else:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(asdict(config), f, indent=2, ensure_ascii=False)

def load_config(path: Optional[str] = None) -> TermimatoConfig:
    if path is None:
        config_dir = Path.home() / ".config" / "termimato"
        path = config_dir / "config.json"
    
    path = Path(path)
    
    if not path.exists():
        return TermimatoConfig()
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config = TermimatoConfig(**data)
        return config
    except (json.JSONDecodeError, TypeError) as e:
        raise ConfigurationError(f"Ошибка загрузки конфигурации: {e}") from e

def _load_config() -> TermimatoConfig:
    #выгрузка
    try:
        return load_config()
    except ConfigurationError:
        return TermimatoConfig()

_current_config = _load_config()