// hooks/useForm.js

import { useState } from 'react';

export const useForm = (initialState) => {
  const [formData, setFormData] = useState(initialState);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleServiceToggle = (service) => {
    setFormData(prevState => ({
      ...prevState,
      services: {
        ...prevState.services,
        [service]: !prevState.services[service]
      }
    }));
  };

  const resetForm = () => {
    setFormData(initialState);
  };

  return {
    formData,
    handleInputChange,
    handleServiceToggle,
    resetForm,
    setFormData
  };
};