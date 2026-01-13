# Threshold-Based Collective Decision-Making Under Noise

This project uses a threshold model (based on Robinson et al., 2011) to simulate how ant colonies pick a new nest. I used Monte Carlo simulations to see how things like noise and different ant thresholds change how accurate the colony is and how fast they make a decision.

You can find the full analysis and all my results in `report.pdf`.

## Project Summary

- Reproduces the threshold-based decision model proposed by Robinson et al. (2011)
- Systematically varies nest-quality noise and acceptance-threshold variability
- Measures effects on accuracy, decision time, and final nest choice
- Focuses on identifying the limits of the threshold rule under uncertainty

## Model at a Glance

- Agents: independent scouts
- Environment: home (−∞), poor (4), good (6)
- Decision rule: accept if perceived quality ≥ individual threshold
- Method: Monte Carlo simulation (500 agents per condition)

## Key Results

- Increasing perceptual noise reduces accuracy and drives behaviour toward random choice
- Decision times decrease with noise due to premature acceptance
- Threshold variability affects performance mainly at low and intermediate noise levels

Detailed figures and analysis are available in `report.pdf`.

## Running the Code

```bash
pip install numpy matplotlib pyyaml
python main.py

## Author

Efe Mirkan Guner  
MSc Artificial Intelligence & Adaptive Systems  
University of Sussex
