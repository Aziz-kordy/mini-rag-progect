

from stores.LLM.LLmfactory import LLMFactory
from stores.vectordb.vectordb_factory import VectorDBFactory
from fastapi import FastAPI

from helpers.config import get_settings,Settings
from motor.motor_asyncio import AsyncIOMotorClient       
from routes import base,data,nlp
from stores.LLM.templates.template_parser import TemplateParser 

app=FastAPI()
@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_connection = AsyncIOMotorClient(settings.mongodb_url)
    app.db_client = app.mongodb_connection[settings.mongodb_database]
    
    llm_factory=LLMFactory(settings)
    app.generation_client=llm_factory.create(provider_name=Settings().GENERATION_MODEL_NAME)
    app.generation_client.set_generation_model_id(model_id=Settings().GENERATION_MODEL_ID)
    
    app.embedding_client=llm_factory.create(provider_name=Settings().EMBEDDING_MODEL_NAME)
    app.embedding_client.set_embedding_model_id(model_id=Settings().EMBEDDING_MODEL_ID,model_size=Settings().EMBEDDING_MODEL_SIZE)
    
    
    vectordb_factory=VectorDBFactory(settings)
    app.vectordb_client=vectordb_factory.create(provider_name=Settings().VECTOR_DB_NAME)
    app.vectordb_client.connect()
    
    app.template_parser=TemplateParser(language=Settings().PRIME_LANGUAGE ,default_language=Settings().DEFAULT_LANGUAGE)
    
    
    
app.include_router(base.base_router) 
app.include_router(data.data_router)


app.on_event("startup")(startup_db_client)
app.include_router(nlp.nlp_router)