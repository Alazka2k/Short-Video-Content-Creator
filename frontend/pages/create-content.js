import React, { useState } from 'react';
import Layout from '../components/Layout';

const CreateContent = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    targetAudience: '',
    duration: '',
    style: 'informative',
    services: {
      contentGeneration: false,
      pictureCreation: false,
      voiceGeneration: false,
      musicGeneration: false,
      e2eVideoGeneration: false,
    },
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/create-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      console.log('API response:', data);
      // Here you can add logic to handle the response, e.g., showing a success message or redirecting to results page
    } catch (error) {
      console.error('Error:', error);
      // Here you can add logic to handle errors, e.g., showing an error message
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Create New Content</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="title" className="block mb-1 text-gray-700">Content Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded text-gray-700"
            required
          />
        </div>
        <div>
          <label htmlFor="description" className="block mb-1 text-gray-700">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded text-gray-700"
            rows="3"
            required
          />
        </div>
        <div>
          <label htmlFor="targetAudience" className="block mb-1 text-gray-700">Target Audience</label>
          <input
            type="text"
            id="targetAudience"
            name="targetAudience"
            value={formData.targetAudience}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded text-gray-700"
          />
        </div>
        <div>
          <label htmlFor="duration" className="block mb-1 text-gray-700">Duration (in seconds)</label>
          <input
            type="number"
            id="duration"
            name="duration"
            value={formData.duration}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded text-gray-700"
            min="1"
            required
          />
        </div>
        <div>
          <label htmlFor="style" className="block mb-1 text-gray-700">Content Style</label>
          <select
            id="style"
            name="style"
            value={formData.style}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded text-gray-700"
          >
            <option value="informative">Informative</option>
            <option value="entertaining">Entertaining</option>
            <option value="tutorial">Tutorial</option>
          </select>
        </div>
        <div>
          <label className="block mb-1 text-gray-700">Services</label>
          <div className="space-y-2">
            {Object.entries(formData.services).map(([service, isSelected]) => (
              <div key={service} className="flex items-center">
                <input
                  type="checkbox"
                  id={service}
                  checked={isSelected}
                  onChange={() => handleServiceToggle(service)}
                  className="mr-2"
                />
                <label htmlFor={service} className="text-gray-700">
                  {service.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                </label>
              </div>
            ))}
          </div>
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
          Create Content
        </button>
      </form>
    </Layout>
  );
};

export default CreateContent;