# Travel AI

> Your intelligent, blazing-fast travel companion for exploring Magical Kenya.

Travel AI is a modern full-stack application designed to help users plan trips, discover hidden gems, and get instant recommendations about Kenyan destinations. Unlike standard chatbots, Travel AI grounds its knowledge in authentic data scraped directly from official tourism sources, ensuring accurate and highly relevant travel advice.

---

## For Non-Technical Readers: What is Travel AI?

Imagine having a local Kenyan tour guide available 24/7. Travel AI is exactly that—a smart chat assistant that knows the ins and outs of Kenya's best destinations, from the white sands of Diani Beach to the wildlife of the Maasai Mara.

**Key Features:**
- **Instant Answers**: Powered by ultra-fast AI (Groq), the assistant replies to your questions in just over a second.
- **Authentic Knowledge**: The AI doesn't just guess; it reads real data from the *Magical Kenya* tourism board to provide factual recommendations.
- **Premium Experience**: A beautiful, glass-like dark mode interface makes trip planning visually stunning and intuitive.

---

## For Developers: Technical Overview

Travel AI is a Retrieval-Augmented Generation (RAG) application leveraging a modern, containerized microservices architecture.

### The Tech Stack

- **Frontend**: React, TypeScript, TailwindCSS, Vite (with a custom Glassmorphic UI)
- **Backend API**: Python, FastAPI
- **LLM Engine**: LangChain + **Groq** (`llama-3.1-8b-instant`) for blazing-fast inference latency (~1.3s).
- **Vector Database**: **Qdrant** for storing and querying embedded text chunks.
- **Embeddings**: Local **Ollama** running `nomic-embed-text` to ensure privacy and cost-efficiency for vector embeddings.
- **Relational DB**: **PostgreSQL** for application state and future user management.
- **Infrastructure**: Fully containerized using **Docker** and orchestrated via `docker-compose.yml`, fronted by **Nginx**.

### How it Works
1. **Data Ingestion (`/scrape`)**: The backend scrapes official destination pages from `magicalkenya.com`, chunks the HTML text, converts them to vector embeddings using Ollama, and upserts them into Qdrant.
2. **Retrieval (RAG)**: When a user asks a question, the query is embedded and matched against Qdrant to find the most relevant Magical Kenya context.
3. **Generation**: The context and the user's prompt are sent to the Groq API, which streams back a highly accurate, context-aware markdown response to the React frontend.

---

## Getting Started (Local Development)

### Prerequisites
- Docker and Docker Compose
- API Keys: You will need a free API key from [Groq Console](https://console.groq.com/keys).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/25thOliver/travelAI.git
   cd travelAI
   ```

2. **Configure Environment Variables:**
   ```bash
   cp .env.example .env
   # Open .env and add your GROQ_API_KEY
   ```

3. **Start the Infrastructure:**
   Spin up the entire stack (FastAPI, React Frontend, Postgres, Qdrant, Ollama, Nginx) with one command:
   ```bash
   docker compose up -d --build
   ```

4. **Initialize the Vector Database:**
   Once the containers are running, you need to populate the AI's "brain" with destination data.
   Run this cURL command to trigger the Magical Kenya scraper:
   ```bash
   curl -X POST http://localhost:8000/scrape \
        -H "X-API-Key: YOUR_API_KEY_FROM_ENV"
   ```

5. **Start Chatting!**
   Open your browser and navigate to exactly:
   [http://localhost:3000](http://localhost:3000)

---

## Deployment instructions

To share this app publicly, the easiest method is deploying the entire Docker stack to a single Virtual Private Server (VPS) like a DigitalOcean Droplet, Hetzner, or AWS EC2 instance. 

Because local `Ollama` is required for the embeddings, standard serverless platforms (like Vercel or Render) are not recommended.

1. SSH into your VPS.
2. Clone this repository.
3. Set your `.env` variables.
4. Run `docker compose up -d --build`.
5. Your app will automatically be served on port `80` via the included Nginx container, making it accessible via your server's public IP Address!

---
