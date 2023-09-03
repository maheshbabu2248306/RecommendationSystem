import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from src.Components.data_transformation import DataTransformation, DataTransformationConfig
from src.Components.model_development import ModelDevelopment, ModelDevelopmentConfig

# To store the data from the source in the Artifacts directory
class DataIngestionConfig:
    movies_dataset_path = os.path.join("Artifacts", "movies.csv")
    ratings_dataset_path = os.path.join("Artifacts", "ratings.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        try:
            ratings = pd.read_csv("Notebook\\ratings.csv")
            movies = pd.read_csv("Notebook\movies.csv")
            
            logging.info("Read the datasets from the notebook folder")

            ratings.to_csv(self.data_ingestion_config.ratings_dataset_path)
            movies.to_csv(self.data_ingestion_config.movies_dataset_path)

            return self.data_ingestion_config.ratings_dataset_path, self.data_ingestion_config.movies_dataset_path

        except Exception as e:
            logging.error("Error while inititating the data ingestion")
            raise CustomException(e,sys)
    
if __name__ == "__main__":

    data_ing = DataIngestion()
    ratings_path, movies_path = data_ing.initiate_data_ingestion()
    transformation_obj = DataTransformation()
    data = transformation_obj.initiate_data_transformation(ratings_path, movies_path)
    print("sparse data: ",data)
    model = ModelDevelopment()
    model.get_recommendations("iron man")