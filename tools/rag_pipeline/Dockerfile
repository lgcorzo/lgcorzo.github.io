FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/tmp \
    SYNC_STATE_FILE=/tmp/rag-sync-state.json \
    DARK_GRAVITY_BASE_URL=https://lgcorzo.github.io \
    R2R_BASE_URL=http://r2r.llm-apps.svc.cluster.local:7272 \
    R2R_COLLECTION_NAME=dark-gravity-knowledge-base

COPY tools/requirements-knowledge.txt /app/tools/requirements-knowledge.txt
RUN pip install --no-cache-dir -r /app/tools/requirements-knowledge.txt

COPY tools/rag_pipeline /app/tools/rag_pipeline
RUN groupadd -g 10001 dg && useradd -u 10001 -g 10001 -M -d /tmp dg \
    && chown -R 10001:10001 /app

USER 10001:10001
ENTRYPOINT ["python3", "-m", "tools.rag_pipeline.sync_knowledge_base"]
