import { Paper, Stack, Typography } from '@mui/material';
import { DurabilityCharts } from '../components/DurabilityCharts';
import { damageSeries } from '../data/mockData';

export function ResultsPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">Results</Typography>
      <DurabilityCharts data={damageSeries} />
      <Paper sx={{ p: 2 }}>
        <Typography>Сводные результаты расчётов по сценариям.</Typography>
      </Paper>
    </Stack>
  );
}
