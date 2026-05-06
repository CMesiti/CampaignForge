from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from server.retrieval.chroma_db import get_vector_db
from server.retrieval.chat_model import get_chat_model
from flask import current_app, g
from server.services.campaignService import CampaignService
from server.services.playerCharService import PlayerService

def retrieve_user_context(campaign_id=None):
   #get the current users information to supply as context. This includes basic 
   player_service = PlayerService()
   campaign_service = CampaignService()
   current_campaign = campaign_service.get_campaign_by_id(campaign_id)
   campaign_characters = player_service.get_campaign_players(campaign_id)
   current_campaign = {'description': current_campaign['description'], 'title':current_campaign["title"]}
   campaign_characters = [{'name':char['character'],
                           'class':char['classes'] , 
                           'stats':char['stats'], 
                           'level': char['level'], 
                           'hitpoints':char['hitpoints'],} for char in campaign_characters]
   return {"Campaign":current_campaign, "Party":campaign_characters}

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
  Use the following context retrieved from the 5e rule-book 
  to answer questions about D&D \n\n{content}"""
  return system_message

def init_agent():
    chat_model = get_chat_model()
    agent = create_agent(chat_model, tools=[], middleware=[prompt_with_context])
    current_app.config['RULEBOOK_AGENT'] = agent

def get_agent():
    return current_app.config['RULEBOOK_AGENT']

def get_agent_response(query, campaign_id):
    try:
        agent = get_agent()
        user_context = retrieve_user_context(campaign_id)
        # functionize and return model output
        chunks = []
        for step in agent.stream(
            {"messages": [{"role": "user", "content": query + 
                        f"The current party and campaign is as follows: {user_context}"}]},
            stream_mode="values",):

            msg = step["messages"][-1]
            if hasattr(msg, "content") and msg.content:
                chunks.append(msg.content) 
        return "".join(chunks)
    except Exception as e:
       raise Exception(e)