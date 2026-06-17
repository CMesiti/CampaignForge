import { useState } from "react";
import { Button, Input, Divider } from "../components/ui";
import styles from "./AuthPage.module.css";

type AuthTab = "login" | "register";

export function AuthPage() {
  const [tab, setTab] = useState<AuthTab>("login");

  // TODO: wire up to api/client.ts → login() / registerUser()
  const [form, setForm] = useState({ email: "", password: "", username: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    setError(null);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      // TODO: call login() or registerUser() from api/client.ts
      // const result = tab === "login"
      //   ? await login({ email: form.email, password: form.password })
      //   : await registerUser(form);
      // localStorage.setItem("access_token", result.access_token);
      // navigate("/campaigns");
      await new Promise((r) => setTimeout(r, 800)); // placeholder
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.glow} aria-hidden="true" />

      <div className={styles.panel}>
        {/* Logo */}
        <div className={styles.brand}>
          <span className={styles.brandRune}>⚔</span>
          <h1 className={styles.brandName}>NarrativeOS</h1>
          <p className={styles.brandTagline}>Your campaign companion</p>
        </div>

        {/* Tab switcher */}
        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${tab === "login" ? styles["tab--active"] : ""}`}
            onClick={() => { setTab("login"); setError(null); }}
            type="button"
          >
            Sign in
          </button>
          <button
            className={`${styles.tab} ${tab === "register" ? styles["tab--active"] : ""}`}
            onClick={() => { setTab("register"); setError(null); }}
            type="button"
          >
            Create account
          </button>
        </div>

        <form className={styles.form} onSubmit={handleSubmit} noValidate>
          {tab === "register" && (
            <Input
              label="Username"
              name="username"
              type="text"
              placeholder="Your adventurer name"
              value={form.username}
              onChange={handleChange}
              autoComplete="username"
              required
            />
          )}

          <Input
            label="Email"
            name="email"
            type="email"
            placeholder="ranger@realm.gg"
            value={form.email}
            onChange={handleChange}
            autoComplete="email"
            required
          />

          <Input
            label="Password"
            name="password"
            type="password"
            placeholder="••••••••"
            value={form.password}
            onChange={handleChange}
            autoComplete={tab === "login" ? "current-password" : "new-password"}
            required
          />

          {error && <p className={styles.errorMsg}>{error}</p>}

          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={loading}
            className={styles.submitBtn}
          >
            {tab === "login" ? "Enter the realm" : "Begin your journey"}
          </Button>
        </form>

        {tab === "login" && (
          <>
            <Divider label="or" />
            <p className={styles.switchPrompt}>
              New here?{" "}
              <button
                type="button"
                className={styles.switchLink}
                onClick={() => setTab("register")}
              >
                Create an account
              </button>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
