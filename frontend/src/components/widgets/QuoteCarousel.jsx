import { MessageSquareQuote } from 'lucide-react'

export default function QuoteCarousel({ comments }) {
    if (!comments || comments.length === 0) return null

    return (
        <div className="glass-panel p-6 h-full flex flex-col">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <MessageSquareQuote className="w-5 h-5 text-accent" /> Contextual Verbatim
            </h3>

            <div className="space-y-4 overflow-y-auto pr-2 flex-1 scrollbar-hide">
                {comments.map((comment, i) => (
                    <div key={i} className="glass-card p-4">
                        <div className="flex justify-between items-start mb-2">
                            <span className="font-semibold text-sm">{comment.author}</span>
                            <div className="flex items-center gap-2">
                                {comment.sentiment.is_sarcastic && (
                                    <span className="text-[10px] uppercase font-bold text-accent bg-accent/10 px-2 py-0.5 rounded">Sarcasm Detected</span>
                                )}
                                <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${comment.sentiment.label === 'positive' ? 'bg-success/10 text-success' :
                                        comment.sentiment.label === 'negative' ? 'bg-error/10 text-error' :
                                            'bg-textMuted/10 text-textMuted'
                                    }`}>
                                    {comment.sentiment.label}
                                </span>
                            </div>
                        </div>

                        <p className="text-sm text-text/90 italic leading-relaxed">
                            "{comment.text}"
                        </p>

                        <div className="mt-3 flex justify-between items-center">
                            <span className="text-xs text-textMuted font-medium text-primary">👍 {comment.likes}</span>
                            {comment.emotion && comment.emotion.length > 0 && (
                                <span className="text-xs font-medium bg-secondary/10 text-secondary px-2 py-0.5 rounded">
                                    {comment.emotion[0].label} ({Math.round(comment.emotion[0].score * 100)}%)
                                </span>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
