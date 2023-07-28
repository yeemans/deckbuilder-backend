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

def sortCardCategories(deckLinks, index):
    deckLink = deckLinks[index]
    deckPage = urllib.urlopen("https://limitlesstcg.com" + deckLink)
    soup = BeautifulSoup(deckPage)
    pokemon, trainers, energies = [], [], []

    columnDivs = soup.select(".decklist-column")

    for i, div in enumerate(columnDivs):
        for tag in div:
            if type(tag) != Tag: continue
            if tag.attrs['class'] != ['decklist-card']: continue
            
            for div2 in tag: 
                if type(div2) != Tag: continue
                if i == 0:
                    pokemon.extend(span.string for span in div2 if type(span) == Tag and span.attrs['class'] == ['card-name'])
                elif i == 1:
                    trainers.extend(span.string for span in div2 if type(span) == Tag and span.attrs['class'] == ['card-name'])
                elif i == 2:
                    energies.extend(span.string for span in div2 if type(span) == Tag and span.attrs['class'] == ['card-name'])
    cardCategories = (set(pokemon), set(trainers), set(energies))
    return cardCategories


pokemon, trainers, energies = set(), set(), set()
for i in range(0, len(deckLinks), 2):
    print(i)
    cardCategories = sortCardCategories(deckLinks, i)
    pokemon.update(cardCategories[0])
    trainers.update(cardCategories[1])
    energies.update(cardCategories[2])

print(pokemon)
print(trainers)
print(energies)

with open('files/pokemon.txt', 'w') as outfile:
  outfile.write('\n'.join(str(i) for i in pokemon))

with open('files/trainers.txt', 'w') as outfile:
  outfile.write('\n'.join(str(i) for i in trainers))

with open('files/energies.txt', 'w') as outfile:
  outfile.write('\n'.join(str(i) for i in energies))


