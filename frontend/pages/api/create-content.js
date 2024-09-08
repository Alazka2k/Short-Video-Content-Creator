// frontend/pages/api/create-content.js

import { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000'; // Adjust this to your backend URL

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { 
      title, 
      videoSubject, 
      generalOptions, 
      contentOptions, 
      visualPromptOptions 
    } = req.body;

    // Validate input
    if (!title || !videoSubject || !generalOptions || !contentOptions || !visualPromptOptions) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Prepare the data for the backend
    const backendRequestData = {
      title,
      videoSubject,
      generalOptions,
      contentOptions,
      visualPromptOptions
    };

    // Call the backend API to start content creation
    const backendResponse = await axios.post(`${BACKEND_URL}/api/create-content`, backendRequestData);

    if (backendResponse.status !== 200) {
      throw new Error('Backend API call failed');
    }

    const { id, message, content } = backendResponse.data;

    res.status(200).json({ id, message, content });
  } catch (error) {
    console.error('Error in content creation:', error);
    res.status(500).json({ error: 'An error occurred while creating the content' });
  }
}