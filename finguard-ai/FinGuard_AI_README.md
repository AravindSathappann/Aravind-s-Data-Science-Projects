# FinGuard AI

FinGuard AI is a Deepgram-powered FinTech call-risk analysis application that analyzes financial customer-support conversations for fraud, compliance, and escalation risk.

Users can either paste a support-call transcript or upload an audio file. Uploaded audio is transcribed using Deepgram Speech-to-Text, then processed through a machine-learning classifier, custom FinTech risk features, RAG-based policy retrieval, and a LangGraph decision workflow.

Results are returned through a Flask web application with an explainable risk classification, relevant policy context, and recommended routing action.

---

## What the App Does

FinGuard AI classifies financial support conversations into four categories:

- Fraud Risk
- Compliance Risk
- Escalation Risk
- Normal Support

The system also retrieves relevant financial-policy context and generates an explainable recommended action.

Example:

```text
Final Prediction: Fraud Risk

Retrieved Policy:
Unauthorized Transaction Dispute Policy

Recommended Action:
Route to fraud specialist, block compromised card if needed,
and open a dispute case.
```

---

## Model Performance

The risk-classification model was trained and evaluated on a balanced synthetic dataset of **400 financial support-call transcripts** across four categories.

### Dataset

```text
Total transcripts: 400

Fraud Risk:          100
Compliance Risk:     100
Escalation Risk:     100
Normal Support:      100
```

The dataset contains clear, ambiguous, and mixed-risk conversations to reduce reliance on simple keyword matching.

Examples include conversations where:

- Fraud terminology appears in a normal-support request
- Unauthorized transactions appear in an escalation case
- Compliance and verification terminology appears in legitimate support requests
- Multiple risk signals occur within the same conversation

### Evaluation

The dataset was divided into:

```text
Training set: 300 transcripts
Held-out test set: 100 transcripts
```

The model achieved:

```text
Accuracy:       95%
Macro F1:       0.95
Weighted F1:    0.95
```

Per-class results:

| Risk Category | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Compliance Risk | 0.96 | 1.00 | 0.98 |
| Escalation Risk | 0.96 | 0.92 | 0.94 |
| Fraud Risk | 0.89 | 0.96 | 0.92 |
| Normal Support | 1.00 | 0.92 | 0.96 |

The fraud-risk classifier achieved **96% recall**, successfully identifying most fraud cases in the held-out evaluation set.

> These metrics are based on synthetic financial-support conversations and should be interpreted as project-level benchmark results rather than production banking performance.

---

## Tech Stack

- Python
- Deepgram API
- Flask
- LangGraph
- Scikit-learn
- Pandas
- NumPy
- TF-IDF
- Logistic Regression
- RAG
- HTML
- CSS
- JavaScript

---

## Project Architecture

```text
Audio File or Transcript
        ↓
Deepgram Speech-to-Text
        ↓
Transcript
        ↓
ML Risk Classification
        ↓
FinTech Feature Extraction
        ↓
RAG Policy Retrieval
        ↓
LangGraph Decision Workflow
        ↓
Explainable Routing Recommendation
        ↓
Flask Web Application
```

---

## Machine-Learning Pipeline

FinGuard AI combines text-based machine learning with manually engineered FinTech risk features.

The classifier uses:

- TF-IDF text representations
- Logistic Regression
- Fraud-related language
- Dollar-amount signals
- Urgency language
- Escalation phrases
- Verification/compliance terminology
- Speaker-turn patterns

The model predicts one of the four support-call risk categories and passes the result into the downstream RAG and LangGraph workflow.

---

## RAG Policy Retrieval

FinGuard AI uses a lightweight Retrieval-Augmented Generation workflow to retrieve relevant financial-policy context.

Current policy domains include:

- Unauthorized transaction disputes
- Compliance and identity verification
- Customer-service escalation
- Normal support procedures

The application returns:

```text
Retrieved Policy
Policy Similarity Score
Recommended Action
```

This allows the final classification to include context explaining why a particular action should be taken.

---

## LangGraph Workflow

LangGraph coordinates the application's decision pipeline.

The workflow combines:

1. ML risk prediction
2. Manual FinTech risk features
3. Policy retrieval
4. Risk-signal validation
5. Final classification
6. Recommended routing action

This provides an explainable decision rather than returning only a classification label.

---

## Project Structure

```text
finguard-ai/
├── api/
│   ├── flask_app.py
│   └── templates/
│       └── index.html
│
├── data/
│   ├── labeled_calls.csv
│   ├── labeled_calls_expanded.csv
│   ├── policies/
│   │   ├── fraud_dispute_policy.txt
│   │   ├── compliance_policy.txt
│   │   ├── escalation_policy.txt
│   │   └── normal_support_policy.txt
│   └── sample_audio/
│
├── models/
│   └── risk_classifier.joblib
│
├── scripts/
│   ├── generate_dataset.py
│   ├── train_model.py
│   ├── predict_call.py
│   ├── test_rag.py
│   ├── run_langgraph_workflow.py
│   ├── test_flask_api.py
│   ├── test_deepgram.py
│   └── transcribe_and_analyze.py
│
├── src/
│   ├── __init__.py
│   ├── risk_model.py
│   ├── feature_engineering.py
│   ├── rag_retriever.py
│   ├── langgraph_workflow.py
│   └── deepgram_client.py
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Prerequisites

Before running the application, install or have access to:

- Python 3.9+
- pip
- Git
- Deepgram API key for audio transcription

A Deepgram API key is not required when analyzing pasted transcripts.

---

## Setup

### 1. Clone the repository

```bash
git clone <your-github-repo-link>
cd finguard-ai
```

If the project already exists locally:

```bash
cd /Users/Aravind/Desktop/finguard-ai
```

---

### 2. Create a virtual environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

When activated, the terminal should display:

```text
(.venv)
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Core dependencies include:

```text
pandas
numpy
scikit-learn
joblib
python-dotenv
flask
requests
langgraph
```

---

## Deepgram API Setup

The Deepgram API is required only for audio transcription.

Create a `.env` file:

```bash
touch .env
```

Add:

```text
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

Do not include quotation marks around the API key.

Make sure `.env` is ignored by Git:

```text
.env
.venv/
__pycache__/
*.pyc
```

Never commit API credentials to GitHub.

---

## Generate the Dataset

FinGuard AI includes a synthetic dataset-generation script that creates **400 balanced and varied financial support conversations**.

Run:

```bash
python3 scripts/generate_dataset.py
```

Expected output:

```text
New harder dataset created!
Total transcripts: 400

Fraud Risk          100
Compliance Risk     100
Escalation Risk     100
Normal Support      100
```

The generated dataset is saved to:

```text
data/labeled_calls_expanded.csv
```

---

## Train the ML Model

Run:

```bash
python3 scripts/train_model.py
```

The training pipeline:

1. Loads the labeled transcript dataset
2. Performs a stratified train/test split
3. Extracts TF-IDF and manual risk features
4. Trains the classification model
5. Evaluates the model on held-out data
6. Saves the trained model

Expected output:

```text
Accuracy: 0.95

Classification Report:
...

Model saved to models/risk_classifier.joblib
```

The trained model is saved to:

```text
models/risk_classifier.joblib
```

---

## Start the Flask App

Run:

```bash
python3 api/flask_app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

The FinGuard AI browser interface should appear.

---

## Using the Application

### Option 1: Analyze a Transcript

Paste a support-call transcript into the browser interface.

Example:

```text
Customer: I did not authorize this $950 transaction.
Customer: My card may have been stolen and I need this fixed today.
Agent: I can help you open a dispute case.
Customer: I am frustrated because I already called twice.
```

Click:

```text
Analyze Transcript
```

FinGuard AI returns:

- Final risk prediction
- ML prediction
- Decision explanation
- Retrieved policy
- Recommended action
- Policy similarity score
- Manual risk features

---

### Option 2: Analyze Audio

Upload a supported audio file:

```text
.wav
.mp3
.m4a
```

Click:

```text
Upload Audio + Analyze
```

The system will:

1. Upload the audio to Deepgram
2. Generate a transcript
3. Extract FinTech risk features
4. Run ML classification
5. Retrieve relevant policy context
6. Execute the LangGraph workflow
7. Return an explainable recommendation

---

## Testing

### Train the model

```bash
python3 scripts/train_model.py
```

### Test risk classification

```bash
python3 scripts/predict_call.py
```

### Test RAG policy retrieval

```bash
python3 scripts/test_rag.py
```

### Test LangGraph workflow

```bash
python3 scripts/run_langgraph_workflow.py
```

### Test Deepgram

```bash
python3 scripts/test_deepgram.py
```

### Test full audio pipeline

```bash
python3 scripts/transcribe_and_analyze.py \
--audio data/sample_audio/fraud_call.wav
```

For `.m4a`:

```bash
python3 scripts/transcribe_and_analyze.py \
--audio data/sample_audio/fraud_call.m4a
```

For `.mp3`:

```bash
python3 scripts/transcribe_and_analyze.py \
--audio data/sample_audio/fraud_call.mp3
```

---

## Flask API

### `GET /`

Loads the FinGuard AI browser application.

---

### `GET /health`

Checks whether the API is running.

```text
http://127.0.0.1:5000/health
```

Example response:

```json
{
  "status": "healthy",
  "service": "FinGuard AI"
}
```

---

### `POST /analyze`

Analyzes a transcript.

```bash
curl -X POST http://127.0.0.1:5000/analyze \
-H "Content-Type: application/json" \
-d '{
  "transcript": "Customer: I did not authorize this 950 dollar transaction. My card may have been stolen."
}'
```

---

### `POST /analyze-audio`

Uploads audio, transcribes it with Deepgram, and analyzes the resulting transcript.

```bash
curl -X POST http://127.0.0.1:5000/analyze-audio \
-F "audio=@data/sample_audio/fraud_call.wav"
```

---

## Example Full-Pipeline Output

```text
Deepgram Transcript:
I did not authorize this 950 dollar transaction.
My card may have been stolen.

Deepgram Confidence:
0.98

Final Prediction:
Fraud Risk

ML Prediction:
Fraud Risk

Decision Reason:
ML prediction confirmed by multiple fraud-risk signals.

Retrieved Policy:
Unauthorized Transaction Dispute Policy

Recommended Action:
Route to fraud specialist, block compromised card if needed,
and open a dispute case.

Policy Similarity Score:
0.6019
```

---

## Troubleshooting

### `No such file or directory`

Make sure the terminal is inside the project directory:

```bash
cd /Users/Aravind/Desktop/finguard-ai
```

---

### `Model not found`

Train the model:

```bash
python3 scripts/train_model.py
```

---

### `Missing DEEPGRAM_API_KEY`

Verify `.env` contains:

```text
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

Then restart Flask:

```bash
python3 api/flask_app.py
```

---

### Audio file not found

Check available audio files:

```bash
ls data/sample_audio
```

Then pass the correct filename to the transcription script.

---

### Browser displays HTML instead of the application

Do not open `index.html` directly.

Start Flask:

```bash
python3 api/flask_app.py
```

Then navigate to:

```text
http://127.0.0.1:5000/
```

---

## Limitations

FinGuard AI is a portfolio and research-oriented prototype.

The current classifier is evaluated on **synthetically generated financial support conversations**, not production customer-service data. Although the classifier achieved **95% accuracy and 0.95 macro F1 on a 100-transcript held-out test set**, these results should not be interpreted as production banking performance.

The included financial-policy documents are example documents created for the project and are not official policies from a financial institution.

---

## Future Improvements

- Evaluate on real or independently sourced financial-support conversations
- Increase dataset size and linguistic diversity
- Add cross-validation and external holdout evaluation
- Add SHAP-based model explanations
- Add speaker diarization
- Add sentiment analysis
- Add PostgreSQL or MongoDB for persistent call storage
- Add Kafka for real-time risk-event streaming
- Add Apache Spark for large-scale transcript analytics
- Add authentication and role-based access
- Add model and API monitoring
- Deploy the Flask application to a cloud platform
- Replace TF-IDF retrieval with embedding-based semantic search
- Expand the policy knowledge base

---

## Resume Summary

**FinGuard AI | Python, Deepgram API, LangGraph, RAG, Flask, Scikit-learn**

- Built a Deepgram-powered FinTech call-risk application that transcribes support audio and classifies conversations across fraud, compliance, escalation, and normal-support categories
- Trained and evaluated a 4-class risk classifier on **400 synthetic support transcripts**, achieving **95% held-out accuracy and 0.95 macro F1**
- Implemented a LangGraph and RAG workflow using transcript-level risk features to retrieve financial-policy context and generate explainable routing recommendations through Flask

---

## Author

Created by Aravind Sathappan.