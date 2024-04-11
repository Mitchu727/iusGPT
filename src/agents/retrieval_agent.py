from abc import ABC, abstractmethod

class RetrievalAgent(ABC):
    @abstractmethod
    def answer(self, question: str) -> str:
        pass


class DummyRetrievalAgent(RetrievalAgent):
    def answer(self, question: str) -> str:
        return "I don't know"