import React from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

const Home = () => {
  return (
    <Layout>
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Create Engaging Video Content in Minutes
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Use AI to generate scripts, visuals, and audio for your next viral video.
        </p>
        <div className="space-x-4">
          <Link href="/create-content">
            <span className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg text-lg">
              Create New Content
            </span>
          </Link>
          <Link href="/dashboard">
            <span className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-6 rounded-lg text-lg">
              View Dashboard
            </span>
          </Link>
        </div>
      </div>
      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <FeatureCard
          title="AI-Powered Scripts"
          description="Generate engaging scripts tailored to your topic and audience."
        />
        <FeatureCard
          title="Custom Visuals"
          description="Create unique visuals that bring your story to life."
        />
        <FeatureCard
          title="Professional Audio"
          description="Add high-quality voiceovers and background music to your videos."
        />
      </div>
    </Layout>
  );
};

const FeatureCard = ({ title, description }) => (
  <div className="bg-white shadow-md rounded-lg p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
    <p className="text-gray-600">{description}</p>
  </div>
);

export default Home;