import os
import uuid
from flask import Flask, render_template_string, request, jsonify
from rag import rag
import db

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Feature Store Assistant</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 1000px;
            width: 100%;
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        h1 {
            color: #1a1a2e;
            font-size: 28px;
            margin-bottom: 8px;
        }
        .subtitle {
            color: #666;
            font-size: 14px;
            margin-bottom: 24px;
        }
        .input-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 20px;
        }
        .input-group textarea {
            width: 100%;
            padding: 16px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.3s;
            outline: none;
            resize: vertical;
            min-height: 70px;
            max-height: 150px;
            line-height: 1.5;
        }
        .input-group textarea:focus {
            border-color: #4a6cf7;
        }
        .input-group textarea::placeholder {
            color: #aaa;
        }
        .input-group button {
            align-self: flex-end;
            padding: 12px 40px;
            background: #4a6cf7;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s, transform 0.1s;
            min-width: 120px;
        }
        .input-group button:hover {
            background: #3a5cd9;
        }
        .input-group button:active {
            transform: scale(0.97);
        }
        .input-group button:disabled {
            background: #aaa;
            cursor: not-allowed;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 16px;
        }
        .loading::after {
            content: '...';
            animation: dots 1.5s steps(4) infinite;
        }
        @keyframes dots {
            0% { content: ''; }
            25% { content: '.'; }
            50% { content: '..'; }
            75% { content: '...'; }
        }
        .answer-box {
            background: #f8f9fc;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            border-left: 4px solid #4a6cf7;
        }
        .answer-box h3 {
            color: #1a1a2e;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #666;
            margin-bottom: 10px;
        }
        .answer-box .answer-text {
            font-size: 16px;
            line-height: 1.7;
            color: #1a1a2e;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin: 16px 0 20px 0;
        }
        .metric-card {
            background: #f8f9fc;
            border-radius: 10px;
            padding: 14px 16px;
            text-align: center;
            border: 1px solid #eee;
        }
        .metric-card .label {
            font-size: 11px;
            text-transform: uppercase;
            color: #888;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        .metric-card .value {
            font-size: 18px;
            font-weight: 700;
            color: #1a1a2e;
            margin-top: 4px;
        }
        .metric-card .value.green { color: #22c55e; }
        .metric-card .value.blue { color: #4a6cf7; }
        .metric-card .value.orange { color: #f59e0b; }
        .metric-card .value.red { color: #ef4444; }
        .metric-card .value.purple { color: #8b5cf6; }
        .feedback-section {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #eee;
            flex-wrap: wrap;
        }
        .feedback-section .label {
            font-size: 14px;
            color: #666;
            font-weight: 500;
        }
        .feedback-btn {
            padding: 10px 28px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
            font-weight: 600;
        }
        .feedback-btn.positive:hover {
            border-color: #22c55e;
            background: #f0fdf4;
            color: #22c55e;
        }
        .feedback-btn.negative:hover {
            border-color: #ef4444;
            background: #fef2f2;
            color: #ef4444;
        }
        .feedback-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .feedback-btn.selected-positive {
            border-color: #22c55e;
            background: #f0fdf4;
            color: #22c55e;
        }
        .feedback-btn.selected-negative {
            border-color: #ef4444;
            background: #fef2f2;
            color: #ef4444;
        }
        .feedback-message {
            margin-left: 12px;
            font-size: 14px;
            color: #22c55e;
            font-weight: 500;
        }
        .error {
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 16px 20px;
            border-radius: 10px;
            margin: 16px 0;
            color: #dc2626;
        }
        .relevance-badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        .relevance-badge.RELEVANT { background: #dcfce7; color: #16a34a; }
        .relevance-badge.PARTLY_RELEVANT { background: #fef3c7; color: #d97706; }
        .relevance-badge.NON_RELEVANT { background: #fef2f2; color: #dc2626; }
        .relevance-badge.UNKNOWN { background: #f3f4f6; color: #6b7280; }
        .explanation-box {
            background: #f8f9fc;
            border-radius: 10px;
            padding: 16px 18px;
            margin: 12px 0 16px 0;
            border: 1px solid #eee;
        }
        .explanation-box .label {
            font-size: 12px;
            color: #888;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        .explanation-box .text {
            font-size: 14px;
            color: #444;
            margin-top: 4px;
            line-height: 1.6;
        }
        .conversation-id {
            font-size: 12px;
            color: #999;
            margin-top: 8px;
            word-break: break-all;
        }
        @media (max-width: 600px) {
            .container { padding: 16px; margin: 10px 0; }
            .input-group button { width: 100%; align-self: stretch; }
            .metrics { grid-template-columns: 1fr 1fr; }
            .feedback-section { flex-direction: column; align-items: stretch; }
            .feedback-btn { text-align: center; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Feature Store Assistant</h1>
        <p class="subtitle">Ask questions about features, computation logic, data sources, and ML models</p>

        <!-- Question Input -->
        <div class="input-group">
            <textarea id="questionInput" rows="2" placeholder="e.g., What features are used in the recommendation model?"></textarea>
            <button id="askBtn" onclick="askQuestion()">Ask</button>
        </div>

        <!-- Loading -->
        <div id="loading" class="loading" style="display:none;">Processing your question</div>

        <!-- Error -->
        <div id="error" class="error" style="display:none;"></div>

        <!-- Answer Section -->
        <div id="answerSection" style="display:none;">
            <div class="answer-box">
                <h3>📝 Answer</h3>
                <div id="answerText" class="answer-text"></div>
            </div>

            <!-- Metrics -->
            <div class="metrics">
                <div class="metric-card">
                    <div class="label">⏱ Response Time</div>
                    <div id="responseTime" class="value blue">-</div>
                </div>
                <div class="metric-card">
                    <div class="label">📥 Input Tokens</div>
                    <div id="inputTokens" class="value orange">-</div>
                </div>
                <div class="metric-card">
                    <div class="label">📤 Output Tokens</div>
                    <div id="outputTokens" class="value purple">-</div>
                </div>
                <div class="metric-card">
                    <div class="label">💰 Cost</div>
                    <div id="cost" class="value green">-</div>
                </div>
                <div class="metric-card">
                    <div class="label">🧠 Model</div>
                    <div id="model" class="value" style="font-size:14px;">-</div>
                </div>
                <div class="metric-card">
                    <div class="label">📊 Relevance</div>
                    <div id="relevance" class="value" style="font-size:14px;">-</div>
                </div>
            </div>

            <!-- Explanation -->
            <div class="explanation-box">
                <div class="label">📋 LLM-as-Judge Explanation</div>
                <div id="explanation" class="text">No explanation provided.</div>
            </div>

            <!-- Conversation ID -->
            <div id="convId" class="conversation-id"></div>

            <!-- Feedback -->
            <div class="feedback-section">
                <span class="label">Was this answer helpful?</span>
                <button id="feedbackPos" class="feedback-btn positive" onclick="sendFeedback(1)">👍 +1</button>
                <button id="feedbackNeg" class="feedback-btn negative" onclick="sendFeedback(-1)">👎 -1</button>
                <span id="feedbackMessage" class="feedback-message"></span>
            </div>
        </div>
    </div>

    <script>
        let currentConversationId = null;

        // Auto-resize textarea
        document.getElementById('questionInput').addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });

        function askQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();

            if (!question) {
                showError('Please enter a question.');
                return;
            }

            // Reset UI
            document.getElementById('answerSection').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('askBtn').disabled = true;

            // Send request
            fetch('/question', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('askBtn').disabled = false;

                if (data.error) {
                    showError(data.error);
                    return;
                }

                // Store conversation ID
                currentConversationId = data.conversation_id;

                // Display answer
                document.getElementById('answerText').textContent = data.answer;
                document.getElementById('responseTime').textContent = data.response_time.toFixed(2) + 's';
                document.getElementById('inputTokens').textContent = data.prompt_tokens;
                document.getElementById('outputTokens').textContent = data.completion_tokens;
                document.getElementById('cost').textContent = '$' + data.openai_cost.toFixed(6);
                document.getElementById('model').textContent = data.model_used;

                // Relevance badge
                const relevance = data.relevance || 'UNKNOWN';
                const relEl = document.getElementById('relevance');
                relEl.textContent = relevance;
                relEl.className = 'value relevance-badge ' + relevance;

                // Explanation - LLM-as-Judge
                document.getElementById('explanation').textContent = data.relevance_explanation || 'No explanation provided.';
                document.getElementById('convId').textContent = 'Conversation ID: ' + data.conversation_id;

                // Reset feedback buttons
                document.getElementById('feedbackPos').className = 'feedback-btn positive';
                document.getElementById('feedbackNeg').className = 'feedback-btn negative';
                document.getElementById('feedbackPos').disabled = false;
                document.getElementById('feedbackNeg').disabled = false;
                document.getElementById('feedbackMessage').textContent = '';

                document.getElementById('answerSection').style.display = 'block';
            })
            .catch(err => {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('askBtn').disabled = false;
                showError('Network error: ' + err.message);
            });
        }

        function sendFeedback(value) {
            if (!currentConversationId) {
                document.getElementById('feedbackMessage').textContent = 'No conversation to rate.';
                return;
            }

            const posBtn = document.getElementById('feedbackPos');
            const negBtn = document.getElementById('feedbackNeg');
            posBtn.disabled = true;
            negBtn.disabled = true;

            fetch('/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    conversation_id: currentConversationId,
                    feedback: value
                })
            })
            .then(response => response.json())
            .then(data => {
                const msg = document.getElementById('feedbackMessage');
                msg.textContent = '✅ Thanks for your feedback!';

                if (value === 1) {
                    posBtn.className = 'feedback-btn positive selected-positive';
                } else {
                    negBtn.className = 'feedback-btn negative selected-negative';
                }
            })
            .catch(err => {
                document.getElementById('feedbackMessage').textContent = 'Error sending feedback.';
                posBtn.disabled = false;
                negBtn.disabled = false;
            });
        }

        function showError(msg) {
            const el = document.getElementById('error');
            el.textContent = msg;
            el.style.display = 'block';
        }

        // Ctrl+Enter support
        document.getElementById('questionInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                askQuestion();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/question', methods=['POST'])
def handle_question():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    conversation_id = str(uuid.uuid4())
    answer_data = rag(question)

    # Save conversation to database
    db.save_conversation(
        conversation_id=conversation_id,
        question=question,
        answer_data=answer_data,
    )

    # Return answer with metrics
    result = {
        'conversation_id': conversation_id,
        'question': question,
        'answer': answer_data['answer'],
        'response_time': answer_data['response_time'],
        'prompt_tokens': answer_data['prompt_tokens'],
        'completion_tokens': answer_data['completion_tokens'],
        'total_tokens': answer_data['total_tokens'],
        'openai_cost': answer_data['openai_cost'],
        'model_used': answer_data['model_used'],
        'relevance': answer_data['relevance'],
        'relevance_explanation': answer_data['relevance_explanation'],
    }

    return jsonify(result)

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    data = request.json
    conversation_id = data.get('conversation_id')
    feedback = data.get('feedback')

    if not conversation_id or feedback not in [1, -1]:
        return jsonify({'error': 'Invalid input'}), 400

    db.save_feedback(
        conversation_id=conversation_id,
        feedback=feedback,
    )

    return jsonify({'message': f'Feedback received: {feedback}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)