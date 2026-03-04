import { useState } from 'react'
import { analyzeVideo } from './services/api'
import {
  BarChart3,
  Search,
  Youtube,
  TrendingUp,
  MessageSquare,
  AlertCircle
} from 'lucide-react'

import SentimentWaterfall from './components/widgets/SentimentWaterfall'
import AspectHeatmap from './components/widgets/AspectHeatmap'
import ThemesList from './components/widgets/ThemesList'
import QuoteCarousel from './components/widgets/QuoteCarousel'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  const extractVideoId = (inputUrl) => {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
    const match = inputUrl.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
  }

  const handleAnalyze = async (e) => {
    e.preventDefault()
    setError(null)

    const videoId = extractVideoId(url)
    if (!videoId) {
      setError("Please enter a valid YouTube URL.")
      return
    }

    setLoading(true)
    try {
      const response = await analyzeVideo(videoId)
      setData(response)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-text p-6 md:p-12">
      {/* Header */}
      <header className="max-w-6xl mx-auto flex items-center justify-between mb-12 animate-fade-in">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-gradient-to-br from-primary to-secondary rounded-xl shadow-lg shadow-primary/20">
            <BarChart3 className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/60">
              Vibe <span className="text-primary">Lens</span>
            </h1>
            <p className="text-sm text-textMuted hidden sm:block">AI-Powered YouTube Sentiment Analyzer</p>
          </div>
        </div>

        {/* Search Bar */}
        <form onSubmit={handleAnalyze} className="flex-1 max-w-xl ml-8 hidden md:flex relative group">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <Youtube className="w-5 h-5 text-textMuted group-focus-within:text-primary transition-colors" />
          </div>
          <input
            type="text"
            placeholder="Paste YouTube Video URL..."
            className="input-field pl-12 pr-32"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            type="submit"
            disabled={loading}
            className="absolute right-2 top-2 bottom-2 btn-primary !py-1 flex items-center gap-2"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <Search className="w-4 h-4" /> Analyze
              </>
            )}
          </button>
        </form>
      </header>

      {/* Mobile Search - Visible only on small screens */}
      <form onSubmit={handleAnalyze} className="md:hidden flex flex-col gap-4 mb-8">
        <input
          type="text"
          placeholder="Paste YouTube Video URL..."
          className="input-field"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button type="submit" className="btn-primary w-full" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Video'}
        </button>
      </form>

      {error && (
        <div className="max-w-6xl mx-auto mb-8 p-4 bg-error/10 border border-error/50 rounded-lg flex items-center gap-3 text-error animate-fade-in">
          <AlertCircle className="w-5 h-5" />
          <p>{error}</p>
        </div>
      )}

      {/* Empty State */}
      {!data && !loading && !error && (
        <div className="max-w-2xl mx-auto mt-24 text-center animate-fade-in-up">
          <div className="w-24 h-24 mx-auto mb-8 relative">
            <div className="absolute inset-0 bg-primary/20 rounded-full blur-xl animate-pulse"></div>
            <div className="relative w-full h-full glass-panel flex items-center justify-center rounded-3xl">
              <MessageSquare className="w-10 h-10 text-primary" />
            </div>
          </div>
          <h2 className="text-3xl font-bold mb-4">Discover Audience Reality</h2>
          <p className="text-textMuted text-lg mb-8 leading-relaxed">
            Drop a YouTube link above to instantly extract emotions, sentiments, themes, and sarcasm from hundreds of viewer comments.
          </p>
        </div>
      )}

      {/* Dashboard Content */}
      {data && !loading && (
        <main className="max-w-7xl mx-auto space-y-6 lg:space-y-8 animate-fade-in-up">
          {/* Metadata Bar */}
          <div className="glass-panel p-6 flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-1">{data.metadata.title}</h2>
              <p className="text-textMuted">{data.metadata.channel} • {new Date(data.metadata.published_at).toLocaleDateString()}</p>
            </div>
            <div className="flex gap-4">
              <div className="text-center px-4 border-r border-white/10">
                <p className="text-sm text-textMuted mb-1">Views</p>
                <p className="font-semibold">{data.metadata.view_count.toLocaleString()}</p>
              </div>
              <div className="text-center px-4 border-r border-white/10">
                <p className="text-sm text-textMuted mb-1">Likes</p>
                <p className="font-semibold text-primary">{data.metadata.like_count.toLocaleString()}</p>
              </div>
              <div className="text-center px-4">
                <p className="text-sm text-textMuted mb-1">Comments</p>
                <p className="font-semibold">{data.metadata.comment_count.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
            {/* Left Column: Waterfall & Topics */}
            <div className="lg:col-span-2 space-y-6 lg:space-y-8">
              <SentimentWaterfall data={data.dashboard.waterfall} overall={data.dashboard.overall_sentiment} />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
                <ThemesList themes={data.dashboard.themes} />
                <AspectHeatmap aspects={data.dashboard.aspects} />
              </div>
            </div>

            {/* Right Column: Key Metrics & Quotes */}
            <div className="space-y-6 lg:space-y-8">
              <div className="glass-panel p-6">
                <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-secondary" /> Top Emotions
                </h3>
                <div className="space-y-4">
                  {data.dashboard.top_emotions.map(([emotion, count]) => (
                    <div key={emotion} className="flex items-center justify-between">
                      <span className="capitalize text-textMuted">{emotion}</span>
                      <div className="flex items-center gap-3">
                        <div className="w-32 h-2 bg-surface rounded-full overflow-hidden">
                          <div
                            className="h-full bg-secondary rounded-full"
                            style={{ width: `${(count / data.dashboard.top_emotions[0][1]) * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium w-6 text-right">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <QuoteCarousel comments={data.dashboard.top_comments} />
            </div>
          </div>
        </main>
      )}
    </div>
  )
}

export default App
