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
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Services</h2>
          <ul>
            {Object.entries(content.services).map(([service, isEnabled]) => (
              <li key={service}>{service}: {isEnabled ? 'Enabled' : 'Disabled'}</li>
            ))}
          </ul>
        </div>
      )}

      {content.generatedContent && (
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Generated Content</h2>
          <h3 className="text-lg font-semibold">{content.generatedContent.video_title}</h3>
          <p>{content.generatedContent.description}</p>
          <h3 className="text-lg font-semibold mt-4">Scenes</h3>
          {content.generatedContent.main_scenes.map((scene, index) => (
            <div key={index} className="mb-2">
              <h4 className="font-semibold">Scene {index + 1}</h4>
              <p>Description: {scene.scene_description}</p>
              <p>Visual Prompt: {scene.visual_prompt}</p>
            </div>
          ))}
        </div>
      )}

      {content.generatedPicture && (
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Generated Image</h2>
          <img src={content.generatedPicture} alt="Generated visual" className="max-w-full h-auto" />
        </div>
      )}

      {content.generatedVoice && (
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Generated Voice</h2>
          <audio controls src={content.generatedVoice} data-testid="voice-audio">
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

      {content.generatedMusic && (
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Generated Music</h2>
          <audio controls src={content.generatedMusic} data-testid="music-audio">
            Your browser does not support the audio element.
          </audio>
        </div>
      )}

      {content.generatedVideo && (
        <div className="mb-4">
          <h2 className="text-xl font-bold mt-4 mb-2">Generated Video</h2>
          <video controls src={content.generatedVideo} className="max-w-full h-auto" data-testid="video-player">
            Your browser does not support the video element.
          </video>
        </div>
      )}

      {content.status === 'error' && (
        <div className="mt-4 text-red-500">
          <h2 className="text-xl font-bold">Error occurred during content creation</h2>
          <p>Error message: {content.errorMessage}</p>
          <p>Error step: {content.errorStep}</p>
        </div>
      )}
    </Layout>
  );
};

export default ContentResult;