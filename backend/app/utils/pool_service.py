import tempfile
import subprocess
from app.utils.container_pool import acquire_container, release_container

def run_function_from_pool(language: str, code: str):
    container_name = acquire_container(language)

    try:
        # Use tempfile to create a temp file safely
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(code)
            temp_path = temp_file.name

        # Copy file into container
        subprocess.run(["docker", "cp", temp_path, f"{container_name}:/code.py"])

        # Run code inside container
        result = subprocess.run(
            ["docker", "exec", container_name, "python", "/code.py"],
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

    finally:
        release_container(language, container_name)
