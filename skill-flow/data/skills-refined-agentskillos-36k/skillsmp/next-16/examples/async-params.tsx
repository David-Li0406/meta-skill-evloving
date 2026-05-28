// Next.js 16: params and searchParams are async

type PageProps = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ q?: string }>
}

export default async function Page({ params, searchParams }: PageProps) {
  // Must await params and searchParams
  const { slug } = await params
  const { q } = await searchParams

  return (
    <div>
      <h1>Slug: {slug}</h1>
      {q && <p>Search: {q}</p>}
    </div>
  )
}
