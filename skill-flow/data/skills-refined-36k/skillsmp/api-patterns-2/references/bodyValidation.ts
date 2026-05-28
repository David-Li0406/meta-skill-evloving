import type { H3Event } from 'h3'
import type { z } from 'zod'

export async function validateBody<T extends z.ZodType>(
  event: H3Event,
  schema: T,
): Promise<z.infer<T>> {
  const result = await readValidatedBody(event, schema.safeParse)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid input',
      data: result.error.format(),
    })
  }

  return result.data
}

export async function validateParams<T extends z.ZodType>(
  event: H3Event,
  schema: T,
): Promise<z.infer<T>> {
  const result = await getValidatedRouterParams(event, schema.safeParse)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid input',
      data: result.error.format(),
    })
  }

  return result.data
}

export async function validateQuery<T extends z.ZodType>(
  event: H3Event,
  schema: T,
): Promise<z.infer<T>> {
  const result = await getValidatedQuery(event, schema.safeParse)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid input',
      data: result.error.format(),
    })
  }

  return result.data
}

export async function validateData<T extends z.ZodType>(
  data: any,
  schema: T,
): Promise<z.infer<T>> {
  const result = await schema.safeParse(data)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Invalid data',
      data: result.error.format(),
    })
  }

  return result.data
}
