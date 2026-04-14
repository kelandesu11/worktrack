from sqlalchemy import text
from sqlalchemy.orm import Session


def refresh_dashboard_materialized_view(db: Session) -> None:
    db.execute(text("REFRESH MATERIALIZED VIEW dashboard_summary_mv"))
    db.commit()
