import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const ContentResult = () => {
  const router = useRouter();
  const { id } = router.query;
  const [content, setContent] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchContent(id);
    }
  }, [id]);

  const fetchContent = async (contentId) => {
    try {
      const response = await fetch(`/api/content/${contentId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch content');
      }
      const data = await response.json();
      setContent(data);
    } catch (error) {
      console.error('Error fetching content:', error);
      setError('An error occurred while fetching the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Layout><div>Loading content...</div></Layout>;
  }

  if (error) {
    return <Layout><div>{error}</div></Layout>;
  }

  if (!content) {
    return <Layout><div>No content available.</div></Layout>;
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">{content.title}</h1>
      <p className="mb-2">{content.description}</p>
      <p className="mb-2">Target Audience: {content.targetAudience}</p>
      <p className="mb-2">Duration: {content.duration} seconds</p>
      <p className="mb-2">Style: {content.style}</p>
      {content.services && (
        <div>
          <h2 className="text-xl font-bold mt-4 mb-2">Services</h2>
          <ul>
            {Object.entries(content.services).map(([service, isEnabled]) => (
              <li key={service}>{service}: {isEnabled ? 'Enabled' : 'Disabled'}</li>
            ))}
          </ul>
        </div>
      )}
    </Layout>
  );
};

export default ContentResult;