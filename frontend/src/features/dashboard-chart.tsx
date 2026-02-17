import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { name: 'A', value: 10 },
  { name: 'B', value: 16 },
  { name: 'C', value: 12 }
]

export const DashboardChart = () => (
  <ResponsiveContainer width="100%" height={240}>
    <LineChart data={data}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="value" stroke="#1976d2" />
    </LineChart>
  </ResponsiveContainer>
)
