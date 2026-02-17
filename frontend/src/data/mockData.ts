import type { DamagePoint, Layer, MixItem, Project, VariantMetric } from '../types';

export const demoLayers: Layer[] = [
  { name: 'Износостойкий слой', material: 'SMA-16', thicknessMm: 50, modulusMpa: 3600 },
  { name: 'Выравнивающий слой', material: 'AC-22', thicknessMm: 80, modulusMpa: 3200 },
  { name: 'Основание', material: 'ЩПС C5', thicknessMm: 180, modulusMpa: 850 },
  { name: 'Подстилающий слой', material: 'Песок', thicknessMm: 250, modulusMpa: 250 },
];

export const damageSeries: DamagePoint[] = [
  { cycle: 1, damage: 6, residualLifeYears: 24 },
  { cycle: 3, damage: 18, residualLifeYears: 20 },
  { cycle: 5, damage: 31, residualLifeYears: 16 },
  { cycle: 7, damage: 49, residualLifeYears: 12 },
  { cycle: 9, damage: 63, residualLifeYears: 9 },
  { cycle: 11, damage: 82, residualLifeYears: 5 },
];

export const mixComposition: MixItem[] = [
  { component: 'Щебень', share: 48 },
  { component: 'Песок', share: 31 },
  { component: 'Битум', share: 9 },
  { component: 'Минпорошок', share: 7 },
  { component: 'Добавка', share: 5 },
];

export const variants: VariantMetric[] = [
  { variant: 'Вариант A', resourceYears: 18, lccMillion: 210, risk: 0.27 },
  { variant: 'Вариант B', resourceYears: 22, lccMillion: 225, risk: 0.18 },
  { variant: 'Вариант C', resourceYears: 20, lccMillion: 198, risk: 0.34 },
  { variant: 'Вариант D', resourceYears: 25, lccMillion: 246, risk: 0.16 },
];

export const projects: Project[] = [
  { id: 'p-101', name: 'Капремонт М-7 (км 122-130)', status: 'active', owner: 'Иванов' },
  { id: 'p-102', name: 'Обход г. Омск', status: 'draft', owner: 'Петрова' },
  { id: 'p-103', name: 'Реконструкция А-322', status: 'archived', owner: 'Сидоров' },
];
