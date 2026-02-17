import { Button, Paper, Stack, Typography } from '@mui/material';
import { Link as RouterLink, useParams } from 'react-router-dom';

export function ProjectDetailPage() {
  const { id } = useParams();

  return (
    <Stack spacing={2}>
      <Typography variant="h4">ProjectDetail</Typography>
      <Paper sx={{ p: 2 }}>
        <Typography>Карточка проекта: {id}</Typography>
        <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
          <Button component={RouterLink} to="/variant-editor" variant="contained">
            VariantEditor
          </Button>
          <Button component={RouterLink} to="/mix-builder" variant="outlined">
            MixBuilder
          </Button>
        </Stack>
      </Paper>
    </Stack>
  );
}
