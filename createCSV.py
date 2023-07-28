import urllib.request as urllib
from bs4 import BeautifulSoup, Tag
import pandas as pd

def getDeckLinks():
    # past 12 months of tournament decks
    url = "https://limitlesstcg.com/decks/lists?show=100"

    page = urllib.urlopen(url).read()
    soup = BeautifulSoup(page)
    deckLinks = []

    for anchor in soup.findAll('a', href=True):
        if "/decks/list/" in anchor['href']:
            deckLinks.append(anchor["href"])

    return deckLinks

deckLinks = getDeckLinks()

def getCardNames(deckLinks, index):
    deckLink = deckLinks[index]
    deckPage = urllib.urlopen("https://limitlesstcg.com" + deckLink)
    soup = BeautifulSoup(deckPage)
    cardCounts = []
    cardNames = []

    columnDivs = soup.select(".decklist-column")

    for div in columnDivs:
        for tag in div:
            if type(tag) != Tag: continue
            if tag.attrs['class'] != ['decklist-card']: continue
            
            for div2 in tag: 
                if type(div2) != Tag: continue
                cardCounts.extend(int(span.string) for span in div2 if type(span) == Tag and span.attrs['class'] == ['card-count'])
                cardNames.extend(span.string for span in div2 if type(span) == Tag and span.attrs['class'] == ['card-name'])

    cardDict = zip(cardNames, cardCounts)
    return list(cardDict)


def getAllCards(deckLinks):
    cardSet = set()
    for i in range(len(deckLinks)):
        cardNames = [cardName for cardName, cardCount in getCardNames(deckLinks, i)]
        cardSet.update(cardNames)

    return cardSet

def convertDictToArray(row):
    newRow = []
    for cardName, cardCount in row.items():
        newRow.append(cardCount)

    return newRow

def createDf(deckLinks, allCards):
    rows = []
    for i in range(0, len(deckLinks), 2): # skip duplicated rows
        print(i)
        row = {card: 0 for card in allCards}

        cardNames = getCardNames(deckLinks, i)
        for cardName, cardCount in cardNames:
            row[cardName] = cardCount

        row = convertDictToArray(row)
        rows.append(row)

    return pd.DataFrame(data=rows, columns=allCards)
    

""" creates cardList
allCards = getAllCards(deckLinks)
with open('cardList.txt', 'w') as outfile:
  outfile.write('\n'.join(str(i) for i in allCards))
"""

allCards = open("files/cardList.txt", 'r')
allCards = [line.split(',')[0][:-1] for line in allCards.readlines()] # cut out new line
allCards = sorted(allCards)

print(allCards)
df = createDf(deckLinks, allCards)
print(df)
df.to_csv("files/deckMatrix.csv", encoding='utf-8')

