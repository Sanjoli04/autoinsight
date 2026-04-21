# AutoInsight: Automated Data Analysis & Insight Generator

AutoInsight is a web-based tool that allows users to upload a CSV dataset and automatically receive a complete exploratory data analysis report along with AI-generated insights.

The system combines statistical analysis, visualization, and large language models to transform raw data into meaningful interpretations with minimal effort.

---

## 🚀 Features

- Upload any CSV dataset and analyze it instantly
- Automatic data cleaning and preprocessing
- Visual insights including:
  - Missing value distribution
  - Correlation heatmap
  - PCA-based variance analysis
  - Pairwise scatter plots
- Automatic detection of time-series data
- Time-series visualization (if applicable)
- AI-generated structured data report using Gemini
- Downloadable ZIP report with all results

---

## 🧠 How It Works

1. User uploads a dataset through the web interface
2. The system processes the dataset and generates visualizations
3. Key statistical summaries are extracted
4. The insights and plots are passed to a language model
5. A structured analytical report is generated automatically
6. All outputs are packaged into a downloadable ZIP file

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas, NumPy
- Matplotlib, Seaborn
- Scikit-learn (PCA, preprocessing)
- Gemini API (Google Generative AI)

---

## 📦 Project Structure

```
AutoInsight/
├── app.py                # Streamlit interface
├── main.py               # Core analysis pipeline
├── requirements.txt      # Dependencies
└── .env.example          # Environment variable template
```

---

## ⚙️ Setup Instructions

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/AutoInsight.git
   cd AutoInsight
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Add your API key

   Create a `.env` file:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Run the application

   ```bash
   streamlit run app.py
   ```

---

## 📊 Output

After processing a dataset, the system generates:

- Multiple visualization plots
- A detailed analytical report (`README.md`)
- A downloadable ZIP file containing all outputs

---

## 💡 Use Cases

- Quick exploratory data analysis
- Academic projects and assignments
- Data storytelling and reporting
- Initial dataset understanding before modeling

---

## 📈 Future Improvements

- Advanced forecasting models (ARIMA, Prophet)
- Interactive visualizations
- Support for larger datasets
- Model-based predictions and anomaly detection

---

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository and submit a pull request.

---

## 📬 Contact

If you have any questions or suggestions, feel free to reach out.
