from typing import List
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain.tools.retriever import create_retriever_tool
import os

os.environ["AWS_REGION"] = "us-east-2"

# ---------- Initialization Block (runs once when module is imported) ---------- #

print("[RAG INIT] Loading web content...")
urls = [
    "https://www.tata.com/about-us/sustainability",
]
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

print(f"[RAG INIT] Loaded {len(docs_list)} raw documents. Splitting...")

# Split content
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100,
    chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)
print(f"[RAG INIT] Split into {len(doc_splits)} document chunks.")

# Embeddings and Vector DB
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=embeddings
)
retriever = vectorstore.as_retriever()

# Tool for RAG
retriever_tool = create_retriever_tool(
    retriever,
    name="tata",
    description="Sustainability Activities",
)

# Chat Model
print("[RAG INIT] Initializing Claude 3.5 Sonnet...")
llm = init_chat_model("us.anthropic.claude-3-5-sonnet-20240620-v1:0", model_provider="bedrock_converse")
response_model = llm.bind_tools([retriever_tool])
print("[RAG INIT] Ready for querying.")

# ---------- Function to be called externally ---------- #

def run_rag_query(prompt: str) -> str:
    """
    Takes a user prompt and returns a Claude 3.5-based RAG response as a string.
    """
    input_state = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    }

    try:
        response = response_model.invoke(input_state["messages"])

        # Check for tool use
        while hasattr(response, "tool_calls") and response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_output = retriever_tool.invoke(tool_call["args"])

            tool_message = ToolMessage(
                tool_call_id=tool_call["id"],
                content=str(tool_output),
            )

            response = response_model.invoke(input_state["messages"] + [response, tool_message])

        return response.content.strip()

    except Exception as e:
        return f"❌ Error during query: {str(e)}"
