import axios from "axios";
import { useState, useEffect, useRef } from "react";
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { MESSAGES_TYPES } from "./constants";

export function MessagesBlock({ messages, addMessage, crewStatus, setCrewStatus }) {
    const [expandedMessages, setExpandedMessages] = useState([]);
    const [isUserScrolling, setIsUserScrolling] = useState(false);

    useEffect(() => {
        const fetchInputRequest = async () => {
            try {
                const url = `${process.env.REACT_APP_FLASK_BASE}${process.env.REACT_APP_FLASK_RETURN_ANSWER_API}`;
                const response = await axios.get(url);
                const message = response.data;
                console.log(message)
                
                if (message.crew_status === "crew_working") {
                    if (crewStatus !== "crew_working") {
                        setCrewStatus("crew_working");
                    }
                } else if(message.crew_status === "user_answer") {
                    if (crewStatus !== "user_answer") {
                        setCrewStatus("user_answer");
                    }
                } else {
                    setCrewStatus("");
                }

                if (message.from && message.data && message.from !== "" && message.data !== "") {
                    addMessage({
                        messageFrom: message.from,
                        messageData: message.data,
                        messageType: message.type ? message.type : "message",
                    });
                }
            } catch (error) {
                console.error("Error fetching input request:", error);
            }
        };

        fetchInputRequest();
        const intervalId = setInterval(fetchInputRequest, 1000);

        return () => clearInterval(intervalId);
    }, [addMessage]);

    useEffect(() => {
        const handleScroll = () => {
          const scrollPosition = window.scrollY + window.innerHeight;
          const scrollHeight = document.body.scrollHeight;
    
          if (scrollPosition < scrollHeight - 10) {
            setIsUserScrolling(true);
          } else {
            setIsUserScrolling(false);
          }
        };
    
        window.addEventListener('scroll', handleScroll);
    
        return () => {
          window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    useEffect(() => {
        if (!isUserScrolling) {
          scrollToBottom();
        }
    }, [messages, isUserScrolling]); 

    const scrollToBottom = () => {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: "smooth",
        });
    };

    const toggleExtraInfo = (messageIndex) => {
        setExpandedMessages((prevMessages) => {
            if (prevMessages.includes(messageIndex)) {
                return prevMessages.filter(index => index !== messageIndex);
            } else {
                return [...prevMessages, messageIndex];
            }
        });
    };

    const downloadFile = (fileName) => {
        if (!fileName) {
            alert("Please enter a file name.");
            return;
        }

        axios({
            url: `${process.env.REACT_APP_FLASK_BASE}download/${fileName}`,
            method: "GET",
            responseType: "blob",
        })
            .then((response) => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement("a");
                link.href = url;
                link.setAttribute("download", fileName);
                document.body.appendChild(link);
                link.click();
            })
            .catch((error) => {
                alert(`File "${fileName}" not found!`);
            });
    };
    
    return (
        <div className="messages _container">
            {messages.map((message, index) => (
                <div key={index} className={`message ${MESSAGES_TYPES[message.type]?.styleClass ? MESSAGES_TYPES[message.type].styleClass : ""}`}>
                    <div className="message__info">
                        <div className="message__info-icon">
                            <img src={`img/icons/${message.from}.png`} alt={`${message.from} icon`} />
                        </div>
                        <h3>{message.from}</h3>
                    </div>
                    <div className="message__textblock">
                        {message.type === "file" ? (
                            <button key={index} onClick={() => downloadFile(message.data)}>
                                Downloaden {message.data}
                            </button>
                        ) : message.type === "stepCallback" ? (
                            <div>
                                <ReactMarkdown
                                    children={message.data.info}
                                    remarkPlugins={[remarkGfm]}
                                    rehypePlugins={[rehypeHighlight]}
                                />
                                {expandedMessages.includes(index) && (
                                    <div style={{ marginTop: "10px" }}>
                                        <ReactMarkdown
                                            children={message.data.extra_info}
                                            remarkPlugins={[remarkGfm]}
                                            rehypePlugins={[rehypeHighlight]}
                                        />
                                    </div>
                                )}
                                <button onClick={() => toggleExtraInfo(index)} style={{ marginTop: "10px" }}>
                                    {expandedMessages.includes(index) ? "Verbergen" : "Uitbreiden"}
                                </button>
                            </div>
                        ) : (
                            <ReactMarkdown
                                children={
                                    typeof message.data === "object"
                                        ? JSON.stringify(message.data, null, 2)
                                        : message.data
                                }
                                remarkPlugins={[remarkGfm]}
                                rehypePlugins={[rehypeHighlight]}
                            />
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
}
