// A compact K-Means implementation that runs entirely in the browser.
// This mirrors the notebook's `KMeans(n_clusters=4)` step on standardized
// features — it's real clustering math, just running client-side instead
// of in a Python process.

function standardize(matrix) {
  const cols = matrix[0].length;
  const means = new Array(cols).fill(0);
  const stds = new Array(cols).fill(0);

  for (let j = 0; j < cols; j++) {
    let sum = 0;
    for (const row of matrix) sum += row[j];
    means[j] = sum / matrix.length;
  }
  for (let j = 0; j < cols; j++) {
    let sq = 0;
    for (const row of matrix) sq += (row[j] - means[j]) ** 2;
    stds[j] = Math.sqrt(sq / matrix.length) || 1;
  }
  return matrix.map((row) => row.map((v, j) => (v - means[j]) / stds[j]));
}

function distance(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += (a[i] - b[i]) ** 2;
  return sum;
}

// Deterministic k-means: instead of random initialization (which would make
// cluster IDs shuffle between page loads), seed centroids from evenly
// spaced points along the data sorted by their first feature. Same input
// data always produces the same cluster assignments.
function kmeans(matrix, k, maxIter = 50) {
  const sortedIdx = matrix
    .map((row, i) => [row[0], i])
    .sort((a, b) => a[0] - b[0])
    .map(([, i]) => i);

  let centroids = [];
  for (let c = 0; c < k; c++) {
    const idx = sortedIdx[Math.floor(((c + 0.5) * matrix.length) / k)];
    centroids.push([...matrix[idx]]);
  }

  let assignments = new Array(matrix.length).fill(0);

  for (let iter = 0; iter < maxIter; iter++) {
    let changed = false;
    for (let i = 0; i < matrix.length; i++) {
      let best = 0;
      let bestDist = Infinity;
      for (let c = 0; c < k; c++) {
        const d = distance(matrix[i], centroids[c]);
        if (d < bestDist) {
          bestDist = d;
          best = c;
        }
      }
      if (assignments[i] !== best) changed = true;
      assignments[i] = best;
    }

    const sums = Array.from({ length: k }, () => new Array(matrix[0].length).fill(0));
    const counts = new Array(k).fill(0);
    for (let i = 0; i < matrix.length; i++) {
      counts[assignments[i]]++;
      for (let j = 0; j < matrix[i].length; j++) sums[assignments[i]][j] += matrix[i][j];
    }
    for (let c = 0; c < k; c++) {
      if (counts[c] === 0) continue;
      centroids[c] = sums[c].map((s) => s / counts[c]);
    }
    if (!changed) break;
  }

  return assignments;
}
