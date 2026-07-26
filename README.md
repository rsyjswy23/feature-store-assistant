# feature-store-assistant

uv add openai python-dotenv pandas numpy scikit-learn tqdm minsearch flask psycopg2-binary pydantic jupyter

## Retrieval Evaluation

Summary of Your Retrieval Evaluation:
Metric	Baseline	Optimized	Improvement
Hit Rate	98.9%	98.9%	0% (already optimal)
MRR	86.1%	89.8%	+3.7%

Optimized Boost Parameters:
python
boost = {
    'feature_name': 2.07,
    'feature_group': 0.18,
    'feature_description': 2.70,
    'computation_logic': 1.91,
    'models_using_feature': 1.17,
    'data_source': 1.30,
    'serving_store': 0.77,
    'update_frequency': 0.58,
}

## RAG Evaluation
LLM AS A JUDGE: use both models with 200 samples:

gpt-4o-mini:
relevance
RELEVANT           0.99
PARTLY_RELEVANT    0.01
NON_RELEVANT       0.00

gpt-4o: 



sample questions: 
3,What is the computation logic behind the avg_order_value_7d feature?
5,"What data source is used to derive the avg_order_value_30d feature, and what is its status?"
8,"How is the 'product_views_30d' feature computed, and what is the time frame considered?"
9,What does the avg_rating_7d feature represent in the context of product quality?
12,How is the 'search_count_7d' feature calculated for each customer?
16,What is the return rate over the last 14 days for a specific product?
19,At what frequency is the inventory stock data updated?
25,What types of models utilize the click_rate_14d feature in their computations?

"What is the difference between the features 'search_to_purchase_conversion_7d' and 'click_rate_7d' measure for customers?"

