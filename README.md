# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and Streamlit, utilizing machine learning to suggest movies based on user preferences.

## 🌟 Overview

This project implements a **content-based filtering** recommendation engine that analyzes movie metadata (genres, cast, crew, keywords) to suggest similar movies. When a user selects a movie they enjoy, the system recommends other films with comparable characteristics using cosine similarity algorithms.

## ✨ Features

- **Intelligent Recommendations**: Get movie suggestions based on content similarity
- **Interactive Web Interface**: User-friendly Streamlit application
- **Movie Posters**: Visual representation of recommended movies
- **Real-time Data**: Integration with TMDB API for movie information
- **Fast Performance**: Optimized with pre-computed similarity matrices
- **Responsive Design**: Works seamlessly across different devices

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- TMDB API key (free registration at [themoviedb.org](https://www.themoviedb.org/))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sahithbaratam/movie-recommendation-streamlit.git
   cd movie-recommendation-streamlit
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure TMDB API**
   - Create an account at [TMDB](https://www.themoviedb.org/)
   - Generate an API key from your account settings
   - Create a `.env` file or update the configuration with your API key

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 💻 Usage

1. Launch the application using `streamlit run app.py`
2. Select a movie from the dropdown menu
3. Click the "Recommend" button
4. View personalized movie recommendations with posters
5. Click on movie titles or posters for more details

## 📁 Project Structure

```
movie-recommendation-streamlit/
│
├── app.py                      # Main Streamlit application
├── model.ipynb                 # Jupyter notebook for model training
├── requirements.txt            # Python dependencies
├── movies_list.pkl            # Preprocessed movie dataset
├── similarity.pkl             # Pre-computed similarity matrix
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
│
└── data/                      # Dataset directory (if applicable)
    ├── movies.csv
    └── credits.csv
```

## 🔬 How It Works

### Content-Based Filtering

The recommendation system works through the following steps:

1. **Data Preprocessing**
   - Load movie and credits datasets
   - Merge datasets on movie ID
   - Extract relevant features (genres, keywords, cast, crew)
   - Clean and process text data

2. **Feature Engineering**
   - Combine multiple features into a single "tags" column
   - Convert text to lowercase and remove spaces
   - Create a bag-of-words representation

3. **Vectorization**
   - Use CountVectorizer or TfidfVectorizer to convert text to numerical vectors
   - Apply stemming to reduce words to their root form

4. **Similarity Calculation**
   - Calculate cosine similarity between movie vectors
   - Store similarity matrix for quick recommendations

5. **Recommendation Generation**
   - Find movies with highest similarity scores
   - Fetch movie posters from TMDB API
   - Display top N recommendations to the user

## 📊 Dataset

This project uses the **TMDB 5000 Movie Dataset** from Kaggle, which includes:

- **Movies Dataset**: 5000+ movies with metadata
  - Title, overview, genres, keywords
  - Budget, revenue, runtime
  - Release dates, production companies
  - Vote counts and averages

- **Credits Dataset**: Cast and crew information
  - Actor names and character roles
  - Director and crew details

**Dataset Source**: [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata)

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning library
  - CountVectorizer for text vectorization
  - Cosine similarity for recommendations
- **NLTK**: Natural language processing (stemming)
- **Requests**: API calls to TMDB
- **Pickle**: Model serialization

## 🔑 API Configuration

### Setting up TMDB API

1. Visit [TMDB](https://www.themoviedb.org/) and create an account
2. Navigate to Settings → API → Create → Developer
3. Fill in the required information
4. Copy your API key

### Adding API Key to the Project

**Method 1: Environment Variables**
```bash
export TMDB_API_KEY='your_api_key_here'
```

**Method 2: Configuration File**
```python
# config.py
TMDB_API_KEY = 'your_api_key_here'
```

**Method 3: .env File** (Recommended)
```
TMDB_API_KEY=your_api_key_here
```


