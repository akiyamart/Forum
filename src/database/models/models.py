import uuid 
from sqlalchemy import String, Column, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base
from src.api.schemas.roles import ForumRole

Base = declarative_base()

class User(Base): 
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(String), nullable=False)

    @property
    def is_admin(self) -> bool: 
        return ForumRole.ROLE_PORTAL_ADMIN in self.roles
    
    @property
    def is_superadmin(self) -> bool: 
        return ForumRole.ROLE_PORTAL_SUPERADMIN in self.roles
    
    def add_admin_privilages(self): 
        if not self.is_admin: 
            return {*self.roles, ForumRole.ROLE_PORTAL_ADMIN}
        
    def remove_admin_privilages(self): 
        if self.is_admin: 
            return {role for role in self.roles if role != ForumRole.ROLE_PORTAL_ADMIN}