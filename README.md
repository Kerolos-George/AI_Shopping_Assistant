# AI Shopping Assistant

A modular AI-powered shopping assistant that simulates personalized shopping experiences using Flask and DeepSeek API.

## Features

- **Buyer Profile Analysis**: Analyzes customer purchase history using AI
- **Smart Recommendations**: Suggests new product categories based on buying patterns  
- **Product Search**: Searches and ranks products from a mock catalog
- **Purchase Simulation**: Simulates purchases with transaction logging
- **Memory Management**: Supports both in-memory and file-based storage
- **RESTful API**: Complete REST API for all operations

## Architecture

The application follows a modular architecture with the following components:

- **Models**: Data structures (`BuyerProfile`)
- **Services**: 
  - `LLMService`: AI-powered analysis using DeepSeek API
  - `CatalogService`: Product catalog management
  - `MemoryService`: Buyer history storage
  - `PurchaseService`: Transaction handling
- **Flask App**: REST API endpoints

## Setup

### Prerequisites

- Python 3.8+
- DeepSeek API key

### Installation


**Option 1: Using requirements.txt**
```bash
pip install -r requirements.txt
```

### Configuration
Your DeepSeek API key is already configured in `config.py`. If you encounter OpenAI library issues, the app will run in fallback mode with mock responses.

### Running the Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Testing

Run the test examples:
```bash
python test_examples.py
```

## API Endpoints

### 1. Add Buyer Profile
```http
POST /buyer
Content-Type: application/json

{
  "user_id": "A123",
  "history": [
    {"product": "Bluetooth headphones", "category": "electronics", "price": 120},
    {"product": "Running shoes", "category": "sportswear", "price": 80}
  ]
}
```

### 2. Get Buyer Profile
```http
GET /buyer/{user_id}
```

### 3. Get AI Recommendations
```http
POST /analyze/{user_id}
```
Returns AI analysis, category recommendations, and ranked products.

### 4. Search Products
```http
GET /search/{category}?user_id={user_id}&max_results=3
```

### 5. Simulate Purchase
```http
POST /purchase
Content-Type: application/json

{
  "user_id": "A123",
  "product_id": 1
}
```

### 6. Get Transaction History
```http
GET /transactions/{user_id}
```

### 7. Get All Categories
```http
GET /categories
```

### 8. Get All Buyers
```http
GET /buyers
```

This will demonstrate all API functionality with example data.

## Configuration

Edit `config.py` to customize:

- **Memory Type**: `"memory"` (in-memory) or `"file"` (persistent storage)
- **File Path**: Location for buyer history storage
- **API Settings**: DeepSeek API configuration
- **Search Results**: Maximum products returned per search

## Example Usage Flow

1. **Add buyer profile** with purchase history
2. **Analyze buyer** to get AI-powered insights and recommendations
3. **Search products** in recommended categories (ranked by preferences)
4. **Simulate purchases** to update buyer history
5. **Track transactions** and updated buyer profiles

## Product Categories

The mock catalog includes:
- Electronics (headphones, phones, laptops, etc.)
- Sportswear (shoes, yoga mats, gym bags, etc.)
- Home Decor (lamps, art, pillows, etc.)
- Books (fiction, cookbooks, travel guides, etc.)
- Fashion (handbags, clothing, accessories, etc.)
- Kitchen (appliances, cookware, utensils, etc.)

## AI Features

- **Pattern Recognition**: Identifies buying patterns and preferences
- **Category Recommendations**: Suggests new product categories
- **Price Sensitivity Analysis**: Understands budget preferences
- **Natural Language Justification**: Explains recommendations conversationally

## Storage Options

- **In-Memory**: Fast, temporary storage (default for development)
- **File-Based**: Persistent JSON storage (recommended for production)

## Error Handling

The API includes comprehensive error handling for:
- Invalid requests
- Missing buyer profiles
- API failures
- Product not found scenarios
- Purchase simulation errors

## Development

The codebase is designed to be:
- **Modular**: Each service handles specific functionality
- **Extensible**: Easy to add new features or storage backends
- **Testable**: Clear separation of concerns
- **Configurable**: Environment-based configuration
