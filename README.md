# Luxury Watch Price Optimization System - Technical Implementation Document


## Table of Contents
1. Introduction
   - Purpose
   - System Overview
   - Document Scope

2. System Architecture
   - High-Level Architecture
   - Component Diagram
   - Data Flow

3. Database Schema Design
   - Entity Relationship Diagram
   - Table Definitions
   - Data Dictionary

4. Component Implementation
   - Web Scraping Module
   - Pricing Engine
   - API Services
   - Visualization Components
   - Alert System

5. Technical Considerations
   - Scalability
   - Reliability
   - Compliance

6. Implementation Roadmap
   - Phase 1 (Weeks 1-4)
   - Phase 2 (Weeks 5-8)
   - Phase 3 (Weeks 9-12)

7. Step-by-Step Implementation Guide
   - Environment Setup
   - Database Setup
   - Component Installation
   - Configuration
   - Testing

8. Appendices
   - Code Samples
   - Reference Materials



## 1. Introduction

### Purpose
This document provides a comprehensive technical implementation guide for the Luxury Watch Price Optimization System. It is designed for technical personnel who may not be familiar with the technology but need to implement the system step by step. The document outlines the system architecture, components, database schema, and provides detailed implementation instructions.

### System Overview
The Luxury Watch Price Optimization System is a sophisticated platform designed to automate the collection, analysis, and optimization of luxury watch pricing across various marketplaces. The system employs a microservices architecture with clear separation of concerns, ensuring scalability and maintainability. It uses web scraping to gather market data, applies pricing rules through a dedicated pricing engine, and provides visualization tools for monitoring and analysis.

### Document Scope
This implementation guide covers:
- Complete system architecture and design principles
- Database schema implementation with PostgreSQL
- Component-level implementation details
- Technical considerations for deployment
- A phased implementation roadmap
- Step-by-step setup and configuration instructions

The document is intended to guide technical teams through the entire implementation process, from initial setup to full deployment of all system components.



## High-Level Architecture
The Luxury Watch Price Optimization System employs a microservices architecture with clear separation of concerns, ensuring scalability and maintainability. The system is organized into five functional layers:

1. **Data Collection Layer** (Yellow components)
   - Web scraping services
   - API integration services
   - Data ingestion pipelines

2. **Data Storage Layer** (Green components)
   - PostgreSQL database
   - Redis cache for performance optimization

3. **Processing Layer** (Blue components)
   - ML model for price prediction
   - Rule-based pricing engine
   - Blockchain verification services

4. **API Layer** (Yellow components)
   - RESTful API services
   - Alert services

5. **Visualization Layer** (Purple components)
   - Dashboard UI
   - Interactive reports

## Component Diagram
The system architecture consists of the following key components:

- **Web Scraping Service**: Collects pricing data from various marketplaces
- **Price API**: Provides access to current and historical pricing data
- **User-Agent API**: Manages rotation of user agents for web scraping
- **Redis Cache**: Stores frequently accessed data for performance
- **PostgreSQL Database**: Primary data storage for all system entities
- **ML Model**: Processes pricing data to predict optimal pricing
- **Pricing Engine**: Applies business rules to determine final pricing
- **Blockchain Service**: Verifies and records price history for audit purposes
- **Alert System**: Monitors price changes and triggers notifications
- **Visualization Dashboard**: Provides interactive UI for data analysis

## Data Flow
Key interactions flow from top to bottom, with data flowing through the layers while maintaining loose coupling between components:

1. Web scraping services collect data from marketplaces
2. Data is stored in PostgreSQL database
3. Pricing engine processes data using business rules
4. ML model analyzes pricing trends
5. API services expose data to visualization layer
6. Alert system monitors for significant changes
7. Dashboard visualizes data for end-users



## Entity Relationship Diagram

The PostgreSQL database requires careful schema design to support the system's functionality. The database schema consists of the following key entities and their relationships:

### WATCHES Table
- **id** (string, PK): Unique identifier
- **name** (string): Watch model name
- **marketplace_type** (string): Source marketplace
- **brand** (string): Watch brand
- **description** (string): Product description
- **created_at** (datetime): Record creation timestamp
- **updated_at** (datetime): Record update timestamp
- **last_scraped** (datetime): Last data collection timestamp

### PRICES Table
- **id** (serial, PK): Unique identifier
- **watch_model_number** (string, FK): Reference to watch
- **price** (decimal): Current price
- **competitor_id** (string): Competitor identifier
- **scraped_at** (datetime): Price collection timestamp
- **active** (boolean): Whether price is current

### REVIEWS Table
- **id** (serial, PK): Unique identifier
- **watch_model_number** (string, FK): Reference to watch
- **content** (text): Review content
- **rating** (integer): Numerical rating
- **posted_at** (datetime): Review posting timestamp

### PRICE_HISTORY Table
- **id** (serial, PK): Unique identifier
- **watch_model_number** (string, FK): Reference to watch
- **price** (decimal): Historical price
- **recorded_at** (datetime): Timestamp
- **blockchain_hash** (string): Verification hash

### ALERTS Table
- **id** (serial, PK): Unique identifier
- **watch_model_number** (string, FK): Reference to watch
- **alert_type** (string): Type of alert
- **alert_data** (json): Alert details
- **triggered_at** (datetime): Alert timestamp
- **resolved** (boolean): Resolution status

## Relationships
- One WATCH can have many PRICES (one-to-many)
- One WATCH can have many REVIEWS (one-to-many)
- PRICES records history in PRICE_HISTORY (one-to-many)
- PRICES triggers ALERTS (one-to-many)

## Data Dictionary

### WATCHES Table
| Field | Type | Description |
|-------|------|-------------|
| id | string | Primary key, unique identifier for each watch |
| name | string | Full model name of the watch |
| marketplace_type | string | Source marketplace (e.g., "official", "gray_market") |
| brand | string | Brand name of the watch manufacturer |
| description | string | Full product description |
| created_at | datetime | When the record was first created |
| updated_at | datetime | When the record was last updated |
| last_scraped | datetime | When data was last collected for this watch |

### PRICES Table
| Field | Type | Description |
|-------|------|-------------|
| id | serial | Primary key, auto-incrementing identifier |
| watch_model_number | string | Foreign key to WATCHES table |
| price | decimal | Current price of the watch |
| competitor_id | string | Identifier of the competitor offering this price |
| scraped_at | datetime | When this price was collected |
| active | boolean | Whether this price is currently active |

### REVIEWS Table
| Field | Type | Description |
|-------|------|-------------|
| id | serial | Primary key, auto-incrementing identifier |
| watch_model_number | string | Foreign key to WATCHES table |
| content | text | Full text content of the review |
| rating | integer | Numerical rating (typically 1-5) |
| posted_at | datetime | When the review was posted |

### PRICE_HISTORY Table
| Field | Type | Description |
|-------|------|-------------|
| id | serial | Primary key, auto-incrementing identifier |
| watch_model_number | string | Foreign key to WATCHES table |
| price | decimal | Historical price point |
| recorded_at | datetime | When this price was recorded |
| blockchain_hash | string | Hash for blockchain verification |

### ALERTS Table
| Field | Type | Description |
|-------|------|-------------|
| id | serial | Primary key, auto-incrementing identifier |
| watch_model_number | string | Foreign key to WATCHES table |
| alert_type | string | Type of alert (e.g., "price_drop", "competitor_change") |
| alert_data | json | Detailed information about the alert |
| triggered_at | datetime | When the alert was triggered |
| resolved | boolean | Whether the alert has been resolved |



## Web Scraping Module

The web scraping module is responsible for collecting pricing data from various marketplaces. It implements the following features:

```python
def __init__(self):
    self.proxy_manager = ProxyManager()
    self.user_agent_rotator = UserAgentRotator()

async def scrape_marketplace(self, marketplace_url):
    proxy = await self.proxy_manager.get_proxy()
    headers = self.user_agent_rotator.get_random_user_agent()
    async with aiohttp.ClientSession() as session:
        async with session.get(marketplace_url,
                              proxy=proxy,
                              headers=headers) as response:
            return await response.text()
```

Key implementation considerations:
- Uses proxy rotation to avoid IP blocking
- Implements user-agent rotation for request anonymization
- Uses asynchronous HTTP requests for improved performance
- Respects robots.txt files for ethical scraping
- Implements rate limiting to avoid overloading target sites

## Pricing Engine

The pricing engine applies business rules to determine optimal pricing based on competitor data and internal strategies:

```python
class PricingEngine:
    def __init__(self):
        self.rules = {
            'rolex_daytona': {
                'competitor_a_discount': 50,
                'competitor_b_match_percent': 0.05,
                'aging_discount_days': 30,
                'aging_discount_percent': 0.02
            }
        }

    def calculate_optimal_price(self, watch_data):
        base_price = self.get_base_price(watch_data)
        competitor_prices = self.get_competitor_prices(watch_data.model_number)
        
        optimal_price = base_price
        
        # Apply pricing rules
        for rule in self.rules[watch_data.category]:
            optimal_price = self.apply_rule(optimal_price, rule, competitor_prices)
            
        return optimal_price
```

Key implementation considerations:
- Rule-based pricing strategy with configurable parameters
- Category-specific pricing rules
- Competitor price monitoring and matching capabilities
- Time-based discounting for aging inventory
- Extensible framework for adding new pricing strategies

## API Services

The system exposes several RESTful API endpoints:

1. **Watch API**
   - `GET /api/watches` - List all watches
   - `GET /api/watches/{id}` - Get watch details
   - `POST /api/watches` - Add new watch
   - `PUT /api/watches/{id}` - Update watch details

2. **Price API**
   - `GET /api/prices` - List all current prices
   - `GET /api/prices/history/{watch_id}` - Get price history
   - `POST /api/prices` - Add new price point

3. **Alert API**
   - `GET /api/alerts` - List all alerts
   - `GET /api/alerts/{id}` - Get alert details
   - `PUT /api/alerts/{id}/resolve` - Mark alert as resolved

Implementation using FastAPI:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/api/watches")
async def get_watches():
    # Implementation details
    return {"watches": watches_list}

@app.get("/api/watches/{watch_id}")
async def get_watch(watch_id: str):
    # Implementation details
    if watch not found:
        raise HTTPException(status_code=404, detail="Watch not found")
    return watch
```

## Visualization Components

The visualization layer includes:

1. **Market Dashboard**
   - Real-time price monitoring
   - Competitor analysis charts
   - Historical price trends

2. **Alerts Dashboard**
   - Active alerts display
   - Alert history and resolution tracking
   - Alert configuration interface

Implementation using Plotly Dash:
```python
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Luxury Watch Price Dashboard"),
    dcc.Graph(
        id='price-history-graph',
        figure=px.line(df, x="date", y="price", color="watch_model")
    )
])
```

## Alert System

The alert system monitors price changes and triggers notifications:

```python
class AlertSystem:
    def __init__(self, db_connection, notification_service):
        self.db = db_connection
        self.notification_service = notification_service
        
    def check_price_alerts(self):
        # Get latest prices
        latest_prices = self.db.query("SELECT * FROM prices WHERE active = TRUE")
        
        for price in latest_prices:
            # Get previous price
            previous_price = self.db.query(
                "SELECT price FROM price_history WHERE watch_model_number = %s ORDER BY recorded_at DESC LIMIT 1",
                (price.watch_model_number,)
            )
            
            # Check for significant price change
            if previous_price and abs(price.price - previous_price.price) / previous_price.price > 0.1:
                # Create alert
                alert_data = {
                    "previous_price": previous_price.price,
                    "current_price": price.price,
                    "percent_change": (price.price - previous_price.price) / previous_price.price * 100
                }
                
                self.db.execute(
                    "INSERT INTO alerts (watch_model_number, alert_type, alert_data, triggered_at, resolved) VALUES (%s, %s, %s, %s, %s)",
                    (price.watch_model_number, "price_change", json.dumps(alert_data), datetime.now(), False)
                )
                
                # Send notification
                self.notification_service.send_alert(
                    "Price change alert",
                    f"Price for {price.watch_model_number} changed by {alert_data['percent_change']}%"
                )
```

Key implementation considerations:
- Database-driven alert configuration
- Multiple alert types (price changes, competitor actions, etc.)
- Notification service integration (email, SMS, etc.)
- Alert resolution tracking



## Scalability

The Luxury Watch Price Optimization System is designed with scalability in mind to handle growing data volumes and user loads:

1. **Horizontal Scaling**
   - All components are containerized for easy deployment across multiple servers
   - Stateless services allow for simple load balancing
   - Database sharding strategy for large data volumes

2. **Performance Optimization**
   - Redis caching for frequently accessed data
   - Asynchronous processing for non-critical operations
   - Batch processing for large data operations

3. **Resource Management**
   - Auto-scaling configuration based on load metrics
   - Database connection pooling
   - Rate limiting for external API calls

## Reliability

To ensure system stability and data integrity:

1. **Retry Mechanisms**
   - Implement retry mechanisms with exponential backoff for external service calls
   - Circuit breaker pattern for failing dependencies
   - Dead letter queues for failed operations

2. **Monitoring**
   - Comprehensive health metrics for all system components
   - Automated alerting for system anomalies
   - Performance monitoring dashboards

3. **Backup Strategies**
   - Regular database backups
   - Redundant storage for critical data
   - Backup pricing strategies when primary methods fail

## Compliance

To ensure ethical and legal operation:

1. **Web Scraping Compliance**
   - Respect robots.txt files for all target websites
   - Implement rate limiting to avoid overloading target sites
   - User-agent identification following best practices

2. **Data Protection**
   - Secure storage of all collected data
   - Encryption for sensitive information
   - Compliance with relevant data protection regulations

3. **Audit Trails**
   - Comprehensive logging of all system operations
   - Blockchain verification for price history
   - Immutable records for compliance verification



The implementation of the Luxury Watch Price Optimization System is divided into three phases over a 12-week period:

## Phase 1 (Weeks 1-4)

### Week 1: Environment Setup
- Set up development, staging, and production environments
- Install required software dependencies
- Configure version control and CI/CD pipelines

### Week 2: Database Implementation
- Create PostgreSQL database schema
- Implement data models and migrations
- Set up data validation and integrity checks

### Week 3: Basic Web Scraping
- Implement proxy rotation mechanism
- Develop user-agent rotation functionality
- Create basic scraper for primary marketplace

### Week 4: Simple Pricing Engine
- Implement base pricing rules
- Develop competitor price tracking
- Create basic price calculation algorithms

## Phase 2 (Weeks 5-8)

### Week 5: Advanced Scraping Features
- Extend scraping to additional marketplaces
- Implement error handling and recovery
- Add data normalization and cleaning

### Week 6: ML/NLP Integration
- Implement sentiment analysis for reviews
- Develop price prediction models
- Create data preprocessing pipelines

### Week 7-8: API Development
- Implement RESTful API endpoints
- Create API documentation
- Develop authentication and authorization
- Implement rate limiting and security measures

## Phase 3 (Weeks 9-12)

### Week 9-10: Blockchain Integration
- Implement price verification using blockchain
- Create immutable audit trails
- Develop smart contracts for price history

### Week 11: Visualization Dashboard
- Create interactive price monitoring dashboard
- Implement competitor analysis visualizations
- Develop historical trend analysis tools

### Week 12: Alert System
- Implement price change detection
- Develop notification services
- Create alert management interface



This section provides detailed instructions for implementing the Luxury Watch Price Optimization System from scratch. Each step is designed to be followed sequentially by technical personnel who may not be familiar with the specific technologies used.

## Step 1: Environment Setup

### Prerequisites
- Linux-based server (Ubuntu 20.04 LTS or newer recommended)
- Python 3.9+ installed
- PostgreSQL 13+ installed
- Redis 6+ installed
- Docker and Docker Compose installed

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-organization/luxury-watch-price-optimization.git
   cd luxury-watch-price-optimization
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your specific configuration
   ```

5. **Start supporting services with Docker**
   ```bash
   docker-compose up -d redis postgres
   ```

## Step 2: Database Setup

1. **Create database and user**
   ```bash
   sudo -u postgres psql
   ```
   
   ```sql
   CREATE DATABASE watch_price_optimization;
   CREATE USER watch_admin WITH ENCRYPTED PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE watch_price_optimization TO watch_admin;
   \q
   ```

2. **Run database migrations**
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

3. **Verify database schema**
   ```bash
   python manage.py db_verify
   ```

## Step 3: Web Scraping Module Setup

1. **Configure proxy settings**
   Edit `config/proxy_config.json`:
   ```json
   {
     "proxy_providers": [
       {
         "name": "provider1",
         "api_key": "your_api_key",
         "endpoint": "https://proxy-provider.com/api/v1/proxies"
       }
     ],
     "rotation_interval": 300,
     "max_failures": 3
   }
   ```

2. **Configure user agent rotation**
   Edit `config/user_agents.json` with a list of user agents or use the default list.

3. **Set up marketplace configurations**
   Edit `config/marketplaces.json`:
   ```json
   {
     "marketplaces": [
       {
         "name": "Luxury Watch Retailer",
         "base_url": "https://example-retailer.com",
         "product_pattern": "/watches/{brand}/{model}",
         "selectors": {
           "price": ".product-price",
           "name": ".product-title",
           "description": ".product-description"
         },
         "rate_limit": 10
       }
     ]
   }
   ```

4. **Test scraper functionality**
   ```bash
   python -m scripts.test_scraper
   ```

## Step 4: Pricing Engine Configuration

1. **Define pricing rules**
   Edit `config/pricing_rules.json`:
   ```json
   {
     "rolex_daytona": {
       "competitor_a_discount": 50,
       "competitor_b_match_percent": 0.05,
       "aging_discount_days": 30,
       "aging_discount_percent": 0.02
     },
     "patek_philippe_nautilus": {
       "competitor_a_discount": 25,
       "competitor_b_match_percent": 0.03,
       "aging_discount_days": 45,
       "aging_discount_percent": 0.01
     }
   }
   ```

2. **Configure base price sources**
   Edit `config/base_prices.json` with manufacturer suggested retail prices.

3. **Test pricing engine**
   ```bash
   python -m scripts.test_pricing_engine
   ```

## Step 5: API Service Deployment

1. **Configure API settings**
   Edit `config/api_config.json`:
   ```json
   {
     "host": "0.0.0.0",
     "port": 8000,
     "debug": false,
     "rate_limit": {
       "default": "100/hour",
       "registered_users": "1000/hour"
     },
     "auth": {
       "jwt_secret": "your_secure_jwt_secret",
       "token_expiry": 86400
     }
   }
   ```

2. **Start API service**
   ```bash
   python -m api.main
   ```

3. **Verify API endpoints**
   ```bash
   curl http://localhost:8000/api/health
   ```

## Step 6: Visualization Dashboard Setup

1. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure dashboard settings**
   Edit `frontend/src/config.js` with API endpoint and other settings.

3. **Build frontend assets**
   ```bash
   npm run build
   ```

4. **Deploy frontend**
   ```bash
   cp -r build/* /var/www/html/
   ```

5. **Configure web server (Nginx example)**
   ```bash
   sudo cp config/nginx/watch-dashboard.conf /etc/nginx/sites-available/
   sudo ln -s /etc/nginx/sites-available/watch-dashboard.conf /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Step 7: Alert System Configuration

1. **Configure notification services**
   Edit `config/notifications.json`:
   ```json
   {
     "email": {
       "smtp_server": "smtp.example.com",
       "smtp_port": 587,
       "username": "alerts@your-company.com",
       "password": "your_secure_password",
       "from_address": "alerts@your-company.com"
     },
     "sms": {
       "provider": "twilio",
       "account_sid": "your_account_sid",
       "auth_token": "your_auth_token",
       "from_number": "+1234567890"
     }
   }
   ```

2. **Configure alert rules**
   Edit `config/alert_rules.json`:
   ```json
   {
     "price_change": {
       "threshold_percent": 10,
       "notification_channels": ["email", "sms"]
     },
     "competitor_price_drop": {
       "threshold_percent": 5,
       "notification_channels": ["email"]
     }
   }
   ```

3. **Start alert service**
   ```bash
   python -m services.alert_service
   ```

## Step 8: System Integration and Testing

1. **Run integration tests**
   ```bash
   python -m pytest tests/integration/
   ```

2. **Start all services**
   ```bash
   ./scripts/start_all_services.sh
   ```

3. **Monitor system health**
   ```bash
   ./scripts/check_system_health.sh
   ```

4. **Perform end-to-end test**
   ```bash
   python -m scripts.e2e_test
   ```

## Step 9: Production Deployment

1. **Set up production environment**
   - Configure production-grade database settings
   - Set up load balancing for API services
   - Configure SSL certificates for secure communication

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up monitoring and alerting**
   - Configure Prometheus for metrics collection
   - Set up Grafana dashboards for visualization
   - Configure alerting for system health issues

4. **Implement backup strategy**
   - Set up automated database backups
   - Configure backup rotation and retention policies
   - Test backup restoration procedures



This section contains the key visual diagrams and illustrations for the Luxury Watch Price Optimization System implementation. These visuals will help clarify the system architecture, data flow, and component relationships for technical personnel who may not be familiar with the technology.

## System Architecture Diagram

The following diagram illustrates the five-layer architecture of the Luxury Watch Price Optimization System, with colors indicating functional grouping:

- Yellow indicates API services and alerts
- Purple highlights visualization components
- Blue represents processing components
- Green shows data storage components
- Red indicates external data sources

![System Architecture Diagram](/home/ubuntu/pdf_screenshots/page5_architecture_diagram.png)

## Database Entity Relationship Diagram

The entity relationship diagram shows the database structure with the following key relationships:

- Lines with crowfeet (||--o{) indicate one-to-many relationships (e.g., one WATCH can have many PRICES)
- PK indicates Primary Keys, FK indicates Foreign Keys
- PRICE_HISTORY maintains a separate table from PRICES to support blockchain verification and audit trails

## Component Interaction Flow

The component interaction flow diagram demonstrates how data moves through the system:

1. Web scraping services collect data from marketplaces
2. Data is stored in PostgreSQL database
3. Pricing engine processes data using business rules
4. ML model analyzes pricing trends
5. API services expose data to visualization layer
6. Alert system monitors for significant changes
7. Dashboard visualizes data for end-users

## Implementation Phases Visual Timeline

The implementation roadmap is divided into three phases over a 12-week period:

### Phase 1 (Weeks 1-4)
- Basic web scraping infrastructure
- Database schema implementation
- Simple pricing engine

### Phase 2 (Weeks 5-8)
- Advanced scraping features
- ML/NLP integration
- API development

### Phase 3 (Weeks 9-12)
- Blockchain integration
- Visualization dashboard
- Alert system implementation



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
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
  ]
}
```

### marketplaces.json
```json
{
  "marketplaces": [
    {
      "name": "LuxuryWatchRetailer",
      "base_url": "https://www.luxurywatchretailer.com",
      "product_pattern": "/watches/{brand}/{model}",
      "selectors": {
        "price": ".product-price",
        "name": ".product-title",
        "description": ".product-description"
      },
      "rate_limit": 10
    },
    {
      "name": "WatchExchange",
      "base_url": "https://www.watchexchange.com",
      "product_pattern": "/products/{brand}-{model}",
      "selectors": {
        "price": "#product-price",
        "name": "h1.product-name",
        "description": "div.product-details"
      },
      "rate_limit": 5
    }
  ]
}
```

### pricing_rules.json
```json
{
  "rolex_daytona": {
    "competitor_a_discount": 50,
    "competitor_b_match_percent": 0.05,
    "aging_discount_days": 30,
    "aging_discount_percent": 0.02
  },
  "patek_philippe_nautilus": {
    "competitor_a_discount": 25,
    "competitor_b_match_percent": 0.03,
    "aging_discount_days": 45,
    "aging_discount_percent": 0.01
  },
  "audemars_piguet_royal_oak": {
    "competitor_a_discount": 75,
    "competitor_b_match_percent": 0.04,
    "aging_discount_days": 60,
    "aging_discount_percent": 0.015
  }
}
```


