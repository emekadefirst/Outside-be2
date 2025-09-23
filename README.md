# Project Setup

If you're setting up the database for the first time:

```bash
# Step 1: Initialize Aerich with your Tortoise config
aerich init -t src.core.database.TORTOISE_ORM

# Step 2: Create initial database schema
aerich init-db

# Step 3: Seed the database with sample data
uv run scripts/seeds.py

find . -type d -name "__pycache__" -exec rm -rf {} +


# Create new migrations
uv run makemigrations

# Apply migrations
uv run migrate


# set wait-for-db.sh to .exe
chmod +x wait-for-it.sh

# build and run image
docker compose -f dev-docker-compose.yml up -d --build

# build Dockerfile
docker build -t ignite-app .

# run docker image
docker run -p 80:80 ignite-app

# view log
docker logs -f ignite-app

# open on browser
http://localhost:8000

# close docker image
docker compose down 

# or
docker compose -f dev-docker-compose.yml down


ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/deploy-key -N ""


Alternative Docker Commands with .env
docker-compose --env-file .env -f dev-docker-compose.yml up -d --build
docker-compose --env-file .env -f dev-docker-compose.yml up -d --build

docker compose --env-file .env --file dev-docker-compose.yml up -d --build


👉 This way, your workflow is clear:  
- Use `uv run makemigrations` and `uv run migrate` for schema changes.  
- The rest remains as in your Docker setup.  
