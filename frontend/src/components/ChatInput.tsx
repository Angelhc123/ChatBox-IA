import React, { useState } from 'react';

interface ChatInputProps {
  onSend: (message: string) => void;
  placeholder?: string;
  disabled?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSend, placeholder, disabled }) => {
  const [value, setValue] = useState('');

  const handleSend = () => {
    if (value.trim()) {
      onSend(value.trim());
      setValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div>
      <textarea
        value={value}
        onChange={e => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={2}
        style={{ resize: 'none' }}
      />
      <button onClick={handleSend} disabled={disabled || !value.trim()} style={{ marginTop: 8, padding: '8px 24px', borderRadius: 8, background: '#39c0ed', color: '#fff', border: 'none', fontWeight: 'bold', float: 'right' }}>
        Enviar
      </button>
    </div>
  );
};

export default ChatInput; 