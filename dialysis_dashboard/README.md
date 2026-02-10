# AI-Based Dialysis Stabilisation System

An **AI-driven, real-time dialysis monitoring and safety system** designed to enhance patient safety during dialysis procedures, especially under **unstable physical conditions such as vibrations or seismic disturbances**.

This project integrates **real-time simulation, intelligent safety logic, a web-based dashboard, and a Flutter-based application**, making it suitable for **smart healthcare systems and disaster-resilient medical infrastructure**.

---

## Project Overview

Dialysis is a **life-critical medical procedure** that demands stable environmental and mechanical conditions. Sudden vibrations—caused by earthquakes, machine instability, or structural disturbances—can result in **dangerous pressure fluctuations**, risking patient safety.

This system continuously:
- Monitors vibration levels
- Adjusts dialysis parameters automatically
- Switches between safety modes
- Notifies users through alerts
- Displays real-time data on Web and Flutter dashboards

---

## Key Features

### Patient Management
- Manual patient entry via UI
- Patient details include:
  - Name
  - Age
  - Gender
- Patient information displayed live during treatment

---

### Adjustable Treatment Time
- Dialysis duration set manually (e.g., 2–4 hours)
- Countdown displayed in **HH:MM:SS**
- Updates every second in real time

---

### Real-Time Monitoring
- Blood Flow (ml/min)
- Arterial Pressure (mmHg)
- Venous Pressure (mmHg)
- Vibration Intensity (g-force)
- System State (Live)

---

### Intelligent Safety Logic

| Mode | Condition | System Response |
|----|----|----|
| **NORMAL** | Vibration < 0.35 g | Standard parameters |
| **STABILISATION** | 0.35 g ≤ Vibration < 0.55 g | Reduced flow & pressure |
| **EMERGENCY STOP** | Vibration ≥ 0.55 g | Dialysis halted immediately |

---

### Alert System
- Timestamped alerts
- Emergency vibration warnings
- Stabilisation mode alerts
- Displayed in:
- Web Dashboard
- Flutter Application

---

## System Architecture

---

## 🧪 Tech Stack

### Backend
- Python
- Flask
- Multithreading
- REST APIs

### Web Frontend
- HTML5
- CSS3 (Dark theme, state-based colors)
- JavaScript (Live polling)

### Flutter Application
- Flutter
- Dart
- HTTP REST integration
- Cross-platform (Web / Desktop / Mobile)

### Version Control
- Git
- GitHub (structured commits)

---

## 📂 Project Structure


---

## 🧪 Tech Stack

### Backend
- Python
- Flask
- Multithreading
- REST APIs

### Web Frontend
- HTML5
- CSS3 (Dark theme, state-based colors)
- JavaScript (Live polling)

### Flutter Application
- Flutter
- Dart
- HTTP REST integration
- Cross-platform (Web / Desktop / Mobile)

### Version Control
- Git
- GitHub (structured commits)

---

## Project Structure

┌──────────────────────────┐
│   Vibration Simulation   │
│ (Seismic / Machine Data) │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│   AI Safety & Control    │
│      (Flask Backend)     │
│                          │
│ • Threshold Evaluation   │
│ • Mode Switching         │
│ • Treatment Timer        │
│ • Alert Generation       │
└─────────────┬────────────┘
              │ REST APIs
              ▼
┌─────────────────────────────────────────┐
│        User Interfaces (Live)           │
│                                         │
│  ┌───────────────┐   ┌────────────────┐ │
│  │ Web Dashboard │   │ Flutter App    │ │
│  │ (HTML/CSS/JS) │   │ (Cross-Platform)││
│  └───────────────┘   └────────────────┘ │
└─────────────────────────────────────────┘

## Tech Stack

### Backend
- Python
- Flask
- Multithreading
- REST APIs

### Web Frontend
- HTML5
- CSS3 (Dark theme, state-based colors)
- JavaScript (Live polling)

### Flutter Application
- Flutter
- Dart
- HTTP REST integration
- Cross-platform (Web / Desktop / Mobile)

### Version Control
- Git
- GitHub (structured commits)

---

## Project Structure

dialysis-stabilisation-system/
│
├── web/                         # Backend + Web Dashboard
│   ├── app.py                   # Flask backend (core logic)
│   │
│   ├── templates/
│   │   └── index.html           # Web dashboard UI
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Dashboard styling
│   │   └── js/
│   │       └── dashboard.js     # Live data polling & UI logic
│   │
│   └── venv/                    # Python virtual environment
│
├── dialysis_dashboard/          # Flutter application
│   ├── lib/
│   │   └── main.dart            # Flutter UI & API integration
│   │
│   ├── pubspec.yaml             # Flutter dependencies
│   └── pubspec.lock
│
├── ai_simulation/               # AI logic & simulation modules
│   ├── dialysis_machine.py
│   └── stabilisation_logic.py
│
├── README.md                    # Project documentation
├── .gitignore
└── requirements.txt             # Backend dependencies



