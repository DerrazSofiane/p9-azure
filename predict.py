import pickle
from scipy import sparse



def test_func(word:str) -> str:
    return f"your word is {word}"


def implicit_predict(userid:int, n:int=5):
    """Recommend n articles for a given userid that he never saw.

    Args:
        userid (int): Id of the user we want to recommend articles
        n (int, optional): Number of articles we want to recommend. Defaults to 5.

    Returns:
        dict: Article ids with their score of prediction.
    """
    # Chargement du modèle
    with open("implicit_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Chargement de la matrice users/items/ratings
    matrix_data = sparse.load_npz("matrix.npz")
    
    # Sélection des données de l'utilisateur
    user_items = matrix_data.tocsr()[userid]
    
    # Prédiction du modèle
    articles, scores = model.recommend(userid, user_items, N=5, filter_already_liked_items=True)
    
    recommendations = {}
    for idx, (article, score) in enumerate(zip(articles, scores)):
        recommendations[idx+1] = {
            "article_id": int(article),
            "score" : float(score)}
        
    return recommendations
