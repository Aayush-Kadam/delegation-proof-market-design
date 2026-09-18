FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 MPLBACKEND=Agg
WORKDIR /research
COPY requirements-lock.txt pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY scripts ./scripts
COPY paper ./paper
COPY results ./results
COPY docs ./docs
COPY configs ./configs
COPY REPRODUCIBILITY.md RESULTS_INDEX.md ./
RUN python -m pip install --no-cache-dir -r requirements-lock.txt && python -m pip install --no-cache-dir -e .
CMD ["python", "-m", "pytest", "-q"]
