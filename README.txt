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
























Movie Revenue predictor!!           By: Aiden Fockens (1 man group)

** Predict the revenue of a new movie by inputting its budget and other features!

Run my code:
 
 - go to "https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies" and download the dataset! Put it in
     the data_analysis folder

 - "make notebooks" will turn the notebooks into .py files and run them. This will show my statistics of my models and pop-up graphs

 - "make webapp" will start my react and flask. This will prompt you to make an account (users are stored in an amazon cloud db)
Then travel to the Data Analysis page, where you can input the features of a new movie to get a predicted revenue and Revenue Category.
This webapp utilizes the models I made in create_model.ipynb and queries them for their predictions.
You can also see all of the graphs that I created in visualize_data.ipynb
(The home page allows you to save your favorite movies and receive new recommendations, also stored in the amazon db)

Overview:
     I used the "Full TMDB Movies Dataset 2024" on Kaggle. It had 2.7 million entries. However, only about 16,000 of them had revenues attached,
so I only took these entries to train with. This lack of data negatively impacted the accuracy of my models. I first did a lot of data visualization to 
determine which features I wanted to use. I found that, for most of my data, its log was better correlated with the log of the revenue than their bare values. 
For my features, I ended up using: 
 -The decade
 -The genres
 -the season
 - log_budget
 - log_runtime (log of movie length)
 - log_vote_count (number of votes for the movie)
 - log_vote_average 
 - has_homepage (if the movie has a website)
 - log_avg_studio_rank (I ranked each studio by average revenue and amount of movies produced, 1 being the best and higher being worse)



I found these features by graphing them along with budget and revenue to determine their relevance, and performing pearsson correlation tests.

I created two models, both of which tried to predict the log of Revenue. I converted this back to a normal number after:

1. Random Forest Categories. For this model, I split the dataset into 5 categories based on revenue: Very low, Low, Medium, High, and Very High.
     In my create_model.py, I print out the thresholds for these buckets and theri sizes. This model gave me an accuracy of .65, and a weighted
     accuracy of .81. 

2. XGBoost. This was a continuous model that directly predicted the log of Revenue. It had a mean squared error of $25,000,000. This is a ton,
     as the average revenue was also about $25,000,000. However, my python file prints out some predicted and real values of revenue, and 
     they are not far off. The mean squared error comes from some of the top-grossing movies which greatly throw off my models accuracy.

Create_Model.ipynb:
     First, I take all the data from the dataset. I then take the necessary features, and reduce my dataset to only entries with an actual
     revenue. I also get rid of the top .97 percent of data, as the outliers make it even harder for my model to be accurate. I compute my 
     features and then test them with the pearsson correlation. I then tested a few different models (regressive model, XGboost, Light Boost, etc.)
     before deciding on using the XGBoost. I also make the Random Forest model, and then save both of these models.

Visualize_data.ipynb:
     This visualized the data from the entire set. It looks at the number of movies by decade, and the budgets and revenues associated
     with each decade, genre, movie length (runtime), score, and language

App.py:
     It uses the saved models, along with the data received in json from the front end, to predict the category and exact revenue amount of a new
     movie. It then sends that back to my front-end where it is displayed. I also saved all the graphs I made and but it in the static folder so
     that they can be displayed on the data analysis page

movie-frontend:
     My react app. It has my styles and js/html and keeps the user session. Supports log_in/log_out and tracking favorite movies that 
     are kept associated with your account.

Data_analysis folder:
     It has my two notebooks as well as my saved models, best_xgb_model.pkl and random_forest_model.pkl. It also has an encoder
     that is used for the random_forest_model to encode each entry with the correct bucket.


Findings:
     While I had quite a low accuracy (msqe of 25 million) most of my predictions were actually good on a singular level. 
     When using the app, I am looking at movies created in 2020, to better predict how much a new movie might make. 
     However, because they haven't been around as long, they have not had the same amount of time to make money. 
     This results in quite low estimations from my model, no matter how high the budget is. The genre of the movie makes a huge difference,
     which is clear through the budget and revenue vs genre graph. The largestindicator of revenue is budget, which is clear 
     when you change the budget on the web app. In the future, I would combine other datasets onto my own to find a larger pool of movies with reliable revenues. 
