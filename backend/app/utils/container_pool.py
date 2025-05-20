# backend/app/utils/container_pool.py

import subprocess
import threading
import time

container_pool = {
    "python": [],
    "javascript": []
}

POOL_SIZE = 2  # Number of containers to keep ready per language

def start_idle_container(language: str):
    image_name = f"{language.lower()}_base"
    container_name = f"idle_{language}_{int(time.time())}"

    command = [
        "docker", "run", "-d",
        "--name", container_name,
        image_name, "tail", "-f", "/dev/null"
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"[POOL] Started idle container: {container_name}")
    return container_name

# def warm_pool(language: str):
#     while len(container_pool[language]) < POOL_SIZE:
#         container = start_idle_container(language)
#         container_pool[language].append(container)



import docker

def initialize_pool(pool_size=2):
    client = docker.from_env()
    print("🔥 Initializing container pool...")

    language = "python"  # Assuming you're only warming Python for now
    container_pool[language] = []

    for i in range(pool_size):
        container_name = f"warmup_pool_{i}"
        try:
            # Remove existing container if any
            try:
                existing = client.containers.get(container_name)
                print(f"⚠️ Container {container_name} already exists. Removing...")
                existing.remove(force=True)
            except docker.errors.NotFound:
                pass

            # Start fresh one
            container = client.containers.run(
                image="python:3.9-slim",
                name=container_name,
                command="sleep 3600",
                detach=True,
                tty=True,
                auto_remove=False
            )

            print(f"✅ Container {container_name} started with ID: {container.short_id}")
            
            # 🔥 Add it to the pool
            container_pool[language].append(container.name)

        except Exception as e:
            print(f"⚠️ Failed to start container {container_name}: {e}")


def acquire_container(language: str):
    if container_pool.get(language):
        if container_pool[language]:
            container_name = container_pool[language].pop(0)

            # Check if it still exists
            result = subprocess.run(["docker", "inspect", container_name], capture_output=True)
            if result.returncode != 0:
                # It doesn't exist anymore
                print(f"⚠️ Container {container_name} not found. Starting a new one.")
                return start_idle_container(language)
            
            return container_name
    
    # No container in pool, fallback
    return start_idle_container(language)


def release_container(language: str, container_name: str):
    container_pool[language].append(container_name)
