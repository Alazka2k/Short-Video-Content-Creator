import React from 'react';
import Head from 'next/head';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Video Content Creator</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-white shadow mt-8 py-4">
        <div className="container mx-auto px-4">
          <p className="text-center text-gray-500 text-sm">
            © 2024 Video Content Creator. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;