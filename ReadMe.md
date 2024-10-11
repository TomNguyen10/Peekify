# A web application generates your weekly Spotify Wrapped

_Under Deverlopment_

## Introduction

Hello there, I hope you're having a good day. Let me introduce myself, my name is Peekify, your Spotify diary.
What I can do is to track your listening activities on Spotify (of course only when you allow me to) and send you a report every week. More specifically, I will analyze your data and send you the report on Monday morning. The report will include your top songs, artists, and albums of the week. I will also analyze your mood compared to the previous weeks to see how you've been doing and give you some advice.

Right now I can only analyze your listening activities for songs (No podcasts or books) I'm sorry :< I will work on that more in the future. I will also develop a feature where you can connect with your friends on the App (Stay tuned)

## Tech Stack

Below is the link to my tech stack:
[Link text](https://lucid.app/publicSegments/view/5948e8ad-71a3-49ef-b8d4-76bee37899be/image.png)

Users will interact with me through the browser where they encounter my Frontend which I use React and Typescript. My backend is built with FastAPI and communicates with the frontend by GraphQL protocol. When you are logged in, you allow me to access your Spotify account to retrieve data and store it in my personal PostgreSQL database hosted in Supabase. I will analyze that data with my own A.I agent (built with LangChain, PyTorch, and some LLMs) and produce your report every week. The report will be stored in MongoDB since it is unstructured data and ready to be sent on Monday morning to yall through GMAIL. Every other data will be dumped into AWS S3 for backup.

## Tech Stack

## Running Frontend

Change the directory to the frontend folder

```
cd frontend
```

Setting up the environment

```
npm install
```

Run the application

```
npm run dev
```

## Running Backend

Change the directory to the backend folder

```
cd backend
```

Add a .env file with these variables:

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
POSTGRESQL_SOURCE=your_postgresql_source
MONGODB_URL=your_mongodb_url
SPOTIFY_API_BASE_URL=your_spotify_api_base_url
```

## Option 1: Run manually

Install the requirements

```
pip install -r requirements.txt
```

Run the server locally

```
cd app
```

```
uvicorn main:app --reload
```

## Option 2: Running Docker Image on Docker Hub (Require docker desktop installation) (Recommended)

Pull the docker image from tom10117/peekify

Run a new container with the pull image from Docker Desktop

# Note

- Always make sure the .env file is created and is included in .gitignore
