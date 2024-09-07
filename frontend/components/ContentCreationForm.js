import React, { useState } from 'react';
import { useForm } from '../hooks/useForm';

const ContentCreationForm = () => {
  const initialState = {
    videoSubject: '',
    generalOptions: {
      sceneAmount: 10,
      lengthDescription: '45 seconds',
    },
    contentOptions: {
      generalDescription: 'End of the world scenarios and step-by-step progression, focusing on both global impact and personal stories within the chaos',
      scriptTone: 'A dramatic, urgent tone that balances between panic and authoritative narration, mimicking a documentary-style voice-over',
      vocabulary: 'Simple vocabulary, with relatively short sentences. Easy to understand and follow. Include some technical or scientific terms related to the scenario, but explain them in simple terms to maintain accessibility.',
      pacingStructure: 'Vary the pacing throughout the script to create tension and maintain viewer interest. Use shorter, punchier sentences for intense moments and longer, more descriptive ones for scene-setting.',
      sensoryThematicElements: 'Incorporate vivid sensory details (sights, sounds, smells, textures) to make the scenes more immersive and engaging. Weave in recurring symbols or motifs throughout the scenes to create a cohesive narrative thread.',
      characterPerspective: 'Consider introducing a relatable character or perspective to humanize the story and increase emotional investment.',
    },
    visualPromptSpecs: {
      pictureDescription: 'An image which describes the corresponding scene. Add information about the scene and details about the time period',
      shotDetails: 'Describe also the lighting effects, the time of the day, and the camera angles',
      imageStyle: 'Photorealistic, cinematic',
      imageDetails: '--ar 9:16 --style raw --s 500 --v 6',
    },
  };

  const { formData, handleInputChange, setFormData } = useForm(initialState);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await fetch('/api/create-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create content');
      }

      const result = await response.json();
      // Handle successful content creation (e.g., redirect to results page)
      console.log('Content created:', result);
    } catch (error) {
      console.error('Error creating content:', error);
      setError(error.message || 'An error occurred while creating the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="videoSubject" className="block text-sm font-medium text-gray-700">
          Video Subject
        </label>
        <input
          type="text"
          id="videoSubject"
          name="videoSubject"
          value={formData.videoSubject}
          onChange={handleInputChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
        />
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">General Options</h3>
        <div className="mt-2 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
          <div>
            <label htmlFor="sceneAmount" className="block text-sm font-medium text-gray-700">
              Number of Scenes
            </label>
            <input
              type="number"
              id="sceneAmount"
              name="generalOptions.sceneAmount"
              value={formData.generalOptions.sceneAmount}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="lengthDescription" className="block text-sm font-medium text-gray-700">
              Video Length
            </label>
            <input
              type="text"
              id="lengthDescription"
              name="generalOptions.lengthDescription"
              value={formData.generalOptions.lengthDescription}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">Content Options</h3>
        <div className="mt-2 space-y-6">
          <div>
            <label htmlFor="generalDescription" className="block text-sm font-medium text-gray-700">
              General Description
            </label>
            <textarea
              id="generalDescription"
              name="contentOptions.generalDescription"
              value={formData.contentOptions.generalDescription}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="scriptTone" className="block text-sm font-medium text-gray-700">
              Script Tone
            </label>
            <textarea
              id="scriptTone"
              name="contentOptions.scriptTone"
              value={formData.contentOptions.scriptTone}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="vocabulary" className="block text-sm font-medium text-gray-700">
              Vocabulary
            </label>
            <textarea
              id="vocabulary"
              name="contentOptions.vocabulary"
              value={formData.contentOptions.vocabulary}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="pacingStructure" className="block text-sm font-medium text-gray-700">
              Pacing Structure
            </label>
            <textarea
              id="pacingStructure"
              name="contentOptions.pacingStructure"
              value={formData.contentOptions.pacingStructure}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="sensoryThematicElements" className="block text-sm font-medium text-gray-700">
              Sensory and Thematic Elements
            </label>
            <textarea
              id="sensoryThematicElements"
              name="contentOptions.sensoryThematicElements"
              value={formData.contentOptions.sensoryThematicElements}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="characterPerspective" className="block text-sm font-medium text-gray-700">
              Character Perspective
            </label>
            <textarea
              id="characterPerspective"
              name="contentOptions.characterPerspective"
              value={formData.contentOptions.characterPerspective}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">Visual Prompt Specifications</h3>
        <div className="mt-2 space-y-6">
          <div>
            <label htmlFor="pictureDescription" className="block text-sm font-medium text-gray-700">
              Picture Description
            </label>
            <textarea
              id="pictureDescription"
              name="visualPromptSpecs.pictureDescription"
              value={formData.visualPromptSpecs.pictureDescription}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="shotDetails" className="block text-sm font-medium text-gray-700">
              Shot Details
            </label>
            <textarea
              id="shotDetails"
              name="visualPromptSpecs.shotDetails"
              value={formData.visualPromptSpecs.shotDetails}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="imageStyle" className="block text-sm font-medium text-gray-700">
              Image Style
            </label>
            <input
              type="text"
              id="imageStyle"
              name="visualPromptSpecs.imageStyle"
              value={formData.visualPromptSpecs.imageStyle}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
          <div>
            <label htmlFor="imageDetails" className="block text-sm font-medium text-gray-700">
              Image Details
            </label>
            <input
              type="text"
              id="imageDetails"
              name="visualPromptSpecs.imageDetails"
              value={formData.visualPromptSpecs.imageDetails}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
            />
          </div>
        </div>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      <div>
        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {isLoading ? 'Creating...' : 'Create Content'}
        </button>
      </div>
    </form>
  );
};

export default ContentCreationForm;