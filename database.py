"""
Database layer for Property Collection Bot using SQLAlchemy ORM
"""

import os
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, BigInteger, Text, Boolean, DateTime, ForeignKey, DECIMAL, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/properti_db')
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ORM Models
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    properties = relationship("Property", back_populates="user", cascade="all, delete-orphan")


class Property(Base):
    __tablename__ = 'properties'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    
    # Property Type & Location
    property_type = Column(String(50), nullable=False)
    condition = Column(String(50))  # Baru, Bekas, Siap Huni, Butuh Renovasi
    address = Column(Text)
    city = Column(String(100), index=True)
    district = Column(String(100))
    province = Column(String(100))
    postal_code = Column(String(10))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    
    # Pricing
    transaction_type = Column(String(20), nullable=False)
    price = Column(BigInteger, index=True)  # Primary price (usually sale, or rent if rent-only)
    rent_price = Column(BigInteger)  # Secondary price if dual listing (e.g. JualSewa)
    price_per_meter = Column(BigInteger)
    negotiable = Column(Boolean, default=True)
    
    # Dimensions
    land_area = Column(Integer)
    building_area = Column(Integer)
    
    # Specifications
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    floors = Column(DECIMAL(3, 1))
    carports = Column(Integer)
    garages = Column(Integer)
    year_built = Column(Integer)
    electricity = Column(Integer)
    orientation = Column(String(50))
    dimensions = Column(String(50))
    row_road = Column(String(100))
    
    # Utilities & Condition
    water_type = Column(String(50))  # PDAM, Sumur, etc.
    furnished = Column(String(50))  # Full, Semi, Unfurnished
    phone_line_count = Column(Integer)
    
    # Legal & Financial
    kpr = Column(Boolean, default=False)
    imb = Column(Boolean, default=False)
    blueprint = Column(Boolean, default=False)
    
    # Facilities (JSON)
    facilities = Column(JSON)
    
    # Description & Contact
    description = Column(Text)
    contact_name = Column(String(255))
    contact_phone = Column(String(50))
    contact_whatsapp = Column(String(50))
    property_url = Column(Text)
    agent_url = Column(Text)
    video_review_url = Column(Text)
    
    # Certificate
    certificate_type = Column(String(50))
    
    # Status
    status = Column(String(20), default='active')
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")


class PropertyImage(Base):
    __tablename__ = 'property_images'
    
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE'), index=True)
    file_id = Column(String(255), nullable=False)
    file_path = Column(Text)
    caption = Column(Text)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    property = relationship("Property", back_populates="images")


# Database initialization
def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        logger.error(f"Error getting database session: {e}")
        db.close()
        raise


# CRUD Operations for Users
def get_or_create_user(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> User:
    """Get existing user or create new one"""
    db = get_db()
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {telegram_id}")
        else:
            # Update last_active
            user.last_active = datetime.utcnow()
            db.commit()
            db.refresh(user)
        
        return user
    except Exception as e:
        logger.error(f"Error getting/creating user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# CRUD Operations for Properties
def create_property(user_id: int, property_data: Dict[str, Any]) -> Property:
    """Create new property listing"""
    db = get_db()
    try:
        property_obj = Property(user_id=user_id, **property_data)
        
        # Calculate price per meter if possible
        if property_obj.price and property_obj.land_area:
            property_obj.price_per_meter = property_obj.price // property_obj.land_area
        
        db.add(property_obj)
        db.commit()
        db.refresh(property_obj)
        logger.info(f"Created property {property_obj.id} for user {user_id}")
        return property_obj
    except Exception as e:
        logger.error(f"Error creating property: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_user_properties(user_id: int, page: int = 1, limit: int = 5) -> Dict[str, Any]:
    """Get properties by user with pagination"""
    db = get_db()
    try:
        query = db.query(Property).filter(Property.user_id == user_id)
        
        # Calculate total and pages
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Get items for current page
        offset = (page - 1) * limit
        properties = query.order_by(Property.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            'items': properties,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page
        }
    except Exception as e:
        logger.error(f"Error getting user properties: {e}")
        raise
    finally:
        db.close()


def search_properties_advanced(user_id: int, filters: Dict[str, Any], page: int = 1, limit: int = 5) -> Dict[str, Any]:
    """
    Search properties using structured filters from AI
    """
    db = get_db()
    try:
        query = db.query(Property).filter(Property.user_id == user_id)
        
        # Apply filters
        if filters.get('property_type'):
            query = query.filter(Property.property_type.ilike(f"%{filters['property_type']}%"))
            
        if filters.get('location_keyword'):
            loc = f"%{filters['location_keyword']}%"
            query = query.filter(
                Property.city.ilike(loc) | 
                Property.district.ilike(loc) | 
                Property.address.ilike(loc)
            )
            
        if filters.get('min_price') is not None:
            query = query.filter(Property.price >= filters['min_price'])
            
        if filters.get('max_price') is not None:
            query = query.filter(Property.price <= filters['max_price'])
            
        if filters.get('min_bedrooms') is not None:
            query = query.filter(Property.bedrooms >= filters['min_bedrooms'])
            
        if filters.get('min_land_area') is not None:
            query = query.filter(Property.land_area >= filters['min_land_area'])

        # Calculate total and pages
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Get items for current page
        offset = (page - 1) * limit
        properties = query.order_by(Property.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            'items': properties,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page
        }
    except Exception as e:
        logger.error(f"Error searching properties advanced: {e}")
        raise
    finally:
        db.close()


def search_properties(user_id: int, keyword: str, page: int = 1, limit: int = 5) -> Dict[str, Any]:
    """Search user properties by keyword"""
    db = get_db()
    try:
        search_term = f"%{keyword}%"
        query = db.query(Property).filter(
            Property.user_id == user_id,
            (
                Property.address.ilike(search_term) |
                Property.description.ilike(search_term) |
                Property.city.ilike(search_term) |
                Property.district.ilike(search_term) |
                Property.property_type.ilike(search_term)
            )
        )
        
        # Calculate total and pages
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Get items for current page
        offset = (page - 1) * limit
        properties = query.order_by(Property.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            'items': properties,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page
        }
    except Exception as e:
        logger.error(f"Error searching properties: {e}")
        raise
    finally:
        db.close()


def get_property_by_id(property_id: int) -> Optional[Property]:
    """Get property by ID"""
    db = get_db()
    try:
        return db.query(Property).filter(Property.id == property_id).first()
    except Exception as e:
        logger.error(f"Error getting property: {e}")
        raise
    finally:
        db.close()


def update_property(property_id: int, update_data: Dict[str, Any]) -> Optional[Property]:
    """Update property"""
    db = get_db()
    try:
        property_obj = db.query(Property).filter(Property.id == property_id).first()
        if property_obj:
            for key, value in update_data.items():
                setattr(property_obj, key, value)
            db.commit()
            db.refresh(property_obj)
            logger.info(f"Updated property {property_id}")
        return property_obj
    except Exception as e:
        logger.error(f"Error updating property: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def delete_property(property_id: int, user_id: int) -> bool:
    """Delete property securely (check ownership)"""
    db = get_db()
    try:
        property_obj = db.query(Property).filter(
            Property.id == property_id,
            Property.user_id == user_id
        ).first()
        
        if property_obj:
            db.delete(property_obj)
            db.commit()
            logger.info(f"Deleted property {property_id} for user {user_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting property: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# CRUD Operations for Property Images
def add_property_image(property_id: int, file_id: str, caption: str = None, is_primary: bool = False) -> PropertyImage:
    """Add image to property"""
    db = get_db()
    try:
        image = PropertyImage(
            property_id=property_id,
            file_id=file_id,
            caption=caption,
            is_primary=is_primary
        )
        db.add(image)
        db.commit()
        db.refresh(image)
        logger.info(f"Added image to property {property_id}")
        return image
    except Exception as e:
        logger.error(f"Error adding property image: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_property_stats(user_id: int = None) -> Dict[str, Any]:
    """Get statistics about properties"""
    db = get_db()
    try:
        query = db.query(Property)
        if user_id:
            query = query.filter(Property.user_id == user_id)
        
        total = query.count()
        active = query.filter(Property.status == 'active').count()
        
        stats = {
            'total': total,
            'active': active,
            'inactive': total - active,
            'by_type': {},
            'by_transaction': {}
        }
        
        # Group by property type
        for prop_type in ['rumah', 'apartemen', 'tanah', 'ruko', 'villa']:
            count = query.filter(Property.property_type == prop_type).count()
            if count > 0:
                stats['by_type'][prop_type] = count
        
        # Group by transaction type
        for trans_type in ['jual', 'sewa']:
            count = query.filter(Property.transaction_type == trans_type).count()
            if count > 0:
                stats['by_transaction'][trans_type] = count
        
        return stats
    except Exception as e:
        logger.error(f"Error getting property stats: {e}")
        raise
    finally:
        db.close()


def get_unique_cities(user_id: int) -> list:
    """Get list of unique cities for user's properties"""
    db = get_db()
    try:
        cities = db.query(Property.city)\
            .filter(Property.user_id == user_id)\
            .filter(Property.city.isnot(None))\
            .filter(Property.city != '')\
            .distinct()\
            .order_by(Property.city)\
            .all()
        return [c[0] for c in cities if c[0]]
    finally:
        db.close()


def get_unique_districts(user_id: int, city: str) -> list:
    """Get list of unique districts for a city"""
    db = get_db()
    try:
        districts = db.query(Property.district)\
            .filter(Property.user_id == user_id)\
            .filter(Property.city == city)\
            .filter(Property.district.isnot(None))\
            .filter(Property.district != '')\
            .distinct()\
            .order_by(Property.district)\
            .all()
        return [d[0] for d in districts if d[0]]
    finally:
        db.close()


def get_properties_by_location(user_id: int, city: str = None, district: str = None, min_price: int = None, max_price: int = None, page: int = 1, limit: int = 5) -> Dict[str, Any]:
    """Get properties filtered by city/district/price with pagination"""
    db = get_db()
    try:
        query = db.query(Property).filter(Property.user_id == user_id)
        
        if city:
            query = query.filter(Property.city == city)
        if district:
            query = query.filter(Property.district == district)
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        
        # Calculate total and pages
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit
        
        # Get items for current page - sort by LOWEST PRICE first
        offset = (page - 1) * limit
        properties = query.order_by(Property.price.asc()).offset(offset).limit(limit).all()
        
        return {
            'items': properties,
            'total_items': total_items,
            'total_pages': total_pages,
            'current_page': page
        }
    except Exception as e:
        logger.error(f"Error getting properties by location: {e}")
        raise
    finally:
        db.close()
