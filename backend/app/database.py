import logging
from typing import Dict, Any
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from backend.app.config import settings

logger = logging.getLogger("bharat_quest.database")
logging.basicConfig(level=logging.INFO)

class DatabaseManager:
    client = None
    db = None
    is_mock: bool = False

    @classmethod
    def connect(cls):
        """
        Connects to live MongoDB. If not reachable, seamlessly falls back to 
        mongomock so the SIH prototype functions smoothly out-of-the-box anywhere.
        """
        import os
        is_vercel = os.environ.get("VERCEL") == "1" or "VERCEL" in os.environ
        if is_vercel and ("localhost" in settings.MONGODB_URI or "127.0.0.1" in settings.MONGODB_URI):
            logger.info("Vercel serverless environment detected. Activating mongomock in-memory database engine.")
            import mongomock
            cls.client = mongomock.MongoClient()
            cls.db = cls.client[settings.DATABASE_NAME]
            cls.is_mock = True
            cls.seed_demo_accounts()
            return cls.db

        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}...")
            real_client = pymongo.MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=1500
            )
            real_client.admin.command('ping')
            cls.client = real_client
            cls.db = cls.client[settings.DATABASE_NAME]
            cls.is_mock = False
            logger.info("Successfully connected to live MongoDB server.")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(
                f"Live MongoDB unreachable ({e}). Activating mongomock in-memory engine "
                "for robust zero-friction hackathon testing."
            )
            import mongomock
            cls.client = mongomock.MongoClient()
            cls.db = cls.client[settings.DATABASE_NAME]
            cls.is_mock = True
            logger.info("Connected to in-memory mongomock database instance.")
            
            # Ensure basic collections exist in mock mode
            if "system_meta" not in cls.db.list_collection_names():
                cls.db["system_meta"].insert_one({
                    "initialized": True,
                    "civilization": "Indus Valley Civilization",
                    "mode": "in-memory-prototype"
                })

        cls.seed_demo_accounts()
        return cls.db

    @classmethod
    def seed_demo_accounts(cls):
        """
        Seeds standard SIH presentation accounts so judges can test instantly.
        """
        if cls.db is None:
            return
        try:
            users_col = cls.db["users"]
            if not users_col.find_one({"username": {"$regex": "^SIH_Explorer$", "$options": "i"}}):
                users_col.insert_one({
                    "username": "SIH_Explorer",
                    "age": 16,
                    "avatar": "🧭",
                    "archetype": "Civic Hydrologist",
                    "password": "1234",
                    "stats": {
                        "xp": 850,
                        "level": 2,
                        "seal_tokens": 30,
                        "completed_quests": ["quest_01_rebuild_city", "quest_03_drainage_challenge"],
                        "discovered_artifacts": ["art_unicorn_seal", "art_standard_brick", "art_painted_pottery"],
                        "explored_locations": ["residential_area", "main_street", "drainage_system", "great_bath"],
                        "badges": [
                            "badge_apprentice_excavator",
                            "badge_artifact_hunter",
                            "badge_master_planner",
                            "badge_heritage_explorer",
                            "badge_sanitation_master"
                        ],
                        "progress_percentage": 52.0
                    }
                })
                logger.info("Seeded SIH presentation demo account 'SIH_Explorer'.")
        except Exception as seed_err:
            logger.warning(f"Demo seeding notice: {seed_err}")

    @classmethod
    def get_db(cls):
        if cls.db is None:
            return cls.connect()
        return cls.db

    @classmethod
    def health_check(cls) -> Dict[str, Any]:
        try:
            db = cls.get_db()
            collections = db.list_collection_names()
            return {
                "status": "healthy",
                "connected": True,
                "engine": "mongomock (In-Memory Fallback)" if cls.is_mock else "MongoDB (Live Service)",
                "database_name": settings.DATABASE_NAME,
                "collections_count": len(collections),
                "collections": collections
            }
        except Exception as err:
            logger.error(f"Database health check failed: {err}")
            return {
                "status": "unhealthy",
                "connected": False,
                "error": str(err)
            }

db_manager = DatabaseManager
