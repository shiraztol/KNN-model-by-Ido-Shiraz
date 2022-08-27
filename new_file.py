import pickle
import pymongo
import pandas as pd


def save_model_to_mongo(model):
    knn_model = pickle.dumps(model)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[""]
    collection = db["models"]
    collection.insert_one({"knn model":knn_model})


def load_model_from_mongo(client, database, collection):
    myclient = pymongo.MongoClient(client)
    mydb = myclient[database]
    mycol = mydb[collection]
    model = mycol.find()[0]["knn model"]
    return model


# # saving the scaler
import pymongo
import pickle
data=pickle.dumps(scaler)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Diabetes"]
collection = db["scaler"]
collection.insert_one({"data":data})