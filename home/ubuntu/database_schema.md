# 3. Database Schema Design

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
