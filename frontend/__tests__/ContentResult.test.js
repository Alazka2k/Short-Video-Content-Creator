import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import ContentResult from '../pages/content-result';

// Mock the next/router
jest.mock('next/router', () => ({
  useRouter: () => ({
    query: { id: '123' },
  }),
}));

// Mock the Layout component
jest.mock('../components/Layout', () => ({ children }) => <div>{children}</div>);

// Mock fetch globally
global.fetch = jest.fn();

describe('ContentResult', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock window.alert
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  test('displays loading state initially', () => {
    global.fetch.mockImplementationOnce(() => new Promise(() => {})); // Never resolves
    render(<ContentResult />);
    expect(screen.getByText('Loading content...')).toBeInTheDocument();
  });

  test('displays content when loaded', async () => {
    const mockContent = {
      title: 'Test Title',
      description: 'Test Description',
      targetAudience: 'Test Audience',
      duration: 60,
      style: 'entertaining',
      services: {
        imageGeneration: true,
        voiceGeneration: true,
        musicGeneration: true,
        videoGeneration: true,
      },
      contentData: JSON.stringify({
        image_url: 'http://example.com/image.jpg',
        voice_url: 'http://example.com/voice.mp3',
        music_url: 'http://example.com/music.mp3',
        video_url: 'http://example.com/video.mp4',
      }),
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockContent),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('Test Title')).toBeInTheDocument();
      expect(screen.getByText('Test Description')).toBeInTheDocument();
      expect(screen.getByText('Test Audience')).toBeInTheDocument();
      expect(screen.getByText('60 seconds')).toBeInTheDocument();
      expect(screen.getByText('entertaining')).toBeInTheDocument();
      expect(screen.getByText(/http:\/\/example.com\/image.jpg/)).toBeInTheDocument();
      expect(screen.getByText(/http:\/\/example.com\/voice.mp3/)).toBeInTheDocument();
      expect(screen.getByText(/http:\/\/example.com\/music.mp3/)).toBeInTheDocument();
      expect(screen.getByText(/http:\/\/example.com\/video.mp4/)).toBeInTheDocument();
    });
  });

  test('displays error message when content not found', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('Content not found.')).toBeInTheDocument();
      expect(window.alert).toHaveBeenCalledWith('An error occurred while fetching the content. Please try again.');
    });
  });
});