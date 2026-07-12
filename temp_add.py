from app.db.database import Base, engine, SessionLocal

# ✅ IMPORT ALL MODELS (IMPORTANT)
from app.models.user import User
from app.models.company_user import CompanyUser
from app.models.chat import Chat
from app.models.message import Message

# ✅ CREATE TABLES
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# OPTIONAL: add demo users again if needed
# demo_users = [
#     "atharvap3@hexaware.com",
#     "PurvaPramodP@hexaware.com",
#     "RohanG11@hexaware.com"
# ]
#
# for email in demo_users:
#     db.add(CompanyUser(email=email))

db.commit()

print("✅ Tables created successfully")