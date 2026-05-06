from langchain_ollama import ChatOllama
from langchain.tools import tool
from flask import current_app
from langchain.messages import AIMessage
from chroma_db import init_vector_db
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent

def retrieval_tool(query:str,top_k=5):
    """Retrieve D&D 5e rulebook information to answer the query."""
    #defaults 10 results
    collection = init_vector_db()
    docs = collection.query(query_texts=[query], n_results=top_k)
    contents = docs['documents'][0] # type: ignore
    metadatas = docs['metadatas'][0] # type: ignore
    serialized = "\n\n".join([f"CONTENT: {content}\n SOURCE: {metadata}" for content, metadata in zip(contents, metadatas)])
    return serialized

@dynamic_prompt
def prompt_with_context(request: ModelRequest):
  """Context with user query"""
  last_query = request.state['messages'][-1].text
  retrieved_docs, content = retrieval_tool(last_query)
  system_message = f"""
  You are a helpful D&D assistant. 
  Use the following context retrieved from the 5e rule-book 
  to answer questions about D&D \n\n{content}"""
  return system_message

def init_llm():
    llm = ChatOllama(
        model="llama3.1",
    )
    print(type(llm))
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
    
get_agent_response("I need information on the druid level 1 spells")



# llm = init_llm()
# messages = [
#     ("system", """You MUST call the retrieval_tool before answering.
#      Do NOT answer from prior knowledge. Always call the tool first."""),
#     ("human", "I need information on the druid level 1 spells"),
# ]
# res = llm.invoke(messages)
# if isinstance(res, AIMessage) and res.tool_calls:
#     print("TOOL CALL: ",res.tool_calls)
# print(res.content)