# Requirements Refining Crew

**Requirements Refining Crew** is a project built with React and Crewai that assists in generating Scrum tasks based on a project topic. The user inputs a topic, and the application automatically creates relevant tasks for efficient project management.

## 📚 Tech Stack

- **Frontend**: React
- **Backend**: Flask (Python) with Crewai integration

## ✨ Functionality

- **Scrum Task Generation**: Creates Scrum tasks based on the provided project topic.
- **Interactive Task Management**: Offers an interface to manage generated tasks.
- **AI-Driven Task Creation**: Uses artificial intelligence to analyze and create appropriate tasks based on input.

## 🚀 Getting Started

### 1. Clone the Repository
First, clone this repository to your local machine using the following command:

```
git clone git@bitbucket.org:mixcom-repo/crewai-analysis.git
```
After downloading the repository, go one folder down (to the project folder).

### 2. Install Python Dependencies
Navigate to the backend directory and install all Python dependencies specified in pyproject.toml

```
cd backend
poetry shell
poetry install
```

### 3. Set Up Environment Variables
To configure the application, you need to set up environment variables for both the **frontend** and **backend**. These variables define key settings for the application.

#### Steps:
1. Locate the `.env-template` file in both the `/frontend` and `/backend` folders.
2. For each folder, follow these steps:
   - Copy the contents of the `.env-template` file.
   - Сreate the new `.env` file in a text editor.
   - Paste the copied content into a new `.env`.

! The data for the flask server for both .env in the /frontend and /backend folders must be the same.

### 4. Start the Frontend Application
First you need to install all npm dependencies.
Navigate to the frontend directory:

```
cd frontend
```
Install dependencies:
```
npm install
```
Now you can start the React server:
```
npm run start
```

### 5. Start the Flask Server
Navigate to the backend/crewai directory and run the Flask server:

```
cd backend/crewai
python server.py
```