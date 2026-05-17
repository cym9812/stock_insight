from dataclasses import dataclass
from pathlib import Path

from backend.core.config import settings


@dataclass(frozen=True)
class LocalDataLayout:
    """Canonical local data directory layout."""

    root: Path

    @property
    def source_data_dir(self) -> Path:
        return self.root / "source_data"

    @property
    def normalized_data_dir(self) -> Path:
        return self.root / "normalized_data"

    @property
    def derived_data_dir(self) -> Path:
        return self.root / "derived_data"

    @property
    def application_data_dir(self) -> Path:
        return self.root / "application_data"

    @property
    def metadata_dir(self) -> Path:
        return self.root / "metadata"

    @property
    def databases_dir(self) -> Path:
        return self.root / "databases"

    @property
    def artifacts_dir(self) -> Path:
        return self.root / "artifacts"

    @property
    def cache_dir(self) -> Path:
        return self.root / "cache"

    @property
    def temporary_dir(self) -> Path:
        return self.root / "temporary"

    @property
    def source_market_quotes_dir(self) -> Path:
        return self.source_data_dir / "market_quotes"

    @property
    def source_text_documents_dir(self) -> Path:
        return self.source_data_dir / "text_documents"

    @property
    def normalized_market_bars_dir(self) -> Path:
        return self.normalized_data_dir / "market_bars"

    @property
    def normalized_text_documents_dir(self) -> Path:
        return self.normalized_data_dir / "text_documents"

    @property
    def derived_market_features_dir(self) -> Path:
        return self.derived_data_dir / "market_features"

    @property
    def derived_text_features_dir(self) -> Path:
        return self.derived_data_dir / "text_features"

    def ensure_directories(self) -> None:
        for directory in (
            self.source_market_quotes_dir,
            self.source_text_documents_dir,
            self.normalized_market_bars_dir,
            self.normalized_text_documents_dir,
            self.derived_market_features_dir,
            self.derived_text_features_dir,
            self.application_data_dir,
            self.metadata_dir,
            self.databases_dir,
            self.artifacts_dir,
            self.cache_dir,
            self.temporary_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


def get_local_data_layout() -> LocalDataLayout:
    return LocalDataLayout(settings.data_root_path)
