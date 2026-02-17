import { Chip, Paper, Stack, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@mui/material';
import { useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { ImportPanel } from '../components/ImportPanel';
import { projects } from '../data/mockData';

export function ProjectsPage() {
  const [importRows, setImportRows] = useState<Record<string, unknown>[]>([]);

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Projects</Typography>
      <ImportPanel onData={setImportRows} />
      <Paper sx={{ p: 2 }}>
        <Typography variant="subtitle1" gutterBottom>
          Импортировано строк: {importRows.length}
        </Typography>
      </Paper>
      <Paper sx={{ p: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Название</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Ответственный</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {projects.map((project) => (
              <TableRow key={project.id}>
                <TableCell>{project.id}</TableCell>
                <TableCell>
                  <RouterLink to={`/projects/${project.id}`}>{project.name}</RouterLink>
                </TableCell>
                <TableCell>
                  <Chip size="small" label={project.status} color={project.status === 'active' ? 'success' : 'default'} />
                </TableCell>
                <TableCell>{project.owner}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Stack>
  );
}
