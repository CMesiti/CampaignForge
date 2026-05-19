import { Link, useLocation } from "react-router-dom";
import { Avatar } from "../ui";
import styles from "./AppShell.module.css";

interface AppShellProps {
  children?: React.ReactNode;
}

const NAV_LINKS = [
  { to: "/campaigns", label: "Campaigns" },
  { to: "/campaigns/join", label: "Join" },
];

export function AppShell({ children }: AppShellProps) {
  const location = useLocation();

  return (
    <div className={styles.shell}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <Link to="/campaigns" className={styles.logo}>
            <span className={styles.logoRune}>⚔</span>
            <span className={styles.logoText}>Realm</span>
          </Link>

          <nav className={styles.nav}>
            {NAV_LINKS.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`${styles.navLink} ${
                  location.pathname.startsWith(link.to) ? styles["navLink--active"] : ""
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>

          {/* TODO: swap initials for real user from auth context */}
          <Avatar initials="SR" size="sm" color="teal" />
        </div>
      </header>

      <main className={styles.main}>{children}</main>
    </div>
  );
}
