"""
Для общего пользования + MIT
"""

import asyncio
import itertools
import time
from typing import Optional, List, Callable, Any
from dataclasses import dataclass, field
from enum import Enum

from .effects import Colors
from .exceptions import AnimationError

class AnimationState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"

@dataclass
class AnimationMetrics:
    start_time: float = 0.0
    end_time: float = 0.0
    frame_count: int = 0
    avg_fps: float = 0.0
    
    @property
    def duration(self) -> float:
        if self.end_time > 0 and self.start_time > 0:
            return self.end_time - self.start_time
        return 0.0
    
    @property
    def fps(self) -> float:
        if self.duration > 0 and self.frame_count > 0:
            return self.frame_count / self.duration
        return 0.0

class BaseAnimator:
    
    def __init__(self, name: str = "Animator"):
        self.name = name
        self.state = AnimationState.IDLE
        self.metrics = AnimationMetrics()
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        
    async def start(self):
        if self.state == AnimationState.RUNNING:
            raise AnimationError(f"{self.name} is already running")
        
        self.state = AnimationState.RUNNING
        self.metrics.start_time = time.time()
        self.metrics.frame_count = 0
        self._stop_event.clear()
        
        try:
            self._task = asyncio.create_task(self._run())
            await self._task
        except Exception as e:
            self.state = AnimationState.ERROR
            raise AnimationError(f"{self.name} failed: {str(e)}")
        finally:
            self.metrics.end_time = time.time()
            
    async def stop(self):
        if self._task and not self._task.done():
            self._stop_event.set()
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self.state = AnimationState.CANCELLED
        
    async def pause(self):
        if self.state == AnimationState.RUNNING:
            self.state = AnimationState.PAUSED
            
    async def resume(self):
        if self.state == AnimationState.PAUSED:
            self.state = AnimationState.RUNNING
    
    async def _run(self):
        raise NotImplementedError("Subclasses must implement _run()")
    
    def _record_frame(self):
        self.metrics.frame_count += 1
    
    def get_stats(self) -> dict:
        return {
            "name": self.name,
            "state": self.state.value,
            "duration": self.metrics.duration,
            "frames": self.metrics.frame_count,
            "fps": self.metrics.fps,
        }

class SpinnerAnimator(BaseAnimator):
    
    def __init__(self, 
                 frames: List[str],
                 label: str = "Loading",
                 color: str = Colors.CYAN,
                 interval: float = 0.1):
        super().__init__(name=f"Spinner-{label}")
        self.frames = frames
        self.label = label
        self.color = color
        self.interval = interval
        self._frame_cycle = None
        
    async def _run(self):
        self._frame_cycle = itertools.cycle(self.frames)
        
        while not self._stop_event.is_set():
            if self.state == AnimationState.PAUSED:
                await asyncio.sleep(0.1)
                continue
                
            frame = next(self._frame_cycle)
            self._render_frame(frame)
            self._record_frame()
            
            try:
                await asyncio.wait_for(
                    self._stop_event.wait(), 
                    timeout=self.interval
                )
            except asyncio.TimeoutError:
                continue
                
    def _render_frame(self, frame: str):
        print(f"\r{self.color}{frame}{Colors.RESET} {self.label}", end="", flush=True)

class ProgressAnimator(BaseAnimator):
    
    def __init__(self,
                 total: int = 100,
                 label: str = "Progress",
                 color: str = Colors.CYAN,
                 width: int = 40,
                 show_percentage: bool = True,
                 show_eta: bool = True):
        super().__init__(name=f"ProgressBar-{label}")
        self.total = total
        self.current = 0
        self.label = label
        self.color = color
        self.width = width
        self.show_percentage = show_percentage
        self.show_eta = show_eta
        self.start_time = None
        
    def update(self, value: int):
        self.current = min(max(value, 0), self.total)
        
    def increment(self, amount: int = 1):
        self.update(self.current + amount)
        
    async def _run(self):
        self.start_time = time.time()
        
        while not self._stop_event.is_set():
            if self.state == AnimationState.PAUSED:
                await asyncio.sleep(0.1)
                continue
                
            self._render_frame()
            self._record_frame()
            
            if self.current >= self.total:
                break
                
            await asyncio.sleep(0.05)  #20кдрв
            
    def _render_frame(self):
        percent = self.current / self.total if self.total > 0 else 0
        filled = int(self.width * percent)
        bar = '█' * filled + '░' * (self.width - filled)
        
        eta_str = ""
        if self.show_eta and self.current > 0 and self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                eta = (elapsed / self.current) * (self.total - self.current)
                eta_str = f" ETA: {eta:.1f}s"
        
        percentage_str = f" {percent:.1%}" if self.show_percentage else ""
        
        print(f"\r{self.color}{self.label}: [{bar}]{percentage_str}{eta_str}{Colors.RESET}", 
              end="", flush=True)
        
    async def complete(self):
        self.current = self.total
        self._render_frame()
        elapsed = time.time() - self.start_time if self.start_time else 0
        print(f"\n{Colors.GREEN}✓ {self.label} completed in {elapsed:.2f}s{Colors.RESET}")

class CountdownAnimator(BaseAnimator):
    
    def __init__(self,
                 seconds: int = 10,
                 format_string: str = "{seconds:02d}",
                 color: str = Colors.BRIGHT_RED,
                 final_message: str = "GO!"):
        super().__init__(name=f"Countdown-{seconds}s")
        self.seconds = seconds
        self.format_string = format_string
        self.color = color
        self.final_message = final_message
        self.current_second = seconds
        
    async def _run(self):
        self.current_second = self.seconds
        
        while self.current_second > 0 and not self._stop_event.is_set():
            if self.state == AnimationState.PAUSED:
                await asyncio.sleep(0.1)
                continue
                
            self._render_frame()
            self._record_frame()
            
            self.current_second -= 1
            
            if self.current_second > 0:
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=1)
                except asyncio.TimeoutError:
                    continue
                    
        if not self._stop_event.is_set():
            print(f"\r{Colors.BRIGHT_GREEN}{self.final_message}{Colors.RESET}")
            self.state = AnimationState.COMPLETED
            
    def _render_frame(self):
        minutes = self.current_second // 60
        seconds = self.current_second % 60
        hours = self.current_second // 3600
        
        formatted = self.format_string.format(
            seconds=self.current_second,
            minutes=minutes,
            hours=hours,
            total_seconds=self.current_second,
            formatted_seconds=f"{seconds:02d}",
            formatted_minutes=f"{minutes:02d}",
            formatted_hours=f"{hours:02d}"
        )
        
        print(f"\r{self.color}{formatted}{Colors.RESET}", end="", flush=True)

class TextAnimator(BaseAnimator):
    
    def __init__(self,
                 text: str,
                 effect_func: Callable,
                 effect_name: str = "TextEffect"):
        super().__init__(name=f"{effect_name}-Animator")
        self.text = text
        self.effect_func = effect_func
        self.effect_name = effect_name
        
    async def _run(self):
        try:
            await self.effect_func(self.text)
            self.state = AnimationState.COMPLETED
        except Exception as e:
            self.state = AnimationState.ERROR
            raise
