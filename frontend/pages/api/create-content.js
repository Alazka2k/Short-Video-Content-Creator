import { PrismaClient } from '@prisma/client'
import { startContentCreation } from '../../lib/contentCreation'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { title, description, targetAudience, duration, style, services } = req.body

      const content = await prisma.content.create({
        data: {
          title,
          description,
          targetAudience,
          duration: parseInt(duration),
          style,
          services: JSON.stringify(services),
          status: 'processing',
          progress: 0,
          currentStep: 'Initializing'
        },
      })

      // Start the content creation process in the background
      startContentCreation(content.id)

      res.status(200).json({ id: content.id })
    } catch (error) {
      console.error('Error creating content:', error)
      res.status(500).json({ error: 'An error occurred while creating the content.' })
    } finally {
      await prisma.$disconnect()
    }
  } else {
    res.setHeader('Allow', ['POST'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}