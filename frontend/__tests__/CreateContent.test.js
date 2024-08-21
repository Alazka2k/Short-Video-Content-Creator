import React from 'react';
import { render, screen, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CreateContent from '../pages/create-content';

// Mock the next/router
const mockPush = jest.fn();
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

// Mock the Layout component
jest.mock('../components/Layout', () => ({ children }) => <div>{children}</div>);

// Mock fetch globally
global.fetch = jest.fn();

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
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: '123' }),
    });

    render(<CreateContent />);

    await act(async () => {
      await userEvent.type(screen.getByTestId('title-input'), 'Test Title');
      await userEvent.type(screen.getByTestId('description-input'), 'Test Description');
      await userEvent.click(screen.getByTestId('submit-button'));
    });

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/create-content', expect.any(Object));
      expect(mockPush).toHaveBeenCalledWith({
        pathname: '/content-result',
        query: { id: '123' },
      });
    }, { timeout: 5000 });
  });

  test('handles form submission error', async () => {
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    global.fetch.mockRejectedValueOnce(new Error('API Error'));
  
    render(<CreateContent />);
  
    await act(async () => {
      await userEvent.type(screen.getByTestId('title-input'), 'Test Title');
      await userEvent.type(screen.getByTestId('description-input'), 'Test Description');
      await userEvent.click(screen.getByTestId('submit-button'));
    });
  
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalled();
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
      expect(screen.getByTestId('error-message')).toHaveTextContent('An error occurred while creating the content. Please try again.');
    }, { timeout: 5000 });
  
    consoleSpy.mockRestore();
  });

  test('disables submit button while loading and enables after completion', async () => {
    jest.useFakeTimers();
    
    global.fetch.mockImplementationOnce(() => 
      new Promise(resolve => setTimeout(() => resolve({ ok: true, json: () => Promise.resolve({ id: '123' }) }), 1000))
    );
  
    render(<CreateContent />);
  
    const submitButton = screen.getByTestId('submit-button');
    
    await act(async () => {
      await userEvent.type(screen.getByTestId('title-input'), 'Test Title');
      await userEvent.type(screen.getByTestId('description-input'), 'Test Description');
      userEvent.click(submitButton);
    });
  
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent('Creating...');
  
    await act(async () => {
      jest.advanceTimersByTime(1000);
    });
  
    await waitFor(() => {
      expect(submitButton).not.toBeDisabled();
      expect(submitButton).toHaveTextContent('Create Content');
    }, { timeout: 5000 });

    jest.useRealTimers();
  });

  test('toggles services correctly', async () => {
    render(<CreateContent />);

    const contentGenerationCheckbox = screen.getByTestId('contentgeneration-checkbox');
    const imageGenerationCheckbox = screen.getByTestId('imagegeneration-checkbox');

    expect(contentGenerationCheckbox).toBeChecked();
    expect(imageGenerationCheckbox).not.toBeChecked();

    await act(async () => {
      await userEvent.click(imageGenerationCheckbox);
      await userEvent.click(contentGenerationCheckbox);
    });

    expect(contentGenerationCheckbox).not.toBeChecked();
    expect(imageGenerationCheckbox).toBeChecked();
  });

  test('submits form with correct data', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: '123' }),
    });

    render(<CreateContent />);

    await act(async () => {
      await userEvent.type(screen.getByTestId('title-input'), 'Test Title');
      await userEvent.type(screen.getByTestId('description-input'), 'Test Description');
      await userEvent.type(screen.getByTestId('target-audience-input'), 'Test Audience');
      await userEvent.type(screen.getByTestId('duration-input'), '60');
      await userEvent.selectOptions(screen.getByTestId('style-select'), 'entertaining');
      await userEvent.click(screen.getByTestId('imagegeneration-checkbox'));
      await userEvent.click(screen.getByTestId('voicegeneration-checkbox'));
    });

    await act(async () => {
      await userEvent.click(screen.getByTestId('submit-button'));
    });

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/create-content', expect.any(Object));
      const requestBody = JSON.parse(global.fetch.mock.calls[0][1].body);
      expect(requestBody).toEqual({
        title: 'Test Title',
        description: 'Test Description',
        targetAudience: 'Test Audience',
        duration: '60',
        style: 'entertaining',
        services: {
          contentGeneration: true,
          imageGeneration: true,
          voiceGeneration: true,
          musicGeneration: false,
          videoGeneration: false,
        },
      });
    }, { timeout: 5000 });
  });
});