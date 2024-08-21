import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';

const ContentResult = () => {
  const router = useRouter();
  const { id } = router.query;
  const [content, setContent] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (id) {
      fetchContent(id);
    }
  }, [id]);

  const fetchContent = async (contentId) => {
    try {
      const response = await fetch(`/api/get-content?id=${contentId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch content');
      }
      const data = await response.json();
      setContent(data);
    } catch (error) {
      console.error('Error fetching content:', error);
      alert('An error occurred while fetching the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <Layout>
        <div>Loading content...</div>
      </Layout>
    );
  }

  if (!content) {
    return (
      <Layout>
        <div>Content not found.</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4 text-gray-800">{content.title}</h1>
      <div className="space-y-4">
        <p><strong>Description:</strong> {content.description}</p>
        <p><strong>Target Audience:</strong> {content.targetAudience}</p>
        <p><strong>Duration:</strong> {content.duration} seconds</p>
        <p><strong>Style:</strong> {content.style}</p>
        <div>
          <strong>Generated Content:</strong>
          <pre className="mt-2 p-4 bg-gray-100 rounded overflow-x-auto">
            {JSON.stringify(JSON.parse(content.contentData), null, 2)}
          </pre>
        </div>
        {content.services.imageGeneration && content.contentData.image_url && (
          <div>
            <strong>Generated Image:</strong>
            <img src={content.contentData.image_url} alt="Generated content" className="mt-2 max-w-full h-auto" />
          </div>
        )}
        {content.services.voiceGeneration && content.contentData.voice_url && (
          <div>
            <strong>Generated Voice:</strong>
            <audio controls src={content.contentData.voice_url} className="mt-2 w-full" />
          </div>
        )}
        {content.services.musicGeneration && content.contentData.music_url && (
          <div>
            <strong>Generated Music:</strong>
            <audio controls src={content.contentData.music_url} className="mt-2 w-full" />
          </div>
        )}
        {content.services.videoGeneration && content.contentData.video_url && (
          <div>
            <strong>Generated Video:</strong>
            <video controls src={content.contentData.video_url} className="mt-2 w-full" />
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ContentResult;