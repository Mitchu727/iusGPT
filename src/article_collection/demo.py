from chroma_db_collection import get_civil_code_collection, print_results
from embeddings import sentence_transformer

if __name__ == "__main__":
    civil_code_collection = get_civil_code_collection()

    question = """
            Stan faktyczny:
            Błażej ma 30 lat i nie jest ubezwłasnowolniony
            Pytanie:
            Odpowiedz czy posiada pełną zdolność do czynności prawnych.
        """

    print(question)
    results = civil_code_collection.query(
        query_texts=[question],
        n_results=10
    )
    print_results(results)

    question = """
        Ubezwłasnowolnienie
        """

    print(question)
    results = civil_code_collection.query(
        query_texts=[question],
        n_results=10
    )
    print_results(results)


    question = """
        Gospodarstwo rolne
        """

    print(question)
    results = civil_code_collection.query(
        query_texts=[question],
        n_results=10
    )
    print_results(results)
