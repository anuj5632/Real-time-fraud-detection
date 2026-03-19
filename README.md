# 🚀 Real-Time Fraud Detection System (MLOps + Spring Boot)

## 📌 Overview
This project is a production-style Real-Time Fraud Detection System built using a microservices architecture. It detects fraudulent financial transactions using a machine learning model and integrates MLOps practices like model tracking, retraining, and deployment.

---

## 🧠 Key Features
- Real-time transaction processing
- Fraud prediction using ML model
- Microservices architecture (Spring Boot + Python)
- Analytics dashboard with filters
- Model retraining pipeline
- Dockerized services
- MLflow for experiment tracking

---

## 🏗️ System Architecture
User → Spring Boot → ML Service → Database → Dashboard

---

## 🔄 System Flow
1. User initiates transaction  
2. Backend processes request  
3. ML model predicts fraud  
4. Data stored in database  
5. Response returned  

---

## 🧱 Tech Stack
- Backend: Spring Boot  
- ML: Python (Scikit-learn)  
- Database: MySQL  
- MLOps: MLflow, Docker  

---

## 🚀 Getting Started

### Clone Repo
git clone https://github.com/your-username/real-time-fraud-detection.git

### Run Backend
mvn spring-boot:run

### Run ML Service
python app.py

---

## 📡 API
POST /api/transactions

---

