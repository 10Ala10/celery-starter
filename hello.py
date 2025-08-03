import os
import time
from celery import Celery

# Create Celery instance with Upstash Redis
# For Upstash, we'll use redis:// with SSL configuration in the app config
redis_url = os.getenv('REDIS_URL', 'rediss://default:ASA5AAIjcDEyYTBhYjU1NGU2OGY0MTQ4YmFhOWU2NmZlNDNlY2EwNnAxMA@causal-mongrel-8249.upstash.io:6379')
app = Celery('hello', broker=redis_url, backend=redis_url)

# Configure Celery (optional - for development)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Windows-specific configuration to avoid billiard issues
    worker_pool='solo',  # Use solo pool to avoid multiprocessing issues on Windows
    worker_concurrency=1,  # Single worker process
    # SSL configuration for Upstash Redis
    broker_use_ssl={
        'ssl_cert_reqs': 'none',
        'ssl_ca_certs': None,
        'ssl_certfile': None,
        'ssl_keyfile': None,
    },
    redis_backend_use_ssl={
        'ssl_cert_reqs': 'none',
        'ssl_ca_certs': None,
        'ssl_certfile': None,
        'ssl_keyfile': None,
    },
    # Celery Beat configuration for periodic tasks
    beat_schedule={
        'check-system-health-every-10-seconds': {
            'task': 'hello.periodic_health_check',
            'schedule': 10.0,  # Run every 10 seconds
        },
        'daily-cleanup': {
            'task': 'hello.daily_cleanup_task',
            'schedule': 60.0,  # Run every 60 seconds (for demo - normally would be daily)
        },
    },
)

@app.task
def add_numbers(x, y):
    """Simple task that adds two numbers with simulated processing time"""
    print(f"🔢 Starting calculation: {x} + {y}")
    
    # Simulate some processing time
    print("⏳ Processing step 1/3...")
    time.sleep(2)
    
    print("⏳ Processing step 2/3...")
    time.sleep(2)
    
    print("⏳ Processing step 3/3...")
    time.sleep(2)
    
    result = x + y
    print(f"✅ Calculation completed: {x} + {y} = {result}")
    return result

@app.task
def say_hello(name):
    """Simple task that says hello with simulated processing time"""
    print(f"👋 Starting greeting process for: {name}")
    
    # Simulate greeting preparation
    print("📝 Preparing personalized greeting...")
    time.sleep(1.5)
    
    print("🎨 Formatting message...")
    time.sleep(1.5)
    
    print("📤 Finalizing greeting...")
    time.sleep(1)
    
    message = f"Hello, {name}!"
    print(f"✅ Greeting completed: {message}")
    return message

@app.task
def long_running_task(duration=10):
    """A longer task to demonstrate task monitoring"""
    print(f"🚀 Starting long-running task (duration: {duration} seconds)")
    
    for i in range(duration):
        print(f"⏱️  Progress: {i+1}/{duration} seconds elapsed...")
        time.sleep(1)
    
    result = f"Task completed after {duration} seconds!"
    print(f"🎉 {result}")
    return result

@app.task
def periodic_health_check():
    """Periodic task that runs every 10 seconds to check system health"""
    import random
    
    # Simulate health check with random metrics
    cpu_usage = random.randint(10, 90)
    memory_usage = random.randint(20, 80)
    status = "healthy" if cpu_usage < 80 and memory_usage < 75 else "warning"
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🏥 [HEALTH CHECK] {timestamp}")
    print(f"   CPU Usage: {cpu_usage}%")
    print(f"   Memory Usage: {memory_usage}%")
    print(f"   Status: {status.upper()}")
    
    result = {
        'timestamp': timestamp,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'status': status
    }
    
    if status == "warning":
        print(f"⚠️  WARNING: High resource usage detected!")
    else:
        print(f"✅ System is healthy")
    
    return result

@app.task
def daily_cleanup_task():
    """Mock daily cleanup task (runs every minute for demo purposes)"""
    import random
    
    # Simulate cleanup activities
    files_cleaned = random.randint(5, 50)
    cache_cleared = random.randint(100, 1000)  # MB
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🧹 [CLEANUP] {timestamp}")
    print(f"   Files cleaned: {files_cleaned}")
    print(f"   Cache cleared: {cache_cleared} MB")
    
    # Simulate cleanup time
    time.sleep(2)
    
    result = {
        'timestamp': timestamp,
        'files_cleaned': files_cleaned,
        'cache_cleared_mb': cache_cleared,
        'cleanup_duration': 2
    }
    
    print(f"✅ Cleanup completed successfully!")
    return result

def get_task_result(task_id):
    """Retrieve a task result by its ID from the backend"""
    result = app.AsyncResult(task_id)
    if result.ready():
        return {
            'task_id': task_id,
            'status': result.status,
            'result': result.result
        }
    else:
        return {
            'task_id': task_id,
            'status': result.status,
            'result': None
        }

def main():
    print("Celery app created with Celery Beat support!")
    print("Available tasks:")
    print("- add_numbers(x, y) - adds two numbers (6 seconds)")
    print("- say_hello(name) - creates a greeting (4 seconds)")
    print("- long_running_task(duration=10) - customizable duration task")
    print("- get_task_result(task_id) - helper to retrieve saved results")
    print("\n🔄 Periodic tasks (Celery Beat):")
    print("- periodic_health_check() - runs every 10 seconds")
    print("- daily_cleanup_task() - runs every 60 seconds (demo)")
    print("\nTo test:")
    print("1. Install dependencies: uv sync")
    print("2. Start worker: celery -A hello worker --loglevel=info")
    print("3. Start beat scheduler (in new terminal): celery -A hello beat --loglevel=info")
    print("4. Manual tasks in Python shell:")
    print("   from hello import add_numbers, say_hello, long_running_task, app")
    print("   result = add_numbers.delay(4, 4)")
    print("   print(f'Task ID: {result.id}')")
    print("   print(f'Result: {result.get()}')")
    print("   # Test long task:")
    print("   # long_task = long_running_task.delay(5)")
    print("   # You can also retrieve results later by task ID:")
    print("   # task_result = app.AsyncResult(task_id)")
    print("   # print(task_result.get())")
    print("\n⏰ All tasks now include sleep to demonstrate async processing!")
    print("🔄 Periodic tasks will run automatically when beat scheduler is started!")
    print("Using Upstash Redis for both broker AND result backend!")

if __name__ == "__main__":
    main()
