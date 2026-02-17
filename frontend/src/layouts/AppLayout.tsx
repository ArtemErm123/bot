import DashboardIcon from '@mui/icons-material/Dashboard';
import FolderIcon from '@mui/icons-material/Folder';
import LoginIcon from '@mui/icons-material/Login';
import { AppBar, Box, Button, Container, Stack, Toolbar, Typography } from '@mui/material';
import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/login', label: 'Login', icon: <LoginIcon fontSize="small" /> },
  { to: '/', label: 'Dashboard', icon: <DashboardIcon fontSize="small" /> },
  { to: '/projects', label: 'Projects', icon: <FolderIcon fontSize="small" /> },
  { to: '/scenarios', label: 'Scenarios' },
  { to: '/results', label: 'Results' },
  { to: '/reports', label: 'Reports' },
];

export function AppLayout() {
  return (
    <>
      <AppBar position="sticky">
        <Toolbar sx={{ gap: 2, flexWrap: 'wrap' }}>
          <Typography variant="h6" sx={{ mr: 1 }}>
            Pavement Planner
          </Typography>
          <Stack direction="row" spacing={1} flexWrap="wrap">
            {navItems.map((item) => (
              <Button
                key={item.to}
                color="inherit"
                component={NavLink}
                to={item.to}
                startIcon={item.icon}
                sx={{ '&.active': { textDecoration: 'underline' } }}
              >
                {item.label}
              </Button>
            ))}
          </Stack>
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 3 }}>
        <Box>
          <Outlet />
        </Box>
      </Container>
    </>
  );
}
