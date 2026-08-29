/**
 * RiskScoreGauge
 * Displays the overall automated risk score (0 = safest) with a
 * qualitative band label.
 *
 * @param {object} props
 * @param {number} props.score       - 0-100
 * @param {number} [props.max=100]
 * @param {string} props.band        - e.g. "Low Risk Assessment"
 * @param {string} [props.description]
 */
export default function RiskScoreGauge({ score = 0, max = 100, band = "", description = "" }) {
  const pct = Math.min(100, Math.max(0, (score / max) * 100));
  const isLow = pct <= 33;
  const isMedium = pct > 33 && pct <= 66;

  const ringColor = isLow ? "border-secondary" : isMedium ? "border-tertiary" : "border-error";
  const scoreColor = isLow ? "text-secondary" : isMedium ? "text-tertiary" : "text-error";

  return (
    <div className="bg-surface-container-lowest border border-outline-variant rounded-lg p-6 flex items-center gap-6">
      <div className={`w-32 h-32 rounded-full border-8 ${ringColor} flex items-center justify-center relative shrink-0`}>
        <div className={`absolute inset-0 rounded-full border-8 ${ringColor} opacity-20`} />
        <span className={`text-4xl font-bold ${scoreColor}`}>{score}</span>
      </div>
      <div>
        <h3 className="text-xl font-semibold text-on-surface mb-1">Overall Risk Score</h3>
        <p className={`text-base font-medium ${scoreColor}`}>{band}</p>
        {description && (
          <p className="text-sm text-on-surface-variant mt-2 max-w-sm">{description}</p>
        )}
      </div>
    </div>
  );
}
