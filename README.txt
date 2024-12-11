Movie Revenue Predictor  
By: Aiden Fockens (1-Man Group)

**Predict the revenue of a new movie by inputting its budget and other features!**

--------------------------------------------------------------------------------

Run My Code:

1. Download the Dataset:
   - Go to https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies
   - Download the dataset and place it in the `data_analysis` folder.

2. Run the Notebooks:
   - Use the command:
     make notebooks
   - This will convert the notebooks to `.py` files and execute them, displaying model statistics and generating graphs.

3. Start the Web Application:
   - Use the command:
     make webapp
   - This starts the React front-end and Flask back-end.
   - Create an account (user data is stored in an Amazon RDS database) and navigate to the **Data Analysis** page to:
     - Input movie features and predict revenue.
     - View graphs generated in `visualize_data.ipynb`.
   - On the **Home** page, save favorite movies and get recommendations.

--------------------------------------------------------------------------------

Github Workflow:

My workflow uses my makefile and tests that both the react app and flask app are correctly running. 

Project Overview:

I used the Full TMDB Movies Dataset 2024 on Kaggle, which includes 2.7 million entries. However, only ~16,000 entries had revenue data, so I trained my models using this subset. This limited data impacted the accuracy of the models.

Key Features Used:
 - Decade: Era of the movie.
 - Genres: Categories of the movie.
 - Season: Time of release.
 - Log-scaled Features:
   - Budget (log_budget)
   - Runtime (log_runtime)
   - Vote count (log_vote_count)
   - Vote average (log_vote_average)
 - Has Homepage: Whether the movie has an official website.
 - Studio Rank: Log of average revenue and production volume by studio.

These features were selected based on visualizations and Pearson correlation tests.

--------------------------------------------------------------------------------

Models:

1. Random Forest (Categorical Prediction):
   - Predicts revenue categories: Very Low, Low, Medium, High, and Very High.
   - Accuracy:
     - Overall: 65%
     - Weighted: 81%
   - Thresholds for these buckets are printed in `create_model.py`.

2. XGBoost (Continuous Prediction):
   - Predicts the log of revenue.
   - Mean Squared Error (MSE): $25M.
     - While this seems large, it’s comparable to the average revenue (~$25M).
   - Predictions align well for most movies, except for top-grossing films.

--------------------------------------------------------------------------------

Project Structure:

Key Components:

- create_model.ipynb:
  - Preprocessed data and engineered features.
  - Removed outliers (top 0.97% of revenue data) for better performance.
  - Tested various models before finalizing XGBoost and Random Forest.
  - Saved models: `best_xgb_model.pkl` and `random_forest_model.pkl`.

- visualize_data.ipynb:
  - Visualized statistics:
    - Movies by decade.
    - Budget and revenue trends by decade, genre, runtime, score, and language.

- app.py:
  - Flask API:
    - Loads pre-trained models.
    - Accepts input features via JSON.
    - Predicts revenue category and exact revenue.
    - Returns predictions to the front-end.

- movie-frontend:
  - React front-end:
    - User authentication (login/logout).
    - Save favorite movies and receive recommendations.
    - Display graphs and predictions.

- data_analysis:
  - Contains notebooks, models, and an encoder for Random Forest.

--------------------------------------------------------------------------------

Findings:

- Web App Reliability:
  - On my web app, I am attempting to predict the revenue of new movies. This means that its decade is 2020, 
    and on average movies made in the 2020s have a low revenue because they haven't been around for very long
    My model learned this quite well, and predicts very small revenues for new movies, even when the budget is 
    heavily increased.
  - It accounts very well for the genre of the movie, as certain genres like Adventure and Science Fiction make way more money than others.
    This is clear when you choose to make a documentary, and your revenue is thoroughly slashed.

- Accuracy Challenges:
  - Limited data impacted accuracy, especially for top-grossing films.
  - Movies created in 2020 had lower revenue predictions due to less time to generate income.

- Most Important Features:
  - Budget: Strongest indicator of revenue.
  - Genre: Highly correlated with revenue.

- Future Work:
  - Combine additional datasets to increase training data.
  - Explore machine learning models that better handle outliers.












