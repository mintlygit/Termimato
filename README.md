<div align="center">

# 🍅 Termimato

**Асинхронная магия для вашего терминала**

[![PyPI Version](https://img.shields.io/pypi/v/termimato?style=flat-square&color=tomato&logo=pypi&logoColor=white)](https://pypi.org/project/termimato/)
[![Python Versions](https://img.shields.io/pypi/pyversions/termimato?style=flat-square&logo=python&logoColor=white)](https://pypi.org/project/termimato/)
[![License](https://img.shields.io/pypi/l/termimato?style=flat-square&color=blue)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/termimato?style=flat-square&color=forestgreen)](https://pypi.org/project/termimato/)
![Visitor Count](https://visitor-badge.laobi.icu/badge?page_id=mintlygit.termimato)

<p align="center">
  <a href="#особенности">Особенности</a> •
  <a href="#установка">Установка</a> •
  <a href="#быстрый-старт">Быстрый старт</a> •
  <a href="#документация">Документация</a>
</p>

</div>

---

## 📖 О проекте

**Termimato** — это мощная асинхронная библиотека для создания профессиональных анимаций и визуальных эффектов прямо в консоли. Забудьте о блокировках ввода/вывода: создавайте красивые CLI-интерфейсы, используя всю мощь `asyncio`.

## ✨ Особенности

| Иконка | Возможность | Описание |
| :---: | :--- | :--- |
| 🎇 | **Богатая коллекция** | Печатная машинка, сканер, глитч, исчезновение, прогресс-бары и многое другое. |
| 🎨 | **Продвинутая палитра** | Поддержка **8-bit**, **True Color (24-bit)**, градиентов и кастомных тем. |
| ⚡ | **Полная асинхронность** | Все эффекты работают через `asyncio` без блокировки основного потока (non-blocking). |
| 🛡️ | **Надежность** | Автоматическое управление курсором, корректная очистка и перехват ошибок. |
| 🔧 | **Гибкость** | Тонкая настройка тем, параметров эффектов и конфигурации терминала. |
| 📱 | **Кросс-платформенность** | Работает на Linux, macOS, Windows Terminal и даже в Termux (Android). |

## 🚀 Установка

Установите библиотеку через pip:

```bash
pip install termimato
import asyncio
from termimato import Termimato, Colors, type_writer

async def main():
    # Инициализация контекстного менеджера для безопасной работы с терминалом
    async with Termimato() as t:
        
        # 1. Простой эффект печатной машинки
        await t.play(type_writer, "Hello, World!", color=Colors.GREEN)
        
        # 2. Спиннер с кастомными параметрами (работает фоном)
        spinner = await t.start_spinner("Processing...", color=Colors.CYAN)
        
        # Эмуляция полезной нагрузки
        await asyncio.sleep(2)
        
        # Остановка спиннера
        spinner.cancel()

if __name__ == "__main__":
    asyncio.run(main())


🗺️ Совместимость
✅ Linux (GNOME Terminal, Konsole, xterm и др.)
✅ macOS (iTerm2, Terminal.app)
✅ Windows (Windows Terminal, PowerShell Core, CMD)
✅ Android (Termux)
🤝 Вклад в развитие (Contributing)
Мы рады любым пул-реквестам! Если у вас есть идеи для новых эффектов или улучшений:
Форкните репозиторий.
Создайте ветку (git checkout -b feature/NewEffect).
Закоммитьте изменения (git commit -m 'Add amazing glitch effect').
Сделайте Push (git push origin feature/NewEffect).
Откройте Pull Request.
📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.
<div align="center">
Created with ❤️ by <a href="https://www.google.com/search?q=https://github.com/%D0%92%D0%90%D0%A8_%D0%9D%D0%98%D0%9A%D0%9D%D0%95%D0%99%D0%9C">mintlygit</a>
</div>
