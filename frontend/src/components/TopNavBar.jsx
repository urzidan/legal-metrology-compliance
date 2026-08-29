import { Bell, Settings } from "lucide-react";

/**
 * TopNavBar
 * Sticky header showing product branding and headline audit stats.
 *
 * @param {object} props
 * @param {number} props.totalAudited
 * @param {number} props.passRate     - 0-100
 * @param {number} props.pending
 * @param {() => void} [props.onProfileClick]
 */
export default function TopNavBar({ totalAudited = 0, passRate = 0, pending = 0, onProfileClick }) {
  return (
    <header className="sticky top-0 z-50 flex justify-between items-center w-full px-8 py-4 bg-surface border-b border-outline-variant">
      <div className="flex items-center gap-6">
        <h1 className="text-3xl font-bold tracking-tight text-on-background">PackSure</h1>
        <span className="bg-primary-container text-on-primary-container text-xs font-semibold px-2 py-1 rounded-full uppercase tracking-wide">
          SIH 2026 | Team Innovate Ninjas
        </span>
      </div>

      <nav className="hidden md:flex flex-1 justify-center">
        <ul className="flex gap-6 text-sm">
          <li>
            <span className="text-primary font-bold border-b-2 border-primary pb-1 block">
              Total Audited: {totalAudited.toLocaleString()}
            </span>
          </li>
          <li>
            <span className="text-on-surface-variant px-2 py-1 rounded block">
              Pass Rate: {passRate.toFixed(1)}%
            </span>
          </li>
          <li>
            <span className="text-on-surface-variant px-2 py-1 rounded block">
              Pending: {pending}
            </span>
          </li>
        </ul>
      </nav>

      <div className="flex items-center gap-3">
        <button aria-label="notifications" className="text-primary hover:bg-surface-container-low p-2 rounded-full transition-colors">
          <Bell size={20} />
        </button>
        <button aria-label="settings" className="text-primary hover:bg-surface-container-low p-2 rounded-full transition-colors">
          <Settings size={20} />
        </button>
        <button
          onClick={onProfileClick}
          className="bg-primary text-on-primary px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider hover:bg-primary-container hover:text-on-primary-container transition-colors"
        >
          Profile
        </button>
      </div>
    </header>
  );
}
