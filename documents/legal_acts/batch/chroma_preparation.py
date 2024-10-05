from src.tools.retriever.chroma import load_articles_as_documents, create_chroma_retriever
from src.utils.utils import get_legal_acts_list_from_directories, get_legal_act_json_path

if __name__ == "__main__":
    list_of_directories = get_legal_acts_list_from_directories()
    for dir_path in list_of_directories:
        dir_name = dir_path.name
        docs = load_articles_as_documents(get_legal_act_json_path(dir_name))
        retriever = create_chroma_retriever(docs, dir_name, create_new_instance=True)

