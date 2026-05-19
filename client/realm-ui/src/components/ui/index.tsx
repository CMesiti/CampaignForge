import React from "react";
import styles from "./ui.module.css";

// ─── Button ───────────────────────────────────────────────────────────────────

type ButtonVariant = "primary" | "ghost" | "danger";
type ButtonSize    = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  icon?: React.ReactNode;
}

export function Button({
  variant = "ghost",
  size = "md",
  loading = false,
  icon,
  children,
  className = "",
  disabled,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={`${styles.btn} ${styles[`btn--${variant}`]} ${styles[`btn--${size}`]} ${loading ? styles["btn--loading"] : ""} ${className}`}
      disabled={disabled || loading}
      {...rest}
    >
      {loading && <span className={styles.spinner} aria-hidden="true" />}
      {!loading && icon && <span className={styles.btnIcon}>{icon}</span>}
      {children && <span>{children}</span>}
    </button>
  );
}

// ─── Input ────────────────────────────────────────────────────────────────────

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({ label, error, hint, id, className = "", ...rest }: InputProps) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, "-");
  return (
    <div className={styles.inputWrapper}>
      {label && (
        <label className={styles.inputLabel} htmlFor={inputId}>
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`${styles.input} ${error ? styles["input--error"] : ""} ${className}`}
        {...rest}
      />
      {error && <p className={styles.inputError}>{error}</p>}
      {hint && !error && <p className={styles.inputHint}>{hint}</p>}
    </div>
  );
}

// ─── Select ───────────────────────────────────────────────────────────────────

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: { value: string; label: string }[];
  error?: string;
}

export function Select({ label, options, error, id, className = "", ...rest }: SelectProps) {
  const selectId = id ?? label?.toLowerCase().replace(/\s+/g, "-");
  return (
    <div className={styles.inputWrapper}>
      {label && (
        <label className={styles.inputLabel} htmlFor={selectId}>
          {label}
        </label>
      )}
      <select
        id={selectId}
        className={`${styles.select} ${error ? styles["input--error"] : ""} ${className}`}
        {...rest}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className={styles.inputError}>{error}</p>}
    </div>
  );
}

// ─── Textarea ────────────────────────────────────────────────────────────────

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export function Textarea({ label, error, id, className = "", ...rest }: TextareaProps) {
  const taId = id ?? label?.toLowerCase().replace(/\s+/g, "-");
  return (
    <div className={styles.inputWrapper}>
      {label && (
        <label className={styles.inputLabel} htmlFor={taId}>
          {label}
        </label>
      )}
      <textarea
        id={taId}
        className={`${styles.textarea} ${error ? styles["input--error"] : ""} ${className}`}
        {...rest}
      />
      {error && <p className={styles.inputError}>{error}</p>}
    </div>
  );
}

// ─── Badge ────────────────────────────────────────────────────────────────────

type BadgeVariant = "gold" | "success" | "warning" | "danger" | "neutral";

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
}

export function Badge({ variant = "neutral", children }: BadgeProps) {
  return (
    <span className={`${styles.badge} ${styles[`badge--${variant}`]}`}>
      {children}
    </span>
  );
}

// ─── Card ─────────────────────────────────────────────────────────────────────

interface CardProps {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
}

export function Card({ children, className = "", onClick, hoverable = false }: CardProps) {
  return (
    <div
      className={`${styles.card} ${hoverable ? styles["card--hoverable"] : ""} ${className}`}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
    >
      {children}
    </div>
  );
}

// ─── Divider ──────────────────────────────────────────────────────────────────

interface DividerProps {
  label?: string;
}

export function Divider({ label }: DividerProps) {
  return (
    <div className={styles.divider}>
      {label && <span className={styles.dividerLabel}>{label}</span>}
    </div>
  );
}

// ─── Avatar ───────────────────────────────────────────────────────────────────

interface AvatarProps {
  initials: string;
  size?: "sm" | "md" | "lg";
  color?: "purple" | "teal" | "coral" | "amber" | "blue";
}

export function Avatar({ initials, size = "md", color = "teal" }: AvatarProps) {
  return (
    <div className={`${styles.avatar} ${styles[`avatar--${size}`]} ${styles[`avatar--${color}`]}`}>
      {initials.slice(0, 2).toUpperCase()}
    </div>
  );
}

// ─── Stat Box (ability score) ────────────────────────────────────────────────

interface StatBoxProps {
  label: string;
  value: number;
}

export function StatBox({ label, value }: StatBoxProps) {
  const modifier = Math.floor((value - 10) / 2);
  const modStr = modifier >= 0 ? `+${modifier}` : `${modifier}`;
  return (
    <div className={styles.statBox}>
      <span className={styles.statBoxLabel}>{label}</span>
      <span className={styles.statBoxValue}>{value}</span>
      <span className={styles.statBoxMod}>{modStr}</span>
    </div>
  );
}

// ─── Step Progress ────────────────────────────────────────────────────────────

interface StepProgressProps {
  steps: string[];
  current: number;
}

export function StepProgress({ steps, current }: StepProgressProps) {
  return (
    <div className={styles.stepProgress}>
      {steps.map((step, i) => (
        <React.Fragment key={step}>
          <div className={styles.stepItem}>
            <div
              className={`${styles.stepCircle} ${
                i < current
                  ? styles["stepCircle--done"]
                  : i === current
                  ? styles["stepCircle--active"]
                  : ""
              }`}
            >
              {i < current ? "✓" : i + 1}
            </div>
            <span
              className={`${styles.stepLabel} ${
                i === current ? styles["stepLabel--active"] : ""
              }`}
            >
              {step}
            </span>
          </div>
          {i < steps.length - 1 && (
            <div
              className={`${styles.stepLine} ${i < current ? styles["stepLine--done"] : ""}`}
            />
          )}
        </React.Fragment>
      ))}
    </div>
  );
}
