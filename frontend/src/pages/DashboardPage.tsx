import { Box, Stack, Typography } from '@mui/material';
import { damageSeries, demoLayers, mixComposition, variants } from '../data/mockData';
import { DurabilityCharts } from '../components/DurabilityCharts';
import { LayerStack } from '../components/LayerStack';
import { MixCompositionChart } from '../components/MixCompositionChart';
import { VariantComparisonTable } from '../components/VariantComparisonTable';

export function DashboardPage() {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">Dashboard</Typography>
      <Box display="grid" gap={2} gridTemplateColumns={{ xs: '1fr', md: '1fr 2fr' }}>
        <LayerStack layers={demoLayers} />
        <DurabilityCharts data={damageSeries} />
      </Box>
      <Box display="grid" gap={2} gridTemplateColumns={{ xs: '1fr', md: '1fr 1fr' }}>
        <MixCompositionChart data={mixComposition} />
        <VariantComparisonTable rows={variants} />
      </Box>
    </Stack>
  );
}
