import os
import subprocess

def build_gvisor_image(function_dir, image_name="gvisor-function-image"):
    dockerfile_path = os.path.join(function_dir, "Dockerfile")
    if not os.path.exists(dockerfile_path):
        raise FileNotFoundError("Dockerfile not found in the function directory!")

    command = [
        "docker", "build", "-t", image_name, function_dir
    ]

    try:
        print(f"📦 Building image '{image_name}' using gVisor-compatible Dockerfile...")
        subprocess.run(command, check=True)
        print(f"✅ Image '{image_name}' built successfully!")
        return image_name
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while building image: {e}")
        return None
