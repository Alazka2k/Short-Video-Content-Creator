import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import CreateContent from '../pages/create-content';

// Mock the next/router
jest.mock('next/router', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock the Layout component
jest.mock('../components/Layout', () => ({ children }) => <div>{children}</div>);

// Mock fetch globally
global.fetch = jest.fn();

describe('CreateContent', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock window.alert
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  test('renders form fields correctly', () => {
    render(<CreateContent />);
    
    expect(screen.getByLabelText(/Content Title/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Target Audience/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Duration/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Content Style/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Content Generation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Image Generation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Voice Generation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Music Generation/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Video Generation/i)).toBeInTheDocument();
  });

  test('submits form with correct data', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ id: '123' }),
    });

    render(<CreateContent />);

    await userEvent.type(screen.getByLabelText(/Content Title/i), 'Test Title');
    await userEvent.type(screen.getByLabelText(/Description/i), 'Test Description');
    await userEvent.type(screen.getByLabelText(/Target Audience/i), 'Test Audience');
    await userEvent.type(screen.getByLabelText(/Duration/i), '60');
    await userEvent.selectOptions(screen.getByLabelText(/Content Style/i), 'entertaining');
    await userEvent.click(screen.getByLabelText(/Image Generation/i));
    await userEvent.click(screen.getByLabelText(/Voice Generation/i));

    await userEvent.click(screen.getByText('Create Content'));

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
    });
  });

  test('handles form submission error', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
    });

    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<CreateContent />);

    await userEvent.click(screen.getByText('Create Content'));

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalled();
      expect(window.alert).toHaveBeenCalledWith('An error occurred while creating the content. Please try again.');
    });

    consoleSpy.mockRestore();
  });
});