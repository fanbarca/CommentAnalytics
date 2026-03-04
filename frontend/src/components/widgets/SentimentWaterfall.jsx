import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { Activity } from 'lucide-react'

export default function SentimentWaterfall({ data, overall }) {
    // Format data for Recharts
    const chartData = data.map((d, i) => ({
        time: i,
        score: d.compound,
        label: new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }))

    const total = overall.positive + overall.negative + overall.neutral
    const getPercentage = (val) => total > 0 ? Math.round((val / total) * 100) : 0

    return (
        <div className="glass-panel p-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                    <Activity className="w-5 h-5 text-primary" /> Sentiment Timeline
                </h3>
                <div className="flex gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-success"></div>
                        <span className="text-sm font-medium">{getPercentage(overall.positive)}% Pos</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-textMuted"></div>
                        <span className="text-sm font-medium">{getPercentage(overall.neutral)}% Neu</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-3 h-3 rounded-full bg-error"></div>
                        <span className="text-sm font-medium">{getPercentage(overall.negative)}% Neg</span>
                    </div>
                </div>
            </div>

            <div className="h-[300px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                        <XAxis dataKey="label" stroke="#64748b" fontSize={12} tickMargin={10} />
                        <YAxis stroke="#64748b" fontSize={12} domain={[-1, 1]} tickFormatter={(val) => val.toFixed(1)} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                            itemStyle={{ color: '#f8fafc' }}
                        />
                        <Line
                            type="monotone"
                            dataKey="score"
                            stroke="#3b82f6"
                            strokeWidth={3}
                            dot={false}
                            activeDot={{ r: 6, fill: '#3b82f6', stroke: '#1e293b', strokeWidth: 2 }}
                        />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}
