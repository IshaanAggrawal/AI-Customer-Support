import time
import json
from functools import wraps
from .logger import logger

class MetricsHandler:
    """
    Handles logging of application metrics (Latency, Usage, Success/Fail).
    Logs are written as structured JSON for easy parsing.
    """
    
    def log_event(self, event_name: str, duration_ms: float = 0, metadata: dict = None):
        """
        Logs a single metric event.
        """
        if metadata is None:
            metadata = {}

        metric_entry = {
            "event": event_name,
            "duration_ms": round(duration_ms, 2),
            "timestamp": time.time(),
            **metadata
        }
        
        # We log at INFO level but with a specific prefix [METRICS]
        # This makes it easy to filter logs later (e.g., grep "[METRICS]")
        logger.info(f"[METRICS] {json.dumps(metric_entry)}")

    def measure_time(self, metric_name: str):
        """
        Decorator to measure how long a function takes to run.
        Usage:
            @metrics.measure_time("groq_generation")
            def my_func(): ...
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    status = "success"
                    return result
                except Exception as e:
                    status = "error"
                    raise e
                finally:
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000 # Convert to ms
                    self.log_event(
                        event_name=metric_name, 
                        duration_ms=duration, 
                        metadata={"status": status}
                    )
            return wrapper
        return decorator

# Singleton Instance
metrics = MetricsHandler()