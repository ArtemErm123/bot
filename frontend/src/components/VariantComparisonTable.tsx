import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import type { VariantMetric } from '../types';

export function VariantComparisonTable({ rows }: { rows: VariantMetric[] }) {
  const bestResource = Math.max(...rows.map((item) => item.resourceYears));
  const bestLcc = Math.min(...rows.map((item) => item.lccMillion));

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Сравнение вариантов
      </Typography>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Вариант</TableCell>
              <TableCell align="right">Ресурс, лет</TableCell>
              <TableCell align="right">LCC, млн ₽</TableCell>
              <TableCell align="right">Риск</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.variant}>
                <TableCell>{row.variant}</TableCell>
                <TableCell align="right" sx={{ bgcolor: row.resourceYears === bestResource ? '#c8e6c9' : undefined }}>
                  {row.resourceYears}
                </TableCell>
                <TableCell align="right" sx={{ bgcolor: row.lccMillion === bestLcc ? '#bbdefb' : undefined }}>
                  {row.lccMillion}
                </TableCell>
                <TableCell align="right">{row.risk.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
