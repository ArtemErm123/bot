import { Paper, Stack, Typography } from '@mui/material';
import { LayerStack } from '../components/LayerStack';
import { demoLayers } from '../data/mockData';

export function VariantEditorPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">VariantEditor</Typography>
      <Paper sx={{ p: 2 }}>
        <Typography mb={2}>Редактор параметров варианта конструкции.</Typography>
        <LayerStack layers={demoLayers} />
      </Paper>
    </Stack>
  );
}
