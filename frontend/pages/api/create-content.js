import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { title, description, targetAudience, duration, style, services } = req.body

      // Call your backend API to create content
      const response = await fetch(`${process.env.BACKEND_URL}/api/create-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          description,
          target_audience: targetAudience,
          duration: parseInt(duration),
          style,
          services,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to create content')
      }

      const contentData = await response.json()

      // Save the content data to your database
      const content = await prisma.content.create({
        data: {
          title,
          description,
          targetAudience,
          duration: parseInt(duration),
          style,
          services: JSON.stringify(services),
          contentData: JSON.stringify(contentData),
        },
      })

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