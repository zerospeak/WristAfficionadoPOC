# 8. Appendices

## Code Samples

### Web Scraping Module (Complete Implementation)

```python
import aiohttp
import asyncio
import json
import random
import time
from datetime import datetime

class ProxyManager:
    def __init__(self, config_path="config/proxy_config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.proxies = []
        self.last_rotation = 0
        
    async def load_proxies(self):
        """Load proxies from configured providers"""
        for provider in self.config["proxy_providers"]:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    provider["endpoint"],
                    headers={"Authorization": f"Bearer {provider['api_key']}"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.proxies.extend(data["proxies"])
        
        self.last_rotation = time.time()
        
    async def get_proxy(self):
        """Get a random proxy from the pool"""
        if not self.proxies or (time.time() - self.last_rotation > self.config["rotation_interval"]):
            await self.load_proxies()
            
        return random.choice(self.proxies) if self.proxies else None

class UserAgentRotator:
    def __init__(self, config_path="config/user_agents.json"):
        with open(config_path, 'r') as f:
            self.user_agents = json.load(f)["user_agents"]
    
    def get_random_user_agent(self):
        """Return a random user agent string"""
        return {
            "User-Agent": random.choice(self.user_agents)
        }

class WebScraper:
    def __init__(self, db_connection):
        self.proxy_manager = ProxyManager()
        self.user_agent_rotator = UserAgentRotator()
        self.db = db_connection
        
        # Load marketplace configurations
        with open("config/marketplaces.json", 'r') as f:
            self.marketplaces = json.load(f)["marketplaces"]
    
    async def scrape_marketplace(self, marketplace_name):
        """Scrape a specific marketplace for watch data"""
        marketplace = next((m for m in self.marketplaces if m["name"] == marketplace_name), None)
        if not marketplace:
            raise ValueError(f"Marketplace {marketplace_name} not found in configuration")
        
        proxy = await self.proxy_manager.get_proxy()
        headers = self.user_agent_rotator.get_random_user_agent()
        
        # Get list of brands to scrape
        brands = await self._get_brands(marketplace, proxy, headers)
        
        for brand in brands:
            # Respect rate limiting
            await asyncio.sleep(60 / marketplace["rate_limit"])
            
            # Get models for this brand
            models = await self._get_models(marketplace, brand, proxy, headers)
            
            for model in models:
                # Respect rate limiting
                await asyncio.sleep(60 / marketplace["rate_limit"])
                
                # Scrape product details
                await self._scrape_product(marketplace, brand, model, proxy, headers)
    
    async def _get_brands(self, marketplace, proxy, headers):
        """Get list of watch brands from marketplace"""
        url = f"{marketplace['base_url']}/brands"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    # Parse HTML to extract brands (implementation depends on site structure)
                    # This is a simplified example
                    return ["rolex", "patek_philippe", "audemars_piguet"]
                else:
                    return []
    
    async def _get_models(self, marketplace, brand, proxy, headers):
        """Get list of watch models for a brand"""
        url = f"{marketplace['base_url']}/brands/{brand}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    # Parse HTML to extract models (implementation depends on site structure)
                    # This is a simplified example
                    if brand == "rolex":
                        return ["daytona", "submariner", "datejust"]
                    elif brand == "patek_philippe":
                        return ["nautilus", "calatrava"]
                    else:
                        return ["royal_oak"]
                else:
                    return []
    
    async def _scrape_product(self, marketplace, brand, model, proxy, headers):
        """Scrape details for a specific watch model"""
        url = marketplace["base_url"] + marketplace["product_pattern"].format(brand=brand, model=model)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy, headers=headers) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Use selectors to extract data
                    # This is a simplified example - real implementation would use BeautifulSoup or similar
                    price = self._extract_with_selector(html, marketplace["selectors"]["price"])
                    name = self._extract_with_selector(html, marketplace["selectors"]["name"])
                    description = self._extract_with_selector(html, marketplace["selectors"]["description"])
                    
                    # Store in database
                    watch_id = f"{brand}_{model}"
                    
                    # Check if watch exists
                    existing_watch = self.db.query(
                        "SELECT id FROM watches WHERE id = %s",
                        (watch_id,)
                    )
                    
                    if not existing_watch:
                        # Insert new watch
                        self.db.execute(
                            "INSERT INTO watches (id, name, brand, description, marketplace_type, created_at, updated_at, last_scraped) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (watch_id, name, brand, description, marketplace["name"], datetime.now(), datetime.now(), datetime.now())
                        )
                    else:
                        # Update existing watch
                        self.db.execute(
                            "UPDATE watches SET name = %s, description = %s, updated_at = %s, last_scraped = %s WHERE id = %s",
                            (name, description, datetime.now(), datetime.now(), watch_id)
                        )
                    
                    # Insert price
                    self.db.execute(
                        "INSERT INTO prices (watch_model_number, price, competitor_id, scraped_at, active) VALUES (%s, %s, %s, %s, %s)",
                        (watch_id, price, marketplace["name"], datetime.now(), True)
                    )
                    
                    # Deactivate old prices
                    self.db.execute(
                        "UPDATE prices SET active = FALSE WHERE watch_model_number = %s AND competitor_id = %s AND id != (SELECT id FROM prices WHERE watch_model_number = %s AND competitor_id = %s ORDER BY scraped_at DESC LIMIT 1)",
                        (watch_id, marketplace["name"], watch_id, marketplace["name"])
                    )
                    
                    # Insert into price history
                    self.db.execute(
                        "INSERT INTO price_history (watch_model_number, price, recorded_at) VALUES (%s, %s, %s)",
                        (watch_id, price, datetime.now())
                    )
    
    def _extract_with_selector(self, html, selector):
        """Extract data from HTML using CSS selector"""
        # This is a simplified example - real implementation would use BeautifulSoup or similar
        # For demonstration purposes only
        if selector == ".product-price":
            return 10000.00  # Example price
        elif selector == ".product-title":
            return "Luxury Watch Model XYZ"  # Example name
        elif selector == ".product-description":
            return "This is a luxury watch with premium features."  # Example description
```

### Pricing Engine (Complete Implementation)

```python
import json
from datetime import datetime, timedelta

class PricingEngine:
    def __init__(self, db_connection, config_path="config/pricing_rules.json"):
        self.db = db_connection
        
        # Load pricing rules
        with open(config_path, 'r') as f:
            self.rules = json.load(f)
        
        # Load base prices
        with open("config/base_prices.json", 'r') as f:
            self.base_prices = json.load(f)
    
    def calculate_optimal_price(self, watch_data):
        """Calculate the optimal price for a watch based on rules and market data"""
        # Get base price
        base_price = self.get_base_price(watch_data)
        
        # Get competitor prices
        competitor_prices = self.get_competitor_prices(watch_data.model_number)
        
        # Start with base price
        optimal_price = base_price
        
        # Apply pricing rules if they exist for this category
        if watch_data.category in self.rules:
            category_rules = self.rules[watch_data.category]
            
            # Apply competitor discount rule
            if "competitor_a_discount" in category_rules and competitor_prices.get("competitor_a"):
                competitor_a_price = competitor_prices["competitor_a"]
                discount = category_rules["competitor_a_discount"]
                optimal_price = min(optimal_price, competitor_a_price - discount)
            
            # Apply competitor match percentage rule
            if "competitor_b_match_percent" in category_rules and competitor_prices.get("competitor_b"):
                competitor_b_price = competitor_prices["competitor_b"]
                match_percent = category_rules["competitor_b_match_percent"]
                optimal_price = min(optimal_price, competitor_b_price * (1 - match_percent))
            
            # Apply aging discount
            if "aging_discount_days" in category_rules and "aging_discount_percent" in category_rules:
                days_threshold = category_rules["aging_discount_days"]
                discount_percent = category_rules["aging_discount_percent"]
                
                # Check if watch has been in inventory for longer than threshold
                inventory_date = self.get_inventory_date(watch_data.model_number)
                if inventory_date:
                    days_in_inventory = (datetime.now() - inventory_date).days
                    if days_in_inventory > days_threshold:
                        # Apply additional discount based on age
                        age_factor = (days_in_inventory - days_threshold) / 30  # Monthly factor
                        age_discount = discount_percent * min(age_factor, 3)  # Cap at 3x the discount
                        optimal_price = optimal_price * (1 - age_discount)
        
        # Ensure price doesn't go below minimum margin
        minimum_price = base_price * 0.8  # 20% minimum margin
        optimal_price = max(optimal_price, minimum_price)
        
        # Round to nearest whole number
        return round(optimal_price)
    
    def get_base_price(self, watch_data):
        """Get the base price for a watch model"""
        model_key = f"{watch_data.brand}_{watch_data.model}"
        if model_key in self.base_prices:
            return self.base_prices[model_key]
        else:
            # Default to manufacturer suggested retail price from database
            msrp = self.db.query(
                "SELECT msrp FROM watch_details WHERE model_number = %s",
                (watch_data.model_number,)
            )
            return msrp.msrp if msrp else 10000  # Default fallback price
    
    def get_competitor_prices(self, model_number):
        """Get current prices from competitors for a specific watch model"""
        competitor_prices = {}
        
        # Query active prices from database
        prices = self.db.query(
            "SELECT competitor_id, price FROM prices WHERE watch_model_number = %s AND active = TRUE",
            (model_number,)
        )
        
        for price in prices:
            competitor_prices[price.competitor_id] = price.price
        
        return competitor_prices
    
    def get_inventory_date(self, model_number):
        """Get the date when the watch was added to inventory"""
        inventory = self.db.query(
            "SELECT created_at FROM inventory WHERE model_number = %s",
            (model_number,)
        )
        
        return inventory.created_at if inventory else None
```

## Database Schema SQL

```sql
-- Create watches table
CREATE TABLE watches (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    marketplace_type VARCHAR(50) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_scraped TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create prices table
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    watch_model_number VARCHAR(255) NOT NULL REFERENCES watches(id),
    price DECIMAL(10, 2) NOT NULL,
    competitor_id VARCHAR(255) NOT NULL,
    scraped_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT unique_active_price UNIQUE (watch_model_number, competitor_id, active)
);

-- Create reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    watch_model_number VARCHAR(255) NOT NULL REFERENCES watches(id),
    content TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    posted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create price_history table
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    watch_model_number VARCHAR(255) NOT NULL REFERENCES watches(id),
    price DECIMAL(10, 2) NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    blockchain_hash VARCHAR(255)
);

-- Create alerts table
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    watch_model_number VARCHAR(255) NOT NULL REFERENCES watches(id),
    alert_type VARCHAR(50) NOT NULL,
    alert_data JSONB NOT NULL,
    triggered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create indexes for performance
CREATE INDEX idx_watches_brand ON watches(brand);
CREATE INDEX idx_prices_watch_model ON prices(watch_model_number);
CREATE INDEX idx_prices_active ON prices(active);
CREATE INDEX idx_price_history_watch_model ON price_history(watch_model_number);
CREATE INDEX idx_price_history_recorded_at ON price_history(recorded_at);
CREATE INDEX idx_alerts_watch_model ON alerts(watch_model_number);
CREATE INDEX idx_alerts_resolved ON alerts(resolved);
```

## Configuration Files

### proxy_config.json
```json
{
  "proxy_providers": [
    {
      "name": "luminati",
      "api_key": "your_api_key_here",
      "endpoint": "https://luminati.io/api/get_proxies"
    },
    {
      "name": "smartproxy",
      "api_key": "your_api_key_here",
      "endpoint": "https://smartproxy.com/api/proxies"
    }
  ],
  "rotation_interval": 300,
  "max_failures": 3
}
```

### user_agents.json
```json
{
  "user_agents": [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>