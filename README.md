# Network Traffic Monitoring Platform

A beginner-friendly, full-stack web application that simulates real-time network traffic monitoring. Built as a learning project to understand how network monitoring systems work — from packet capture concepts to live dashboard rendering.

> **Note:** This project uses simulated traffic data. It does not capture actual packets from a live network interface.

---

## Overview

The dashboard gives you a live view of network packets flowing through a simulated environment. You can watch packets appear in real time, filter them by protocol or IP address, and track running statistics — all from a clean, minimal interface. A built-in data generator lets you produce 150 realistic synthetic packets on demand, so you always have something to work with.

---

## Tech Stack

- **Backend** — Python 3, Flask
- **Frontend** — HTML, CSS, Vanilla JavaScript
- **Data Storage** — CSV (`data.csv`)
- **Traffic Generation** — Custom `data_generator.py` module

---

## Project Structure

```
network-traffic-monitor/
├── app.py                  # Flask backend — routes, filtering, stats
├── data_generator.py       # Synthetic traffic data generator
├── data.csv                # Packet data (auto-generated or pre-loaded)
├── templates/
│   └── index.html          # Frontend dashboard
└── static/
    └── style.css           # Styling
```

---

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/your-username/network-traffic-monitor.git
cd network-traffic-monitor

# 2. Install the only dependency
pip install flask

# 3. Start the app
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000`.

---



---

## What I Learned

Working on this project helped me get hands-on experience with:

- How network traffic monitoring systems are structured
- Building and consuming a REST API with Flask
- Connecting a frontend to a backend without any JavaScript framework
- Filtering and processing structured data in Python
- Designing a full-stack application from scratch as a beginner

---

## Author

**Hafsa Kokab**

---

⭐ Final Note

This project is designed for learning purposes and demonstrates how network monitoring systems work in a simplified and beginner-friendly way.
