from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools.retriever import create_retriever_tool


from .urlscrape import crawl_with_prefix

start_url = "https://www.thehindubusinessline.com/opinion"
depth = 2
urls = crawl_with_prefix(start_url, depth)

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits, embedding=embeddings
)

retriever = vectorstore.as_retriever()

# Can create multiple retrieval tools
retriever_tool = create_retriever_tool(
    retriever,
    "opinions",
    "Search and return information about opinions of the Hindustan Times.",
)

def generate_query_or_respond(state, response_model):
    """Call the model to generate a response based on the current state. Given
    the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
    """
    response = (
        response_model
        # Attach those tools here
        .bind_tools([retriever_tool]).invoke(state["messages"])
    )
    return {"messages": [response]}