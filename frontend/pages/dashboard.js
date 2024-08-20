import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

const Dashboard = () => {
  const [contentList, setContentList] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch('/api/get-content');
        const data = await response.json();
        setContentList(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching content:', error);
        setIsLoading(false);
      }
    };

    fetchContent();
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold mb-4 text-gray-800">Dashboard</h1>
      <Link href="/create-content">
        <span className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-4 inline-block">
          Create New Content
        </span>
      </Link>
      {isLoading ? (
        <p>Loading content...</p>
      ) : contentList.length === 0 ? (
        <p>No content created yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {contentList.map((content) => (
            <div key={content.id} className="bg-white shadow-md rounded-lg p-4">
              <h2 className="text-xl font-semibold mb-2">{content.title}</h2>
              <p className="text-gray-600 mb-2">{content.description}</p>
              <p className="text-sm text-gray-500">Style: {content.style}</p>
              <p className="text-sm text-gray-500">Duration: {content.duration}s</p>
              <div className="mt-2">
                <h3 className="text-sm font-semibold">Services:</h3>
                <ul className="text-sm text-gray-500">
                  {Object.entries(content.services).map(([service, isSelected]) => (
                    isSelected && (
                      <li key={service}>
                        {service.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      </li>
                    )
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </Layout>
  );
};

export default Dashboard;