import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CreateContent from '../pages/create-content';
import { createContent } from '../lib/contentCreation';

// Mock the next/router
const mockPush = jest.fn();
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock the Layout component
jest.mock('../components/Layout', () => ({ children }) => <div>{children}</div>);

// Mock the ContentCreationForm component
jest.mock('../components/forms/ContentCreationForm', () => {
  return function MockContentCreationForm({ onSubmit }) {
    return (
      <form data-testid="content-creation-form" onSubmit={(e) => {
        e.preventDefault();
        onSubmit({
          title: 'Test Title',
          description: 'Test Description',
          targetAudience: 'Test Audience',
          duration: '60',
          sceneAmount: '5',
          style: 'entertaining',
          services: {
            contentGeneration: true,
            imageGeneration: true,
            voiceGeneration: true,
            musicGeneration: false,
            videoGeneration: false,
          },
        });
      }}>
        <input data-testid="title-input" />
        <input data-testid="description-input" />
        <input data-testid="target-audience-input" />
        <input data-testid="duration-input" />
        <select data-testid="style-select"></select>
        <input data-testid="contentgeneration-checkbox" type="checkbox" />
        <input data-testid="imagegeneration-checkbox" type="checkbox" />
        <input data-testid="voicegeneration-checkbox" type="checkbox" />
        <input data-testid="musicgeneration-checkbox" type="checkbox" />
        <input data-testid="videogeneration-checkbox" type="checkbox" />
        <button data-testid="submit-button" type="submit">Submit</button>
      </form>
    );
  };
});

// Mock the createContent function
jest.mock('../lib/contentCreation', () => ({
  createContent: jest.fn(),
}));

describe('CreateContent', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders form fields correctly', () => {
    render(<CreateContent />);
    
    expect(screen.getByTestId('title-input')).toBeInTheDocument();
    expect(screen.getByTestId('description-input')).toBeInTheDocument();
    expect(screen.getByTestId('target-audience-input')).toBeInTheDocument();
    expect(screen.getByTestId('duration-input')).toBeInTheDocument();
    expect(screen.getByTestId('style-select')).toBeInTheDocument();
    expect(screen.getByTestId('contentgeneration-checkbox')).toBeInTheDocument();
    expect(screen.getByTestId('imagegeneration-checkbox')).toBeInTheDocument();
    expect(screen.getByTestId('voicegeneration-checkbox')).toBeInTheDocument();
    expect(screen.getByTestId('musicgeneration-checkbox')).toBeInTheDocument();
    expect(screen.getByTestId('videogeneration-checkbox')).toBeInTheDocument();
  });

  test('handles successful form submission', async () => {
    createContent.mockResolvedValueOnce({ id: '123' });

    render(<CreateContent />);

    await act(async () => {
      await userEvent.click(screen.getByTestId('submit-button'));
    });

    await waitFor(() => {
      expect(createContent).toHaveBeenCalledWith({
        title: 'Test Title',
        description: 'Test Description',
        targetAudience: 'Test Audience',
        duration: '60',
        sceneAmount: '5',
        style: 'entertaining',
        services: {
          contentGeneration: true,
          imageGeneration: true,
          voiceGeneration: true,
          musicGeneration: false,
          videoGeneration: false,
        },
      });
      expect(mockPush).toHaveBeenCalledWith({
        pathname: '/content-result',
        query: { id: '123' },
      });
    });
  });

  // Add more tests as needed...
});