import os 

DATABASE_URL = os.environ.get("DATABASE_URL","postgresql://pulsewatch:pulsewatch@localhost:5432/pulsewatch")
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")