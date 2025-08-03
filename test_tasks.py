#!/usr/bin/env python3
"""
Test script for Celery tasks
Run this while your worker is running in another terminal
"""

import os
from hello import add_numbers, say_hello, long_running_task, app, get_task_result

def test_tasks():
    print("🚀 Testing Celery Tasks...")
    print("=" * 50)
    
    # Test 1: Add Numbers
    print("\n1️⃣ Testing add_numbers(15, 27)...")
    result1 = add_numbers.delay(15, 27)
    print(f"   Task ID: {result1.id}")
    try:
        final_result = result1.get(timeout=10)  # Wait max 10 seconds
        print(f"   ✅ Result: {final_result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Say Hello
    print("\n2️⃣ Testing say_hello('World')...")
    result2 = say_hello.delay("World")
    print(f"   Task ID: {result2.id}")
    try:
        final_result = result2.get(timeout=10)
        print(f"   ✅ Result: {final_result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Multiple tasks
    print("\n3️⃣ Testing multiple tasks...")
    tasks = []
    for i in range(3):
        task = add_numbers.delay(i, i * 2)
        tasks.append(task)
        print(f"   Queued task {i+1}: {task.id}")
    
    print("\n   Waiting for results...")
    for i, task in enumerate(tasks):
        try:
            result = task.get(timeout=10)
            print(f"   ✅ Task {i+1} result: {result}")
        except Exception as e:
            print(f"   ❌ Task {i+1} error: {e}")
    
    # Test 4: Long running task (non-blocking)
    print("\n4️⃣ Testing long_running_task (5 seconds)...")
    long_task = long_running_task.delay(5)
    print(f"   Task ID: {long_task.id}")
    print("   ⏳ This will take 5 seconds - you can see progress in worker terminal...")
    try:
        result = long_task.get(timeout=15)
        print(f"   ✅ Long task result: {result}")
    except Exception as e:
        print(f"   ❌ Long task error: {e}")
    
    # Test 5: Task result retrieval
    print("\n5️⃣ Testing task result retrieval...")
    if tasks:
        task_id = tasks[0].id
        saved_result = get_task_result(task_id)
        print(f"   Retrieved result: {saved_result}")
    
    print("\n🎉 Testing completed!")
    print("\n💡 Pro tip: Watch the worker terminal to see task progress in real-time!")

if __name__ == "__main__":
    # Set environment variable if not already set
    if not os.getenv('REDIS_URL'):
        os.environ['REDIS_URL'] = 'rediss://default:ASA5AAIjcDEyYTBhYjU1NGU2OGY0MTQ4YmFhOWU2NmZlNDNlY2EwNnAxMA@causal-mongrel-8249.upstash.io:6379'
    
    test_tasks()