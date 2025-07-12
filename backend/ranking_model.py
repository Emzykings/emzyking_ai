"""
This module trains and uses a basic ML classifier to predict the best agent
for a given user prompt. It can be used to rank agents by confidence level.

Author: Emzyking AI
"""

import os
import joblib
from typing import List, Tuple
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Path to save trained model
MODEL_PATH = "models/agent_ranking_model.joblib"

def train_ranking_model(training_data: List[Tuple[str, str]]) -> None:
    """
    Train and save a text classifier to map prompts to agent labels.

    Args:
        training_data (List[Tuple[str, str]]): List of (prompt, agent_label) tuples.
    """
    prompts, labels = zip(*training_data)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
        ("clf", LinearSVC())
    ])

    X_train, X_test, y_train, y_test = train_test_split(prompts, labels, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("[Model Evaluation]\n", classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"[Model Saved] to {MODEL_PATH}")

def load_model() -> Pipeline:
    """
    Load the trained ranking model.

    Returns:
        Pipeline: Trained scikit-learn pipeline.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train it first.")
    return joblib.load(MODEL_PATH)

def score_prompt(prompt: str, agent_labels: List[str]) -> List[Tuple[str, float]]:
    """
    Scores a prompt against a list of agent labels using the trained model.

    Args:
        prompt (str): User input prompt.
        agent_labels (List[str]): Candidate agent labels.

    Returns:
        List[Tuple[str, float]]: List of (agent_label, confidence_score) sorted by confidence.
    """
    model = load_model()
    clf = model.named_steps["clf"]
    vectorized_prompt = model.named_steps["tfidf"].transform([prompt])

    # Use decision function for confidence scores if available
    if hasattr(clf, "decision_function"):
        scores = clf.decision_function(vectorized_prompt)
    else:
        raise ValueError("Classifier does not support confidence scoring.")

    confidence_scores = list(zip(clf.classes_, scores[0]))
    confidence_scores.sort(key=lambda x: x[1], reverse=True)
    return confidence_scores
