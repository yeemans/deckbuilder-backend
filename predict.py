from scipy.spatial.distance import cosine
import pandas as pd
from collections import Counter

ENERGYFILE = open("files/energies.txt", 'r')
ENERGIES = allCards = [line.split(',')[0][:-1] for line in ENERGYFILE.readlines()] # cut out new line

def getTenNeighbors(cardName, data):
    sortedNames = data.loc[cardName].sort_values(ascending=False).index[:10]
    return sortedNames

def getRecommendations(deck, neighbors, data_ibs):
   allCardNames = data_ibs.index
   neighborScores = {card: 0 for card in allCardNames}

   for index, card in enumerate(allCardNames):
        for neighbor in neighbors.loc[card]:
            cardCount = deck[index]
            # do not recommend cards with 4 copies that are not energies
            if neighbor not in ENERGIES and deck[neighbor] == 4: continue
            if neighbor == card: continue # don't recommend a card to itself

            for neighborScore in data_ibs.loc[neighbor]:
                neighborScores[neighbor] += cardCount * neighborScore

    # reduce recommendation score depending on how many times card is already in deck
   realScores = []

   for card, score in neighborScores.items():
       # penalize cards that are already in deck, except energies
       if score not in ENERGIES: score /= (deck.loc[card] + 1)
       realScores.append([card, score])
       #else: realScores.append([card, score])
   recommendations = sorted(realScores, key = lambda x: x[1], reverse=True) 
   return recommendations[:10] # get ten recommendations

df = pd.read_csv("files/deckMatrix.csv")
# card vs card similarity dataframe
data_ibs = pd.DataFrame(index=df.columns,columns=df.columns)

# Lets fill in those empty spaces with cosine similarities
for i in range(len(df.columns)):
    # Loop through the columns for each column
    for j in range(len(df.columns)):
      # Fill in placeholder with cosine similarities
      data_ibs.iloc[i,j] = 1-cosine(df.iloc[:,i], df.iloc[:,j])

#print(data_ibs)
# Create a placeholder dataframe for closest neighbours to an item
neighbors = pd.DataFrame(index=data_ibs.columns,columns=range(10))
# Loop through our similarity dataframe and fill in neighbouring item names
for i in range(0,len(data_ibs.columns)):
    cardName = data_ibs.columns[i]
    neighbors.iloc[i,:10] = getTenNeighbors(cardName, data_ibs)

deck = df.iloc[-1]
recommendations = getRecommendations(deck, neighbors, data_ibs)
print(recommendations)

