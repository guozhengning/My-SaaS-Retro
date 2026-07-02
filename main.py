from saas_retro.db import Base
from saas_retro.db import models as _models  # noqa: F401


def main():
    print(f"Loaded {len(Base.metadata.tables)} SQLAlchemy tables.")


if __name__ == "__main__":
    main()
