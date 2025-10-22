
import streamlit as st
import pickle
import pandas as pd
import requests
import time  # For loading delays

import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSVs
movies_csv = pd.read_csv('../archive (4)/tmdb_5000_movies.csv')
credits_csv = pd.read_csv('../archive (4)/tmdb_5000_credits.csv')


# Merge
df = movies_csv.merge(credits_csv, left_on='id', right_on='movie_id', how='left')

# Combine features into tags
def combine_features(row):
    features = []
    for col in ['genres','keywords','cast','crew']:
        if col in row and pd.notnull(row[col]):
            row_list = ast.literal_eval(row[col])
            if isinstance(row_list,list):
                features += [x['name'] for x in row_list if 'name' in x]
    if 'overview' in row and pd.notnull(row['overview']):
        features.append(row['overview'])
    return features

df['tags'] = df.apply(combine_features, axis=1)

# Prepare final DataFrame
movies = df[['id','original_title','tags']].copy()
movies.rename(columns={'original_title':'title'}, inplace=True)
movies['tags'] = movies['tags'].fillna('')
movies['tags'] = movies['tags'].apply(lambda x: " ".join(x))
movies['tags'] = movies['tags'].apply(lambda x: x.lower())

# Compute similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()
similarity = cosine_similarity(vectors)


# Enhanced fetch function: Gets poster, genres, overview, and vote_average
@st.cache_data(ttl=3600)
def fetch_movie_details(movie_id):
    api_key = "1def2806abec7bc1af0cf4b4555f00ac"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster = "https://image.tmdb.org/t/p/w500/" + data.get('poster_path','')
            genres = [g['name'] for g in data.get('genres',[])]
            overview = data.get('overview','No description available.')
            rating = data.get('vote_average',0)/2
            return poster, genres, overview, rating
        except Exception as e:
            time.sleep(0.3)
    # If it still fails, return None
    return None

import time
def recommend(movie, num_recommendations=10):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]

    recommended_titles = []
    recommended_details = []

    for i in movie_list:
        if len(recommended_titles) >= num_recommendations:
            break

        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        similarity_score = i[1] * 100

        details = fetch_movie_details(movie_id)
        if details is None:
            continue  # skip this movie if API failed

        poster, genres, overview, rating = details
        recommended_details.append((poster, genres, overview, rating, similarity_score))
        recommended_titles.append(title)

        time.sleep(0.2)  # optional delay

    return recommended_titles, recommended_details



# CSS Styling
import streamlit as st




# Session state for advanced features
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}  # {movie_title: rating}
if 'viewed_history' not in st.session_state:
    st.session_state.viewed_history = []
if 'profile_genres' not in st.session_state:
    st.session_state.profile_genres = []





# Advanced CSS (with animations)
st.markdown("""
    <style>
    .stApp { background-color: #1a1a2e !important; color: #ffffff !important; }
    h1 { color: #FFD700 !important; text-align: center !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important; font-size: 3rem !important; animation: fadeIn 1s ease-in !important; }
    @keyframes fadeIn { from {opacity: 0; transform: translateY(-20px);} to {opacity: 1; transform: translateY(0);} }
    .stApp > div > div > div { background: rgba(26,26,46,0.9) !important; padding: 1.5rem !important; border-radius: 15px !important; margin: 0.5rem 0 !important; box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important; transition: transform 0.3s ease !important; }
    .stApp > div > div > div:hover { transform: translateY(-5px) !important; }
    .stSelectbox, .stTextInput, .stMultiSelect { background: rgba(0,0,0,0.5) !important; border-radius: 10px !important; padding: 1rem !important; }
    .stSelectbox > label, .stTextInput > label, .stMultiSelect > label { color: #FFD700 !important; font-weight: bold !important; }
    .stSelectbox > div > div > select, .stTextInput > div > input, .stMultiSelect > div > div > select { background: rgba(255,255,255,0.1) !important; color: #ffffff !important; border: 1px solid #FFD700 !important; border-radius: 8px !important; }
    .stButton > button { background: linear-gradient(45deg, #533483, #0f3460) !important; color: #ffffff !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 2rem !important; font-weight: bold !important; box-shadow: 0 4px 15px rgba(83,52,131,0.4) !important; transition: all 0.3s ease !important; }
    .stButton > button:hover { background: linear-gradient(45deg, #0f3460, #533483) !important; box-shadow: 0 6px 20px rgba(83,52,131,0.6) !important; transform: translateY(-2px) !important; }
    .recommend-header { color: #FFD700 !important; text-align: center !important; font-size: 1.8rem !important; margin: 2rem 0 1rem 0 !important; text-shadow: 1px 1px 3px rgba(0,0,0,0.8) !important; }
    .stText { color: #FFD700 !important; font-weight: bold !important; text-align: center !important; font-size: 1.1rem !important; margin-bottom: 0.5rem !important; }
    .stImage > img { border-radius: 12px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important; transition: transform 0.3s ease !important; }
    .stImage > img:hover { transform: scale(1.05) !important; }
    .stImage > figcaption { color: #FFD700 !important; font-weight: bold !important; text-align: center !important; }
    [data-testid="column"] { padding: 0.5rem !important; }
    .welcome { background: linear-gradient(135deg, #0f3460, #533483) !important; border-radius: 15px !important; padding: 2rem !important; text-align: center !important; color: #FFD700 !important; animation: fadeIn 1s ease-in !important; }
    .star-rating { color: #FFD700 !important; font-size: 1.2rem !important; }
    .similarity-bar { background: rgba(255,255,255,0.2) !important; border-radius: 10px !important; height: 8px !important; margin: 0.5rem 0 !important; }
    .similarity-fill { background: linear-gradient(90deg, #FFD700, #FF6B6B) !important; height: 100% !important; border-radius: 10px !important; transition: width 0.5s ease !important; }
    .favorite-btn { background: #FF6B6B !important; color: white !important; border-radius: 50% !important; width: 40px !important; height: 40px !important; font-size: 1.5rem !important; }
    .remove-btn { background: #FF4757 !important; color: white !important; border-radius: 5px !important; padding: 0.25rem 0.5rem !important; font-size: 0.8rem !important; }
    .stSidebar { background: rgba(26,26,46,0.95) !important; }
    .insight-box { background: rgba(255,215,0,0.1) !important; border-left: 4px solid #FFD700 !important; padding: 1rem !important; border-radius: 5px !important; margin: 1rem 0 !important; }
    .tab-content { animation: slideIn 0.5s ease-out !important; }
    @keyframes slideIn { from {opacity: 0; transform: translateX(20px);} to {opacity: 1; transform: translateX(0);} }
    </style>
""", unsafe_allow_html=True)

# Welcome Intro
with st.container():
    st.markdown(
        '<div class="welcome"><h2>🌟 Advanced Movie Discovery Engine</h2><p>AI-powered hybrid recommendations with genre filters, user ratings, analytics, and more. Explore 5000+ movies intelligently!</p></div>',
        unsafe_allow_html=True)


# Session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = []


# Sidebar favorites
with st.sidebar:
    st.header("❤ Your Favorites")
    if st.session_state.favorites:
        for fav in st.session_state.favorites[-5:]:
            st.write(fav)
    else:
        st.info("No favorites yet! Like some recommendations to save them.")

st.title("🎬 Movie Recommendation System")

# Movie dropdown (no search)
selected_movie = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Slider for number of recommendations
num_recommendations = st.slider('How many recommendations?', 5, 20, 10)

# Show selected movie info
if selected_movie:
    with st.spinner('Fetching details...'):
        time.sleep(0.5)
        selected_index = movies[movies['title'] == selected_movie].index[0]
        selected_id = movies.iloc[selected_index].id
        poster, genres, overview, rating = fetch_movie_details(selected_id)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster, use_container_width=True, caption=selected_movie)
        st.markdown(f'<div class="star-rating">⭐ {rating:.1f}/5</div>', unsafe_allow_html=True)
    with col2:
        st.subheader(selected_movie)
        st.write("Genres: " + ", ".join(genres))
        st.write("Overview: " + overview[:200] + "..." if len(overview) > 200 else overview)

# Recommendation button
if st.button('🎥 Get Recommendations'):
    with st.spinner('Generating recommendations...'):
        time.sleep(1)
        names, details = recommend(selected_movie, num_recommendations=num_recommendations)

    st.markdown('<h3 class="recommend-header">Recommended Movies:</h3>', unsafe_allow_html=True)
    idx = 0
    rows = (num_recommendations + 3) // 4
    cols_per_row = 4

    for r in range(rows):
        cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            with cols[c]:
                if idx < num_recommendations:
                    title = names[idx]
                    poster, genres, overview, rating, sim_score = details[idx]

                    if st.button('❤', key=f'fav_{idx}'):
                        if title not in st.session_state.favorites:
                            st.session_state.favorites.append(title)
                            st.success(f'Added {title} to favorites!')

                    st.markdown(f"{title}")
                    st.image(poster, use_container_width=True)
                    st.markdown(
                        f'<div class="star-rating">⭐ {rating:.1f}/5 | Genres: {", ".join(genres[:3])}</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'<div class="similarity-bar"><div class="similarity-fill" style="width: {sim_score}%;"></div></div><small>{sim_score:.0f}% Similar</small>',
                        unsafe_allow_html=True
                    )
                    st.caption(overview[:100] + "...")
                    idx += 1
                else:
                    st.empty()

                # Footer
st.markdown("---")



st.markdown("Powered by TMDB API | 'Movies are like writing fiction...' – Margot Robbies")