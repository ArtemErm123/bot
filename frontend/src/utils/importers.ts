import Papa from 'papaparse';
import * as XLSX from 'xlsx';

export type ImportFormat = 'csv' | 'xlsx' | 'json';

export function detectFormat(fileName: string): ImportFormat | null {
  const ext = fileName.split('.').pop()?.toLowerCase();
  if (ext === 'csv' || ext === 'xlsx' || ext === 'json') {
    return ext;
  }
  return null;
}

export function parseTextData(content: string, format: Exclude<ImportFormat, 'xlsx'>): Record<string, unknown>[] {
  if (format === 'json') {
    const parsed = JSON.parse(content);
    return Array.isArray(parsed) ? parsed : [parsed];
  }

  const result = Papa.parse<Record<string, unknown>>(content, {
    header: true,
    skipEmptyLines: true,
  });

  return result.data;
}

export function parseXlsxData(buffer: ArrayBuffer): Record<string, unknown>[] {
  const workbook = XLSX.read(buffer, { type: 'array' });
  const firstSheet = workbook.SheetNames[0];
  const sheet = workbook.Sheets[firstSheet];
  return XLSX.utils.sheet_to_json(sheet, { defval: '' });
}
