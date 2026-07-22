// Embedded dataset — a representative snapshot per country, in the same
// shape/spirit as the Kaggle "world-energy-transition-2000-2025" dataset
// used in the original Colab notebook. Shipping the data with the site
// means there's nothing to download, no API key, and no server needed.
const COUNTRIES = [
  { code: "US", name: "United States", region: "North America", incomeGroup: "High income", population: 335, gdp: 27.4, renewableShare: 22, fossilShare: 60, carbonIntensity: 368 },
  { code: "DE", name: "Germany", region: "Europe", incomeGroup: "High income", population: 84, gdp: 4.5, renewableShare: 46, fossilShare: 42, carbonIntensity: 311 },
  { code: "CN", name: "China", region: "Asia", incomeGroup: "Upper middle income", population: 1412, gdp: 17.7, renewableShare: 31, fossilShare: 62, carbonIntensity: 543 },
  { code: "IN", name: "India", region: "Asia", incomeGroup: "Lower middle income", population: 1428, gdp: 3.7, renewableShare: 23, fossilShare: 73, carbonIntensity: 632 },
  { code: "BR", name: "Brazil", region: "South America", incomeGroup: "Upper middle income", population: 216, gdp: 2.1, renewableShare: 82, fossilShare: 16, carbonIntensity: 96 },
  { code: "NO", name: "Norway", region: "Europe", incomeGroup: "High income", population: 5.5, gdp: 0.5, renewableShare: 98, fossilShare: 2, carbonIntensity: 26 },
  { code: "FR", name: "France", region: "Europe", incomeGroup: "High income", population: 68, gdp: 3.0, renewableShare: 27, fossilShare: 8, carbonIntensity: 55 },
  { code: "GB", name: "United Kingdom", region: "Europe", incomeGroup: "High income", population: 67, gdp: 3.3, renewableShare: 43, fossilShare: 40, carbonIntensity: 238 },
  { code: "JP", name: "Japan", region: "Asia", incomeGroup: "High income", population: 125, gdp: 4.2, renewableShare: 22, fossilShare: 71, carbonIntensity: 494 },
  { code: "AU", name: "Australia", region: "Oceania", incomeGroup: "High income", population: 26, gdp: 1.7, renewableShare: 32, fossilShare: 66, carbonIntensity: 549 },
  { code: "CA", name: "Canada", region: "North America", incomeGroup: "High income", population: 40, gdp: 2.1, renewableShare: 68, fossilShare: 19, carbonIntensity: 128 },
  { code: "ES", name: "Spain", region: "Europe", incomeGroup: "High income", population: 48, gdp: 1.6, renewableShare: 50, fossilShare: 30, carbonIntensity: 174 },
  { code: "IT", name: "Italy", region: "Europe", incomeGroup: "High income", population: 59, gdp: 2.2, renewableShare: 41, fossilShare: 55, carbonIntensity: 259 },
  { code: "ZA", name: "South Africa", region: "Africa", incomeGroup: "Upper middle income", population: 60, gdp: 0.4, renewableShare: 12, fossilShare: 86, carbonIntensity: 707 },
  { code: "MX", name: "Mexico", region: "North America", incomeGroup: "Upper middle income", population: 128, gdp: 1.8, renewableShare: 24, fossilShare: 71, carbonIntensity: 423 },
  { code: "SE", name: "Sweden", region: "Europe", incomeGroup: "High income", population: 10, gdp: 0.6, renewableShare: 71, fossilShare: 2, carbonIntensity: 42 },
];

function findCountry(code) {
  return COUNTRIES.find((c) => c.code === code) || COUNTRIES[0];
}
