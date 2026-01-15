# VOC Dashboard - Voice of Customer Analytics

## 🎯 Overview
Professional Voice of Customer (VOC) Dashboard with advanced analytics, sentiment analysis, and strategic insights visualization.

**Features:**
- 📊 Real-time sentiment analysis with gauge charts
- 🎨 Modern, interactive visualizations
- 📍 Zone, State, and City-based filtering
- 💬 Customer emotion tracking
- 🏆 Store performance heatmap
- 📈 Trend analysis and key drivers

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit: http://localhost:5000

### Deploy to Render
See DEPLOYMENT.md for complete instructions

## 📁 Project Structure
```
├── Original Code.html          # Main dashboard UI
├── latest_t_mapped.csv        # Customer feedback data
├── app.py                     # Flask server
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment config
└── README.md                  # This file
```

## 🔧 Required Files
- **Original Code.html** - Dashboard interface (React/Recharts)
- **latest_t_mapped.csv** - Processed VOC data
- **app.py** - Flask web server
- **requirements.txt** - Dependencies
- **Procfile** - Render configuration

## 📊 Data Format
The CSV file requires these columns:
- Business Name
- Zone, State, City
- Store Code
- Mall/HS
- Sentiment (POSITIVE, NEGATIVE, NEUTRAL)
- Customer Response
- FY (Financial Year)
- Quarter
- Month
- ImprovementCategory

## 🌐 Live Dashboard
[View on Render](https://your-dashboard-name.onrender.com)

## 📝 License
Internal Use Only

## 👥 Support
For issues or questions, contact the Analytics team.
