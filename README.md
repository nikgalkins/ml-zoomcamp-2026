# Machine Learning Zoomcamp 2026

My coursework for the [Machine Learning Zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) by DataTalks.Club.

## Progress

### Homework 1 — Introduction to Machine Learning

Topics:
- pandas and NumPy
- exploratory data analysis
- missing values
- matrix operations
- introduction to linear regression

[Open the notebook](01_intro_homework.ipynb)

## Background

I work with GIS, geospatial data, Python automation, and data engineering.  
I'm taking ML Zoomcamp to add applied machine learning and ML engineering skills to this stack.

### Homework 2 — Machine Learning for Regression

Topics:
- train / validation / test splitting
- missing-value imputation
- linear regression
- RMSE
- regularization
- model stability across random seeds

[Open the notebook](02_regression_homework.ipynb)

### Homework 4 — Evaluation

Topics:
- ROC AUC and numerical feature importance
- logistic regression with one-hot encoding
- precision, recall, and threshold selection
- F1 score
- five-fold cross-validation
- regularization tuning with fold-local preprocessing

[Open the notebook](04_evaluation_homework.ipynb)

Uses the official 2026 lead-scoring dataset with `converted` as the target.
The notebook includes saved outputs, precision/recall and F1 plots, and all six
calculated answers matched to the official choices.

To reproduce with Python 3.12, install the [pinned dependencies](04_evaluation_requirements.txt)
with `python -m pip install -r 04_evaluation_requirements.txt`, then open the notebook
from this directory and select **Restart Kernel and Run All**. The included
[dataset snapshot](course_lead_scoring_2026.csv) is checked by SHA-256; the notebook
downloads it from the official source if it is missing.

### Homework 5 — Deploying Machine Learning Models

Uses the unchanged official 2026 release with Python 3.11.15 and locked dependencies.
Model checksum, direct inference, and the FastAPI endpoints passed local verification.
Docker execution is blocked because Docker Desktop and its CLI are unavailable.

[Answers, commands, and verification evidence](05_deployment/answers.md)
