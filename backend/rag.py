from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_mistralai import ChatMistralAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


llm = ChatMistralAI(
    model="mistral-large-latest",
    mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0.2
)

prompt = PromptTemplate(
    template="""
       You are a helpful assistant.
       Answer ONLY from the provided transcript context.
       If the context is insufficient, just say you don't know.

       {context}
       Question: {question}
       """,
    input_variables=["context", "question"]
)

def format_docs(retrieved_docs):
    return " ".join(doc.page_content for doc in retrieved_docs)

def extract_video_id(url: str):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return parse_qs(parsed.query).get("v", [None])[0]

def build_rag_chain(youtube_url: str):
    # 1. Fetch transcript
    video_id = extract_video_id(youtube_url)
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id, languages=["en"])
        transcript = " ".join(chunk.text for chunk in transcript_list)
    except TranscriptsDisabled:
        raise ValueError("Transcript is disabled for this video")

    # 2. Chunk
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    chunks = text_splitter.create_documents([transcript])

    # 3. Embed and store
    vector_store = FAISS.from_documents(chunks, embeddings)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    # 4. Build chain
    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_docs),
        'question': RunnablePassthrough()
    })
    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain