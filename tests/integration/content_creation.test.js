import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import ContentCreationPage from '../../pages/create-content';

jest.mock('next/router', () => ({
  useRouter() {
    return {
      push: jest.fn(),
    };
  },
}));

describe('Content Creation Integration', () => {
  let mock;

  beforeEach(() => {
    mock = new MockAdapter(axios);
  });

  afterEach(() => {
    mock.reset();
  });

  it('creates content and redirects to result page', async () => {
    mock.onPost('/api/create-content').reply(201, { id: 1, title: 'Test Video' });
    
    render(<ContentCreationPage />);
    
    fireEvent.change(screen.getByLabelText(/video subject/i), { target: { value: 'Test Subject' } });
    fireEvent.change(screen.getByLabelText(/style/i), { target: { value: 'Documentary' } });
    fireEvent.change(screen.getByLabelText(/number of scenes/i), { target: { value: '3' } });
    fireEvent.change(screen.getByLabelText(/duration/i), { target: { value: '60' } });
    
    fireEvent.click(screen.getByText(/create content/i));
    
    await waitFor(() => {
      expect(mock.history.post[0].url).toBe('/api/create-content');
      expect(JSON.parse(mock.history.post[0].data)).toEqual(expect.objectContaining({
        videoSubject: 'Test Subject',
        generalOptions: expect.objectContaining({
          style: 'Documentary',
          sceneAmount: 3,
          duration: 60
        })
      }));
    });
    
    // Check if redirect happened
    expect(require('next/router').useRouter().push).toHaveBeenCalledWith({
      pathname: '/content-result',
      query: { id: 1 },
    });
  });

  // Add more integration tests as needed
});