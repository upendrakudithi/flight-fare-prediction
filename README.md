# ✈️ Flight Fare Prediction

A Machine Learning based web application that predicts flight ticket fares based on flight-related input features. The application uses a trained Machine Learning model with a Flask backend and a simple web interface.

## 🚀 Project Overview

This project demonstrates an end-to-end Machine Learning workflow:

- Data preprocessing and cleaning
- Exploratory analysis and model training
- Saving the trained model
- Integrating the model with a Flask web application
- Accepting user input through a web interface
- Generating a predicted flight fare

## ✨ Features

- Flight fare prediction through a web interface
- Flask-based backend
- Trained Machine Learning model
- Data preprocessing and feature handling
- HTML/CSS frontend
- Saved trained model using `model.pkl`
- Dockerfile included for containerization

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **HTML**
- **CSS**
- **Jupyter Notebook**
- **Docker**

## 📂 Project Structure

```text
flight-fare-prediction/
│
├── static/
│   └── css/
│
├── templates/
│   └── ...
│
├── Airfare_Prediction (1).ipynb
├── app.py
├── model.pkl
├── Clean_Dataset.csv
├── requirements.txt
├── Dockerfile
└── README.md
```

## ⚙️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/upendrakudithi/flight-fare-prediction.git
cd flight-fare-prediction
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask application

```bash
python app.py
```

### 5. Open the application

Open the local URL shown in the terminal, typically:

```text
http://127.0.0.1:5000/
```

## 🧠 Machine Learning Workflow

The project follows a typical Machine Learning pipeline:

```text
Dataset
   ↓
Data Cleaning & Preprocessing
   ↓
Feature Preparation
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Saved Model (model.pkl)
   ↓
Flask Web Application
   ↓
Flight Fare Prediction
```

## 📊 Dataset

The project includes the cleaned dataset used during the Machine Learning workflow. The notebook contains the data analysis, preprocessing, model development, and experimentation.

## 🐳 Docker

A `Dockerfile` is included in the project for containerizing the application.

## 🔮 Future Enhancements

- Deploy the application to a cloud platform
- Improve model performance through additional feature engineering
- Add more flight and route-related features
- Improve the user interface and user experience
- Add automated model retraining

## 👨‍💻 Author

**Upendra Kudithi**

GitHub: [upendrakudithi](https://github.com/upendrakudithi)

---

⭐ If you find this project useful, feel free to explore the repository.
