import axios from "axios"
import type { PredictionResponse } from "../types/prediction"

const API_URL = "http://127.0.0.1:8000"

export const predictSentiment = async (
  text: string
): Promise<PredictionResponse> => {

  const response = await axios.post(
    `${API_URL}/predict`,
    {
      text: text
    }
  )

  return response.data
}