# backend/app/routers/functions.py

from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.crud import create_function
from app.utils.docker_runner import run_function_in_docker
from app.utils.docker_runner import run_function_in_docker_runc
import time
from app.utils.pool_service import run_function_from_pool

router = APIRouter(prefix="/functions", tags=["Functions"])

@router.post("/", response_model=schemas.FunctionOut)
def create_function(func_data: schemas.FunctionCreate, db: Session = Depends(get_db)):
    return crud.create_function(db, func_data)
@router.get("/metrics")
def get_all_metrics(
    function_id: int = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ExecutionMetric)
    if function_id is not None:
        query = query.filter(ExecutionMetric.function_id == function_id)
    return query.order_by(ExecutionMetric.timestamp.desc()).all()
# def get_all_metrics(db: Session = Depends(get_db)):
#     return db.query(ExecutionMetric).all()
@router.get("/{func_id}", response_model=schemas.FunctionOut)
def read_function(func_id: int, db: Session = Depends(get_db)):
    func = crud.get_function(db, func_id)
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    return func

@router.get("/", response_model=list[schemas.FunctionOut])
def list_functions(db: Session = Depends(get_db)):
    return crud.get_all_functions(db)

@router.put("/{func_id}", response_model=schemas.FunctionOut)
def update_function(func_id: int, func_data: schemas.FunctionCreate, db: Session = Depends(get_db)):
    return crud.update_function(db, func_id, func_data)

@router.delete("/{func_id}")
def delete_function(func_id: int, db: Session = Depends(get_db)):
    return crud.delete_function(db, func_id)


@router.post("/{func_id}/execute")
def execute_function(func_id: int, db: Session = Depends(get_db)):
    func = crud.get_function(db, func_id)
    if not func:
        raise HTTPException(status_code=404, detail="Function not found")
    
    result = run_function_in_docker(func.id, func.timeout)
    return result

# @router.post("/{func_id}/execute")
# def execute_function(
#     func_id: int,
#     runtime: str = Query("runc", enum=["runc", "runsc"]),  # 👈 runtime option with default and validation
#     db: Session = Depends(get_db)
# ):
#     func = crud.get_function(db, func_id)
#     if not func:
#         raise HTTPException(status_code=404, detail="Function not found")
    
#     result = run_function_in_docker(func.id, func.timeout, runtime=runtime)  # 👈 Pass runtime here
#     return result

from app.utils.docker_runner import run_function_in_docker, warm_up_container_st  # 👈 make sure both are imported
#repeated
# @router.post("/{func_id}/warmup")
# def warmup_function(func_id: int, runtime: str = Query("runc", enum=["runc", "runsc"]), db: Session = Depends(get_db)):
#     func = crud.get_function(db, func_id)
#     if not func:
#         raise HTTPException(status_code=404, detail="Function not found")
    
#     try:
#         warm_up_container(func_id, runtime)
#         return {"message": f"Container for function {func_id} warmed up using runtime '{runtime}'."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    #removed now because its repeated
@router.post("/execute-function-runc/")
def execute_function(
    func_id: int,
    timeout: float = 5.0,
    runtime: str = Query("runc", enum=["runc", "runsc"])
):
    """
    Execute a specific function inside a container using the specified runtime.
    """
    try:
        start = time.time()
        result = run_function_in_docker_runc(func_id, timeout, runtime)
        duration = round(time.time() - start, 4)
        result["duration"] = duration
        return {
            "function_id": func_id,
            "runtime": runtime,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare-performance/")
def compare_function_performance(func_id: int, timeout: float = 5.0):
    """
    Compare execution between runc and runsc.
    """
    try:
        # runc
        start_runc = time.time()
        runc_result = run_function_in_docker_runc(func_id, timeout, runtime="runc")
        runc_duration = round(time.time() - start_runc, 4)
        runc_result["duration"] = runc_duration

        # runsc
        start_runsc = time.time()
        runsc_result = run_function_in_docker_runc(func_id, timeout, runtime="runsc")
        runsc_duration = round(time.time() - start_runsc, 4)
        runsc_result["duration"] = runsc_duration

        # Comparison summary
        faster = "runc" if runc_duration < runsc_duration else "runsc"
        diff = round(abs(runc_duration - runsc_duration), 4)

        return {
            "function_id": func_id,
            "results": {
                "runc": runc_result,
                "runsc": runsc_result
            },
            "summary": {
                "faster_runtime": faster,
                "time_difference_seconds": diff
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from app.utils.docker_runner import warm_up_container
@router.post("/warmup/")
def warmup_function(func_id: int, runtime: str = Query("runc", enum=["runc", "runsc"])):
    """
    Warm up container before actual execution.
    """
    try:
        warm_up_container(func_id, runtime)
        return {"message": f"Container warm-up done for function {func_id} using {runtime}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# from app.utils.docker_runner import run_function_in_docker
from app.model.execution_metric import ExecutionMetric
@router.post("/functions/{function_id}/run")
def run_function(
    function_id: int,
    timeout: float = Query(5.0),
    runtime: str = Query("runc"),
    db: Session = Depends(get_db)
):
    result = run_function_in_docker_runc(function_id, timeout, runtime, db)
    return {
        "function_id": function_id,
        "runtime": runtime,
        "result": result
    }
from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str
    code: str

@router.post("/execute-pool")
def execute_code_from_pool(request: CodeRequest):
    try:
        result = run_function_from_pool(request.language, request.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))