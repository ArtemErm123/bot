import { Paper, Stack, Typography } from '@mui/material';

export function ScenariosPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">Scenarios</Typography>
      <Paper sx={{ p: 2 }}>
        <Typography>Управление сценариями нагрузок и климата.</Typography>
      </Paper>
    </Stack>
  );
}
