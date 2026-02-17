import { Paper, Stack, Typography } from '@mui/material';

export function ReportsPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">Reports</Typography>
      <Paper sx={{ p: 2 }}>
        <Typography>Формирование отчётов и экспорт в PDF/XLSX (заглушка).</Typography>
      </Paper>
    </Stack>
  );
}
