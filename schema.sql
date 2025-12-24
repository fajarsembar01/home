-- Database schema for Property Collection Bot

-- Users table: Track Telegram users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Properties table: Main property data
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Property Type & Location
    property_type VARCHAR(50) NOT NULL, -- rumah, apartemen, tanah, ruko, villa, dll
    address TEXT,
    city VARCHAR(100),
    district VARCHAR(100), -- kecamatan
    province VARCHAR(100),
    postal_code VARCHAR(10),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Pricing
    transaction_type VARCHAR(20) NOT NULL, -- jual, sewa
    price BIGINT, -- in Rupiah
    price_per_meter BIGINT, -- calculated
    negotiable BOOLEAN DEFAULT TRUE,
    
    -- Dimensions
    land_area INTEGER, -- in square meters
    building_area INTEGER, -- in square meters
    
    -- Specifications
    bedrooms INTEGER,
    bathrooms INTEGER,
    floors INTEGER,
    carports INTEGER,
    garages INTEGER,
    year_built INTEGER,
    
    -- Facilities (stored as JSON array)
    facilities JSONB,
    
    -- Description & Contact
    description TEXT,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),
    contact_whatsapp VARCHAR(50),
    
    -- Certificate & Legal
    certificate_type VARCHAR(50), -- SHM, SHGB, AJB, Girik, dll
    
    -- Status
    status VARCHAR(20) DEFAULT 'active', -- active, sold, rented, inactive
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Property Images table: Multiple photos per property
CREATE TABLE IF NOT EXISTS property_images (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
    file_id VARCHAR(255) NOT NULL, -- Telegram file_id for easy retrieval
    file_path TEXT, -- Optional: local storage path
    caption TEXT,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_properties_user_id ON properties(user_id);
CREATE INDEX IF NOT EXISTS idx_properties_city ON properties(city);
CREATE INDEX IF NOT EXISTS idx_properties_property_type ON properties(property_type);
CREATE INDEX IF NOT EXISTS idx_properties_transaction_type ON properties(transaction_type);
CREATE INDEX IF NOT EXISTS idx_properties_price ON properties(price);
CREATE INDEX IF NOT EXISTS idx_properties_status ON properties(status);
CREATE INDEX IF NOT EXISTS idx_property_images_property_id ON property_images(property_id);
CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to auto-update updated_at
CREATE TRIGGER update_properties_updated_at 
    BEFORE UPDATE ON properties 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert initial data for testing (optional)
-- You can remove this if not needed
INSERT INTO users (telegram_id, username, first_name) 
VALUES (123456789, 'test_user', 'Test User') 
ON CONFLICT (telegram_id) DO NOTHING;
