from flask import Flask
from flask import request
from flask_cors import CORS
import predict
import pandas as pd
import json

from pokemontcgsdk import Card

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["GET"])
def search():
    cards = Card.where(q=f"name:{request.args.get('query')} legalities.standard:legal")
    images = [card.images.small for card in cards]
    names = [card.name for card in cards]

    return {"images": images, "names": names}

@app.route("/allCards", methods=["GET"])
def getAllCards():
    allCards = open("files/cardList.txt", 'r')
    allCards = [line.split(',')[0][:-1] for line in allCards.readlines()] # cut out new line
    allCards.sort()
    return {"cards": allCards}

@app.route("/recommend", methods=["GET"])
def recommend():
    deck = stringToArray(request.args.get('deck'))

    # make a dataframe out of deck with each card in allCards as neighbors 
    cardFile = open("files/cardList.txt", 'r')
    allCards = [line.split(',')[0][:-1] for line in cardFile.readlines()]
    allCards.sort()
    df = pd.DataFrame(data=[deck], columns=allCards)

    recommendations = predict.getRecommendations(df.loc[0], predict.neighbors, predict.data_ibs)
    return {"recommendations": recommendations}

def stringToArray(array):
    # turn stringified array from client side to a python list
    array = array.split(",")
    return [int(cardCount) for cardCount in array]
