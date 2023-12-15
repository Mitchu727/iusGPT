# Development journal

## 8th December
In this week I've tried to provide context for the LLM without the usage of OpenAi embeddings (which are defaults in llama_index). 
At first, I've tried to set up mistral with chroma Db to be fully independent of commercial solutions:
 - I worked on the base of https://blog.gopenai.com/rag-pipeline-with-mistral-7b-instruct-model-a-step-by-step-guide-138df378a0c2, however this article refers to another which is behind the paywall.
 - Then I've also tried with this article https://medium.com/@scholarly360/mistral-7b-complete-guide-on-colab-129fa5e9a04d. I had to make small change regarding the creation of `llm` object. However, this approach also did not work due to the problems with `BitsAndBytes` library on windows.  
 - Similar approach was tried on the basis of this article: https://medium.com/@zekaouinoureddine/ask-your-web-pages-using-mistral-7b-langchain-f976e1e151ca, however it also did not due to the problems with `BitsAndBytes`.

I've also had doubts if mistral could answer questions in polish due to the [test on HuggingFace](https://huggingface.co/mistralai/Mistral-7B-v0.1).

Eventually I've decided to still use ChatGpt, but with custom embeddings. I supported myself with [this thread on stack overflow](https://stackoverflow.com/questions/76372225/use-llamaindex-with-different-embeddings-model). This approach worked and is currently implemented in [main.py](src/main.py), but the source file is .

All code from these attempts is saved in [different_approaches directory](different_approaches).

## 15th December

In this week I've set up repo, cleaned code a little bit and started investigating how to load civil code from pdf and cleans it so llm can correctly answer questions on the base of it.

At first, I've run the model on automatically extracted tex from pdf. Text was extracted using `PyPDF2` library. The system answered all the questions wrong.

Then I've automatically extracted only four relevant pages from PDF to check if yhe problem is in to large context or text formatting. It got a little better but still the responses are from ideal.

Another step was cleaning the articles from "Kancelaria Sejmu" footnote which could worsen embeddings quality. The system also answered wrong.

The logs show that the document is embedded line by line, so maybe it would be beneficial to fit one article into one line. It also did not work well. However, after manually reducing number of articles in a file the responses became correct. This indicates that the problem may be in numbers.

I've run into issues with limited rpm for chat gpt.

# Goal

The goal of the project is to create a cognitive assistant which is able to solve different law problems on the base of Polish law and to measure the capabilities of LLMs usage in this field. 