<h1 align="center">🚗⚡ Electric Vehicle (EV) Population Analysis</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Category-Data%20Analytics-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Tools-Python%20%7C%20Pandas%20%7C%20EDA-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Model-ML%20%7C%20Forecasting-green?style=flat-square" />
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-red?style=flat-square" />
</p>

<p align="center">
  A complete end-to-end data analytics project analysing Electric Vehicle adoption trends across regions, manufacturers, and time.  
  Includes EDA, Feature Engineering, Clustering, Forecasting, and an Interactive Streamlit Dashboard.
</p>

---

## 📌 **Table of Contents**
- [🔍 Project Overview](#-project-overview)
- [📊 Key Insights](#-key-insights)
- [🧠 Machine Learning Work](#-machine-learning-work)
- [📈 Forecasting](#-forecasting)
- [📺 Streamlit Dashboard](#-streamlit-dashboard)
- [⚙️ Installation](#️-installation)
- [🚀 How to Run](#-how-to-run)
- [📁 Dataset](#-dataset)
- [🧾 License](#-license)

---

## 🔍 **Project Overview**

Electric Vehicles (EVs) are rapidly gaining adoption worldwide.  
This project aims to **analyze EV adoption trends**, understand:

✔ Which states register the most EVs  
✔ Which manufacturers dominate the market  
✔ Factors that influence EV growth  
✔ Future EV adoption forecast (next 3 years)  
✔ Segmentation of states using clustering  
✔ Interactive dashboard for real-time exploration  

This project follows a **professional end-to-end workflow** suitable for a Data Analyst / Data Scientist portfolio.

---

## 📊 **Key Insights (From EDA)**

Some of the most important findings:

- 🚀 **EV adoption is accelerating year-over-year**
- 🏆 **Tesla dominates** EV registrations in most states
- 🌎 Certain states show significantly faster growth than others
- 💸 EV range and price (MSRP) show moderate correlation
- 🧭 State-level EV density varies widely (clustered later)

Visual examples:

<p align="center">
  <img src="reports/figures/make_distribution.png" width="500px">
</p>
<p align="center">
  <em>Distribution of EVs by manufacturer</em>
</p>

---

## 🧠 **Machine Learning Work**

### **1️⃣ Feature Engineering**
Created additional features for deeper analysis:

- `vehicle_age`  
- `state_ev_count`  
- `make_avg_range`  
- Missing-value indicator flags  
- Aggregated features (make-level statistics)

---

### **2️⃣ Clustering (KMeans)**  
Segmented states based on:

- EV adoption count  
- Average EV range  
- Number of unique manufacturers  
- Yearly growth rate  

This helps identify:

🔹 High-adoption states  
🔹 Emerging markets  
🔹 Underdeveloped EV ecosystems  

---

## 📈 **Forecasting (Time Series)**

Used `statsmodels` Exponential Smoothing (ETS) to forecast **next 3 years of EV registrations**.

Model used:

- Additive trend  
- No seasonality  
- Automatically estimated initial values  

Forecast chart example:

<p align="center">
  <img src="reports/figures/ev_forecast.png" width="520px">
</p>

---

## 📺 **Streamlit Dashboard**

An interactive dashboard for exploring:

✔ Top EV manufacturers  
✔ State-level adoption  
✔ EV growth by year  
✔ Filtering by state  

Run the dashboard:

```bash
streamlit run dashboard/app.py

