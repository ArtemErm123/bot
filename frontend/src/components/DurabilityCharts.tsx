import { Paper, Typography } from '@mui/material';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import type { DamagePoint } from '../types';

export function DurabilityCharts({ data }: { data: DamagePoint[] }) {
  return (
    <Paper sx={{ p: 2, height: 340 }}>
      <Typography variant="h6" gutterBottom>
        Повреждаемость и остаточный ресурс
      </Typography>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="cycle" label={{ value: 'Годы эксплуатации', position: 'insideBottomRight', offset: -5 }} />
          <YAxis yAxisId="left" />
          <YAxis yAxisId="right" orientation="right" />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="damage" stroke="#e53935" name="Повреждаемость, %" strokeWidth={2} />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="residualLifeYears"
            stroke="#1e88e5"
            name="Остаточный ресурс, лет"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </Paper>
  );
}
