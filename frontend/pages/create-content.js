import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const CreateContent = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    targetAudience: '',
    duration: '',
    style: 'informative',
    services: {
      contentGeneration: true,
      imageGeneration: false,
      voiceGeneration: false,
      musicGeneration: false,
      videoGeneration: false,
    },
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(null);

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
        throw new Error('Failed to create content');
      }
  
      const result = await response.json();

      // Poll for progress updates
      const pollInterval = setInterval(async () => {
        const progressResponse = await fetch(`/api/content-progress/${result.id}`);
        const progressData = await progressResponse.json();
        setProgress(progressData);

        if (progressData.status === 'completed') {
          clearInterval(pollInterval);
          router.push({
            pathname: '/content-result',
            query: { id: result.id },
          });
        }
      }, 2000);

    } catch (error) {
      console.error('Error creating content:', error);
      setError('An error occurred while creating the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Create New Content</h1>
      {error && <div className="text-red-500 mb-4" role="alert" data-testid="error-message">{error}</div>}
      {progress && (
        <div className="mb-4">
          <h2 className="text-lg font-semibold">Progress: {progress.progress_percentage}%</h2>
          <p>Step: {progress.current_step} / {progress.total_steps}</p>
          <p>Status: {progress.status}</p>
          <p>Estimated time remaining: {progress.estimated_time_remaining} seconds</p>
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4" data-testid="create-content-form">
        {/* ... (rest of the form remains the same) ... */}
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
          disabled={isLoading}
          data-testid="submit-button"
        >
          {isLoading ? 'Creating...' : 'Create Content'}
        </button>
      </form>
    </Layout>
  );
};

export default CreateContent;