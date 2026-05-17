from langchain_community.chat_models import ChatLlamaCpp
from huggingface_hub import hf_hub_download
from flask import current_app

def init_llm():
    model_path = hf_hub_download(repo_id="bartowski/Meta-Llama-3.1-8B-Instruct-GGUF", filename="Meta-Llama-3.1-8B-Instruct-Q4_K_S.gguf")

    chat_model = ChatLlamaCpp(temperature=0.5,
        model_path=model_path,
        n_ctx=4096,
        n_gpu_layers=35,
        n_batch=256,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
        f16_kv=True,
        max_tokens=1024)
    current_app.config["CHAT_MODEL"] = chat_model

def get_chat_model():
    return current_app.config["CHAT_MODEL"]