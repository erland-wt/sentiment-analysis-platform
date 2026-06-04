import { useState } from "react"
import { predictSentiment } from "./services/api"
import type { PredictionResponse } from "./types/prediction"
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts"

function App() {

  const [text, setText] = useState("")
  const [result, setResult] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!text.trim()) return
    try {
      setLoading(true)
      const response =
        await predictSentiment(text)
      setResult(response)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (
    sentiment: string
  ) => {
    if (sentiment === "positive") {
      return "bg-green-100 border-green-500"
    }
    if (sentiment === "negative") {
      return "bg-red-100 border-red-500"
    }
    return "bg-yellow-100 border-yellow-500"
  }

  const getOverallBadge = (
    sentiment: string
  ) => {
    if (sentiment === "positive") {
      return "bg-green-500 text-white"
    }
    if (sentiment === "negative") {
      return "bg-red-500 text-white"
    }
    return "bg-yellow-500 text-white"
  }

  const chartData = result
  ? [
      {
        name: "Positive",
        value:
          result.statistics.positive
      },

      {
        name: "Neutral",
        value:
          result.statistics.neutral
      },

      {
        name: "Negative",
        value:
          result.statistics.negative
      }
    ]
  : []

 const COLORS = [
    "#22c55e",
    "#eab308",
    "#ef4444"
  ]

  const formatSentiment = (
    sentiment: string
  ) => {

    return (
      sentiment.charAt(0).toUpperCase() +
      sentiment.slice(1)
    )
  }

  return (
    <div className="min-h-screen bg-linear-to-br from slate-100 to-slate-200 p-8">
      <div className="mb-10 text-center">
        <h1 className="text-5xl font-bold mb-4">Sentiment Analyzer</h1>
        <p className="text-gray-600 text-lg">Analyze news, reviews, comments, and long-form text instantly.</p>
      </div>

      <div className="max-w-3xl mx-auto">
        <textarea
          className="w-full h-64 p-5 rounded-2xl border bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Masukkan teks..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="mt-5 px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>

          {
            result && (
              <div className="mt-10 bg-white p-8 rounded-3xl shadow-xl">
                <h2 className="text-2xl font-bold mb-4">
                  Result
                </h2>

                <div className="mb-6 bg-blue-50 p-5 rounded-xl">
                  <h3 className="font-bold text-lg">
                    Insight Summary
                  </h3>

                  <p className="mt-2 text-gray-700">
                    {result.summary}
                  </p>

                </div>

                <p>
                  Overall Sentiment:
                  {" "}
                  <span
                    className={`px-4 py-2 rounded-full font-bold
                      ${getOverallBadge(
                        result.overall_sentiment
                      )}
                    `}
                  >
                    {formatSentiment(result.overall_sentiment)}
                  </span>
                </p>

                <div className="mt-4">
                  <div className="w-full h-4 bg-gray-200 rounded-full">
                    <div
                      className="h-4 bg-blue-500 rounded-full"
                      style={{
                        width: `${result.confidence * 100}%`
                      }}
                    />
                  </div>

                  <p className="text-sm text-gray-600 mt-2">
                    {(result.confidence * 100).toFixed(2)}%
                  </p>
                </div>

                <div className="mt-8">
                  <div className="grid grid-cols-3 gap-4 mt-6">
                    <div className="bg-slate-100 p-4 rounded-xl">
                      <h3 className="font-bold">
                        Overall Sentiment
                      </h3>

                      <p>{formatSentiment(result.overall_sentiment)}</p>
                    </div>

                    <div className="bg-slate-100 p-4 rounded-xl">
                      <h3 className="font-bold">
                        Confidence
                      </h3>

                      <p>
                        {(result.confidence * 100).toFixed(2)}%
                      </p>
                    </div>

                  </div>

                  <h3 className="text-xl font-bold mt-8 mb-4">
                    Sentence Analysis
                  </h3>

                  <div className="space-y-3">
                    {result.sentences.map(
                      (item, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-xl border-l-4
                            ${getSentimentColor(item.sentiment)
                            }
                          `}
                        >
                          <p>
                            {item.sentence}
                          </p>

                          <p className="mt-2 text-sm font-semibold">
                            {formatSentiment(item.sentiment)}
                          </p>

                        </div>
                      )
                    )}
                  </div>
                </div>

                <div className="mt-8">
                  <h3 className="text-xl font-bold mb-4">
                    Statistics
                  </h3>

                  <div className="grid grid-cols-3 gap-4">
                    <div
                      className="
                        bg-green-100
                        p-4
                        rounded-xl
                        text-center
                      "
                    >
                      <p className="font-bold">
                        Positive
                      </p>

                      <p className="text-2xl">
                        {result.statistics.positive}
                      </p>

                      <p className="text-sm">
                        {
                          result.statistics
                            .positive_percentage
                        }%
                      </p>

                    </div>

                    <div
                      className="
                        bg-yellow-100
                        p-4
                        rounded-xl
                        text-center
                      "
                    >
                      <p className="font-bold">
                        Neutral
                      </p>

                      <p className="text-2xl">
                        {result.statistics.neutral}
                      </p>

                      <p className="text-sm">
                        {
                          result.statistics
                            .neutral_percentage
                        }%
                      </p>

                    </div>

                    <div className="bg-red-100 p-4 rounded-xl text-center">
                      <p className="font-bold">
                        Negative
                      </p>

                      <p className="text-2xl">
                        {result.statistics.negative}
                      </p>

                      <p className="text-sm">
                        {
                          result.statistics
                            .negative_percentage
                        }%
                      </p>

                    </div>

                  </div>

                </div>

                <div className="mt-10">
                  <h3 className="text-xl font-bold mb-4">
                    Sentiment Distribution
                  </h3>

                  <div
                    className="
                      bg-white
                      rounded-xl
                      p-4
                      shadow
                      h-87.5
                    "
                  >

                    <ResponsiveContainer
                      width="100%"
                      height="100%"
                    >

                      <PieChart>

                        <Pie
                          data={chartData}
                          dataKey="value"
                          nameKey="name"
                          outerRadius={120}
                          label
                        >

                          {
                            chartData.map(
                              (_, index) => (
                                <Cell
                                  key={index}
                                  fill={
                                    COLORS[index]
                                  }
                                />
                              )
                            )
                          }

                        </Pie>

                        <Tooltip />

                      </PieChart>

                    </ResponsiveContainer>

                  </div>

                </div>
              </div>
            )
          }
          
          
      </div>
    </div>
  )
}

export default App