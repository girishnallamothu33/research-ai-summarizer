from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base
import datetime

class SummaryHistory(Base):
    __tablename__ = "summary_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    discipline = Column(String)
    extracted_text = Column(Text)
    short_summary = Column(Text)
    detailed_summary = Column(Text)
    keywords = Column(JSON)
    key_insights = Column(JSON)
    discipline_interpretation = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TopicCluster(Base):
    __tablename__ = "topic_clusters"

    id = Column(Integer, primary_key=True, index=True)
    summary_id = Column(Integer)
    topic_label = Column(String)
    cluster_id = Column(Integer)
