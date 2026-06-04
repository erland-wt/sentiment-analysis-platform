import axios from "axios"
import type { PredictionResponse } from "../types/prediction"

const API_URL =
  import.meta.env.VITE_API_URL

export const predictSentiment = async (
  text: string
): Promise<PredictionResponse> => {

  try {
    const response = await axios.post(
      `${API_URL}/predict`,
      {
        text
      }
    )
    
    return response.data
  } catch (error) {
    console.error(
      "Prediction Error:",
      error
    )

    throw error
  }
}