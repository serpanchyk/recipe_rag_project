```bash
docker build -t recipe-rag-assistant .

sudo docker run -d   -p 8000:8000   --env-file .env   --name rag-api   recipe-rag-assistant

python recipe_ui.py