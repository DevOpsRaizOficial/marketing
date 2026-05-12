# Multi-stage build pra reduzir tamanho final (~80 MB)
FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage final: só Python + deps já compiladas
FROM python:3.12-slim

# segurança: usuário não-root
RUN useradd --create-home --shell /bin/bash app
WORKDIR /home/app

# Copia deps do builder
COPY --from=builder --chown=app:app /root/.local /home/app/.local
ENV PATH=/home/app/.local/bin:$PATH

# Copia código da aplicação
COPY --chown=app:app . .

USER app

EXPOSE 8000

# Health-check builtin (Docker engine lê isso)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
