from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# Load model lazily to save startup time if unused and save memory
model = None

def get_model():
    global model
    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def group_texts(texts: list[str], num_clusters: int = 3):
    if len(texts) < num_clusters:
        num_clusters = max(1, len(texts))
        
    encoder = get_model()
    embeddings = encoder.encode(texts)
    
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    clusters = kmeans.fit_predict(embeddings)
    
    # Reduce to 2D for visualization
    if len(texts) > 1:
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(embeddings)
    else:
        reduced = np.array([[0.0, 0.0]])
        
    result = []
    for i, txt in enumerate(texts):
        result.append({
            "text": txt[:80] + "...",
            "cluster": int(clusters[i]),
            "x": float(reduced[i][0]),
            "y": float(reduced[i][1])
        })
    return result
