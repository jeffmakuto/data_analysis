# Quantitative Data Analysis Exercises

This project provides small synthetic datasets and a Python script to demonstrate common quantitative data-analysis workflows: descriptive statistics, hypothesis testing, correlation/regression, multiple regression, ANOVA, chi-square tests, and visualizations.

Files added
- `data/` contains CSV datasets:
	- `sales.csv` — numeric sales values for descriptive stats and histogram
	- `tutoring.csv` — scores for tutored vs non-tutored groups (t-test)
	- `advertising.csv` — ad spend, awareness, sales revenue (correlation & regression)
	- `houses.csv` — house prices and predictors (multiple regression)
	- `anova_scores.csv` — exam scores under 3 teaching methods (one-way ANOVA)
	- `chi_square.csv` — categorical variables for chi-square test
- `analysis.py` — main script that runs analyses and saves outputs to `outputs/`
- `requirements.txt` — Python packages needed

How to run (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python analysis.py
```

Outputs
- `outputs/` will contain:
	- PNG plots (histogram, boxplots, scatterplots, bar chart)
	- regression and model summaries as text files
	- `analysis_summary.json` with the numeric results

Brief interpretation guidance (what the script does)
- Descriptive statistics: mean, median, mode, variance, std. deviation for sales values and a histogram.
- T-test: compares mean exam scores for tutored vs non-tutored students using an independent t-test (Welch's t-test).
- Correlation & regression: computes Pearson correlation between advertising spend and sales revenue; fits a simple linear regression (sales ~ ad_spend) and writes coefficients and a summary.
- Multiple regression: predicts house price from size, bedrooms, and location dummies; saves regression summary.
- ANOVA: one-way ANOVA compares scores across three teaching methods; boxplot visualizes differences.
- Chi-square: tests association between service type and satisfaction; bar chart shows counts.

Next steps / suggestions
- Replace the synthetic CSVs with your real datasets (keep column names or adapt `analysis.py`).
- Add more diagnostics (residual plots, multicollinearity checks, transformations).
- If you want, I can run the script here (if you allow package installs) and attach the generated plots and summary.