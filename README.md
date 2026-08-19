# Fraud-Detection-System

An end-to-end Fraud Detection System using Machine Learning (Random Forest) and SMOTE. Features a Flask API for real-time transaction inference, SQLite logging, and automated email alerts. Containerized with Docker for seamless deployment, this project provides a scalable, secure solution for identifying unauthorized financial activity.

## Key Features

* **Machine Learning Model:** Uses a **Random Forest** classifier combined with **SMOTE** (Synthetic Minority Over-sampling Technique) to effectively handle imbalanced financial transaction data.
* **Real-Time Inference API:** Built with **Flask** to handle real-time transaction scoring and fraud prediction requests.
* **Logging & Alerts:** Integrates **SQLite logging** for transaction tracking alongside automated email alerts for high-risk activity.
* **Docker Support:** Fully containerized with **Docker** for smooth deployment and scaling.

---

## Tech Stack

* **Language:** Python, Jupyter Notebook
* **Backend Framework:** Flask
* **Machine Learning:** Scikit-learn (Random Forest), imbalanced-learn (SMOTE)
* **Database:** SQLite
* **Deployment:** Docker

---

## Getting Started

### Prerequisites

* Python 3.x
* Docker (optional, for containerized deployment)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/HeetrajsinhJadeja/Fraud-Detection-System.git](https://github.com/HeetrajsinhJadeja/Fraud-Detection-System.git)
   cd Fraud-Detection-System

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run the Flask API:**
   ```bash
   python app.py
