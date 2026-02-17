import { Paper, Stack, Typography } from '@mui/material';
import { MixCompositionChart } from '../components/MixCompositionChart';
import { mixComposition } from '../data/mockData';

export function MixBuilderPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">MixBuilder</Typography>
      <Paper sx={{ p: 2 }}>
        <Typography mb={2}>Конструктор состава смеси.</Typography>
        <MixCompositionChart data={mixComposition} />
      </Paper>
    </Stack>
  );
}
