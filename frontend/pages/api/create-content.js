import { PrismaClient } from '@prisma/client'
import { startContentCreation } from '../../lib/contentCreation'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST'])
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` })
  }

  try {
    const { title, description, targetAudience, duration, style, sceneAmount, services } = req.body

    // Input validation
    if (!title || !description || !targetAudience || !duration || !style || !sceneAmount) {
      return res.status(400).json({ error: 'Missing required fields' })
    }

    if (isNaN(parseInt(duration)) || isNaN(parseInt(sceneAmount))) {
      return res.status(400).json({ error: 'Duration and sceneAmount must be numbers' })
    }

    const content = await prisma.content.create({
      data: {
        title,
        description,
        targetAudience,
        duration: parseInt(duration),
        style,
        sceneAmount: parseInt(sceneAmount),
        services: JSON.stringify(services),
        status: 'processing',
        progressPercentage: 0,
        currentStep: 'Initializing'
      },
    })

    // Start the content creation process in the background
    startContentCreation(content.id).catch(error => {
      console.error('Error in content creation process:', error)
      // You might want to implement a notification system here to alert admins of failed processes
    })

    res.status(200).json({ id: content.id })
  } catch (error) {
    console.error('Error creating content:', error)
    if (error.code === 'P2002') {
      return res.status(400).json({ error: 'A content with this title already exists' })
    }
    res.status(500).json({ error: 'An unexpected error occurred while creating the content' })
  }
}