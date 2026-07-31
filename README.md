# Facebook Social Network Analysis

**Complete Big Data Analytics Project with Beautiful UI**

**GitHub Repository:** [https://github.com/KarreJohnHyde/bigdatas](https://github.com/KarreJohnHyde/bigdatas)

## 🚀 Quick Start (with Smart Checkpoints)

### **RUN THIS ONE COMMAND:**

```bash
python app.py
```

That's it! The dashboard will open automatically in your browser at `http://localhost:5000`. The analysis uses smart checkpoints to save your progress!

---

## 📊 What This Does

This project performs **complete in-depth analysis** of the Facebook social network dataset:

1. **Loads Network Data** - 4,039 users, 88,234 connections
2. **Analyzes User Influence** - Calculates centrality measures (degree, betweenness, closeness, eigenvector)
3. **Detects Communities** - Identifies groups using 3 algorithms (Louvain, Label Propagation, Greedy Modularity)
4. **Creates Visualizations** - Generates charts and graphs
5. **Shows Beautiful Dashboard** - Professional UI with real-time analysis progress

---

## 🎨 Features

### **Beautiful Loading UI:**
- Real-time progress bar showing analysis steps
- Step-by-step indicator (Load Data → Analyze → Detect → Visualize → Complete)
- Smooth animations and modern design

### **Complete Dashboard:**
- **Network Statistics**: Total users, connections, density, average degree
- **Top Influential Users**: Top 3 users with their centrality scores
- **Community Analysis**: Results from 3 different detection methods
- **Interactive Charts**: Centrality distribution and community sizes
- **Network Insights**: Key findings about network structure and influence

### **ONE-TIME Analysis:**
- Runs complete analysis ONCE when you start the app
- Shows live progress during analysis
- Results displayed instantly when complete
- No need to click "Start Analysis" - it runs automatically!

---

## 📁 Project Structure

```
bigdatas/
├── app.py                    # Main application (RUN THIS FILE)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── src/                      # Python source code
│   ├── data_loader.py        # Load Facebook network data
│   ├── centrality_analyzer.py # Calculate centrality measures
│   ├── community_detector.py  # Detect communities
│   └── visualizer.py         # Create visualizations
│
├── ui/                       # User Interface (HTML, CSS, JS)
│   ├── templates/
│   │   └── index.html        # Main dashboard template
│   └── static/
│       ├── css/
│       │   └── style.css     # Beautiful styling
│       └── js/
│           └── app.js        # Dashboard logic
│
├── data/                     # Data files
│   ├── raw/                  # Original Facebook dataset
│   ├── results/              # Analysis results (CSV, HTML, PNG)
│   └── analysis_cache/       # Cached analysis data
│
└── config/                   # Configuration
    └── settings.yaml         # Analysis settings
```

---

## 🎯 How It Works

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Watch the analysis:**
   - Beautiful loading screen appears
   - Progress bar updates in real-time
   - Shows current step (Loading data, Analyzing, etc.)

3. **View results:**
   - Dashboard automatically appears when complete
   - See network statistics, top users, communities
   - Interactive charts and insights

---

## 📊 Analysis Results

### **Network Overview:**
- 4,039 users (nodes)
- 88,234 connections (edges)
- Network density: 0.0108
- Average connections per user: 43.7

### **Top Influential Users:**
- **User 107** - Most influential (25.9% degree centrality)
- **User 1684** - Highly connected (19.6% degree centrality)
- **User 1912** - Key connector (18.7% degree centrality)

### **Communities Detected:**
- **Louvain:** 16 communities (modularity: 0.8349)
- **Label Propagation:** 44 communities (modularity: 0.7368)
- **Greedy Modularity:** 13 communities (modularity: 0.7774)

---

## 🔧 Requirements

- Python 3.8+
- Flask
- NetworkX
- Pandas
- NumPy
- Matplotlib
- Seaborn

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

---

## 🌟 Key Features

✅ **ONE file to run** - Just `python app.py`  
✅ **Beautiful UI** - Modern gradient design with animations  
✅ **Real-time progress** - See analysis steps as they happen  
✅ **Complete analysis** - Centrality, communities, visualizations  
✅ **Professional dashboard** - Perfect for client presentations  
✅ **Fast loading** - Optimized for quick results  
✅ **No manual steps** - Everything runs automatically  

---

## 💡 Perfect for:

- Academic projects
- Client presentations
- Big data analytics demonstrations
- Social network analysis research
- Network science education

---

## 📧 Support

For any issues or questions, please check:
- Project structure in `src/` folder
- UI code in `ui/` folder
- Configuration in `config/settings.yaml`

---

## 🚀 Deployment to GitHub

To deploy this project to your GitHub repository ([KarreJohnHyde/bigdatas](https://github.com/KarreJohnHyde/bigdatas)):

1. Make sure you have Git installed on your machine.
2. Open your terminal in the project directory (`c:/bigdatas`).
3. Run the following commands:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with complete big data analytics project"
   git branch -M main
   git remote add origin https://github.com/KarreJohnHyde/bigdatas.git
   git push -u origin main
   ```
4. (Optional) Deploying on a platform like Render or Heroku:
   - Make sure you connect your GitHub repository to your platform of choice.
   - Start Command: `gunicorn app:app` (You may need to add `gunicorn` to `requirements.txt`).

---

**🎉 Enjoy your beautiful Facebook Social Network Analysis dashboard!**
