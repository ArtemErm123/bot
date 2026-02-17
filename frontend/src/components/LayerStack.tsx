import { Box, Paper, Stack, Typography } from '@mui/material';
import type { Layer } from '../types';

const palette = ['#1e88e5', '#43a047', '#fdd835', '#8d6e63', '#ab47bc'];

export function LayerStack({ layers }: { layers: Layer[] }) {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Схема слоёв конструкции
      </Typography>
      <Stack spacing={1}>
        {layers.map((layer, idx) => (
          <Box
            key={layer.name}
            sx={{
              borderRadius: 1,
              p: 1.5,
              color: '#fff',
              backgroundColor: palette[idx % palette.length],
            }}
          >
            <Typography fontWeight={700}>{layer.name}</Typography>
            <Typography variant="body2">
              {layer.material} · {layer.thicknessMm} мм · E={layer.modulusMpa} МПа
            </Typography>
          </Box>
        ))}
      </Stack>
    </Paper>
  );
}
