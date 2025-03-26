import React from 'react';

const ErrorMessage = ({ message }) => (
  message ? <div className="error-message">{message}</div> : null
);

export default ErrorMessage;