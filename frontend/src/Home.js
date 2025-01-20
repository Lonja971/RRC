import "./css/Home.css";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { MessagesBlock } from "./components/messages-block";
import { MESSAGES_TYPES } from "./components/constants";

export function Home(){
    const [userRequest, setUserRequest] = useState('');
    const [messages, setMessages] = useState([
      {
        type: MESSAGES_TYPES.message,
        from: 'assistant',
        data: 'Groeten! Hoe kan ik je helpen?',
      }
    ]);
    const [crewStatus, setCrewStatus] = useState("");

    function addMessage({ messageFrom, messageData, messageType }){
      setMessages((prevMessages) => [...prevMessages, {
        from: messageFrom,
        data: messageData,
        type: messageType
      }]);
    }
  
    const handleSubmit = (e) => {
        e.preventDefault();
        let query = userRequest
        if (query){
          setUserRequest('');
  
          addMessage({
            messageFrom: "user", 
            messageData: query,
            messageType: "userMessage"
          })
          const url = `${process.env.REACT_APP_FLASK_BASE}${process.env.REACT_APP_FLASK_SEND_MESSAGE_API}`;
      
          axios.post(url, {query})
            .then((res) => {
              console.log(res)
              const message = res.data
              if(message.from !== undefined && message.data !== undefined && message.from !== "" && message.data !== ""){
                addMessage({
                  messageFrom: message.from, 
                  messageData: message.data,
                  messageType: message.type
                })
              }
              if (message.file_name) {
                addMessage({
                  messageFrom: "Bestand downloaden", 
                  messageData: message.file_name,
                  messageType: "file"
                })
              }
            })
            .catch((error) => {
              console.error('Error:', error);
            });
        }else{
          alert(`Uw aanvraag is leeg.!`)
        }

    };

    const handleKeyDown = (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleSubmit(event);
      }
    };
  
    return (
      <div className="chat">
        { crewStatus !== "" ? (
          <div className="crew-is-working-block">
            { crewStatus === "crew_working" ? (
              "Crew werkt..."
            ) : crewStatus === "user_answer" ? (
              "Crew wacht op uw antwoord..."
            ) : ""}
          </div>
        ) : ""}
        <div className="main-title">
          <h1>Requirements Refining Crew</h1>
        </div>
        <div className="chat__container">
          <MessagesBlock messages={messages} addMessage={addMessage} crewStatus={crewStatus} setCrewStatus={setCrewStatus}/>
          <div className="sendbox">
            <form onSubmit={handleSubmit} className="sendbox__form _container">
              <textarea
                type="text"
                value={userRequest}
                onChange={(e) => setUserRequest(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Voer een bericht in"
              />
              <button type="submit" className={`${!userRequest ? "inactive" : ""}`}>
                Versturen
              </button>
            </form>
          </div>
        </div>
      </div>
    );
}