export type Layer = {
  name: string;
  material: string;
  thicknessMm: number;
  modulusMpa: number;
};

export type DamagePoint = {
  cycle: number;
  damage: number;
  residualLifeYears: number;
};

export type MixItem = {
  component: string;
  share: number;
};

export type VariantMetric = {
  variant: string;
  resourceYears: number;
  lccMillion: number;
  risk: number;
};

export type Project = {
  id: string;
  name: string;
  status: 'draft' | 'active' | 'archived';
  owner: string;
};

export type MaterialRecord = {
  id: string;
  name: string;
  density: number;
  category: string;
};

export type RecipeRecord = {
  id: string;
  name: string;
  binder: number;
  aggregate: number;
  additive: number;
};
