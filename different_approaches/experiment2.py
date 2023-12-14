# BASED ON https://medium.com/@scholarly360/mistral-7b-complete-guide-on-colab-129fa5e9a04d
# #### CopyLeft Yogendra-Sisodia
#
# import torch
# from transformers import BitsAndBytesConfig
# from langchain import HuggingFacePipeline
# from langchain import PromptTemplate, LLMChain
#
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
#
# # NOTES
# # trzeba obniżyć wersję transformers pip install transformers==4.30
# # instalacja pytorch'a z dobrą wersjąCUDA
# if __name__ == "__main__":
#     quantization_config = BitsAndBytesConfig(
#         load_in_4bit=True,
#         bnb_4bit_compute_dtype=torch.float16,
#         bnb_4bit_quant_type="nf4",
#         bnb_4bit_use_double_quant=True,
#     )
#     model_id = "mistralai/Mistral-7B-Instruct-v0.1"
#
#     model_4bit = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", quantization_config=quantization_config, )
#     tokenizer = AutoTokenizer.from_pretrained(model_id)
#
#     pipeline = pipeline(
#             "text-generation",
#             model=model_4bit,
#             tokenizer=tokenizer,
#             use_cache=True,
#             device_map="auto",
#             max_length=500,
#             do_sample=True,
#             top_k=5,
#             num_return_sequences=1,
#             eos_token_id=tokenizer.eos_token_id,
#             pad_token_id=tokenizer.eos_token_id,
#     )
#     llm = HuggingFacePipeline(pipeline=pipeline)
#
#     #### Prompt
#     template = """<s>[INST] You are a helpful, respectful and honest assistant. Answer exactly in few words from the context
#     Answer the question below from context below :
#     {context}
#     {question} [/INST] </s>
#     """
#
#     question_p = """What is the date for announcement"""
#     context_p = """ On August 10 said that its arm JSW Neo Energy has agreed to buy a portfolio of 1753 mega watt renewable energy generation capacity from Mytrah Energy India Pvt Ltd for Rs 10,530 crore."""
#     prompt = PromptTemplate(template=template, input_variables=["question","context"])
#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#     response = llm_chain.run(
#         {
#             "question": question_p,
#             "context": context_p
#         }
#     )
#     response

#### CopyLeft Yogendra-Sisodia

# import chromadb
# from chromadb.config import Settings
# from langchain.llms import HuggingFacePipeline
# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.chains import RetrievalQA
# from langchain.vectorstores import Chroma
#
# mna_news = """JSW Energy on August 10 said that its arm JSW Neo Energy has agreed to buy a portfolio of 1753 mega watt renewable energy generation capacity from Mytrah Energy India Pvt Ltd for Rs 10,530 crore.
# Sajjan Jindal led JSW group had signed an exclusivity agreement with Hyderabad based Mytrah Energy to buy the latter’s wind and solar assets.
# This is the largest acquisition by JSW Energy since inception, which comprises 17 special purpose vehicles and 1 ancillary SPV.  The transaction is subject to approval of the Competition Commission of India (CCI) and other customary approvals standard to a transaction of this size, the company said in a release.
# With this acquisition, JSW Energy's current  operational generation capacity will go up by over 35 percent from 4,784 MW to 6,537 MW.  Currently about 2,500 MW of under-construction wind and hydro projects which are likely to be commissioned in phases over the next 18-24 months, JSW Energy platform capacity gets enhanced to 9.1 GW – where the share of renewables increases to  65 percent, JSW said in a stock exchange filing. Further, this is likely to help the company in achieving its renewable-led capacity growth target of 10 GW by FY25, well ahead of timelines, the firm added.
# """
#
# from langchain.schema.document import Document
#
# if __name__ == "__main__":
#     documents = [Document(page_content=mna_news, metadata={"source": "local"})]
#     #######################
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
#     all_splits = text_splitter.split_documents(documents)
#     model_name = "sentence-transformers/all-mpnet-base-v2"
#     model_kwargs = {"device": "cuda"}
#     embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
#     #######################
#     vectordb = Chroma.from_documents(documents=all_splits, embedding=embeddings, persist_directory="chroma_db")
#     #######################
#     retriever = vectordb.as_retriever()
#     #######################
#
#     # def run_my_rag(qa, query):
#     #     print(f"Query: {query}\n")
#     #     result = qa.run(query)
#     #     print("\nResult: ", result)
#     #
#     # ### Ask Queries Now
#     # query =""" What company is buyer and seller here """
#     # run_my_rag(qa, query)