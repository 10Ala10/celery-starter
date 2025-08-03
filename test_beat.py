#!/usr/bin/env python3
"""
Test script to monitor periodic tasks and test manual execution
Run this while your worker and beat scheduler are running
"""

import os
import time
from hello import periodic_health_check, daily_cleanup_task, app

def test_periodic_tasks():
    """Test the periodic tasks manually"""
    print("🔄 Testing Periodic Tasks...")
    print("=" * 50)
    
    # Test 1: Manual health check
    print("\n1️⃣ Testing periodic_health_check manually...")
    try:
        result = periodic_health_check.delay()
        print(f"   Task ID: {result.id}")
        final_result = result.get(timeout=10)
        print(f"   ✅ Result: {final_result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Manual cleanup task
    print("\n2️⃣ Testing daily_cleanup_task manually...")
    try:
        result = daily_cleanup_task.delay()
        print(f"   Task ID: {result.id}")
        final_result = result.get(timeout=10)
        print(f"   ✅ Result: {final_result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 Manual testing completed!")

def monitor_beat_tasks():
    """Monitor periodic tasks for a while"""
    print("\n👀 Monitoring periodic tasks...")
    print("This will check the task status for 2 minutes")
    print("Make sure your worker and beat scheduler are running!")
    print("Press Ctrl+C to stop monitoring")
    
    start_time = time.time()
    try:
        while time.time() - start_time < 120:  # Monitor for 2 minutes
            print(f"\n⏰ Monitoring... ({int(time.time() - start_time)}s elapsed)")
            
            # Check active tasks
            inspect = app.control.inspect()
            active_tasks = inspect.active()
            
            if active_tasks:
                for worker, tasks in active_tasks.items():
                    if tasks:
                        print(f"   🔥 Worker {worker} has {len(tasks)} active tasks")
                        for task in tasks:
                            print(f"      - {task['name']} (ID: {task['id'][:8]}...)")
            else:
                print("   💤 No active tasks currently")
            
            time.sleep(10)  # Check every 10 seconds
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped by user")

if __name__ == "__main__":
    # Set environment variable if not already set
    if not os.getenv('REDIS_URL'):
        os.environ['REDIS_URL'] = 'rediss://default:ASA5AAIjcDEyYTBhYjU1NGU2OGY0MTQ4YmFhOWU2NmZlNDNlY2EwNnAxMA@causal-mongrel-8249.upstash.io:6379'
    
    print("🚀 Celery Beat Test Script")
    print("Choose an option:")
    print("1. Test periodic tasks manually")
    print("2. Monitor periodic tasks")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice in ["1", "3"]:
        test_periodic_tasks()
    
    if choice in ["2", "3"]:
        monitor_beat_tasks()
    
    print("\n✅ Done!")