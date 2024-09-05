// hooks/useProgress.js

import { useState, useEffect } from 'react';
import { getContentProgress } from '../utils/api';

export const useProgress = (contentId) => {
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let intervalId;

    const pollProgress = async () => {
      try {
        const progressData = await getContentProgress(contentId);
        setProgress(progressData);

        if (progressData.status === 'completed') {
          clearInterval(intervalId);
        }
      } catch (err) {
        setError('Failed to fetch progress');
        clearInterval(intervalId);
      }
    };

    if (contentId) {
      intervalId = setInterval(pollProgress, 2000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [contentId]);

  return { progress, error };
};