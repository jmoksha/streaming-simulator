# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Requirements (1 min)
```bash
pip install -r requirements.txt
```

### 2. Run Dashboard (immediate)
```bash
streamlit run app/streamlit_dashboard.py
```

**That's it!** The dashboard opens in your browser at `http://localhost:8501`

---

## First Steps in Dashboard

### Run Your First Simulation
1. **Sidebar** → Set parameters:
   - Users: 1000
   - Steps: 50
   - Keep defaults for now

2. **Main Tab** → Click **"🚀 Run Simulation"**

3. **View Results**:
   - Metrics appear instantly
   - Charts visualize user flow
   - Insights auto-generated

### Explore Transition Matrix
1. **"📊 Transition Analysis"** tab
2. See how users transition between states
3. Heatmap shows probability strengths

### Understand the Theory
1. **"🔬 Theory & Properties"** tab
2. Read Markov chain fundamentals
3. Check if model is ergodic

---

## Key Metrics to Watch

| Metric | What It Means | Good Range |
|--------|--------------|-----------|
| **Conversion Rate** | % free users → paid | >20% |
| **Churn Rate** | % users who leave | <30% |
| **Subscribers** | Active paid users | High % of total |
| **Active Users** | Not churned | >70% |

---

## Try These Experiments

### Experiment 1: Boost Conversion
1. Sidebar → **Quick Adjustments**
2. Select **"Increase Trial→Subscriber"**
3. Click **"Apply Adjustment"**
4. Re-run simulation
5. Compare metrics

### Experiment 2: Reduce Churn
1. Sidebar → **Quick Adjustments**
2. Select **"Decrease Churn Rate"**
3. Run simulation
4. Note the improvement

### Experiment 3: Poisson Arrivals
1. Sidebar → Toggle **"Enable New User Arrivals"**
2. Set λ (Lambda) = 15
3. Run simulation
4. See continuous user growth

---

## Understanding Results

### Steady-State Distribution
- Predicted long-run user percentages
- In tab: **"🔬 Theory & Properties"**
- Shows equilibrium state

### Funnel Chart
- Shows drop-off at each stage
- Identifies weakest conversion step
- Highlight for optimization

### Time Series
- User count over time
- Shows how distribution evolves
- Colors: each engagement state

---

## Next: Jupyter Notebook

For detailed analysis:
```bash
jupyter notebook notebooks/analysis.ipynb
```

**Includes**:
- Step-by-step explanations
- Mathematical verification
- Custom experiments
- Publication-ready plots

---

## Common Questions

**Q: Why is conversion only 31%?**  
A: Realistic for freemium models. Optimize by increasing `visitor→subscriber` probability.

**Q: What's steady-state?**  
A: Long-run equilibrium—proportion of users in each state after many time steps.

**Q: Can I modify probabilities?**  
A: Yes! Sidebar → **Advanced Edit** mode to customize any transition.

**Q: How do I compare scenarios?**  
A: Run simulation A, note metrics. Apply adjustment. Run simulation B. Compare.

---

## Tips for Success

✓ **Start with defaults** to understand baseline  
✓ **One change at a time** for clear insights  
✓ **Multiple runs** reduce random variation  
✓ **Check steady-state** for long-term thinking  
✓ **Export results** using Streamlit download button  

---

## Troubleshooting

**Dashboard won't start?**
```bash
# Ensure correct directory
cd streaming_simulator
streamlit run app/streamlit_dashboard.py
```

**Import errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Slow performance?**
- Reduce number of users or steps
- Disable arrivals if not needed

---

**Ready to dive deeper? Check README.md for complete documentation!**
