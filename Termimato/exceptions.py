"""
Кастомные исключения для библиотеки Termimato
"""

class TermimatoError(Exception):
    pass

class AnimationError(TermimatoError):
    def __init__(self, message: str, effect_name: str = None):
        self.effect_name = effect_name
        super().__init__(f"Animation error{f' in {effect_name}' if effect_name else ''}: {message}")

class ConfigurationError(TermimatoError):
    pass

class EffectNotFoundError(TermimatoError):
    def __init__(self, effect_name: str, available_effects: list = None):
        message = f"Effect '{effect_name}' not found."
        if available_effects:
            message += f" Available effects: {', '.join(available_effects)}"
        super().__init__(message)

class TerminalError(TermimatoError):
    pass

class ColorError(TermimatoError):
    pass

class AnimationInterruptedError(TermimatoError):
    pass

class ValidationError(TermimatoError):
    pass