import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import pandas as pd
from scipy.sparse import csr_matrix
from src.utils import save_object

class DataTransformationConfig:
    csr_data_path = os.path.join("Artifacts", "csr_sparse_data.npz")
    final_dataset_path = os.path.join("Artifacts", "final_dataset.csv")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    
    def initiate_data_transformation(self, ratings_path, movies_path):
        try:
            logging.info("Starting data transformation")

            ratings_df = pd.read_csv(ratings_path)
            movies_df = pd.read_csv(movies_path)

            ratings_pivot_table = ratings_df.pivot(index="movieId",columns="userId", values="rating") 
            logging.debug("ratings_pivot_table: {}".format(ratings_pivot_table))

            ratings_pivot_table.fillna(0, inplace=True)
            

            no_user_voted = ratings_df.groupby('movieId')['rating'].agg('count')
            no_movie_rated = ratings_df.groupby('userId')['movieId'].agg('count')

            final_dataset = ratings_pivot_table.loc[no_user_voted[no_user_voted>10].index,:]
            final_dataset = final_dataset.loc[:,no_movie_rated[no_movie_rated>50].index]

            csr_data = csr_matrix(final_dataset.values)
            final_dataset.reset_index(inplace=True)

            logging.info("csr_data created and returning")
            
            final_dataset.to_csv(self.data_transformation_config.final_dataset_path)
            logging.info("final_dataset created")

            save_object(self.data_transformation_config.csr_data_path, csr_data)
            

            return csr_data

        except Exception as e:
            logging.error("Error while datatransformation")
            raise CustomException(e,sys)