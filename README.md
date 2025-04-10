# Requirements Refining Crew

**Requirements Refining Crew** is een chatwebsite met kunstmatige intelligentie die projectbeschrijvingen analyseert en op basis daarvan User Stories en Taken genereert voor het Scrum-bord. Hierdoor kunnen ontwikkelaars sneller en efficiënter werken binnen het Scrum-framework.

## ✨ Functionality

- **Scrum Task Generation**: Creates Scrum tasks based on the provided project topic.
- **Interactive Task Management**: Offers an interface to manage generated tasks.
- **AI-Driven Task Creation**: Uses artificial intelligence to analyze and create appropriate tasks based on input.

## 📚 Tech Stack

- **Frontend**: React.js
- **Backend**: Python (Flask), CrewAI framework
- **AI integratie**: CrewAI agents (LLM pipelines)

## 🧱 Architectuur

Het systeem is opgedeeld in twee hoofdcomponenten:

- **Frontend**: gebruikers voeren hun input in via een chatinterface

- **Backend**: AI verwerkt input via CrewAI-agents en retourneert gestructureerde output De frontend communiceert met de backend via een REST API.

## API

#### Download het bestand.

```
  ${domain}/api/download/${filename}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Method`  | `GET`    |                                   |
| `filename`| `string` | **Required** Filename.            |

#### Stuur een bericht.

```
  ${domain}/api/send_message/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Method`  | `POST`   |                                   |
| `query   `| `string` | **Required** Berichtentest.       |

#### Alle berichten ontvangen.

```
  ${domain}/api/return_answer/
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Method`  | `GET`    |                                   |

## 🚀 Getting Started

### 1. Clone the Repository
First, clone this repository to your local machine using the following command:

```
git clone https://github.com/Lonja971/RRC.git
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