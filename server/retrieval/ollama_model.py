from langchain_ollama import ChatOllama
from ollama import chat
from flask import current_app
from chroma_db import init_vector_db
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent

def retrieval_tool(query:str,top_k=5):
    """Retrieve D&D 5e rulebook information to answer the query.
    Args: query: user question, top_k: top k most similar chunks from vectorDB
    Returns: Additional context related to the question from the 5e Rulebook"""
    #defaults 10 results
    collection = init_vector_db()
    docs = collection.query(query_texts=[query], n_results=int(top_k))
    contents = docs['documents'][0] # type: ignore
    metadatas = docs['metadatas'][0] # type: ignore
    serialized = "\n\n".join([f"CONTENT: {content}\n SOURCE: {metadata}" for content, metadata in zip(contents, metadatas)])
    return serialized

@dynamic_prompt
def prompt_with_context(request: ModelRequest):
  """Context with user query"""
  last_query = request.state['messages'][-1].text
  content = retrieval_tool(last_query)
  system_message = f"""
  You are a helpful D&D assistant. 
  Use the following context retrieved from the 5e rule-book 
  to answer questions about D&D \n\n{content}"""
  return system_message

def init_llm():
    llm = ChatOllama(
        model="llama3.1",
    )
    return llm

def init_agent():
    chat_model = init_llm()
    agent = create_agent(chat_model, tools=[], middleware=[prompt_with_context])
    return agent

def get_agent_response(query):
    agent = init_agent()
    # user_context = retrieve_user_context(campaign_id)
    # functionize and return model output
    chunks = []
    for step in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",):

        msg = step["messages"][-1]
        if hasattr(msg, "content") and msg.content:
            chunks.append(msg.content) 
    return "".join(chunks)
    

messages = [
    {"role": "system", "content":"You are a helpful D&D assistant."
    "Use the retrieval tool to get relevant information from the 5e rule-book"
    "to answer questions about D&D"},
    {"role": "user", "content": "What are the highest level druid spells and their effects?"}]
response = chat(model='llama3.1', messages = messages, tools=[retrieval_tool])
messages.append(response.message)
if response.message.tool_calls:
  print("toolCall")
  # only recommended for models which only return a single tool call
  call = response.message.tool_calls[0]
  print(call)
  result = retrieval_tool(**call.function.arguments)
  # add the tool result to the messages
  messages.append({"role": "tool", "tool_name": call.function.name, "content": str(result)})

  final_response = chat(model="llama3.1", messages=messages, tools=[retrieval_tool])
  print(final_response.message.content)