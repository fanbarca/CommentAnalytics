import { Layers } from 'lucide-react'

export default function AspectHeatmap({ aspects }) {
    if (!aspects || Object.keys(aspects).length === 0) return null

    // Convert dict to array and sort by mentions
    const aspectList = Object.entries(aspects)
        .map(([name, data]) => ({ name, ...data }))
        .sort((a, b) => b.mentions - a.mentions)
        .slice(0, 8)

    return (
        <div className="glass-panel p-6 h-full">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Layers className="w-5 h-5 text-primary" /> Feature Sentiment
            </h3>

            <div className="grid grid-cols-2 gap-4">
                {aspectList.map(aspect => {
                    const isPositive = aspect.label === 'positive'
                    const isNegative = aspect.label === 'negative'
                    const isNeutral = aspect.label === 'neutral'

                    return (
                        <div
                            key={aspect.name}
                            className={`p-4 rounded-xl border flex flex-col justify-between h-24 transition-colors ${isPositive ? 'bg-success/5 border-success/20 hover:border-success/40' :
                                    isNegative ? 'bg-error/5 border-error/20 hover:border-error/40' :
                                        'bg-white/5 border-white/10 hover:border-white/20'
                                }`}
                            title={aspect.quotes[0] || ""}
                        >
                            <div className="flex justify-between items-start">
                                <span className="font-semibold capitalize truncate">{aspect.name}</span>
                                {isPositive && <span className="text-xl leading-none">😌</span>}
                                {isNegative && <span className="text-xl leading-none">😠</span>}
                                {isNeutral && <span className="text-xl leading-none">😐</span>}
                            </div>
                            <div className="mt-auto flex justify-between items-center text-sm">
                                <span className="text-textMuted">{aspect.mentions} mentions</span>
                                <span className={`font-bold ${isPositive ? 'text-success' : isNegative ? 'text-error' : 'text-textMuted'
                                    }`}>
                                    {aspect.compound > 0 ? '+' : ''}{aspect.compound.toFixed(2)}
                                </span>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
