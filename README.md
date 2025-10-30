# PredictiveAnalyticsApp 🚀

### Create Predictive Models Based on Your Data 📊

**PredictiveAnalyticsApp** is a user-friendly desktop application designed to simplify the processes of loading, editing, and analyzing data from `.csv` files, as well as subsequently building powerful predictive models.

No more need to write code for basic analysis or data preprocessing. This application allows you to quickly prepare data and get predictions, whether it's weather forecasting, predicting a student's grade probability, estimating startup success chances, or anything else you can imagine!

-----

### Key Features 🛠️

* **📝 Built-in CSV Editor:** An intuitive interface for viewing, editing, sorting, and deleting unnecessary columns directly within the application.
* **⚙️ Flexible Preprocessing Tools:**
    * **Sorting:** Sort data by one or multiple columns.
    * **Merging:** Combine data from multiple `.csv` files into one.
    * **Column Removal:** Easily remove irrelevant columns to clean your data.
* **🔮 Predictive Modeling:**
    * Load prepared datasets.
    * Select target variables for forecasting.
    * Use built-in machine learning algorithms to build predictive models and obtain forecasts.

-----

### Use Cases 💡

* **☁️ Weather Forecasting:** Load historical weather data (temperature, humidity, pressure) to predict the probability of rain tomorrow.
* **🧑‍🎓 Education:** Analyze student performance data to forecast the probability of achieving a high grade on an upcoming exam.
* **📈 Business Success:** Evaluate market data and predict the probability of a new startup's success.

-----

### Getting Started ▶️

#### Installation 📥

To install the application, clone the repository:

```bash
git clone https://github.com/Birewon/PredictiveAnalyticsApp.git
cd PredictiveAnalyticsApp
```

Then install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

#### Launching the Application 🚀

After installing the dependencies, launch the application from the project's root directory:

```bash
python main.py
```

-----

### Roadmap 🗺️

Below is an overview of the current status and future plans for PredictiveAnalyticsApp.

#### Already Implemented:

* ✅ **CSV File Loading:** Ability to load one or two `.csv` files into the application.
* ✅ **Select Save Directory:** Functionality to choose the directory where processed files will be saved.
* ✅ **Basic CSV Concatenation:** Merge two uploaded `.csv` files into one output file.
* ✅ **Status Reports:** Display real-time updates and error messages in the user interface.

#### Planned Features:

* ⏳ **Advanced CSV Preprocessing:**
    * Sort data by selected columns.
    * Merge/join CSV files based on common columns (join types: `inner`, `outer`, `left`, `right`).
    * Select and remove columns.
    * Handle missing values (imputation, deletion of rows/columns).
* ⏳ **Predictive Model Building Interface:**
    * Selection of target (dependent) and feature (independent) variables.
    * Choice of common machine learning algorithms (e.g., Linear Regression, Logistic Regression, Decision Trees).
    * Configuration of train-test data split.
* ⏳ **Model Evaluation and Visualization:**
    * Display of model performance metrics (e.g., accuracy, recall, F1-score, R-squared).
    * Visualizations for data distribution and model predictions.
* ⏳ **Interactive Data Visualization:** Basic plots (histograms, scatter plots) of uploaded data.

-----

### Built With 💻

* **🐍 Python:** The primary programming language.
* **🎨 PyQt5:** For creating the graphical user interface.
* **🐼 pandas:** For efficient processing and manipulation of `.csv` data.
* **🤖 scikit-learn:** For implementing various predictive modeling algorithms.

-----

### Contributing 🤝

The application welcomes ideas and suggestions! If you have any feedback or would like to contribute, please create an [Issue](https://github.com/Birewon/PredictiveAnalyticsApp/issues) or [Pull Request](https://github.com/Birewon/PredictiveAnalyticsApp/pulls) on GitHub.