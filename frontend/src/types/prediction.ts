export interface SentenceResult {
  sentence: string
  clean_sentence: string
  sentiment: string
}

export interface PredictionResponse {
  overall_sentiment: string
  summary: string
  confidence: number

  sentences: {
    sentence: string
    clean_sentence: string
    sentiment: string
  }[]

  statistics: {
    positive: number
    neutral: number
    negative: number

    positive_percentage: number
    neutral_percentage: number
    negative_percentage: number
  }
}

export interface Statistics {
  positive: number
  neutral: number
  negative: number
}