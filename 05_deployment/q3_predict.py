"""Compute Homework 5 Q3 with the unchanged official pipeline."""

import json
import pickle
from pathlib import Path

lead = {
    "lead_source": "paid_ads",
    "industry": "technology",
    "employment_status": "employed",
    "location": "north_america",
    "number_of_courses_viewed": 2,
    "annual_income": 79276.0,
    "interaction_count": 4,
    "lead_score": 0.41,
}

with Path(__file__).with_name("pipeline.bin").open("rb") as model_file:
    pipeline = pickle.load(model_file)

probability = float(pipeline.predict_proba([lead])[0, 1])
print(json.dumps({"conversion_probability": probability, "rounded": f"{probability:.3f}"}))
