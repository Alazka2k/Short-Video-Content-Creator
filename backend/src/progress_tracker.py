import time
from typing import Dict, Any

class ProgressTracker:
    def __init__(self, total_steps: int):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        self.step_times: Dict[int, float] = {}

    def update(self, step: int, info: Dict[str, Any] = None):
        self.current_step = step
        self.step_times[step] = time.time()
        if info:
            print(f"Step {step}/{self.total_steps} completed. Info: {info}")
        else:
            print(f"Step {step}/{self.total_steps} completed.")

    def get_progress(self) -> Dict[str, Any]:
        elapsed_time = time.time() - self.start_time
        progress = (self.current_step / self.total_steps) * 100
        return {
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress_percentage": round(progress, 2),
            "elapsed_time": round(elapsed_time, 2),
            "estimated_time_remaining": self._estimate_time_remaining(),
        }

    def _estimate_time_remaining(self) -> float:
        if self.current_step == 0:
            return 0
        avg_time_per_step = (time.time() - self.start_time) / self.current_step
        remaining_steps = self.total_steps - self.current_step
        return round(avg_time_per_step * remaining_steps, 2)