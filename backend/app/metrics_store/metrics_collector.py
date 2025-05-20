from sqlalchemy.orm import Session

from app.model.execution_metric import ExecutionMetric


def save_execution_metric(db: Session, metric_data: dict):
    metric = ExecutionMetric(**metric_data)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric
