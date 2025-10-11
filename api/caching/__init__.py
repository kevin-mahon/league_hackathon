from main import db
import datetime
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry(db.Model):
    id: int
    key: str
    value: str
    timestamp: datetime.datetime

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime)

    def __repr__(self):
        return f"<CacheEntry {self.key}>"
    


def save_cache(key, data):
    try:
        record = Cache.query.filter_by(key=key).first()
        if record:
            record.data = data
            record.updated_at = datetime.utcnow()
        else:
            record = Cache(key=key, data=data)
            db.session.add(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error saving cache for key {key}: {e}", exc_info=True)
        raise
        

def get_cache(key, ttl_seconds=None):
    try:
        record = Cache.query.filter_by(key=key).first()
        if not record:
            return None

        if ttl_seconds:
            age = (datetime.utcnow() - record.updated_at).total_seconds()
            if age > ttl_seconds:
                return None  # stale

        return record.data
    except Exception as e:
        logger.error(f"Error retrieving cache for key {key}: {e}", exc_info=True)
        return None