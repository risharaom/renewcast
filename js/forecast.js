// A lightweight, deterministic trend model. It's not the notebook's actual
// scikit-learn RandomForestRegressor (that needs a Python process to run —
// see the /backend project if you want that full version), but it uses the
// same underlying relationship the notebook explored: current renewable
// share + population/GDP-scaled demand, projected forward with a realistic
// growth curve. Same inputs always produce the same outputs.

function generateForecast(countryCode, targetYear) {
  const country = findCountry(countryCode);

  const seed = countryCode.charCodeAt(0) + countryCode.charCodeAt(1) + targetYear;
  const rand = (n) => {
    const x = Math.sin(seed * (n + 1)) * 10000;
    return x - Math.floor(x);
  };

  const baseDemand = 50 + country.population * 3.5 + country.gdp * 80;
  const baseRenewable = baseDemand * (country.renewableShare / 100);

  const series = [];
  for (let year = 2015; year <= targetYear; year++) {
    const t = year - 2015;
    const isFuture = year > 2025;
    const genGrowth = 1 + 0.045 * t + (rand(t) - 0.5) * 0.04;
    const demGrowth = 1 + 0.022 * t + (rand(t + 20) - 0.5) * 0.03;
    const gen = baseRenewable * genGrowth;
    const dem = baseDemand * demGrowth;
    series.push({
      year,
      historicalGeneration: isFuture ? null : Math.round(gen),
      predictedGeneration: isFuture ? Math.round(gen) : null,
      historicalDemand: isFuture ? null : Math.round(dem),
      predictedDemand: isFuture ? Math.round(dem) : null,
      coverage: Math.round((gen / dem) * 1000) / 10,
    });
  }

  const overlapIdx = series.findIndex((s) => s.year === 2025);
  if (overlapIdx >= 0) {
    series[overlapIdx].predictedGeneration = series[overlapIdx].historicalGeneration;
    series[overlapIdx].predictedDemand = series[overlapIdx].historicalDemand;
  }

  const last = series[series.length - 1];
  const predictedGeneration = last.predictedGeneration ?? 0;
  const predictedDemand = last.predictedDemand ?? 0;
  const coverage = (predictedGeneration / predictedDemand) * 100;
  const gap = predictedDemand - predictedGeneration;

  return {
    country,
    targetYear,
    series,
    stats: { predictedGeneration, predictedDemand, coverage, gap },
  };
}
