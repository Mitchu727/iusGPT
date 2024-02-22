from src.secrets import OPEN_API_KEY, HUGGING_FACE_API_KEY
from chromadb.utils import embedding_functions

sentence_transformer = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HUGGING_FACE_API_KEY,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)