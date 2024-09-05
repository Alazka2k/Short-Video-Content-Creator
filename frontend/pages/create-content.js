import React from 'react';
import { useRouter } from 'next/router';
import Layout from '../components/Layout';
import ContentCreationForm from '../components/forms/ContentCreationForm';
import { createContent } from '../lib/contentCreation';

const CreateContent = () => {
  const router = useRouter();

  const handleSubmit = async (formData) => {
    try {
      const result = await createContent(formData);
      router.push({
        pathname: '/content-result',
        query: { id: result.id },
      });
    } catch (error) {
      console.error('Error creating content:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  return (
    <Layout>
      <h1>Create Content</h1>
      <ContentCreationForm onSubmit={handleSubmit} />
    </Layout>
  );
};

export default CreateContent;