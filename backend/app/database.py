import os
import json
import logging
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from backend.app.config import settings

logger = logging.getLogger("anveshika.database")
logging.basicConfig(level=logging.INFO)

STATE_FILE = os.path.join(tempfile.gettempdir(), "anveshika_state.json")

class DatabaseManager:
    client = None
    db = None
    is_mock: bool = False

    @classmethod
    def get_state_file_path(cls) -> str:
        return STATE_FILE

    @classmethod
    def save_state(cls):
        """
        Safely serializes in-memory mongomock collections to /tmp/anveshika_state.json
        so serverless function container warm invocations retain user profiles and progress.
        """
        if cls.db is None or not cls.is_mock:
            return
        try:
            users = []
            for u in cls.db["users"].find():
                u_copy = dict(u)
                if "_id" in u_copy:
                    u_copy["_id"] = str(u_copy["_id"])
                users.append(u_copy)
            
            payload = {
                "saved_at": datetime.utcnow().isoformat(),
                "users": users
            }
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, default=str)
        except Exception as e:
            logger.warning(f"Unable to write state to /tmp ({e}). In-memory state remains active.")

    @classmethod
    def load_state(cls):
        """
        Restores collections from /tmp/anveshika_state.json if available.
        """
        if cls.db is None or not os.path.exists(STATE_FILE):
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                payload = json.load(f)
            users = payload.get("users", [])
            for u in users:
                clean_name = u.get("username", "")
                if clean_name and not cls.db["users"].find_one({"username": {"$regex": f"^{clean_name}$", "$options": "i"}}):
                    # Strip stringified _id so mongomock generates a fresh ObjectId
                    u.pop("_id", None)
                    cls.db["users"].insert_one(u)
            logger.info(f"Loaded {len(users)} user profiles from /tmp/anveshika_state.json")
        except Exception as e:
            logger.warning(f"Unable to load state from /tmp ({e}).")

    @classmethod
    def connect(cls):
        """
        Connects to live MongoDB. If not reachable or running in serverless without cloud URI,
        activates mongomock with /tmp persistence so Anveshika runs zero-friction anywhere.
        """
        is_vercel = os.environ.get("VERCEL") == "1" or "VERCEL" in os.environ or "AWS_LAMBDA_FUNCTION_NAME" in os.environ
        has_cloud_mongo = ("mongodb+srv://" in settings.MONGODB_URI) or ("localhost" not in settings.MONGODB_URI and "127.0.0.1" not in settings.MONGODB_URI and "mongodb://" in settings.MONGODB_URI)

        if is_vercel and not has_cloud_mongo:
            logger.info("Vercel serverless environment detected without external Atlas URI. Activating mongomock in-memory engine with /tmp state file.")
            try:
                import mongomock
                cls.client = mongomock.MongoClient()
                cls.db = cls.client[settings.DATABASE_NAME]
                cls.is_mock = True
                cls.load_state()
                cls.seed_demo_accounts()
                return cls.db
            except Exception as e:
                logger.error(f"Error initializing mongomock: {e}")

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
                "with resilient /tmp fallback."
            )
            import mongomock
            cls.client = mongomock.MongoClient()
            cls.db = cls.client[settings.DATABASE_NAME]
            cls.is_mock = True
            cls.load_state()
            logger.info("Connected to in-memory mongomock database instance.")
            
            if "system_meta" not in cls.db.list_collection_names():
                cls.db["system_meta"].insert_one({
                    "initialized": True,
                    "platform": "Anveshika: Interactive Living Museum",
                    "mode": "serverless-in-memory"
                })

        cls.seed_demo_accounts()
        return cls.db

    @classmethod
    def seed_demo_accounts(cls):
        """
        Seeds standard presentation accounts so judges and students can test instantly.
        """
        if cls.db is None:
            return
        
        demo_profiles = [
            {
                "username": "Anveshika_Explorer",
                "age": 15,
                "avatar": "🧭",
                "archetype": "Civic Hydrologist & Heritage Scholar",
                "password": "1234",
                "stats": {
                    "xp": 950,
                    "level": 3,
                    "seal_tokens": 45,
                    "completed_quests": ["quest_01_rebuild_city", "quest_02_lost_artifact", "quest_03_drainage_challenge"],
                    "discovered_artifacts": ["art_unicorn_seal", "art_standard_brick", "art_painted_pottery", "art_dancing_girl"],
                    "explored_locations": ["residential_area", "main_street", "drainage_system", "great_bath", "granary_mound"],
                    "badges": [
                        "badge_apprentice_excavator",
                        "badge_artifact_hunter",
                        "badge_master_planner",
                        "badge_heritage_explorer",
                        "badge_sanitation_master"
                    ],
                    "progress_percentage": 68.0
                }
            },
            {
                "username": "Arjun",
                "age": 14,
                "avatar": "🧑‍🎓",
                "archetype": "Town Architect",
                "password": "1234",
                "stats": {
                    "xp": 250,
                    "level": 1,
                    "seal_tokens": 20,
                    "completed_quests": [],
                    "discovered_artifacts": [],
                    "explored_locations": ["residential_area"],
                    "badges": ["badge_apprentice_excavator"],
                    "progress_percentage": 15.0
                }
            },
            {
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
            }
        ]

        try:
            users_col = cls.db["users"]
            for profile in demo_profiles:
                p_name = profile["username"]
                if not users_col.find_one({"username": {"$regex": f"^{p_name}$", "$options": "i"}}):
                    profile["created_at"] = datetime.utcnow().isoformat() + "Z"
                    profile["last_login_at"] = datetime.utcnow().isoformat() + "Z"
                    profile["session_token"] = f"anveshika_{p_name.lower()}"
                    users_col.insert_one(profile)
            cls.save_state()
        except Exception as seed_err:
            logger.warning(f"Demo seeding notice: {seed_err}")

    @classmethod
    def ensure_user(cls, username: str, age: int = 14, avatar: str = "🧑‍🎓", archetype: str = "Heritage Explorer") -> Dict[str, Any]:
        """
        Guarantees that a user profile exists in the database.
        If the user does not exist (e.g. fresh serverless container or guest player),
        it dynamically initializes a default profile so quests, profiles, and rewards
        never fail with 404 or 500 errors.
        """
        db = cls.get_db()
        clean = (username or "Arjun").strip()
        users_col = db["users"]
        
        user = users_col.find_one({"username": {"$regex": f"^{clean}$", "$options": "i"}})
        if user:
            return user
        
        now_str = datetime.utcnow().isoformat() + "Z"
        new_user = {
            "username": clean,
            "age": age,
            "avatar": avatar,
            "archetype": archetype,
            "password": "1234",
            "session_token": f"anveshika_{clean.lower()[:8]}",
            "created_at": now_str,
            "last_login_at": now_str,
            "stats": {
                "xp": 150,
                "level": 1,
                "seal_tokens": 15,
                "unlocked_zones": ["citadel_gateway", "citadel_great_bath"],
                "completed_quests": [],
                "badges": ["badge_apprentice_excavator"],
                "discovered_artifacts": [],
                "explored_locations": [],
                "unlocked_content": ["unlock_lower_town", "unlock_common_vitrines"],
                "progress_percentage": 0.0
            }
        }
        users_col.insert_one(new_user)
        cls.save_state()
        logger.info(f"Auto-provisioned default player session profile for '{clean}'")
        return new_user

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
                "engine": "mongomock with /tmp state persistence" if cls.is_mock else "MongoDB (Live Service)",
                "database_name": settings.DATABASE_NAME,
                "collections_count": len(collections),
                "collections": collections,
                "state_file": STATE_FILE if cls.is_mock else None
            }
        except Exception as err:
            logger.error(f"Database health check failed: {err}")
            return {
                "status": "unhealthy",
                "connected": False,
                "error": str(err)
            }

db_manager = DatabaseManager
