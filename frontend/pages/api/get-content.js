import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const contents = await prisma.content.findMany({
        orderBy: {
          createdAt: 'desc',
        },
      })

      res.status(200).json(contents)
    } catch (error) {
      console.error('Error fetching content:', error)
      res.status(500).json({ error: 'An error occurred while fetching content.' })
    } finally {
      await prisma.$disconnect()
    }
  } else {
    res.setHeader('Allow', ['GET'])
    res.status(405).end(`Method ${req.method} Not Allowed`)
  }
}