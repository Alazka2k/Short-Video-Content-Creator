import { NextApiRequest, NextApiResponse } from 'next';
import { PrismaClient } from '@prisma/client';
import { Configuration, OpenAIApi } from 'openai';
import { VideoScript } from '../../../shared/types/VideoScript';

const prisma = new PrismaClient();
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { 
      title, 
      videoSubject, 
      generalOptions, 
      contentOptions, 
      visualPromptOptions 
    } = req.body;

    // Validate input
    if (!title || !videoSubject || !generalOptions || !contentOptions || !visualPromptOptions) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Generate the prompt
    const initialPrompt = generatePrompt(title, videoSubject, generalOptions, contentOptions, visualPromptOptions);

    // Call OpenAI API
    const response = await openai.createChatCompletion({
      model: "gpt-4o-2024-08-06",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: initialPrompt }
      ],
      functions: [
        {
          name: "generate_video_script",
          description: "Generate a structured video script",
          parameters: {
            type: "object",
            properties: {
              title: { type: "string" },
              description: { type: "string" },
              hashtags: { type: "array", items: { type: "string" } },
              opening_scene: { 
                type: "object",
                properties: {
                  description: { type: "string" },
                  visual_prompt: { type: "string" }
                }
              },
              scenes: { 
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    description: { type: "string" },
                    visual_prompt: { type: "string" }
                  }
                }
              },
              closing_scene: { 
                type: "object",
                properties: {
                  description: { type: "string" },
                  visual_prompt: { type: "string" }
                }
              }
            },
            required: ["title", "description", "hashtags", "opening_scene", "scenes", "closing_scene"]
          }
        }
      ],
      function_call: { name: "generate_video_script" }
    });

    const functionCall = response.data.choices[0].message?.function_call;
    if (!functionCall || !functionCall.arguments) {
      throw new Error('Failed to generate video script');
    }

    const videoScript: VideoScript = JSON.parse(functionCall.arguments);

    // Save to database
    const savedContent = await prisma.content.create({
      data: {
        title: videoScript.title,
        videoSubject,
        generatedContent: JSON.stringify(videoScript),
        generalOptions: {
          create: generalOptions
        },
        contentOptions: {
          create: contentOptions
        },
        visualPromptOptions: {
          create: visualPromptOptions
        },
        scenes: {
          create: [
            { type: 'OPENING', description: videoScript.opening_scene.description },
            ...videoScript.scenes.map((scene, index) => ({
              type: 'MAIN',
              description: scene.description
            })),
            { type: 'CLOSING', description: videoScript.closing_scene.description }
          ]
        },
        visualPrompts: {
          create: [
            { type: 'OPENING', description: videoScript.opening_scene.visual_prompt, sceneNumber: 0 },
            ...videoScript.scenes.map((scene, index) => ({
              type: 'MAIN',
              description: scene.visual_prompt,
              sceneNumber: index + 1
            })),
            { type: 'CLOSING', description: videoScript.closing_scene.visual_prompt, sceneNumber: videoScript.scenes.length + 1 }
          ]
        },
      },
      include: {
        generalOptions: true,
        contentOptions: true,
        visualPromptOptions: true,
        scenes: true,
        visualPrompts: true,
      },
    });

    res.status(200).json({ id: savedContent.id, message: 'Content created successfully', content: savedContent });
  } catch (error) {
    console.error('Error in content creation:', error);
    res.status(500).json({ error: 'An error occurred while creating the content' });
  }
}

function generatePrompt(title: string, videoSubject: string, generalOptions: any, contentOptions: any, visualPromptOptions: any): string {
  // Implement the prompt generation logic here
  // Combine all the options into a structured prompt
  // ...
  return `Generate a video script about "${title}" with the following specifications...`;
}