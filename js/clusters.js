// Runs K-Means on the embedded country dataset and produces the same shape
// of summary the fuller Python backend does: cluster id, description,
// group averages, and member countries — ordered so "Cluster 3" reads as
// the cleanest group, like the original notebook's output.

function computeClusters() {
  const features = COUNTRIES.map((c) => [
    c.renewableShare,
    c.fossilShare,
    c.carbonIntensity,
  ]);
  const scaled = standardize(features);
  const assignments = kmeans(scaled, 4);

  const withCluster = COUNTRIES.map((c, i) => ({ ...c, rawCluster: assignments[i] }));

  // Order raw cluster ids by average renewable share, low -> high, so the
  // labels read the same way every time regardless of k-means' internal ids.
  const groups = {};
  withCluster.forEach((c) => {
    (groups[c.rawCluster] ||= []).push(c);
  });
  const order = Object.entries(groups)
    .map(([id, members]) => [id, members.reduce((s, m) => s + m.renewableShare, 0) / members.length])
    .sort((a, b) => a[1] - b[1])
    .map(([id]) => id);

  const remap = {};
  order.forEach((oldId, newId) => (remap[oldId] = newId));

  const countriesWithCluster = withCluster.map((c) => ({ ...c, cluster: remap[c.rawCluster] }));

  const descriptions = [
    "Lower renewable share, higher fossil reliance and carbon intensity relative to the other discovered groups.",
    "Moderate renewable adoption with a still-significant fossil fuel base in the generation mix.",
    "Above-average renewable share with a generation mix actively shifting away from fossil fuels.",
    "Highest renewable share and lowest carbon intensity of the discovered groups — clean energy leaders.",
  ];

  const clusters = order.map((oldId, newId) => {
    const members = countriesWithCluster.filter((c) => c.cluster === newId);
    const avg = (key) => members.reduce((s, m) => s + m[key], 0) / members.length;
    return {
      id: newId,
      name: `Cluster ${newId}`,
      description: descriptions[newId],
      avgRenewable: Math.round(avg("renewableShare") * 10) / 10,
      avgFossil: Math.round(avg("fossilShare") * 10) / 10,
      avgCarbon: Math.round(avg("carbonIntensity") * 10) / 10,
      members,
    };
  });

  return { countries: countriesWithCluster, clusters };
}
