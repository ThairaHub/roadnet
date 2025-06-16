

interface ResponseWrapper<T> {
  success: boolean;
  data: T;
  error?: string | null;
}

type Item = {
    id: string
    name: string
    description: string
  }

type ItemCreate = {
    name: string
    description: string
  }

type UserOut = {
  id: number
  username: string
  email: string
}

type GroupedRoadFeature = {
  updated_at: string | null;
  is_current: Boolean
  customer_id: number
  geometry_points: number
}
