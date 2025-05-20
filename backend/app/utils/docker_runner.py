import subprocess
import uuid

def run_function_in_docker(func_id: int, timeout: float):
    # Unique container name for isolation
    container_name = f"run_{func_id}_{uuid.uuid4().hex[:6]}"
    image_name = f"function_{func_id}"

    try:
        # Run container
        result = subprocess.run(
            ["docker", "run", "--rm", "--name", container_name, image_name],
            capture_output=True,
            text=True,
            timeout=timeout  # Timeout in seconds
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Execution exceeded timeout of {timeout} seconds.",
            "exit_code": -1
        }
# def run_function_in_docker_st(func_id: int, timeout: float, runtime: str = "runc"):
#     container_name = f"run_{func_id}_{uuid.uuid4().hex[:6]}"
#     image_name = f"function_{func_id}"

#     try:
#         result = subprocess.run(
#             ["docker", "run", "--rm", "--runtime", runtime, "--name", container_name, image_name],
#             capture_output=True,
#             text=True,
#             timeout=timeout
#         )
#         return {
#             "stdout": result.stdout,
#             "stderr": result.stderr,
#             "exit_code": result.returncode
#         }

#     except subprocess.TimeoutExpired:
#         return {
#             "stdout": "",
#             "stderr": f"Execution exceeded timeout of {timeout} seconds.",
#             "exit_code": -1
#         }

import subprocess
import uuid

import subprocess
import time

def warm_up_container_st(func_id: int):
    print(f"\n🌡 Warming up container for function {func_id}...")

    container_name = f"warmup_function_{func_id}"
    image_name = f"function_{func_id}"
    
    # Custom warm-up command
    cmd = [
        "docker", "run", "--rm",
        "--name", container_name,
        image_name,
        "python", "-c", "import time; print('🔥 Container Ready!'); time.sleep(2)"
    ]

    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        print(f"[Warm-up ✅] Success for function {func_id} in {duration}s")
        print(f"  🔸 STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            print(f"  ⚠️ STDERR:\n{result.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        print(f"[Warm-up ❌] Failed for function {func_id}")
        print(f"  🔸 STDOUT:\n{e.stdout.strip()}")
        print(f"  ⚠️ STDERR:\n{e.stderr.strip()}")
def warm_up_container(func_id: int, runtime: str = "runc"):
    print(f"\n🌡 Warming up container for function {func_id} using {runtime}...")

    container_name = f"warmup_function_{func_id}"
    image_name = f"function_{func_id}"

    cmd = [
        "docker", "run", "--rm",
        "--runtime", runtime,
        "--name", container_name,
        image_name,
        "python", "-c", "import time; print('🔥 Container Ready!'); time.sleep(2)"
    ]

    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        print(f"[Warm-up ✅] Success for function {func_id} in {duration}s")
        print(f"  🔸 STDOUT:\n{result.stdout.strip()}")
        if result.stderr.strip():
            print(f"  ⚠️ STDERR:\n{result.stderr.strip()}")

    except subprocess.CalledProcessError as e:
        print(f"[Warm-up ❌] Failed for function {func_id}")
        print(f"  🔸 STDOUT:\n{e.stdout.strip()}")
        print(f"  ⚠️ STDERR:\n{e.stderr.strip()}")
import subprocess
import uuid
import time
import os
# ALLOWED_RUNTIMES = {"runc", "runsc"}  # ✅ runc = native, runsc = gVisor

# def run_function_in_docker_runc(func_id: int, timeout: float, runtime: str = "runc"):
#     if runtime not in ALLOWED_RUNTIMES:
#         raise ValueError(f"Unsupported runtime: {runtime}")

#     container_name = f"run_{func_id}_{uuid.uuid4().hex[:6]}"
#     image_name = f"function_{func_id}"

#     try:
#         start_time = time.time()
#         result = subprocess.run(
#             ["docker", "run", "--rm", "--runtime", runtime, "--name", container_name, image_name],
#             capture_output=True,
#             text=True,
#             timeout=timeout
#         )
#         end_time = time.time()

#         return {
#             "stdout": result.stdout,
#             "stderr": result.stderr,
#             "exit_code": result.returncode,
#             "duration": round(end_time - start_time, 3)
#         }

#     except subprocess.TimeoutExpired:
#         return {
#             "stdout": "",
#             "stderr": f"Execution exceeded timeout of {timeout} seconds.",
#             "exit_code": -1
#         }

# def warm_up_container_runc(func_id: int, runtime: str = "runc"):
#     if runtime not in ALLOWED_RUNTIMES:
#         raise ValueError(f"Unsupported runtime: {runtime}")

#     print(f"\n🌡 Warming up container for function {func_id} using {runtime}...")

#     container_name = f"warmup_function_{func_id}"
#     image_name = f"function_{func_id}"

#     cmd = [
#         "docker", "run", "--rm",
#         "--runtime", runtime,
#         "--name", container_name,
#         image_name,
#         "python", "-c", "import time; print('🔥 Container Ready!'); time.sleep(2)"
#     ]

#     start_time = time.time()
#     try:
#         result = subprocess.run(cmd, capture_output=True, text=True, check=True)
#         end_time = time.time()
#         duration = round(end_time - start_time, 2)

#         print(f"[Warm-up ✅] Success for function {func_id} in {duration}s")
#         print(f"  🔸 STDOUT:\n{result.stdout.strip()}")
#         if result.stderr.strip():
#             print(f"  ⚠️ STDERR:\n{result.stderr.strip()}")

#     except subprocess.CalledProcessError as e:
#         print(f"[Warm-up ❌] Failed for function {func_id}")
#         print(f"  🔸 STDOUT:\n{e.stdout.strip()}")
#         print(f"  ⚠️ STDERR:\n{e.stderr.strip()}")
    
import subprocess, uuid, time
from app.metrics_store.metrics_collector import save_execution_metric

# def run_function_in_docker_runc(func_id: int, timeout: float, runtime: str = "runc", db=None):
#     container_name = f"run_{func_id}_{uuid.uuid4().hex[:6]}"
#     image_name = f"function_{func_id}"

#     start_time = time.time()
#     try:
#         result = subprocess.run(
#             ["docker", "run", "--rm", "--runtime", runtime, "--name", container_name, image_name],
#             capture_output=True,
#             text=True,
#             timeout=timeout
#         )
#         end_time = time.time()

#         metric = {
#             "function_id": func_id,
#             "runtime": runtime,
#             "duration": round(end_time - start_time, 4),
#             "exit_code": result.returncode,
#             "error_message": None,
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         }

#     except subprocess.TimeoutExpired:
#         end_time = time.time()
#         metric = {
#             "function_id": func_id,
#             "runtime": runtime,
#             "duration": round(end_time - start_time, 4),
#             "exit_code": -1,
#             "error_message": f"Execution exceeded timeout of {timeout} seconds.",
#             "stdout": "",
#             "stderr": ""
#         }

#     if db:
#         save_execution_metric(db, metric)

#     return metric
import subprocess
import uuid
import time

def run_function_in_docker_runc(func_id: int, timeout: float, runtime: str = "runc", db=None):
    container_name = f"run_{func_id}_{uuid.uuid4().hex[:6]}"
    image_name = f"function_{func_id}"

    start_time = time.time()
    try:
        # Running the container with the specified runtime
        result = subprocess.run(
            ["docker", "run", "--rm", "--runtime", runtime, "--name", container_name, image_name],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        end_time = time.time()

        # Collect metrics about the execution
        metric = {
            "function_id": func_id,
            "runtime": runtime,
            "duration": round(end_time - start_time, 4),
            "exit_code": result.returncode,
            "error_message": None,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.TimeoutExpired:
        end_time = time.time()
        # Handle timeout exception
        metric = {
            "function_id": func_id,
            "runtime": runtime,
            "duration": round(end_time - start_time, 4),
            "exit_code": -1,
            "error_message": f"Execution exceeded timeout of {timeout} seconds.",
            "stdout": "",
            "stderr": ""
        }

    except Exception as e:
        end_time = time.time()
        # Handle other exceptions
        metric = {
            "function_id": func_id,
            "runtime": runtime,
            "duration": round(end_time - start_time, 4),
            "exit_code": -1,
            "error_message": str(e),
            "stdout": "",
            "stderr": str(e)
        }

    if db:
        save_execution_metric(db, metric)

    return metric
