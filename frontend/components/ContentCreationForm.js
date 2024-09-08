import React, { useState } from 'react';
import { useForm } from '../hooks/useForm';
import { generateRandomParameters } from '../utils/randomParameters';
import ParameterTooltip from './ParameterTooltip';

const ContentCreationForm = ({ onSubmit }) => {
  const initialState = {
    videoSubject: '',
    generalOptions: {
      style: '',
      description: '',
      sceneAmount: 5,
      duration: 60,
      tone: '',
      vocabulary: '',
      targetAudience: '',
    },
    contentOptions: {
      pacing: '',
      description: '',
    },
    visualPromptOptions: {
      pictureDescription: '',
      style: '',
      imageDetails: '',
      shotDetails: '',
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
      await onSubmit(formData);
    } catch (error) {
      console.error('Error creating content:', error);
      setError(error.message || 'An error occurred while creating the content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRandomize = () => {
    const randomParams = generateRandomParameters();
    setFormData((prevData) => ({
      ...prevData,
      ...randomParams,
    }));
  };

  const tooltips = {
    videoSubject: {
      explanation: "The main topic or subject of your video content.",
      example: "The history of space exploration"
    },
    style: {
      explanation: "The overall style or genre of the video.",
      example: "Documentary"
    },
    description: {
      explanation: "A brief overview of the video content.",
      example: "A chronological journey through major milestones in space exploration"
    },
    sceneAmount: {
      explanation: "The number of distinct scenes or segments in the video.",
      example: "5"
    },
    duration: {
      explanation: "The total length of the video in seconds.",
      example: "180"
    },
    tone: {
      explanation: "The emotional tone or mood of the video.",
      example: "Inspiring"
    },
    vocabulary: {
      explanation: "The level of language complexity used in the video.",
      example: "Technical"
    },
    targetAudience: {
      explanation: "The intended audience for the video.",
      example: "Science enthusiasts aged 15-25"
    },
    pacing: {
      explanation: "The speed at which the content is presented.",
      example: "Moderate"
    },
    contentDescription: {
      explanation: "Detailed description of the content structure and flow.",
      example: "Start with early rocket developments, move to the space race, then cover modern space exploration"
    },
    pictureDescription: {
      explanation: "General description of the visual style for the entire video.",
      example: "High-contrast images of rockets and space technology against starry backgrounds"
    },
    visualStyle: {
      explanation: "The overall visual aesthetic of the video.",
      example: "Sleek and futuristic"
    },
    imageDetails: {
      explanation: "Specific details about the images to be used.",
      example: "Include close-ups of astronaut helmets and wide shots of launch pads"
    },
    shotDetails: {
      explanation: "Information about camera angles and shot compositions.",
      example: "Mix of aerial views for launches and eye-level shots for interviews"
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="videoSubject" className="block text-lg font-medium text-gray-700">
          The video should be about:
          <ParameterTooltip {...tooltips.videoSubject} />
        </label>
        <input
          type="text"
          id="videoSubject"
          name="videoSubject"
          value={formData.videoSubject}
          onChange={handleInputChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          required
          placeholder={tooltips.videoSubject.example}
        />
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">General Options</h3>
        <div className="mt-2 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
          <div>
            <label htmlFor="style" className="block text-sm font-medium text-gray-700">
              Style
              <ParameterTooltip {...tooltips.style} />
            </label>
            <input
              type="text"
              id="style"
              name="generalOptions.style"
              value={formData.generalOptions.style}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.style.example}
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              Description
              <ParameterTooltip {...tooltips.description} />
            </label>
            <textarea
              id="description"
              name="generalOptions.description"
              value={formData.generalOptions.description}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.description.example}
            />
          </div>
          <div>
            <label htmlFor="sceneAmount" className="block text-sm font-medium text-gray-700">
              Number of Scenes
              <ParameterTooltip {...tooltips.sceneAmount} />
            </label>
            <input
              type="number"
              id="sceneAmount"
              name="generalOptions.sceneAmount"
              value={formData.generalOptions.sceneAmount}
              onChange={handleInputChange}
              min="1"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.sceneAmount.example}
            />
          </div>
          <div>
            <label htmlFor="duration" className="block text-sm font-medium text-gray-700">
              Duration (seconds)
              <ParameterTooltip {...tooltips.duration} />
            </label>
            <input
              type="number"
              id="duration"
              name="generalOptions.duration"
              value={formData.generalOptions.duration}
              onChange={handleInputChange}
              min="1"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.duration.example}
            />
          </div>
          <div>
            <label htmlFor="tone" className="block text-sm font-medium text-gray-700">
              Tone
              <ParameterTooltip {...tooltips.tone} />
            </label>
            <input
              type="text"
              id="tone"
              name="generalOptions.tone"
              value={formData.generalOptions.tone}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.tone.example}
            />
          </div>
          <div>
            <label htmlFor="vocabulary" className="block text-sm font-medium text-gray-700">
              Vocabulary
              <ParameterTooltip {...tooltips.vocabulary} />
            </label>
            <input
              type="text"
              id="vocabulary"
              name="generalOptions.vocabulary"
              value={formData.generalOptions.vocabulary}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.vocabulary.example}
            />
          </div>
          <div>
            <label htmlFor="targetAudience" className="block text-sm font-medium text-gray-700">
              Target Audience
              <ParameterTooltip {...tooltips.targetAudience} />
            </label>
            <input
              type="text"
              id="targetAudience"
              name="generalOptions.targetAudience"
              value={formData.generalOptions.targetAudience}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.targetAudience.example}
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">Content Options</h3>
        <div className="mt-2 space-y-6">
          <div>
            <label htmlFor="pacing" className="block text-sm font-medium text-gray-700">
              Pacing
              <ParameterTooltip {...tooltips.pacing} />
            </label>
            <input
              type="text"
              id="pacing"
              name="contentOptions.pacing"
              value={formData.contentOptions.pacing}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.pacing.example}
            />
          </div>
          <div>
            <label htmlFor="contentDescription" className="block text-sm font-medium text-gray-700">
              Content Description
              <ParameterTooltip {...tooltips.contentDescription} />
            </label>
            <textarea
              id="contentDescription"
              name="contentOptions.description"
              value={formData.contentOptions.description}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.contentDescription.example}
            />
          </div>
        </div>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-900">Visual Prompt Options</h3>
        <div className="mt-2 space-y-6">
          <div>
            <label htmlFor="pictureDescription" className="block text-sm font-medium text-gray-700">
              Picture Description
              <ParameterTooltip {...tooltips.pictureDescription} />
            </label>
            <textarea
              id="pictureDescription"
              name="visualPromptOptions.pictureDescription"
              value={formData.visualPromptOptions.pictureDescription}
              onChange={handleInputChange}
              rows={3}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.pictureDescription.example}
            />
          </div>
          <div>
            <label htmlFor="visualStyle" className="block text-sm font-medium text-gray-700">
              Visual Style
              <ParameterTooltip {...tooltips.visualStyle} />
            </label>
            <input
              type="text"
              id="visualStyle"
              name="visualPromptOptions.style"
              value={formData.visualPromptOptions.style}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.visualStyle.example}
            />
          </div>
          <div>
            <label htmlFor="imageDetails" className="block text-sm font-medium text-gray-700">
              Image Details
              <ParameterTooltip {...tooltips.imageDetails} />
            </label>
            <input
              type="text"
              id="imageDetails"
              name="visualPromptOptions.imageDetails"
              value={formData.visualPromptOptions.imageDetails}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.imageDetails.example}
            />
          </div>
          <div>
            <label htmlFor="shotDetails" className="block text-sm font-medium text-gray-700">
              Shot Details
              <ParameterTooltip {...tooltips.shotDetails} />
            </label>
            <input
              type="text"
              id="shotDetails"
              name="visualPromptOptions.shotDetails"
              value={formData.visualPromptOptions.shotDetails}
              onChange={handleInputChange}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
              required
              placeholder={tooltips.shotDetails.example}
            />
          </div>
        </div>
      </div>

      {error && <p className="text-red-500">{error}</p>}

      <div className="flex justify-between">
        <button
          type="button"
          onClick={handleRandomize}
          className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          Randomize Parameters
        </button>
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