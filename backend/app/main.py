from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import TextInput, TagResponse, TaggedNode, EpistemologyTag
from app.epistemology_engine import EpistemologyEngine
import time
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Epistemology Mapper", debug=settings.API_DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = EpistemologyEngine(min_confidence=settings.MIN_CONFIDENCE_THRESHOLD)
graph = {"nodes": [], "links": []}

@app.post("/api/tag/text", response_model=TagResponse)
async def tag_text(input_data: TextInput):
    start = time.time()
    text = input_data.text.strip()
    if len(text) > settings.MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text too long (max {settings.MAX_TEXT_LENGTH})")
    
    tags = engine.detect_epistemologies(text)
    tags = tags[:settings.MAX_TAGS_PER_TEXT]
    
    node = TaggedNode(
        id=str(uuid.uuid4()),
        text=text[:200],
        tags=tags,
        source_type="text"
    )
    graph["nodes"].append(node)
    if len(graph["nodes"]) > 1:
        graph["links"].append({
            "source": graph["nodes"][-2].id,
            "target": node.id
        })
    
    processing_time = round(time.time() - start, 3)
    
    logger.info(f"Processed text with {len(tags)} tags in {processing_time}s")
    
    return TagResponse(
        success=True,
        node=node,
        error=None,
        processing_time=processing_time
    )

@app.get("/api/epistemologies")
async def list_epistemologies():
    return engine.explanations

@app.get("/api/graph")
async def get_graph():
    return graph

@app.get("/api/stats")
async def get_stats():
    total_nodes = len(graph["nodes"])
    total_links = len(graph["links"])
    
    tag_counts = {}
    for node in graph["nodes"]:
        for tag in node.tags:
            tag_name = tag.name.value
            if tag_name in tag_counts:
                tag_counts[tag_name] += 1
            else:
                tag_counts[tag_name] = 1
    
    return {
        "total_nodes": total_nodes,
        "total_links": total_links,
        "tag_distribution": tag_counts
    }
