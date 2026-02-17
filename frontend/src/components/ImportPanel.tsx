import UploadFileIcon from '@mui/icons-material/UploadFile';
import { Alert, Button, Paper, Stack, Typography } from '@mui/material';
import { useRef, useState } from 'react';
import { detectFormat, parseTextData, parseXlsxData } from '../utils/importers';

export function ImportPanel({ onData }: { onData: (rows: Record<string, unknown>[]) => void }) {
  const [message, setMessage] = useState<string>('');
  const [error, setError] = useState<string>('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    setError('');
    const format = detectFormat(file.name);
    if (!format) {
      setError('Поддерживаются только CSV / XLSX / JSON');
      return;
    }

    try {
      let rows: Record<string, unknown>[] = [];
      if (format === 'xlsx') {
        rows = parseXlsxData(await file.arrayBuffer());
      } else {
        rows = parseTextData(await file.text(), format);
      }

      onData(rows);
      setMessage(`Импортировано ${rows.length} строк из ${file.name}`);
    } catch {
      setError(`Не удалось обработать файл ${file.name}`);
    }
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Stack spacing={1.5}>
        <Typography variant="h6">Импорт материалов / рецептов</Typography>
        <Typography variant="body2">Выберите CSV, XLSX или JSON файл.</Typography>
        <input
          ref={inputRef}
          type="file"
          hidden
          accept=".csv,.xlsx,.json"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) {
              void handleFile(file);
            }
          }}
        />
        <Button variant="contained" startIcon={<UploadFileIcon />} onClick={() => inputRef.current?.click()}>
          Загрузить файл
        </Button>
        {message && <Alert severity="success">{message}</Alert>}
        {error && <Alert severity="error">{error}</Alert>}
      </Stack>
    </Paper>
  );
}
