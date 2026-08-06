from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Song(Base):
    __tablename__ = "songs"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    youtube_url = Column(String)
    audio_path = Column(String)
    duration = Column(Float)
    lyrics_text = Column(Text)
    created_at = Column(String, nullable=False)

    segments = relationship(
        "Segment", back_populates="song", cascade="all, delete-orphan",
        order_by="Segment.line_number"
    )


class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(String, ForeignKey("songs.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)

    song = relationship("Song", back_populates="segments")
