# 4. Component Implementation

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
