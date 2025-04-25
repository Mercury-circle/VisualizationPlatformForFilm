from utils import get_df

def getMovieDetialsById(movieId):
    df = get_df()
    filmInfoTable = df.values
    movieDetails = []
    for item in filmInfoTable:
        if item[0] == movieId:
            item[17] = item[17].split(sep=',')
            movieDetails.append(list(item))
    return movieDetails

def getMovieDetialsByWords(searchWords):
    df = get_df()
    filmInfoTable = df.values
    movieDetails = []
    for item in filmInfoTable:
        if item[1].find(searchWords) != -1:
            item[17] = item[17].split(sep=',')
            movieDetails.append(item)
    return movieDetails
