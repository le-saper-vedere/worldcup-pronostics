const BASE_URL = 'http://localhost:8000'

export async function api<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`)

  if (!response.ok) {
    throw new Error(`API Error ${response.status}: ${response.statusText}`)
  }

  return response.json()
}
