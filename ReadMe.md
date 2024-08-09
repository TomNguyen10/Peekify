# A web application generate your weekly Spotify Wrapped

_Under Deverlopment_

## Running Frontend
Change the directory to the frontend folder
```
cd frontend
```

### Setting up the environment
```
npm install
```

### Run the application
```
npm run dev
```

# Running Backend
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

## Option 2: Using Docker (Recommended) (Require docker desktop installation)
Build the docker image and name it to peekify
```
docker build -t peekify .
```
Run the a docker image with the new built image and also name it peekify
```
docker run --name peekify -d -p 8000:8000 peekify 
```
# Note
- Always make sure the .env file is created and is included in .gitignore
