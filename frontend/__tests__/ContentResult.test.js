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
  let consoleErrorSpy;

  beforeEach(() => {
    jest.clearAllMocks();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleErrorSpy.mockRestore();
  });

  test('displays loading state initially', async () => {
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
        contentGeneration: true,
        imageGeneration: false,
        voiceGeneration: true,
        musicGeneration: false,
        videoGeneration: true,
      },
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockContent),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('Test Title')).toBeInTheDocument();
      expect(screen.getByText('Test Description')).toBeInTheDocument();
      expect(screen.getByText('Target Audience: Test Audience')).toBeInTheDocument();
      expect(screen.getByText('Duration: 60 seconds')).toBeInTheDocument();
      expect(screen.getByText('Style: entertaining')).toBeInTheDocument();
      expect(screen.getByText('contentGeneration: Enabled')).toBeInTheDocument();
      expect(screen.getByText('imageGeneration: Disabled')).toBeInTheDocument();
      expect(screen.getByText('voiceGeneration: Enabled')).toBeInTheDocument();
      expect(screen.getByText('musicGeneration: Disabled')).toBeInTheDocument();
      expect(screen.getByText('videoGeneration: Enabled')).toBeInTheDocument();
    });
  });

  test('displays error message when content fetch fails', async () => {
    global.fetch.mockImplementationOnce(() => 
      Promise.reject(new Error('Failed to fetch content'))
    );

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('An error occurred while fetching the content. Please try again.')).toBeInTheDocument();
    });

    expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching content:', expect.any(Error));
  });

  test('displays no content available message when content is null', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(null),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('No content available.')).toBeInTheDocument();
    });
  });
  
  test('displays generated content correctly', async () => {
    const mockContent = {
      title: 'Test Title',
      description: 'Test Description',
      targetAudience: 'Test Audience',
      duration: 60,
      style: 'entertaining',
      services: {
        contentGeneration: true,
        imageGeneration: false,
        voiceGeneration: true,
        musicGeneration: false,
        videoGeneration: true,
      },
      generatedContent: {
        video_title: 'Generated Video Title',
        description: 'Generated video description',
        main_scenes: [
          {
            scene_description: 'Scene 1 description',
            visual_prompt: 'Scene 1 visual prompt'
          },
          {
            scene_description: 'Scene 2 description',
            visual_prompt: 'Scene 2 visual prompt'
          }
        ]
      }
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockContent),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('Test Title')).toBeInTheDocument();
      expect(screen.getByText('Test Description')).toBeInTheDocument();
      expect(screen.getByText('Target Audience: Test Audience')).toBeInTheDocument();
      expect(screen.getByText('Duration: 60 seconds')).toBeInTheDocument();
      expect(screen.getByText('Style: entertaining')).toBeInTheDocument();
      expect(screen.getByText('Generated Video Title')).toBeInTheDocument();
      expect(screen.getByText('Generated video description')).toBeInTheDocument();
      expect(screen.getByText(/Scene 1 description/)).toBeInTheDocument();
      expect(screen.getByText(/Scene 1 visual prompt/)).toBeInTheDocument();
      expect(screen.getByText(/Scene 2 description/)).toBeInTheDocument();
      expect(screen.getByText(/Scene 2 visual prompt/)).toBeInTheDocument();
    });
  });

  test('displays generated assets when available', async () => {
    const mockContent = {
      // ... other fields
      generatedPicture: 'https://example.com/image.jpg',
      generatedVoice: 'https://example.com/voice.mp3',
      generatedMusic: 'https://example.com/music.mp3',
      generatedVideo: 'https://example.com/video.mp4',
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockContent),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByAltText('Generated visual')).toHaveAttribute('src', 'https://example.com/image.jpg');
      expect(screen.getByTestId('voice-audio')).toHaveAttribute('src', 'https://example.com/voice.mp3');
      expect(screen.getByTestId('music-audio')).toHaveAttribute('src', 'https://example.com/music.mp3');
      expect(screen.getByTestId('video-player')).toHaveAttribute('src', 'https://example.com/video.mp4');
    });
  });

  test('displays error state when content has error status', async () => {
    const mockContent = {
      status: 'error',
      errorMessage: 'Content generation failed',
      errorStep: 'image_generation',
    };

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockContent),
    });

    render(<ContentResult />);

    await waitFor(() => {
      expect(screen.getByText('Error occurred during content creation')).toBeInTheDocument();
      expect(screen.getByText('Error message: Content generation failed')).toBeInTheDocument();
      expect(screen.getByText('Error step: image_generation')).toBeInTheDocument();
    });
  });
});