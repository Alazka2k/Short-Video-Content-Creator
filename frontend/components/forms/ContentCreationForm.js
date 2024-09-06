import React, { useState, useEffect } from 'react';

const ContentCreationForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    targetAudience: '',
    duration: '',
    style: 'informative',
    sceneAmount: 5,
    services: {
      contentGeneration: true,
      imageGeneration: false,
      voiceGeneration: false,
      musicGeneration: false,
      videoGeneration: false,
    },
  });
  const [contentId, setContentId] = useState(null);
  const [progress, setProgress] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

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
    setIsLoading(true);
    setError('');
    setContentId(null);
    setProgress(null);

    try {
      const response = await fetch('/api/create-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create content');
      }

      const result = await response.json();
      setContentId(result.id);
    } catch (error) {
      console.error('Error creating content:', error);
      setError(error.message || 'An error occurred while creating the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let intervalId;
    if (contentId) {
      intervalId = setInterval(async () => {
        try {
          const response = await fetch(`/api/content-progress/${contentId}`);
          if (!response.ok) {
            throw new Error('Failed to fetch progress');
          }
          const data = await response.json();
          setProgress(data);
          if (data.status === 'completed' || data.status === 'error') {
            clearInterval(intervalId);
          }
        } catch (error) {
          console.error('Error fetching progress:', error);
          setError('Failed to fetch progress. Please refresh the page.');
          clearInterval(intervalId);
        }
      }, 2000);
    }
    return () => clearInterval(intervalId);
  }, [contentId]);

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h1 className="text-2xl font-bold mb-4">Create Video Content</h1>
      {error && <p className="text-red-500 mb-4" data-testid="error-message">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4" data-testid="create-content-form">
        <div>
          <label htmlFor="title" className="block mb-1">Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            required
            data-testid="title-input"
          />
        </div>
        <div>
          <label htmlFor="description" className="block mb-1">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            required
            data-testid="description-input"
          ></textarea>
        </div>
        <div>
          <label htmlFor="targetAudience" className="block mb-1">Target Audience</label>
          <input
            type="text"
            id="targetAudience"
            name="targetAudience"
            value={formData.targetAudience}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            required
            data-testid="target-audience-input"
          />
        </div>
        <div>
          <label htmlFor="duration" className="block mb-1">Duration (in seconds)</label>
          <input
            type="number"
            id="duration"
            name="duration"
            value={formData.duration}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            required
            data-testid="duration-input"
          />
        </div>
        <div>
          <label htmlFor="style" className="block mb-1">Style</label>
          <select
            id="style"
            name="style"
            value={formData.style}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            data-testid="style-select"
          >
            <option value="informative">Informative</option>
            <option value="entertaining">Entertaining</option>
            <option value="educational">Educational</option>
          </select>
        </div>
        <div>
          <label htmlFor="sceneAmount" className="block mb-1">Number of Scenes</label>
          <input
            type="number"
            id="sceneAmount"
            name="sceneAmount"
            value={formData.sceneAmount}
            onChange={handleInputChange}
            className="w-full px-3 py-2 border rounded"
            required
            data-testid="scene-amount-input"
          />
        </div>
        <div>
          <h3 className="font-semibold mb-2">Services</h3>
          {Object.entries(formData.services).map(([service, isEnabled]) => (
            <label key={service} className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={isEnabled}
                onChange={() => handleServiceToggle(service)}
                data-testid={`${service.toLowerCase()}-checkbox`}
              />
              <span>{service}</span>
            </label>
          ))}
        </div>
        
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
          disabled={isLoading}
          data-testid="submit-button"
        >
          {isLoading ? 'Creating...' : 'Create Content'}
        </button>
      </form>

      {progress && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-2">Content Creation Progress</h2>
          <p>Status: {progress.status}</p>
          <p>Current Step: {progress.currentStepName}</p>
          <p>Progress: {progress.progressPercentage}%</p>
          {progress.status === 'completed' && (
            <p className="text-green-500 font-semibold">Content creation completed!</p>
          )}
          {progress.status === 'error' && (
            <div>
              <p className="text-red-500 font-semibold">Error occurred during content creation</p>
              <p>Error message: {progress.errorMessage}</p>
              <p>Error step: {progress.errorStep}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ContentCreationForm;