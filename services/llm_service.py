from openai import OpenAI
from typing import Dict, List, Any
import json
from config import Config
from models.buyer import BuyerProfile

class LLMService:
    """Service for handling LLM-based recommendations using DeepSeek API"""
    
    def __init__(self):
        try:
            self.client = OpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                base_url=Config.DEEPSEEK_BASE_URL
            )
        except Exception as e:
            print(f"Warning: Failed to initialize OpenAI client: {e}")
            print("Continuing with mock responses for testing...")
            self.client = None
    
    def analyze_buyer_history(self, buyer_profile: BuyerProfile) -> Dict[str, Any]:
        """Analyze buyer history and generate insights"""
        
        history_text = json.dumps(buyer_profile.history, indent=2)
        
        prompt = f"""
        Analyze this buyer's purchase history and provide insights:
        
        Buyer ID: {buyer_profile.user_id}
        Purchase History:
        {history_text}
        
        Please provide:
        1. Key buying patterns and preferences
        2. Preferred product categories
        3. Price sensitivity analysis
        4. Shopping frequency patterns
        
        Respond in JSON format with keys: patterns, preferred_categories, price_sensitivity, frequency_analysis
        """
        
        try:
            if self.client is None:
                # Fallback mock response when client is not available
                return {
                    "patterns": f"Based on {len(buyer_profile.history)} purchases, user shows consistent buying behavior",
                    "preferred_categories": buyer_profile.get_product_categories(),
                    "price_sensitivity": "moderate",
                    "frequency_analysis": "regular purchaser"
                }
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an expert shopping behavior analyst. Provide detailed insights in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse JSON response
            content = response.choices[0].message.content
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            except:
                # Fallback if JSON parsing fails
                return {
                    "patterns": content,
                    "preferred_categories": buyer_profile.get_product_categories(),
                    "price_sensitivity": "moderate",
                    "frequency_analysis": "regular"
                }
                
        except Exception as e:
            print(f"Error analyzing buyer history: {e}")
            return {
                "patterns": "Unable to analyze patterns",
                "preferred_categories": buyer_profile.get_product_categories(),
                "price_sensitivity": "moderate",
                "frequency_analysis": "regular"
            }
    
    def recommend_product_category(self, buyer_profile: BuyerProfile, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend a new product category based on analysis"""
        
        current_categories = buyer_profile.get_product_categories()
        price_range = buyer_profile.get_price_range()
        
        prompt = f"""
        Based on this buyer's analysis, recommend a new product category:
        
        Current preferred categories: {current_categories}
        Price range: ${price_range['min']:.2f} - ${price_range['max']:.2f} (avg: ${price_range['avg']:.2f})
        Buying patterns: {analysis.get('patterns', 'Not available')}
        Price sensitivity: {analysis.get('price_sensitivity', 'moderate')}
        
        Recommend a NEW product category (different from current ones) that would appeal to this buyer.
        Provide the recommendation in JSON format with keys: recommended_category, reasoning, suggested_price_range
        """
        
        try:
            if self.client is None:
                # Fallback mock response when client is not available
                current_categories = buyer_profile.get_product_categories()
                print(f"DEBUG: Current categories: {current_categories}")  # Debug output
                
                # Suggest a category not in their current list
                all_categories = ["electronics", "sportswear", "home_decor", "books", "fashion", "kitchen"]
                new_categories = [cat for cat in all_categories if cat not in current_categories]
                print(f"DEBUG: Available new categories: {new_categories}")  # Debug output
                
                recommended = new_categories[0]  # Default to books instead of home_decor
                
                return {
                    "recommended_category": recommended,
                    "reasoning": f"Based on your purchase history in {', '.join(current_categories)}, {recommended} would complement your lifestyle and expand your interests",
                    "suggested_price_range": price_range
                }
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a product recommendation expert. Suggest new product categories based on buyer behavior."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            except:
                return {
                    "recommended_category": "home_decor",
                    "reasoning": content,
                    "suggested_price_range": {"min": price_range['min'], "max": price_range['max']}
                }
                
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            # Use the same logic as the fallback above
            current_categories = buyer_profile.get_product_categories()
            all_categories = ["electronics", "sportswear", "home_decor", "books", "fashion", "kitchen"]
            new_categories = [cat for cat in all_categories if cat not in current_categories]
            recommended = new_categories[0] if new_categories else "books"
            
            return {
                "recommended_category": recommended,
                "reasoning": f"Based on your purchase history, {recommended} would be a great new category to explore",
                "suggested_price_range": {"min": price_range['min'], "max": price_range['max']}
            }
    
    def justify_recommendation(self, recommendation: Dict[str, Any], buyer_profile: BuyerProfile) -> str:
        """Provide natural language justification for the recommendation"""
        
        prompt = f"""
        Explain why this product recommendation makes sense for the buyer:
        
        Buyer ID: {buyer_profile.user_id}
        Recommended Category: {recommendation.get('recommended_category', 'N/A')}
        Reasoning: {recommendation.get('reasoning', 'N/A')}
        
        Provide a friendly, conversational explanation (2-3 sentences) of why this recommendation is perfect for this buyer.
        """
        
        try:
            if self.client is None:
                # Fallback mock response when client is not available
                return f"Based on your shopping history, {recommendation.get('recommended_category', 'this category')} seems like a great fit for your preferences and budget! It complements your existing purchases perfectly."
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a friendly shopping assistant explaining recommendations in a conversational tone."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating justification: {e}")
            return f"Based on your shopping history, {recommendation.get('recommended_category', 'this category')} seems like a great fit for your preferences and budget!" 