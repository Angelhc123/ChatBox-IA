import React from 'react';
import './ChatBubble.css';
import iaAvatar from '../assets/ia-avatar.png';
import userAvatar from '../assets/user-avatar.png';

interface ChatBubbleProps {
  message: string;
  from: 'user' | 'ia';
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ message, from }) => {
  // Función para formatear el mensaje con markdown básico
  const formatMessage = (text: string) => {
    // Convertir **texto** a <strong>texto</strong>
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convertir • a lista con mejor formato
    formatted = formatted.replace(/• /g, '• ');
    
    // Mantener saltos de línea
    formatted = formatted.replace(/\n/g, '<br/>');
    
    return formatted;
  };

  return (
    <div className={`bubble-row ${from}`}>
      <img
        className="avatar"
        src={from === 'ia' ? iaAvatar : userAvatar}
        alt={from === 'ia' ? 'IA' : 'Usuario'}
      />
      <div 
        className={`chat-bubble ${from}`}
        dangerouslySetInnerHTML={{ __html: formatMessage(message) }}
      />
    </div>
  );
};

export default ChatBubble; 