import { Request, Response, NextFunction } from 'express'

export const apiKeyAuth = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization
  const apiKey = authHeader && authHeader.split(' ')[1]

  if (apiKey === process.env.SECRET_API_KEY) {
    next()
  } else {
    res.status(401).send('Unauthorized')
  }
}
