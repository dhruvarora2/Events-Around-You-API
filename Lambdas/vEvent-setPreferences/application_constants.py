
genreId = {
    
    'R&B': 'KnvZfZ7vAee',
    'hip-hop': 'KnvZfZ7vAv1',
    'rap' : 'KnvZfZ7vAv1',
    'classical': 'KnvZfZ7v7nJ',
    'jazz': 'KnvZfZ7vAvE',
    'foreign': 'KnvZfZ7vAk1',
    'dance': 'KnvZfZ7vAvF',
    'electronic':'KnvZfZ7vAvF',
    'comedy': 'KnvZfZ7vAkA',
    'animation': 'KnvZfZ7vAkd',
    'music': 'KnvZfZ7vAkJ',
    'miscellaneous': 'KnvZfZ7vAka',
    'family': 'KnvZfZ7vAkF',
    'miscellaneous theatre': 'KnvZfZ7v7ld',
    'theatre': 'KnvZfZ7v7l1'
}

categoryList = ["arts & theatre", "film", "miscellaneous", "music", "sports", "undefined", "donation", "event style", "group", "individual", "merchandise", "nonticket", "parking", "transportation", "upsell", "venue based"]


def isValidCategory(category):
    if category in categoryList:
        return True
    else:
        return False
    
def isValidGenre(genre):
    if genre in genreId:
        return True
    else:
        return False

def getGenreId(genre):
    if genre.lower() in genreId:
        return genreId[genre.lower()]
    else:
        return None
