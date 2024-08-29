import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { id } = req.query

      if (!id) {
        return res.status(400).json({ error: 'Content ID is required' })
      }

      const content = await prisma.content.findUnique({
        where: { id: parseInt(id) },
        select: {
          id: true,
          status: true,
          progress: true,
          currentStep: true,
        },
      })

      if (!content) {
        return res.status(404).json({ error: 'Content not found' })
      }

      res.status(200).json(content)
    } catch (error) {
      console.error('Error fetching content progress:', error)
      res.status(500).json({ error: 'An error occurred while fetching the content progress.' })
    } finally {
      await prisma.$disconnect()
    }
  } else {
    res.setHeader('Allow', ['GET'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}