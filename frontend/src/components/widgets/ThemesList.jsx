import { MessageCircle } from 'lucide-react'

export default function ThemesList({ themes }) {
    if (!themes || themes.length === 0) return null

    return (
        <div className="glass-panel p-6 h-full">
            <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <MessageCircle className="w-5 h-5 text-secondary" /> Key Conversation Themes
            </h3>

            <div className="space-y-4">
                {themes.map((theme, i) => (
                    <div key={theme.theme_id || i} className="glass-card p-4">
                        <div className="flex items-center gap-3 mb-3">
                            <div className="w-8 h-8 rounded-full bg-secondary/20 text-secondary flex items-center justify-center font-bold text-sm">
                                #{i + 1}
                            </div>
                            <div className="flex-1">
                                <h4 className="font-semibold truncate">{theme.name}</h4>
                            </div>
                        </div>

                        <div className="flex flex-wrap gap-2">
                            {theme.keywords.map(kw => (
                                <span key={kw} className="px-2 py-1 bg-white/5 border border-white/10 rounded-md text-xs text-textMuted font-medium hover:bg-white/10 hover:text-text transition-colors cursor-default">
                                    {kw}
                                </span>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}
