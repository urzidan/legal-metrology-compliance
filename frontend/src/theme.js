// theme.js
// Central palette pulled from the original Stitch tailwind.config so every
// component references one source of truth instead of hard-coded hexes.

export const colors = {
  primary: "#000000",
  onPrimary: "#ffffff",
  primaryContainer: "#131b2e",
  onPrimaryContainer: "#7c839b",
  secondary: "#006c4a",
  onSecondary: "#ffffff",
  secondaryContainer: "#82f5c1",
  onSecondaryContainer: "#00714e",
  error: "#ba1a1a",
  onError: "#ffffff",
  errorContainer: "#ffdad6",
  onErrorContainer: "#93000a",
  background: "#f8f9ff",
  onBackground: "#0b1c30",
  surface: "#f8f9ff",
  surfaceContainerLowest: "#ffffff",
  surfaceContainerLow: "#eff4ff",
  surfaceContainer: "#e5eeff",
  surfaceDim: "#cbdbf5",
  onSurface: "#0b1c30",
  onSurfaceVariant: "#45464d",
  outline: "#76777d",
  outlineVariant: "#c6c6cd",
  inverseSurface: "#213145",
  inverseOnSurface: "#eaf1ff",
};

// Status → color mapping used across the compliance table, bounding boxes,
// and violation cards so "pass/flag/pending" always reads the same way.
export const statusColor = {
  pass: { text: "text-secondary", bg: "bg-secondary-container", border: "border-secondary" },
  flagged: { text: "text-error", bg: "bg-error-container", border: "border-error" },
  pending: { text: "text-on-surface-variant", bg: "bg-surface-container", border: "border-outline" },
};
