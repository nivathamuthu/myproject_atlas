"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();
    setError("");

    if (!email.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (!password) {
      setError("Please enter your password.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email.trim(),
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail ||
            "Unable to sign in. Please check your credentials."
        );
        return;
      }

      /*
       * Store the JWT temporarily.
       *
       * For the current development stage we use
       * sessionStorage. Later we can move this to
       * a secure HttpOnly cookie for production.
       */
      sessionStorage.setItem(
        "atlas_access_token",
        data.access_token
      );

      sessionStorage.setItem(
        "atlas_user_email",
        email.trim()
      );

      window.location.href = "/dashboard";
    } catch (error) {
      console.error(
        "Login request failed:",
        error
      );

      setError(
        "Unable to connect to Atlas. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="relative min-h-screen overflow-hidden bg-[#040914] text-white">
      {/* Background */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -left-40 -top-40 h-[520px] w-[520px] rounded-full bg-blue-600/[0.12] blur-[130px]" />

        <div className="absolute -bottom-48 -right-40 h-[560px] w-[560px] rounded-full bg-indigo-500/[0.10] blur-[140px]" />

        <div className="absolute left-[45%] top-[25%] h-72 w-72 rounded-full bg-cyan-500/[0.035] blur-[100px]" />

        <div
          className="absolute inset-0 opacity-[0.025]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.6) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.6) 1px, transparent 1px)",
            backgroundSize: "52px 52px",
          }}
        />
      </div>

      {/* Header */}
      <header className="relative z-20 border-b border-white/[0.07] bg-[#040914]/70 backdrop-blur-xl">
        <div className="mx-auto flex h-[76px] max-w-7xl items-center justify-between px-6 lg:px-10">
          <Link
            href="/"
            className="group flex items-center gap-3"
          >
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-blue-400/20 bg-blue-500/10 text-lg font-bold text-blue-300 shadow-lg shadow-blue-900/20 transition group-hover:border-blue-400/40 group-hover:bg-blue-500/15">
              <span className="absolute inset-0 rounded-xl bg-blue-400/10 blur-md" />
              <span className="relative">A</span>
            </div>

            <div>
              <div className="text-[17px] font-bold tracking-[0.2em]">
                ATLAS
              </div>

              <div className="text-[9px] uppercase tracking-[0.3em] text-slate-500">
                Intelligence Platform
              </div>
            </div>
          </Link>

          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-500 sm:block">
              New to Atlas?
            </span>

            <Link
              href="/register"
              className="rounded-lg border border-white/10 bg-white/[0.03] px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-blue-400/30 hover:bg-blue-500/10 hover:text-white"
            >
              Create account
            </Link>
          </div>
        </div>
      </header>

      {/* Main */}
      <section className="relative z-10 flex min-h-[calc(100vh-76px)] items-center px-6 py-10 lg:px-10 lg:py-14">
        <div className="mx-auto grid w-full max-w-6xl items-center gap-12 lg:grid-cols-[1fr_410px] xl:gap-20">

          {/* LEFT SIDE */}
          <div className="hidden lg:block">
            <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-blue-400/15 bg-blue-500/[0.06] px-3.5 py-2 text-xs font-medium text-blue-300 backdrop-blur-sm">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-blue-400 opacity-60" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-400" />
              </span>

              Secure intelligence workspace
            </div>

            <h1 className="max-w-2xl text-[52px] font-semibold leading-[1.05] tracking-[-0.035em] text-white xl:text-[60px]">
              Welcome back
              <span className="block bg-gradient-to-r from-blue-300 via-blue-400 to-cyan-300 bg-clip-text text-transparent">
                to intelligence.
              </span>
            </h1>

            <p className="mt-7 max-w-xl text-[15px] leading-7 text-slate-400">
              Sign in to continue exploring your information,
              research, and knowledge workflows through Atlas.
            </p>

            {/* Intelligence Network */}
            <div className="relative mt-10 h-[190px] max-w-xl overflow-hidden rounded-2xl border border-white/[0.07] bg-white/[0.025] backdrop-blur-sm">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/[0.05] via-transparent to-cyan-500/[0.03]" />

              {/* Lines */}
              <div className="absolute left-[20%] top-[48%] h-px w-[27%] rotate-[-18deg] bg-gradient-to-r from-blue-500/50 to-transparent" />

              <div className="absolute left-[43%] top-[44%] h-px w-[24%] rotate-[20deg] bg-gradient-to-r from-blue-400/50 to-transparent" />

              <div className="absolute left-[44%] top-[46%] h-px w-[20%] rotate-[-42deg] bg-gradient-to-r from-cyan-400/40 to-transparent" />

              <div className="absolute left-[65%] top-[52%] h-px w-[17%] rotate-[32deg] bg-gradient-to-r from-blue-400/40 to-transparent" />

              {/* Center */}
              <div className="absolute left-[44%] top-[35%] flex h-16 w-16 items-center justify-center rounded-2xl border border-blue-400/30 bg-blue-500/10 shadow-[0_0_40px_rgba(59,130,246,0.18)]">
                <div className="absolute inset-2 rounded-xl border border-blue-300/10" />

                <span className="text-xl font-bold text-blue-300">
                  A
                </span>
              </div>

              {/* Nodes */}
              <IntelligenceNode
                className="left-[13%] top-[30%]"
                label="DATA"
              />

              <IntelligenceNode
                className="left-[72%] top-[23%]"
                label="KNOWLEDGE"
              />

              <IntelligenceNode
                className="left-[72%] top-[65%]"
                label="INSIGHT"
              />

              <IntelligenceNode
                className="left-[20%] top-[68%]"
                label="RESEARCH"
              />

              <div className="absolute bottom-4 left-5 text-[9px] uppercase tracking-[0.25em] text-slate-600">
                Atlas intelligence network
              </div>
            </div>

            {/* Features */}
            <div className="mt-8 grid max-w-xl grid-cols-3 gap-5">
              <Feature
                title="Secure"
                text="Protected access"
              />

              <Feature
                title="Connected"
                text="Unified knowledge"
              />

              <Feature
                title="Intelligent"
                text="Actionable insights"
              />
            </div>
          </div>

          {/* RIGHT LOGIN BOX */}
          <div className="w-full">
            <div className="relative overflow-hidden rounded-[26px] border border-white/[0.13] bg-white/[0.055] p-6 shadow-2xl shadow-black/40 backdrop-blur-2xl sm:p-7">
              {/* Card glow */}
              <div className="pointer-events-none absolute -right-20 -top-20 h-48 w-48 rounded-full bg-blue-500/[0.10] blur-3xl" />

              <div className="pointer-events-none absolute bottom-0 left-0 h-32 w-32 rounded-full bg-cyan-500/[0.035] blur-3xl" />

              <div className="relative">
                {/* Card Header */}
                <div className="mb-7">
                  <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl border border-blue-400/20 bg-blue-500/10 text-lg font-semibold text-blue-300">
                    A
                  </div>

                  <h2 className="text-[24px] font-semibold tracking-tight text-white">
                    Welcome back
                  </h2>

                  <p className="mt-1.5 text-sm leading-6 text-slate-400">
                    Sign in to your Atlas intelligence workspace.
                  </p>
                </div>

                {/* Form */}
                <form
                  onSubmit={handleSubmit}
                  className="space-y-5"
                >
                  {/* Email */}
                  <div>
                    <label
                      htmlFor="email"
                      className="mb-2 block text-xs font-semibold uppercase tracking-wide text-slate-400"
                    >
                      Email address
                    </label>

                    <input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(event) =>
                        setEmail(event.target.value)
                      }
                      placeholder="you@company.com"
                      autoComplete="email"
                      required
                      className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400/50 focus:bg-black/25 focus:ring-4 focus:ring-blue-500/[0.08]"
                    />
                  </div>

                  {/* Password */}
                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <label
                        htmlFor="password"
                        className="text-xs font-semibold uppercase tracking-wide text-slate-400"
                      >
                        Password
                      </label>

                      <button
                        type="button"
                        className="text-[11px] font-medium text-blue-400 transition hover:text-blue-300"
                      >
                        Forgot password?
                      </button>
                    </div>

                    <div className="relative">
                      <input
                        id="password"
                        type={
                          showPassword
                            ? "text"
                            : "password"
                        }
                        value={password}
                        onChange={(event) =>
                          setPassword(event.target.value)
                        }
                        placeholder="Enter your password"
                        autoComplete="current-password"
                        required
                        className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 pr-12 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-blue-400/50 focus:bg-black/25 focus:ring-4 focus:ring-blue-500/[0.08]"
                      />

                      <EyeButton
                        visible={showPassword}
                        onClick={() =>
                          setShowPassword(
                            (current) => !current
                          )
                        }
                        label="Toggle password visibility"
                      />
                    </div>
                  </div>

                  {/* Error */}
                  {error && (
                    <div className="rounded-xl border border-red-400/20 bg-red-500/[0.08] px-4 py-3 text-xs leading-5 text-red-300">
                      {error}
                    </div>
                  )}

                  {/* Secure login info */}
                  <div className="flex items-start gap-2 pt-1">
                    <span className="mt-0.5 text-emerald-400">
                      ✓
                    </span>

                    <p className="text-[11px] leading-5 text-slate-500">
                      Your connection is protected by Atlas
                      secure authentication.
                    </p>
                  </div>

                  {/* Submit */}
                  <button
                    type="submit"
                    disabled={loading}
                    className="group relative w-full overflow-hidden rounded-xl bg-blue-600 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    <span className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/[0.12] to-transparent transition-transform duration-700 group-hover:translate-x-full" />

                    <span className="relative">
                      {loading
                        ? "Signing in..."
                        : "Sign in to Atlas"}
                    </span>
                  </button>
                </form>

                {/* Register */}
                <div className="mt-6 border-t border-white/[0.08] pt-5 text-center">
                  <span className="text-xs text-slate-500">
                    Don't have an account?{" "}
                  </span>

                  <Link
                    href="/register"
                    className="text-xs font-semibold text-blue-400 transition hover:text-blue-300"
                  >
                    Create an account
                  </Link>
                </div>
              </div>
            </div>

            <p className="mt-4 text-center text-[10px] uppercase tracking-[0.2em] text-slate-700">
              Project Atlas · Secure Authentication
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}


/* -------------------------------------------------
   Eye Button
------------------------------------------------- */

function EyeButton({
  visible,
  onClick,
  label,
}: {
  visible: boolean;
  onClick: () => void;
  label: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      className="absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-slate-500 transition hover:bg-white/[0.05] hover:text-slate-300"
    >
      {visible ? (
        <svg
          width="17"
          height="17"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z" />
          <circle cx="12" cy="12" r="2.5" />
        </svg>
      ) : (
        <svg
          width="17"
          height="17"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M3 3l18 18" />

          <path d="M10.6 6.2A9.7 9.7 0 0 1 12 6c6 0 9.5 6 9.5 6a16.5 16.5 0 0 1-3.1 3.7" />

          <path d="M6.7 6.8C4.1 8.3 2.5 12 2.5 12s3.5 6 9.5 6c1.4 0 2.7-.3 3.8-.8" />
        </svg>
      )}
    </button>
  );
}


/* -------------------------------------------------
   Intelligence Node
------------------------------------------------- */

function IntelligenceNode({
  className,
  label,
}: {
  className: string;
  label: string;
}) {
  return (
    <div className={`absolute ${className}`}>
      <div className="flex items-center gap-2">
        <span className="relative flex h-3 w-3">
          <span className="absolute inset-0 rounded-full bg-blue-400/30 blur-sm" />

          <span className="relative h-3 w-3 rounded-full border border-blue-400/40 bg-blue-400/30" />
        </span>

        <span className="text-[8px] font-medium tracking-[0.16em] text-slate-600">
          {label}
        </span>
      </div>
    </div>
  );
}


/* -------------------------------------------------
   Feature
------------------------------------------------- */

function Feature({
  title,
  text,
}: {
  title: string;
  text: string;
}) {
  return (
    <div>
      <div className="flex items-center gap-2">
        <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />

        <span className="text-xs font-semibold text-slate-300">
          {title}
        </span>
      </div>

      <p className="mt-1 pl-3.5 text-[10px] text-slate-600">
        {text}
      </p>
    </div>
  );
}