# AI-Chatbot

# 🤖 Retrieval-Augmented Generation (RAG) Chatbot

A Retrieval-Augmented Generation (RAG) AI chatbot built with **FastAPI** (backend) and **Streamlit** (frontend), containerized with Docker, and deployed on **AWS EC2**.  

---

## 📂 Project Structure
AI-chatbot/
│── backend/ # FastAPI backend
│ ├── main.py
│ ├── requirements.txt
│ ├── Dockerfile
│ └── assets/
│
│── frontend/ # Streamlit UI
│ ├── app.py
│ ├── requirements.txt
│ ├── Dockerfile
| ├── assets/
│
│── docker-compose.yml # Compose setup for backend + frontend
│── .env # AWS credentials(please make it on your own in the root with access private and modelid)
│── .github/workflows/ # CI/CD pipeline
│── README.md


---

## 🚀 Features

- ✅ **FastAPI Backend** – API endpoints to communicate with Amazon Bedrock & stream responses.  
- ✅ **Streamlit Frontend** – Chat UI with live streaming responses.  
- ✅ **Containerized** – Separate Dockerfiles for backend and frontend.  
- ✅ **Orchestrated** – `docker-compose.yml` for multi-service setup.  
- ✅ **AWS EC2 Deployment** – Full system runs in the cloud.  
- ✅ **CI/CD** – Automated builds & checks using GitHub Actions.  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/sonicisastorm/AI-Chatbot.git
cd AI-Chatbot
```

## 2️⃣ Environment Variables
```bash
Create a .env file in the project root:
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
MODEL_ID=your-modelid
```
3️⃣ Install Dependencies (locally)

I recommend uv
Backend: 
```bash
cd backend
uv sync
```
Frontend:
```bash
cd frontend
uv sync

```
4️⃣ Run Locally with Docker
```bash
docker-compose up --build
```
```bash
Backend: http://localhost:8000/docs
Frontend: http://localhost:8501
```

☁️AWS EC2 Deployment

Launch an EC2 instance and SSH into it:
```bash
ssh -i your-key.pem ubuntu@<EC2-IP>
```
Install Docker & Docker Compose.

Clone repo:
```bash
git clone https://github.com/sonicisastorm/AI-Chatbot.git
cd AI-Chatbot
```
Copy your .env file to the EC2 instance.

Deploy:
```bash
docker-compose up --build -d
```
# 📸 Screenshots
Backend
![backend](https://github.com/sonicisastorm/AI-Chatbot/blob/main/backend/assets/FastAPI%20-%20Swagger%20UI.png)
Frontend
![frontend](https://github.com/sonicisastorm/AI-Chatbot/blob/main/frontend/assets/Claude%20Sonnet%20RAG%20Chatbot.png)
EC2
![EC2](https://github.com/sonicisastorm/AI-Chatbot/blob/main/workflows/docker-compose%20ps.png)

