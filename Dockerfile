FROM ghcr.io/astral-sh/uv:alpine as builder
LABEL authors="eppv"

WORKDIR /temp/outline-wiki-api
COPY . .

RUN uv sync --group docs
RUN uv run mkdocs build --site-dir /site


FROM nginx:alpine as server

COPY --from=builder /site /usr/share/nginx/html

EXPOSE 80
