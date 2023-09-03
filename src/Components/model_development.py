import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from sklearn.neighbors import NearestNeighbors
from scipy import sparse
import pandas as pd


class ModelDevelopmentConfig:
    model_path = os.path.join("Artifacts", "model.pkl")
    csr_data_path = os.path.join("Artifacts", "csr_sparse_data.npz")
    movies_df_path = os.path.join("Artifacts", "movies.csv")
    final_dataset_path = os.path.join("Artifacts", "final_dataset.csv")

class ModelDevelopment:
    def __init__(self):
        self.model_development_config = ModelDevelopmentConfig()

    def get_recommendations(self,movie_name):
        
        df = self.initiate_model_training(movie_name)
        return df

    def initiate_model_training(self, movie_name):
        try:
            csr_data = sparse.load_npz(self.model_development_config.csr_data_path)
            logging.debug("csr data loaded")
            movies = pd.read_csv(self.model_development_config.movies_df_path)
            logging.debug("movies df loaded")

            model = NearestNeighbors(n_neighbors=10, algorithm="brute",metric="cosine")
            model.fit(csr_data)
            #movies_df = pd.read_csv(movies_df_path)
            final_dataset = pd.read_csv(self.model_development_config.final_dataset_path)
            n_movies_to_reccomend = 15
            movie_name = movie_name.title()
            movie_list = movies[movies['title'].str.contains(movie_name)] 
            print("movie_list", movie_list)
            if len(movie_list):        
                movie_idx= movie_list.iloc[0]['movieId'] 
                print("Movie_idx first value: ", movie_idx)
                movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
                print("Movie_idx second value: ", movie_idx)
                distances , indices = model.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
                rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
                recommend_frame = []
                for val in rec_movie_indices:
                    movie_idx = final_dataset.iloc[val[0]]['movieId']
                    idx = movies[movies['movieId'] == movie_idx].index
                    recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
                print("before df :", recommend_frame)
                df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
                df = df.sort_values(by=["Distance"])
                #return df
                return recommend_frame
            else:
                logging.error("No movies found, please try another one..!!")
                print("No movies found, please try another one..!!")
                return []

        except Exception as e:
            logging.error("Could not initiate model training")
            raise CustomException(e,sys)
