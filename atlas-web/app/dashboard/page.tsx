"use client";

import {
  ChangeEvent,
  DragEvent,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { useRouter } from "next/navigation";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://localhost:8000";

const MAX_FILE_SIZE = 100 * 1024 * 1024;
const MAX_BULK_FILES = 50;

type UploadStatus =
  | "SUCCESS"
  | "FAILED"
  | "DUPLICATE"
  | "PROCESSING"
  | "PENDING"
  | string;

type RecentUpload = {
  id: string;
  fileName: string;
  size: number;
  status: UploadStatus;
  storageReference?: string;
  uploadedAt: string;
};

type ApiFile = {
  upload_id: string;
  file_name: string;
  file_size: number;
  content_type: string;
  file_type?: string | null;
  page_count?: number | null;
  sheet_count?: number | null;
  slide_count?: number | null;
  title?: string | null;
  author?: string | null;
  parsed_status?: string | null;
  status: string;
  storage_reference?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
};

type FilesResponse = {
  count: number;
  total_size: number;
  files: ApiFile[];
};

type BulkFileResult = {
  file_name: string;
  status: string;
  upload_id?: string;
  storage_reference?: string;
  message?: string;
};

type BulkUploadResponse = {
  status: string;
  total: number;
  successful: number;
  duplicates: number;
  failed: number;
  results: BulkFileResult[];
};

function formatFileSize(bytes: number): string {
  if (!bytes || bytes <= 0) {
    return "0 MB";
  }

  const mb = bytes / (1024 * 1024);

  if (mb < 1024) {
    return `${mb.toFixed(2)} MB`;
  }

  const gb = mb / 1024;

  return `${gb.toFixed(2)} GB`;
}

function formatUploadDate(dateString: string): string {
  try {
    return new Date(dateString).toLocaleString(
      "en-IN",
      {
        dateStyle: "medium",
        timeStyle: "short",
      }
    );
  } catch {
    return dateString;
  }
}

function getStatusStyle(status: string): string {
  const normalized = status.toUpperCase();

  if (
    normalized === "SUCCESS" ||
    normalized === "COMPLETED"
  ) {
    return "border-emerald-400/20 bg-emerald-400/10 text-emerald-300";
  }

  if (
    normalized === "FAILED" ||
    normalized === "ERROR"
  ) {
    return "border-red-400/20 bg-red-400/10 text-red-300";
  }

  if (normalized === "DUPLICATE") {
    return "border-amber-400/20 bg-amber-400/10 text-amber-300";
  }

  return "border-blue-400/20 bg-blue-400/10 text-blue-300";
}

export default function Dashboard() {
  const router = useRouter();

  const fileInputRef =
    useRef<HTMLInputElement | null>(null);

  const [userEmail, setUserEmail] =
    useState("");

  const [selectedFiles, setSelectedFiles] =
    useState<File[]>([]);

  const [isDragging, setIsDragging] =
    useState(false);

  const [uploading, setUploading] =
    useState(false);

  const [uploadProgress, setUploadProgress] =
    useState(0);

  const [uploadMessage, setUploadMessage] =
    useState("");

  const [uploadError, setUploadError] =
    useState("");

  const [bulkResult, setBulkResult] =
    useState<BulkUploadResponse | null>(null);

  const [recentUploads, setRecentUploads] =
    useState<RecentUpload[]>([]);

  const [totalUploads, setTotalUploads] =
    useState(0);

  const [totalStorage, setTotalStorage] =
    useState(0);

  const [loadingUploads, setLoadingUploads] =
    useState(true);

  // ============================================================
  // LOAD RECENT UPLOADS + STORAGE STATISTICS
  // ============================================================

  const loadRecentUploads = useCallback(
    async () => {
      try {
        setLoadingUploads(true);

        const response = await fetch(
          `${API_BASE_URL}/api/files?limit=50`,
          {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Unable to load uploaded files. Status: ${response.status}`
          );
        }

        const data: FilesResponse =
          await response.json();

        const mappedUploads: RecentUpload[] =
          data.files.map((file) => ({
            id: file.upload_id,
            fileName: file.file_name,
            size: file.file_size,
            status: file.status,
            storageReference:
              file.storage_reference ||
              undefined,
            uploadedAt:
              file.created_at ||
              file.updated_at ||
              new Date().toISOString(),
          }));

        setRecentUploads(mappedUploads);

        setTotalUploads(data.count);

        setTotalStorage(data.total_size);

        sessionStorage.setItem(
          "atlas_recent_uploads",
          JSON.stringify(mappedUploads)
        );
      } catch (error) {
        console.error(
          "Failed to load uploaded files:",
          error
        );

        const storedUploads =
          sessionStorage.getItem(
            "atlas_recent_uploads"
          );

        if (storedUploads) {
          try {
            const parsedUploads =
              JSON.parse(
                storedUploads
              ) as RecentUpload[];

            setRecentUploads(parsedUploads);

            setTotalUploads(
              parsedUploads.length
            );

            const fallbackStorage =
              parsedUploads.reduce(
                (total, upload) =>
                  total + upload.size,
                0
              );

            setTotalStorage(
              fallbackStorage
            );
          } catch {
            sessionStorage.removeItem(
              "atlas_recent_uploads"
            );

            setRecentUploads([]);
            setTotalUploads(0);
            setTotalStorage(0);
          }
        }
      } finally {
        setLoadingUploads(false);
      }
    },
    []
  );

  // ============================================================
  // AUTH + INITIAL LOAD
  // ============================================================

  useEffect(() => {
    const token =
      sessionStorage.getItem(
        "atlas_access_token"
      );

    if (!token) {
      router.replace("/login");
      return;
    }

    const email =
      sessionStorage.getItem(
        "atlas_user_email"
      );

    if (email) {
      setUserEmail(email);
    }

    loadRecentUploads();
  }, [
    router,
    loadRecentUploads,
  ]);

  // ============================================================
  // FILE VALIDATION
  // ============================================================

  const validateFiles = (
    files: File[]
  ): File[] => {
    setUploadError("");
    setUploadMessage("");
    setBulkResult(null);
    setUploadProgress(0);

    if (files.length === 0) {
      return [];
    }

    if (files.length > MAX_BULK_FILES) {
      setUploadError(
        `You can select a maximum of ${MAX_BULK_FILES} files at once.`
      );

      return [];
    }

    const oversizedFiles = files.filter(
      (file) =>
        file.size > MAX_FILE_SIZE
    );

    if (oversizedFiles.length > 0) {
      setUploadError(
        `${oversizedFiles.length} file(s) exceed the maximum allowed size of 100 MB.`
      );

      return [];
    }

    const emptyFiles = files.filter(
      (file) => file.size === 0
    );

    if (emptyFiles.length > 0) {
      setUploadError(
        `${emptyFiles.length} file(s) are empty and cannot be uploaded.`
      );

      return [];
    }

    return files;
  };

  // ============================================================
  // FILE SELECTION
  // ============================================================

  const selectFiles = (files: File[]) => {
    const validFiles =
      validateFiles(files);

    if (validFiles.length === 0) {
      setSelectedFiles([]);
      return;
    }

    setSelectedFiles(validFiles);
  };

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    const files = Array.from(
      event.target.files || []
    );

    selectFiles(files);
  };

  // ============================================================
  // DRAG AND DROP
  // ============================================================

  const handleDragOver = (
    event: DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (
    event: DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (
    event: DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setIsDragging(false);

    const files = Array.from(
      event.dataTransfer.files || []
    );

    selectFiles(files);
  };

  // ============================================================
  // REMOVE SELECTED FILE
  // ============================================================

  const removeSelectedFile = (
    index: number
  ) => {
    setSelectedFiles((current) =>
      current.filter(
        (_, fileIndex) =>
          fileIndex !== index
      )
    );

    setUploadError("");
    setUploadMessage("");
    setBulkResult(null);
  };

  // ============================================================
  // CLEAR SELECTED FILES
  // ============================================================

  const clearSelectedFiles = () => {
    setSelectedFiles([]);
    setUploadError("");
    setUploadMessage("");
    setBulkResult(null);
    setUploadProgress(0);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // ============================================================
  // BULK UPLOAD
  // ============================================================

  const handleBulkUpload = async () => {
    if (selectedFiles.length === 0) {
      setUploadError(
        "Please select at least one file."
      );

      return;
    }

    const token =
      sessionStorage.getItem(
        "atlas_access_token"
      );

    if (!token) {
      router.replace("/login");
      return;
    }

    setUploading(true);
    setUploadProgress(10);
    setUploadMessage("");
    setUploadError("");
    setBulkResult(null);

    try {
      const formData = new FormData();

      selectedFiles.forEach((file) => {
        formData.append(
          "files",
          file
        );
      });

      setUploadProgress(25);

      const response = await fetch(
        `${API_BASE_URL}/api/files/bulk`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        }
      );

      setUploadProgress(75);

      const contentType =
        response.headers.get(
          "content-type"
        );

      let data: BulkUploadResponse | null =
        null;

      if (
        contentType?.includes(
          "application/json"
        )
      ) {
        data =
          await response.json();
      }

      if (!response.ok) {
        throw new Error(
          (
            data as any
          )?.detail ||
          "Bulk upload failed."
        );
      }

      if (!data) {
        throw new Error(
          "Invalid response received from the server."
        );
      }

      setUploadProgress(100);

      setBulkResult(data);

      if (data.failed > 0) {
        setUploadMessage(
          `Bulk upload completed with ${data.failed} failed file(s).`
        );
      } else if (
        data.duplicates > 0
      ) {
        setUploadMessage(
          `Bulk upload completed with ${data.duplicates} duplicate file(s).`
        );
      } else {
        setUploadMessage(
          `${data.successful} document(s) uploaded successfully.`
        );
      }

      setSelectedFiles([]);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      await loadRecentUploads();
    } catch (error) {
      console.error(
        "Bulk upload failed:",
        error
      );

      setUploadError(
        error instanceof Error
          ? error.message
          : "Bulk upload failed."
      );

      await loadRecentUploads();
    } finally {
      setUploading(false);
    }
  };

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    sessionStorage.removeItem(
      "atlas_access_token"
    );

    sessionStorage.removeItem(
      "atlas_user_email"
    );

    router.replace("/login");
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <main className="min-h-screen bg-[#040914] text-white relative overflow-hidden">

      {/* ======================================================
          BACKGROUND GLOWS
      ====================================================== */}

      <div className="pointer-events-none absolute inset-0">

        <div className="absolute -top-48 -left-48 h-[520px] w-[520px] rounded-full bg-blue-600/15 blur-[130px]" />

        <div className="absolute top-1/3 left-1/2 h-[400px] w-[400px] -translate-x-1/2 rounded-full bg-cyan-500/5 blur-[120px]" />

        <div className="absolute -bottom-48 -right-48 h-[520px] w-[520px] rounded-full bg-indigo-600/15 blur-[130px]" />

        <div
          className="absolute inset-0 opacity-[0.035]"
          style={{
            backgroundImage:
              "linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px)",
            backgroundSize:
              "42px 42px",
          }}
        />
      </div>

      {/* ======================================================
          HEADER
      ====================================================== */}

      <header className="relative z-10 border-b border-white/[0.07] bg-[#040914]/80 backdrop-blur-xl">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8">

          <div className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 shadow-lg shadow-blue-600/30">
              <span className="text-lg font-bold">
                A
              </span>
            </div>

            <div>
              <p className="text-sm font-semibold tracking-[0.18em]">
                ATLAS
              </p>

              <p className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
                Intelligence Platform
              </p>
            </div>

          </div>

          <div className="flex items-center gap-4">

            <div className="hidden text-right sm:block">

              <p className="text-sm text-slate-300">
                {userEmail || "User"}
              </p>

              <p className="text-xs text-slate-500">
                Secure workspace
              </p>

            </div>

            <button
              onClick={handleLogout}
              className="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:border-white/20 hover:bg-white/[0.08] hover:text-white"
            >
              Sign out
            </button>

          </div>

        </div>

      </header>

      {/* ======================================================
          CONTENT
      ====================================================== */}

      <div className="relative z-10 mx-auto max-w-7xl px-6 py-10 lg:px-8">

        {/* PAGE HEADER */}

        <div className="mb-8">

          <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1 text-xs text-blue-300">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-400" />
            Secure intelligence workspace
          </div>

          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">

            Welcome back to{" "}

            <span className="bg-gradient-to-r from-blue-300 via-blue-400 to-cyan-300 bg-clip-text text-transparent">
              intelligence.
            </span>

          </h1>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
            Upload, validate and process your
            documents through the Atlas
            intelligence pipeline.
          </p>

        </div>

        {/* ====================================================
            STAT CARDS
        ==================================================== */}

        <div className="grid gap-4 md:grid-cols-3">

          {/* TOTAL DOCUMENTS */}

          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.035] p-5 backdrop-blur-xl">

            <div className="flex items-start justify-between">

              <div>

                <p className="text-sm text-slate-400">
                  Total Documents
                </p>

                <p className="mt-2 text-3xl font-semibold text-white">
                  {totalUploads}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  Documents stored in Atlas
                </p>

              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-300">

                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                >
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <path d="M14 2v6h6" />
                  <path d="M8 13h8" />
                  <path d="M8 17h6" />
                </svg>

              </div>

            </div>

          </div>

          {/* TOTAL STORAGE */}

          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.035] p-5 backdrop-blur-xl">

            <div className="flex items-start justify-between">

              <div>

                <p className="text-sm text-slate-400">
                  Total Storage Used
                </p>

                <p className="mt-2 text-3xl font-semibold text-white">
                  {formatFileSize(
                    totalStorage
                  )}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  Across all uploaded documents
                </p>

              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-300">

                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                >
                  <ellipse
                    cx="12"
                    cy="5"
                    rx="8"
                    ry="3"
                  />
                  <path d="M4 5v7c0 1.66 3.58 3 8 3s8-1.34 8-3V5" />
                  <path d="M4 12v7c0 1.66 3.58 3 8 3s8-1.34 8-3v-7" />
                </svg>

              </div>

            </div>

          </div>

          {/* MAX FILE SIZE */}

          <div className="rounded-2xl border border-white/[0.08] bg-white/[0.035] p-5 backdrop-blur-xl">

            <div className="flex items-start justify-between">

              <div>

                <p className="text-sm text-slate-400">
                  Max File Size
                </p>

                <p className="mt-2 text-3xl font-semibold text-white">
                  100 MB
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  Maximum allowed per document
                </p>

              </div>

              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-300">

                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                >
                  <path d="M12 3v12" />
                  <path d="m7 10 5 5 5-5" />
                  <path d="M5 21h14" />
                </svg>

              </div>

            </div>

          </div>

        </div>

        {/* ====================================================
            BULK UPLOAD + PIPELINE
        ==================================================== */}

        <div className="mt-6 grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">

          {/* BULK UPLOAD CARD */}

          <section className="rounded-[26px] border border-white/[0.08] bg-white/[0.035] p-6 shadow-2xl backdrop-blur-xl">

            <div className="mb-5">

              <div className="flex items-center justify-between gap-4">

                <div>

                  <p className="text-lg font-semibold">
                    Bulk document upload
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Select up to 50 documents.
                    Each file can be up to 100 MB.
                  </p>

                </div>

                <div className="rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1 text-xs text-blue-300">
                  Max 50 files
                </div>

              </div>

            </div>

            {/* DROPZONE */}

            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`rounded-2xl border border-dashed p-10 text-center transition ${
                isDragging
                  ? "border-blue-400 bg-blue-400/10"
                  : "border-white/10 bg-[#040914]/50 hover:border-blue-400/30"
              }`}
            >

              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-300">

                <svg
                  width="26"
                  height="26"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.8"
                >
                  <path d="M12 16V4" />
                  <path d="m7 9 5-5 5 5" />
                  <path d="M5 20h14" />
                </svg>

              </div>

              <p className="mt-4 text-sm font-medium text-slate-200">
                Drag and drop multiple documents here
              </p>

              <p className="mt-2 text-xs text-slate-500">
                or choose multiple files from your computer
              </p>

              <button
                type="button"
                disabled={uploading}
                onClick={() =>
                  fileInputRef.current?.click()
                }
                className="mt-5 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-medium text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Choose files
              </button>

              <input
                ref={fileInputRef}
                type="file"
                multiple
                className="hidden"
                onChange={handleFileChange}
              />

            </div>

            {/* SELECTED FILES */}

            {selectedFiles.length > 0 && (

              <div className="mt-4 rounded-2xl border border-blue-400/15 bg-blue-400/[0.06] p-4">

                <div className="flex items-center justify-between gap-4">

                  <div>

                    <p className="text-sm font-medium text-slate-200">
                      {selectedFiles.length}{" "}
                      {selectedFiles.length === 1
                        ? "file"
                        : "files"}{" "}
                      selected
                    </p>

                    <p className="mt-1 text-xs text-slate-500">
                      Total size:{" "}
                      {formatFileSize(
                        selectedFiles.reduce(
                          (total, file) =>
                            total + file.size,
                          0
                        )
                      )}
                    </p>

                  </div>

                  <button
                    type="button"
                    disabled={uploading}
                    onClick={clearSelectedFiles}
                    className="text-xs text-slate-500 hover:text-white disabled:opacity-50"
                  >
                    Clear all
                  </button>

                </div>

                {/* FILE LIST */}

                <div className="mt-4 max-h-64 space-y-2 overflow-y-auto">

                  {selectedFiles.map(
                    (file, index) => (

                      <div
                        key={`${file.name}-${index}`}
                        className="flex items-center justify-between gap-3 rounded-xl border border-white/[0.06] bg-[#040914]/50 px-3 py-2.5"
                      >

                        <div className="flex min-w-0 items-center gap-3">

                          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-blue-300">

                            <svg
                              width="16"
                              height="16"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              strokeWidth="1.8"
                            >
                              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                              <path d="M14 2v6h6" />
                            </svg>

                          </div>

                          <div className="min-w-0">

                            <p className="truncate text-xs font-medium text-slate-200">
                              {file.name}
                            </p>

                            <p className="mt-0.5 text-[11px] text-slate-500">
                              {formatFileSize(
                                file.size
                              )}
                            </p>

                          </div>

                        </div>

                        <button
                          type="button"
                          disabled={uploading}
                          onClick={() =>
                            removeSelectedFile(
                              index
                            )
                          }
                          className="shrink-0 text-xs text-slate-500 hover:text-red-300 disabled:opacity-50"
                        >
                          Remove
                        </button>

                      </div>

                    )
                  )}

                </div>

                {/* UPLOAD BUTTON */}

                <button
                  type="button"
                  disabled={uploading}
                  onClick={handleBulkUpload}
                  className="mt-4 w-full rounded-xl bg-blue-600 py-3 text-sm font-medium text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {uploading
                    ? "Processing documents..."
                    : `Upload ${selectedFiles.length} ${
                        selectedFiles.length === 1
                          ? "document"
                          : "documents"
                      }`}
                </button>

                {/* PROGRESS */}

                {uploading && (

                  <div className="mt-4">

                    <div className="mb-2 flex justify-between text-xs text-slate-500">

                      <span>
                        Processing secure pipeline
                      </span>

                      <span>
                        {uploadProgress}%
                      </span>

                    </div>

                    <div className="h-1.5 overflow-hidden rounded-full bg-white/10">

                      <div
                        className="h-full rounded-full bg-blue-500 transition-all duration-300"
                        style={{
                          width: `${uploadProgress}%`,
                        }}
                      />

                    </div>

                  </div>

                )}

              </div>

            )}

            {/* BULK RESULT */}

            {bulkResult && (

              <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">

                <div className="rounded-xl border border-white/[0.07] bg-white/[0.025] p-3">

                  <p className="text-xs text-slate-500">
                    Total
                  </p>

                  <p className="mt-1 text-xl font-semibold text-white">
                    {bulkResult.total}
                  </p>

                </div>

                <div className="rounded-xl border border-emerald-400/15 bg-emerald-400/[0.05] p-3">

                  <p className="text-xs text-slate-500">
                    Uploaded
                  </p>

                  <p className="mt-1 text-xl font-semibold text-emerald-300">
                    {bulkResult.successful}
                  </p>

                </div>

                <div className="rounded-xl border border-amber-400/15 bg-amber-400/[0.05] p-3">

                  <p className="text-xs text-slate-500">
                    Duplicates
                  </p>

                  <p className="mt-1 text-xl font-semibold text-amber-300">
                    {bulkResult.duplicates}
                  </p>

                </div>

                <div className="rounded-xl border border-red-400/15 bg-red-400/[0.05] p-3">

                  <p className="text-xs text-slate-500">
                    Failed
                  </p>

                  <p className="mt-1 text-xl font-semibold text-red-300">
                    {bulkResult.failed}
                  </p>

                </div>

              </div>

            )}

            {/* SUCCESS */}

            {uploadMessage && (

              <div className="mt-4 rounded-xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-300">
                {uploadMessage}
              </div>

            )}

            {/* ERROR */}

            {uploadError && (

              <div className="mt-4 rounded-xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-300">
                {uploadError}
              </div>

            )}

          </section>

          {/* PIPELINE */}

          <section className="rounded-[26px] border border-white/[0.08] bg-white/[0.035] p-6 backdrop-blur-xl">

            <p className="text-lg font-semibold">
              Atlas pipeline
            </p>

            <p className="mt-1 text-sm text-slate-500">
              Every document follows a secure
              processing path.
            </p>

            <div className="mt-6 space-y-3">

              {[
                [
                  "01",
                  "Ingest",
                  "Receive documents",
                ],
                [
                  "02",
                  "Validate",
                  "Signature and integrity",
                ],
                [
                  "03",
                  "Understand",
                  "Parse and extract",
                ],
                [
                  "04",
                  "Connect",
                  "Build knowledge",
                ],
              ].map(
                ([number, title, description]) => (

                  <div
                    key={number}
                    className="flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.025] p-3"
                  >

                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-500/10 text-xs font-semibold text-blue-300">
                      {number}
                    </div>

                    <div>

                      <p className="text-sm font-medium text-slate-200">
                        {title}
                      </p>

                      <p className="text-xs text-slate-500">
                        {description}
                      </p>

                    </div>

                  </div>

                )
              )}

            </div>

          </section>

        </div>

        {/* ====================================================
            RECENT UPLOADS
        ==================================================== */}

        <section className="mt-6 rounded-[26px] border border-white/[0.08] bg-white/[0.035] p-6 backdrop-blur-xl">

          <div className="flex items-center justify-between gap-4">

            <div>

              <p className="text-lg font-semibold">
                Recent uploads
              </p>

              <p className="mt-1 text-sm text-slate-500">
                Documents stored in the Atlas
                database.
              </p>

            </div>

            <div className="rounded-full border border-blue-400/20 bg-blue-400/10 px-3 py-1 text-xs text-blue-300">
              {totalUploads}{" "}
              {totalUploads === 1
                ? "document"
                : "documents"}
            </div>

          </div>

          <div className="mt-5 overflow-hidden rounded-2xl border border-white/[0.06]">

            {loadingUploads ? (

              <div className="px-5 py-10 text-center text-sm text-slate-500">
                Loading your documents...
              </div>

            ) : recentUploads.length === 0 ? (

              <div className="px-5 py-10 text-center text-sm text-slate-500">
                No documents uploaded yet.
              </div>

            ) : (

              <div className="divide-y divide-white/[0.06]">

                {recentUploads.map(
                  (upload) => (

                    <div
                      key={upload.id}
                      className="flex flex-col gap-3 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
                    >

                      <div className="flex min-w-0 items-center gap-3">

                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-300">

                          <svg
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                          >
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                            <path d="M14 2v6h6" />
                          </svg>

                        </div>

                        <div className="min-w-0">

                          <p className="truncate text-sm font-medium text-slate-200">
                            {upload.fileName}
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            {formatFileSize(
                              upload.size
                            )}{" "}
                            ·{" "}
                            {formatUploadDate(
                              upload.uploadedAt
                            )}
                          </p>

                        </div>

                      </div>

                      <span
                        className={`w-fit rounded-full border px-2.5 py-1 text-xs ${getStatusStyle(
                          upload.status
                        )}`}
                      >
                        {upload.status}
                      </span>

                    </div>

                  )
                )}

              </div>

            )}

          </div>

        </section>

        {/* ====================================================
            STORAGE SUMMARY
        ==================================================== */}

        <section className="mt-6 rounded-[26px] border border-white/[0.08] bg-white/[0.035] p-6 backdrop-blur-xl">

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

            <div>

              <p className="text-sm font-medium text-slate-300">
                Storage summary
              </p>

              <p className="mt-1 text-xs text-slate-500">
                Total size of all documents currently
                recorded in Atlas.
              </p>

            </div>

            <p className="text-2xl font-semibold text-white">
              {formatFileSize(
                totalStorage
              )}
            </p>

          </div>

        </section>

      </div>

    </main>
  );
}