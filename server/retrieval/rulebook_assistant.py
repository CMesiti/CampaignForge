from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from server.retrieval.chroma_db import get_vector_db
from server.retrieval.chat_model import get_chat_model
from flask import current_app


def retrieve_context(query: str, top_k = 5):
  """Retrieve D&D 5e rulebook information to answer the query."""
  #defaults 10 results
  collection = get_vector_db()
  docs = collection.query(query_texts=[query], n_results=top_k)
  contents = docs['documents'][0]
  metadatas = docs['metadatas'][0]
  serialized = "\n\n".join([f"CONTENT: {content}\n SOURCE: {metadata}" for content, metadata in zip(contents, metadatas)])
  return docs, serialized

#Simple 2-step RAG solution,
@dynamic_prompt
def prompt_with_context(request: ModelRequest):
  """Context with user query"""
  last_query = request.state['messages'][-1].text
  retrieved_docs, content = retrieve_context(last_query)
  system_message = f"""
  You are a helpful D&D assistant. 
  Use the following context retrieved from the 5e rulebook 
  to answer questions about D&D \n\n{content}"""
  return system_message

def init_agent():
    chat_model = get_chat_model()
    agent = create_agent(chat_model, tools=[], middleware=[prompt_with_context])
    current_app.config['RULEBOOK_AGENT'] = agent

def get_agent():
    return current_app.config['RULEBOOK_AGENT']

def get_agent_response(query):
    agent = get_agent()
    # functionize and return model output
    response = ""
    for step in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        msg = step["messages"][-1]
        if hasattr(msg, "content") and msg.content:
            response += msg.content 
    return response