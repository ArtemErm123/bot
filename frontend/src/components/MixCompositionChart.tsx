import { Paper, Typography } from '@mui/material';
import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts';
import type { MixItem } from '../types';

const colors = ['#1976d2', '#26a69a', '#ffb300', '#8e24aa', '#ef5350'];

export function MixCompositionChart({ data }: { data: MixItem[] }) {
  return (
    <Paper sx={{ p: 2, height: 340 }}>
      <Typography variant="h6" gutterBottom>
        Диаграмма состава смеси
      </Typography>
      <ResponsiveContainer width="100%" height="90%">
        <PieChart>
          <Pie data={data} dataKey="share" nameKey="component" outerRadius={110} label>
            {data.map((entry, i) => (
              <Cell key={entry.component} fill={colors[i % colors.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Paper>
  );
}
