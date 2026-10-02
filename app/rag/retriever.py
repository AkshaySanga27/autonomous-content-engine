from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

ROOT=Path(__file__).resolve().parents[2]
DB=ROOT/'chroma_db'
KB=ROOT/'knowledge_base'
_collection=None

def collection():
    global _collection
    if _collection is None:
        client=chromadb.PersistentClient(path=str(DB))
        _collection=client.get_or_create_collection('brand_knowledge', embedding_function=DefaultEmbeddingFunction())
        if _collection.count()==0:
            docs=[]; ids=[]
            for f in KB.glob('*.txt'):
                docs.append(f.read_text(encoding='utf-8')); ids.append(f.stem)
            if docs: _collection.add(documents=docs, ids=ids)
    return _collection

def retrieve(query, n=2):
    r=collection().query(query_texts=[query], n_results=min(n, collection().count()))
    return '\n\n'.join(r.get('documents',[[]])[0])
