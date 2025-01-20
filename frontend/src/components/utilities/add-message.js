export const addMessage = ({messageFrom, messageData, messageType, setMessages}) => {
    const message = {
        type: messageType,
        from: messageFrom,
        data: messageData,
    };
    setMessages((prevMessages) => [...prevMessages, message]);
};