from pathlib import Path
import yaml
from pydantic import BaseModel


class Settings(BaseModel):
    genius: dict = {"access_token": ""}
    whisper: dict = {"model_size": "large-v3", "device": "auto", "compute_type": "float16"}
    audio: dict = {"sample_rate": 16000, "format": "wav"}
    storage: dict = {
        "data_dir": "data/songs",
        "anki_dir": "~/Documents/Anki",
    }
    database: dict = {"url": "sqlite+aiosqlite:///data/what.db"}

    @property
    def data_dir(self) -> Path:
        p = Path(self.storage["data_dir"])
        if not p.is_absolute():
            p = Path(__file__).parent.parent.parent.parent / p
        p.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def anki_dir(self) -> Path:
        p = Path(self.storage["anki_dir"]).expanduser()
        return p

    @property
    def db_url(self) -> str:
        url = self.database["url"]
        if url.startswith("sqlite"):
            p = Path(__file__).parent.parent.parent.parent / "data" / "what.db"
            return f"sqlite+aiosqlite:///{p}"
        return url


def load_settings() -> Settings:
    config_path = Path(__file__).parent.parent.parent.parent / "configs" / "default.yaml"
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
        return Settings(**data)
    return Settings()


settings = load_settings()
