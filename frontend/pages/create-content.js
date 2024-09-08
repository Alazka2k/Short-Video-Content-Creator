import React, { useState } from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import ContentCreationForm from '../components/ContentCreationForm';
import ResultDashboard from '../components/ResultDashboard';
import { createContent } from '../lib/contentCreation';

const CreateContent = () => {
  const router = useRouter();
  const [generatedContent, setGeneratedContent] = useState(null);

  const handleSubmit = async (formData) => {
    try {
      const result = await createContent(formData);
      setGeneratedContent(result);
    } catch (error) {
      console.error('Error creating content:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4">Create Content</h1>
      <ContentCreationForm onSubmit={handleSubmit} />
      {generatedContent && (
        <div className="mt-8">
          <h2 className="text-xl font-bold mb-4">Generated Content</h2>
          <ResultDashboard content={generatedContent} />
        </div>
      )}
    </Layout>
  );
};

export default CreateContent;