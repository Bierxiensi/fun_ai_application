from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor

api_key=""

Settings.chunk_size = 512
Settings.chunk_overlap = 50
Settings.embed_model = DashScopeEmbedding(
    model_name="text-embedding-v2",
    api_key=api_key
)
Settings.llm = DashScope(
    model=DashScopeGenerationModels.QWEN_MAX,
    api_key=api_key
)

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)
response_synthesizer = get_response_synthesizer()
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.1)],
)

if __name__ == "__main__":
    response = query_engine.query("客户经理被投诉了，投诉一次扣多少分")
    print(response)
