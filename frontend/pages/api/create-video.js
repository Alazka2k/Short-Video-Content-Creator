// pages/api/create-video.js
export default function handler(req, res) {
    if (req.method === 'POST') {
      // Here we'll later add the logic to create the video
      // For now, let's just echo back the received data
      res.status(200).json({ message: 'Video creation request received', data: req.body });
    } else {
      res.setHeader('Allow', ['POST']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }