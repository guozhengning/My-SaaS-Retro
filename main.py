from saas_retro.db import Base
from saas_retro.db import models as _models  # noqa: F401
from sqlalchemy.engine import make_url

from saas_retro.config import get_settings


def main():
    print(f"Loaded {len(Base.metadata.tables)} SQLAlchemy tables.")
    print(f"Configured dialect: {make_url(get_settings().database_url).get_backend_name()}")
    print("Run API with: uv run uvicorn saas_retro.app:app --reload")


if __name__ == "__main__":
    main()
