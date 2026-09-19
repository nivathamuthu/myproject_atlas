"use client";

import { Fraunces, Inter } from "next/font/google";
import React from "react";

const display = Fraunces({
  subsets: ["latin"],
  weight: ["500", "600"],
});

const body = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export default function AtlasOverviewPage() {
  const goToLogin = () => {
    window.location.href = "/login";
  };

  const goToRegister = () => {
    window.location.href = "/register";
  };

  return (
    <main className={`${body.className} min-h-screen overflow-hidden bg-[#040914] text-white`}>
      {/* Background */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-[5%] top-[-180px] h-[500px] w-[500px] rounded-full bg-amber-500/10 blur-[140px]" />

        <div className="absolute right-[-120px] top-[15%] h-[550px] w-[550px] rounded-full bg-teal-500/10 blur-[150px]" />

        <div className="absolute bottom-[-200px] left-[30%] h-[500px] w-[500px] rounded-full bg-rose-500/10 blur-[150px]" />
      </div>

      {/* Navbar */}
      <header className="relative z-20 border-b border-white/10 bg-[#040914]/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5 lg:px-10">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-400 text-sm font-black text-[#040914]">
              A
            </div>

            <div>
              <p className={`${display.className} text-lg font-semibold tracking-wide`}>
                ATLAS
              </p>

              <p className="text-[9px] uppercase tracking-[0.28em] text-white/35">
                Intelligence Platform
              </p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden items-center gap-8 md:flex">
            <a
              href="#overview"
              className="text-sm text-white/45 transition hover:text-white"
            >
              Overview
            </a>

            <a
              href="#security"
              className="text-sm text-white/45 transition hover:text-white"
            >
              Security
            </a>

            <a
              href="#pipeline"
              className="text-sm text-white/45 transition hover:text-white"
            >
              Pipeline
            </a>
          </nav>

          {/* Auth buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={goToLogin}
              className="rounded-lg px-4 py-2 text-sm text-white/65 transition hover:bg-white/[0.06] hover:text-white"
            >
              Sign In
            </button>

            <button
              onClick={goToRegister}
              className="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-[#040914] transition hover:bg-white/90"
            >
              Create Account
            </button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section
        id="overview"
        className="relative z-10 mx-auto max-w-7xl px-6 pb-20 pt-20 lg:px-10 lg:pb-28 lg:pt-28"
      >
        <div className="grid items-center gap-16 lg:grid-cols-[1.05fr_0.95fr]">
          {/* Left */}
          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 backdrop-blur-xl">
              <span className="h-2 w-2 rounded-full bg-amber-300" />

              <span className="text-[10px] uppercase tracking-[0.25em] text-white/45">
                AI-Native Knowledge Engineering
              </span>
            </div>

            <h1 className={`${display.className} max-w-3xl text-5xl font-semibold leading-[1.05] tracking-tight sm:text-6xl lg:text-7xl`}>
              Turn documents into
              <br />

              <span className="text-white/40">
                enterprise-ready knowledge.
              </span>
            </h1>

            <p className="mt-7 max-w-2xl text-base leading-8 text-white/45 sm:text-lg">
              Atlas continuously acquires documents from APIs, crawlers,
              bulk imports and manual uploads, then validates, parses and
              enriches them into a knowledge graph and vector index —
              ready to power search, retrieval and generative AI
              applications at scale.
            </p>

            {/* Buttons */}
            <div className="mt-9 flex flex-wrap gap-3">
              <button
                onClick={goToRegister}
                className="rounded-xl bg-white px-6 py-3.5 text-sm font-semibold text-[#040914] transition hover:bg-white/90"
              >
                Create your account
              </button>

              <button
                onClick={goToLogin}
                className="rounded-xl border border-white/10 bg-white/[0.04] px-6 py-3.5 text-sm text-white/70 backdrop-blur-xl transition hover:bg-white/[0.08] hover:text-white"
              >
                Sign in
              </button>
            </div>

            {/* Trust */}
            <div className="mt-10 flex flex-wrap items-center gap-x-7 gap-y-3 text-xs text-white/25">
              <span>12+ file formats supported</span>

              <span className="h-1 w-1 rounded-full bg-white/20" />

              <span>Scales beyond 1M documents</span>

              <span className="h-1 w-1 rounded-full bg-white/20" />

              <span>Domain-independent architecture</span>
            </div>
          </div>

          {/* Right intelligence visualization */}
          <div className="relative">
            <div className="relative mx-auto aspect-square max-w-[480px]">
              {/* Outer rings */}
              <div className="absolute inset-[8%] rounded-full border border-white/[0.07]" />

              <div className="absolute inset-[18%] rounded-full border border-white/[0.08]" />

              <div className="absolute inset-[30%] rounded-full border border-white/[0.09]" />

              {/* Center */}
              <div className="absolute left-1/2 top-1/2 flex h-28 w-28 -translate-x-1/2 -translate-y-1/2 items-center justify-center rounded-3xl border border-white/15 bg-white/[0.07] shadow-2xl backdrop-blur-2xl">
                <div className="text-center">
                  <div className="mx-auto flex h-10 w-10 items-center justify-center rounded-xl bg-amber-400 text-sm font-black text-[#040914]">
                    A
                  </div>

                  <p className="mt-2 text-[9px] uppercase tracking-[0.2em] text-white/45">
                    Atlas
                  </p>
                </div>
              </div>

              {/* DATA */}
              <div className="absolute left-[3%] top-[22%] rounded-2xl border border-white/10 bg-white/[0.05] px-5 py-4 backdrop-blur-xl">
                <p className="text-[9px] uppercase tracking-[0.2em] text-amber-300/60">
                  Acquire
                </p>

                <p className="mt-1 text-sm font-medium">
                  Documents
                </p>
              </div>

              {/* KNOWLEDGE */}
              <div className="absolute right-[0%] top-[20%] rounded-2xl border border-white/10 bg-white/[0.05] px-5 py-4 backdrop-blur-xl">
                <p className="text-[9px] uppercase tracking-[0.2em] text-teal-300/60">
                  Enrich
                </p>

                <p className="mt-1 text-sm font-medium">
                  Entities &amp; Graph
                </p>
              </div>

              {/* RESEARCH */}
              <div className="absolute bottom-[17%] left-[4%] rounded-2xl border border-white/10 bg-white/[0.05] px-5 py-4 backdrop-blur-xl">
                <p className="text-[9px] uppercase tracking-[0.2em] text-rose-300/60">
                  Index
                </p>

                <p className="mt-1 text-sm font-medium">
                  Vector Store
                </p>
              </div>

              {/* INSIGHT */}
              <div className="absolute bottom-[14%] right-[3%] rounded-2xl border border-white/10 bg-white/[0.05] px-5 py-4 backdrop-blur-xl">
                <p className="text-[9px] uppercase tracking-[0.2em] text-emerald-300/60">
                  Retrieve
                </p>

                <p className="mt-1 text-sm font-medium">
                  Knowledge APIs
                </p>
              </div>

              {/* Connecting lines */}
              <div className="absolute left-[27%] top-[37%] h-px w-[25%] rotate-[20deg] bg-white/10" />

              <div className="absolute right-[27%] top-[37%] h-px w-[25%] -rotate-[20deg] bg-white/10" />

              <div className="absolute bottom-[36%] left-[27%] h-px w-[25%] -rotate-[20deg] bg-white/10" />

              <div className="absolute bottom-[34%] right-[27%] h-px w-[25%] rotate-[20deg] bg-white/10" />
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section
        id="security"
        className="relative z-10 border-y border-white/10 bg-white/[0.015]"
      >
        <div className="mx-auto grid max-w-7xl gap-px px-6 lg:grid-cols-3 lg:px-10">
          {/* Security */}
          <div className="px-0 py-12 lg:px-8 lg:py-16">
            <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <path d="M12 3L20 6V11C20 16.5 16.5 20 12 21C7.5 20 4 16.5 4 11V6L12 3Z" />

                <path d="M9 12L11 14L15 10" />
              </svg>
            </div>

            <h2 className={`${display.className} text-xl font-semibold`}>
              Secure by design
            </h2>

            <p className="mt-3 text-sm leading-6 text-white/40">
              Every document is validated, deduplicated and
              integrity-checked before it enters the trusted
              processing pipeline, with full audit history and
              role-based access.
            </p>
          </div>

          {/* Intelligence */}
          <div className="border-white/10 px-0 py-12 lg:border-x lg:px-8 lg:py-16">
            <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <circle cx="12" cy="12" r="3" />

                <path d="M12 2V5" />
                <path d="M12 19V22" />
                <path d="M2 12H5" />
                <path d="M19 12H22" />

                <path d="M4.9 4.9L7 7" />
                <path d="M17 17L19.1 19.1" />

                <path d="M19.1 4.9L17 7" />
                <path d="M7 17L4.9 19.1" />
              </svg>
            </div>

            <h2 className={`${display.className} text-xl font-semibold`}>
              Intelligent processing
            </h2>

            <p className="mt-3 text-sm leading-6 text-white/40">
              Parse PDF, DOCX, PPTX, XLSX, CSV, XML, JSON, HTML,
              Markdown, EML and scanned images, then extract
              metadata and entities with LLM-based enrichment.
            </p>
          </div>

          {/* Knowledge */}
          <div className="px-0 py-12 lg:px-8 lg:py-16">
            <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
              >
                <circle cx="12" cy="5" r="2" />

                <circle cx="5" cy="19" r="2" />

                <circle cx="19" cy="19" r="2" />

                <path d="M12 7V12" />

                <path d="M12 12L5 17" />

                <path d="M12 12L19 17" />
              </svg>
            </div>

            <h2 className={`${display.className} text-xl font-semibold`}>
              Connected knowledge
            </h2>

            <p className="mt-3 text-sm leading-6 text-white/40">
              Extracted entities feed a knowledge graph and vector
              index, giving downstream apps semantic search and
              retrieval-augmented generation out of the box.
            </p>
          </div>
        </div>
      </section>

      {/* Pipeline */}
      <section
        id="pipeline"
        className="relative z-10 mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-28"
      >
        <div className="max-w-2xl">
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/60">
            How Atlas works
          </p>

          <h2 className={`${display.className} mt-4 text-3xl font-semibold tracking-tight sm:text-4xl`}>
            A secure path from
            <span className="text-white/40">
              {" "}
              file to insight.
            </span>
          </h2>

          <p className="mt-4 text-sm leading-7 text-white/40">
            Every document moves through the same controlled
            pipeline — acquisition, validation, parsing, enrichment,
            indexing and evaluation — with retries and full
            observability at each stage.
          </p>
        </div>

        <div className="mt-12 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[
            {
              number: "01",
              title: "Acquire",
              text: "Pull documents from APIs, crawlers, bulk imports and manual uploads on a schedule.",
            },
            {
              number: "02",
              title: "Validate & parse",
              text: "Deduplicate, check integrity and parse every format into a normalized representation.",
            },
            {
              number: "03",
              title: "Enrich & connect",
              text: "Extract metadata and entities, then update the knowledge graph and vector index.",
            },
            {
              number: "04",
              title: "Serve & evaluate",
              text: "Expose search and retrieval APIs, backed by continuous quality evaluation.",
            },
          ].map((item) => (
            <div
              key={item.number}
              className="rounded-2xl border border-white/10 bg-white/[0.035] p-6 backdrop-blur-xl"
            >
              <span className="text-[10px] tracking-[0.25em] text-white/25">
                {item.number}
              </span>

              <h3 className={`${display.className} mt-5 text-lg font-semibold`}>
                {item.title}
              </h3>

              <p className="mt-3 text-sm leading-6 text-white/35">
                {item.text}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 border-t border-white/10">
        <div className="mx-auto max-w-7xl px-6 py-20 text-center lg:px-10 lg:py-24">
          <p className="text-xs uppercase tracking-[0.3em] text-white/30">
            Start with Atlas
          </p>

          <h2 className={`${display.className} mx-auto mt-5 max-w-2xl text-3xl font-semibold sm:text-4xl`}>
            Bring your documents.
            <br />

            <span className="text-white/40">
              Atlas will handle the intelligence.
            </span>
          </h2>

          <button
            onClick={goToRegister}
            className="mt-8 rounded-xl bg-white px-7 py-3.5 text-sm font-semibold text-[#040914] transition hover:bg-white/90"
          >
            Create Account
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-6 py-7 text-xs text-white/25 sm:flex-row sm:items-center sm:justify-between lg:px-10">
          <div>
            © {new Date().getFullYear()} Atlas Intelligence Platform
          </div>

          <div>
            AI-native knowledge engineering platform
          </div>
        </div>
      </footer>
    </main>
  );
}
