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


command 
uv run jupyter notebook

running the flask application
uv run python app.py
 
you test it with curl
```
URL=http://localhost:5000
QUESTION="'what features are used for personalized promotion campaigns?'"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"question": "'${QUESTION}'"}' \
    ${URL}/question
```

Example response:

```json
{
  "answer": "The features used for personalized promotion campaigns include:\n\n1. **purchase_count_30d_web** - Monthly purchase count indicator from the web channel.\n2. **purchase_count_14d_web** - Bi-weekly purchase count measurement from the web channel.\n3. **purchase_count_7d_web** - Short-term weekly purchase count metric from the web channel.\n4. **purchase_count_30d_mobile** - Monthly purchase count indicator from the mobile app channel.\n5. **purchase_count_14d_mobile** - Bi-weekly purchase count measurement from the mobile app channel.\n6. **purchase_count_7d_mobile** - Short-term weekly purchase count metric from the mobile app channel.",
  "conversation_id": "65f65c7e-6383-4753-b29f-530ad418e594",
  "question": "what features are used for personalized promotion campaigns?"
}
```

You can also send feedback:
## sending feedback to id
```
URL=http://localhost:5000
ID="65f65c7e-6383-4753-b29f-530ad418e594"

curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"conversation_id": "'"${ID}"'", "feedback": 1}' \
    ${URL}/feedback
```
you will receive acknowlegement:
```json
{
  "message": "Feedback received for conversation 65f65c7e-6383-4753-b29f-530ad418e594: 1"
}
```

alternatively, we can use [test.py](test.py) for testing.
```bash
uv run python test.py
```