import { Button, Paper, Stack, TextField, Typography } from '@mui/material';

export function LoginPage() {
  return (
    <Paper sx={{ maxWidth: 460, p: 3, mx: 'auto' }}>
      <Stack spacing={2}>
        <Typography variant="h5">Login</Typography>
        <TextField label="Email" type="email" />
        <TextField label="Password" type="password" />
        <Button variant="contained">Sign in</Button>
      </Stack>
    </Paper>
  );
}
