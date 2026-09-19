"use client";

import Link from "next/link";
import { FormEvent, useEffect, useRef, useState } from "react";

export default function VerifyOtpPage() {
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [seconds, setSeconds] = useState(60);

  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    const storedEmail = sessionStorage.getItem(
      "atlas_registration_email"
    );

    if (storedEmail) {
      setEmail(storedEmail);
    } else {
      setError(
        "Registration email was not found. Please register again."
      );
    }
  }, []);

  useEffect(() => {
    if (seconds <= 0) return;

    const timer = setInterval(() => {
      setSeconds((previous) => previous - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [seconds]);

  const handleOtpChange = (index: number, value: string) => {
    if (!/^\d?$/.test(value)) {
      return;
    }

    const updatedOtp = [...otp];
    updatedOtp[index] = value;

    setOtp(updatedOtp);
    setError("");
    setMessage("");

    if (value && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (
    index: number,
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (
      event.key === "Backspace" &&
      !otp[index] &&
      index > 0
    ) {
      inputRefs.current[index - 1]?.focus();
    }

    if (event.key === "ArrowLeft" && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }

    if (event.key === "ArrowRight" && index < 5) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handlePaste = (
    event: React.ClipboardEvent<HTMLInputElement>
  ) => {
    event.preventDefault();

    const pasted = event.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, 6);

    if (!pasted) return;

    const updatedOtp = ["", "", "", "", "", ""];

    pasted.split("").forEach((digit, index) => {
      updatedOtp[index] = digit;
    });

    setOtp(updatedOtp);
    setError("");
    setMessage("");

    const nextIndex = Math.min(pasted.length, 5);
    inputRefs.current[nextIndex]?.focus();
  };

  const handleVerify = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setError("");
    setMessage("");

    const otpValue = otp.join("");

    if (otpValue.length !== 6) {
      setError(
        "Please enter the complete 6-digit verification code."
      );
      return;
    }

    if (!email) {
      setError(
        "Registration email was not found. Please register again."
      );
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/auth/verify-otp",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            otp: otpValue,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail ||
            "Invalid or expired verification code."
        );
        return;
      }

      setMessage(
        data.message || "Email verified successfully."
      );

      // Remove temporary registration email.
      sessionStorage.removeItem(
        "atlas_registration_email"
      );

      // Give the user a moment to see the success message.
      setTimeout(() => {
        window.location.href = "/login";
      }, 1000);
    } catch (error) {
      console.error(
        "OTP verification request failed:",
        error
      );

      setError(
        "Unable to connect to Atlas. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResend = async () => {
    if (seconds > 0 || !email) {
      return;
    }

    setError("");
    setMessage("");
    setResending(true);

    try {
      const response = await fetch(
        "http://localhost:8000/api/auth/resend-otp",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(
          data.detail ||
            "Unable to resend the verification code."
        );
        return;
      }

      setMessage(
        data.message ||
          "A new verification code has been sent to your email."
      );

      setSeconds(60);
      setOtp(["", "", "", "", "", ""]);

      inputRefs.current[0]?.focus();
    } catch (error) {
      console.error(
        "Resend OTP request failed:",
        error
      );

      setError(
        "Unable to connect to Atlas. Please make sure the backend is running."
      );
    } finally {
      setResending(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#07111f] text-white">
      {/* Header */}
      <header className="border-b border-white/10">
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-lg font-bold shadow-lg shadow-blue-600/20">
              A
            </div>

            <div>
              <div className="text-lg font-semibold tracking-wide">
                ATLAS
              </div>

              <div className="text-[10px] uppercase tracking-[0.25em] text-slate-500">
                Intelligence Platform
              </div>
            </div>
          </Link>

          <Link
            href="/login"
            className="text-sm font-medium text-slate-400 transition hover:text-white"
          >
            Sign in
          </Link>
        </div>
      </header>

      {/* OTP Section */}
      <section className="relative flex min-h-[calc(100vh-80px)] items-center justify-center overflow-hidden px-6 py-12">
        <div className="absolute left-1/2 top-20 -z-0 h-80 w-80 -translate-x-1/2 rounded-full bg-blue-600/10 blur-3xl" />

        <div className="relative z-10 w-full max-w-md">
          <div className="rounded-3xl border border-white/10 bg-white p-8 shadow-2xl shadow-black/30 sm:p-10">
            {/* Icon */}
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50 text-xl text-blue-600">
              @
            </div>

            {/* Heading */}
            <div className="mt-6 text-center">
              <h1 className="text-3xl font-bold text-slate-900">
                Verify your email
              </h1>

              <p className="mt-3 text-sm leading-6 text-slate-500">
                We sent a 6-digit verification code to
              </p>

              <p className="mt-1 truncate px-4 text-sm font-semibold text-slate-800">
                {email || "your email address"}
              </p>
            </div>

            <form onSubmit={handleVerify} className="mt-8">
              {/* OTP inputs */}
              <div className="flex justify-center gap-2 sm:gap-3">
                {otp.map((digit, index) => (
                  <input
                    key={index}
                    ref={(element) => {
                      inputRefs.current[index] = element;
                    }}
                    type="text"
                    inputMode="numeric"
                    maxLength={1}
                    value={digit}
                    onChange={(event) =>
                      handleOtpChange(
                        index,
                        event.target.value
                      )
                    }
                    onKeyDown={(event) =>
                      handleKeyDown(index, event)
                    }
                    onPaste={handlePaste}
                    aria-label={`Verification digit ${
                      index + 1
                    }`}
                    className="h-12 w-10 rounded-xl border border-slate-300 bg-white text-center text-lg font-semibold text-slate-900 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 sm:h-14 sm:w-12"
                  />
                ))}
              </div>

              {/* Error */}
              {error && (
                <div className="mt-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center text-sm text-red-600">
                  {error}
                </div>
              )}

              {/* Success */}
              {message && (
                <div className="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-center text-sm text-emerald-700">
                  {message}
                </div>
              )}

              {/* Verify */}
              <button
                type="submit"
                disabled={loading}
                className="mt-6 w-full rounded-xl bg-blue-600 px-5 py-3.5 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading
                  ? "Verifying..."
                  : "Verify email"}
              </button>
            </form>

            {/* Resend */}
            <div className="mt-6 text-center">
              <p className="text-sm text-slate-500">
                Didn't receive the code?
              </p>

              <button
                type="button"
                onClick={handleResend}
                disabled={seconds > 0 || resending}
                className="mt-2 text-sm font-semibold text-blue-600 transition hover:text-blue-700 disabled:cursor-not-allowed disabled:text-slate-400"
              >
                {resending
                  ? "Sending..."
                  : seconds > 0
                    ? `Resend code in ${seconds}s`
                    : "Resend verification code"}
              </button>
            </div>

            {/* Change email */}
            <div className="mt-7 border-t border-slate-200 pt-6 text-center">
              <Link
                href="/register"
                className="text-sm font-medium text-slate-500 transition hover:text-slate-800"
              >
                ← Use a different email
              </Link>
            </div>

            {/* Security */}
            <div className="mt-6 flex items-center justify-center gap-2 text-xs text-slate-400">
              <span className="text-emerald-500">✓</span>
              Your verification code expires shortly
            </div>
          </div>

          <p className="mt-6 text-center text-xs text-slate-500">
            Project Atlas · Secure Authentication
          </p>
        </div>
      </section>
    </main>
  );
}

