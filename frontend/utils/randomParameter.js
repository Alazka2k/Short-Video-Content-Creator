// utils/randomParameters.js

const getRandomElement = (array) => array[Math.floor(Math.random() * array.length)];

export const generateRandomParameters = () => {
  const styles = ['Documentary', 'Action', 'Comedy', 'Drama', 'Sci-Fi'];
  const tones = ['Serious', 'Light-hearted', 'Informative', 'Emotional', 'Suspenseful'];
  const vocabularies = ['Simple', 'Technical', 'Academic', 'Casual', 'Poetic'];
  const pacings = ['Slow', 'Moderate', 'Fast', 'Dynamic'];
  const imageStyles = ['Realistic', 'Cartoon', 'Abstract', 'Vintage', 'Futuristic'];

  return {
    generalOptions: {
      style: getRandomElement(styles),
      description: 'Randomly generated description',
      sceneAmount: Math.floor(Math.random() * 10) + 3, // 3 to 12 scenes
      duration: (Math.floor(Math.random() * 12) + 1) * 30, // 30 to 360 seconds, in 30-second increments
      tone: getRandomElement(tones),
      vocabulary: getRandomElement(vocabularies),
      targetAudience: `${getRandomElement(['Children', 'Teenagers', 'Adults', 'Seniors'])} ${getRandomElement(['interested in', 'curious about', 'learning'])} ${getRandomElement(['science', 'history', 'technology', 'arts'])}`,
    },
    contentOptions: {
      pacing: getRandomElement(pacings),
      description: 'Randomly generated content description',
    },
    visualPromptOptions: {
      pictureDescription: 'Randomly generated picture description',
      style: getRandomElement(imageStyles),
      imageDetails: 'Randomly generated image details',
      shotDetails: getRandomElement(['Close-up', 'Medium shot', 'Wide shot', 'Aerial view']),
    },
  };
};