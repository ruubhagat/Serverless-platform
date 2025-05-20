# backend/app/crud.py

from sqlalchemy.orm import Session
from app import models, schemas
from pathlib import Path
import shutil
import subprocess
# def create_function(db: Session, func: schemas.FunctionCreate):
#     db_func = models.Function(**func.dict())
#     db.add(db_func)
#     db.commit()
#     db.refresh(db_func)
#     return db_func
# def create_function(db: Session, func: schemas.FunctionCreate):
#     db_func = models.Function(**func.dict())
#     db.add(db_func)
#     db.commit()
#     db.refresh(db_func)

#     # --- Step 1: Create executions directory ---
#     func_dir = Path("executions") / str(db_func.id)
#     func_dir.mkdir(parents=True, exist_ok=True)
#         # --- Step 2: Save the function code ---
#     ext = "py" if func.language == "python" else "js"
#     file_path = func_dir / f"function.{ext}"

#     with open(file_path, "w") as f:
#         f.write(func.route)
#     # --- Step 3: Copy base Dockerfile ---
#     # language = func.language.strip().lower()  # ensure correct casing and spacing
#     # dockerfile_src = f"docker/{language}-base.Dockerfile"
#     # shutil.copy(dockerfile_src, func_dir / "Dockerfile")
#     # # --- Step 4: Build Docker image ---
#     # subprocess.run(["docker", "build", "-t", f"function_{db_func.id}", "."], cwd=func_dir)

#     # return db_func
    
#     # dockerfile_src = Path(__file__).resolve().parent.parent / "docker" / f"{func.language.lower()}-base.Dockerfile"
#     dockerfile_src = Path(__file__).resolve().parents[2] / "docker" / f"{func.language.lower()}-base.Dockerfile"


#     if not dockerfile_src.exists():
#         raise FileNotFoundError(f"Dockerfile not found at: {dockerfile_src}")

#     shutil.copy(dockerfile_src, func_dir / "Dockerfile")

#     subprocess.run(["docker", "build", "-t", f"function_{db_func.id}", "."], cwd=func_dir)

#     return db_func

from app.utils.docker_runner import warm_up_container_st  # 👈 import here

# def create_function(db: Session, func: schemas.FunctionCreate):
#     db_func = models.Function(**func.dict())
#     db.add(db_func)
#     db.commit()
#     db.refresh(db_func)

#     # --- Step 1: Create executions directory ---
#     func_dir = Path("executions") / str(db_func.id)
#     func_dir.mkdir(parents=True, exist_ok=True)

#     # --- Step 2: Save the function code ---
#     ext = "py" if func.language == "python" else "js"
#     file_path = func_dir / f"function.{ext}"
#     with open(file_path, "w") as f:
#         f.write(func.route)

#     # --- Step 3: Copy base Dockerfile ---
#     dockerfile_src = Path(__file__).resolve().parents[2] / "docker" / f"{func.language.lower()}-base.Dockerfile"
#     if not dockerfile_src.exists():
#         raise FileNotFoundError(f"Dockerfile not found at: {dockerfile_src}")
#     shutil.copy(dockerfile_src, func_dir / "Dockerfile")

#     # --- Step 4: Build Docker image ---
#     subprocess.run(["docker", "build", "-t", f"function_{db_func.id}", "."], cwd=func_dir)

#     # --- ✅ Step 5: Warm-up container ---
#     warm_up_container(db_func.id)

#     return db_func
import time  # ⬅️ Add this at the top if not already

def create_function(db: Session, func: schemas.FunctionCreate):
    db_func = models.Function(**func.dict())
    db.add(db_func)
    db.commit()
    db.refresh(db_func)

    # Step 1: Create executions directory
    func_dir = Path("executions") / str(db_func.id)
    func_dir.mkdir(parents=True, exist_ok=True)

    # Step 2: Save the function code
    ext = "py" if func.language == "python" else "js"
    file_path = func_dir / f"function.{ext}"
    with open(file_path, "w") as f:
        f.write(func.route)

    # Step 3: Copy base Dockerfile
    dockerfile_src = Path(__file__).resolve().parents[2] / "docker" / f"{func.language.lower()}-base.Dockerfile"
    print(dockerfile_src)
    if not dockerfile_src.exists():
        raise FileNotFoundError(f"Dockerfile not found at: {dockerfile_src}")
    shutil.copy(dockerfile_src, func_dir / "Dockerfile")

    # Step 4: Build Docker image
    subprocess.run(["docker", "build", "-t", f"function_{db_func.id}", "."], cwd=func_dir)

    # ✅ Step 5: Warm-up container and measure time
    start_time = time.time()
    warm_up_container_st(db_func.id)
    end_time = time.time()
    print(f"[Warm-up] Function {db_func.id} container started in {end_time - start_time:.2f} seconds")

    return db_func

def get_function(db: Session, func_id: int):
    return db.query(models.Function).filter(models.Function.id == func_id).first()

def get_all_functions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Function).offset(skip).limit(limit).all()

def update_function(db: Session, func_id: int, func_data: schemas.FunctionCreate):
    func = get_function(db, func_id)
    if func:
        for key, value in func_data.dict().items():
            setattr(func, key, value)
        db.commit()
        db.refresh(func)
    return func

def delete_function(db: Session, func_id: int):
    func = get_function(db, func_id)
    if func:
        db.delete(func)
        db.commit()
    return func
