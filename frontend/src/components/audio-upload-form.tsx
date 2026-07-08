"use client";

import { FormEvent, useMemo, useState } from "react";
import { createAssessment } from "@/lib/api";

const ACCEPTED_AUDIO_TYPES = ["audio/mpeg", "audio/mp4", "audio/wav", "audio/webm"];
const MAX_FILE_SIZE_MB = 25;

type SubmissionState = "idle" | "submitting" | "not-implemented" | "error";

export function AudioUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [state, setState] = useState<SubmissionState>("idle");
  const [message, setMessage] = useState<string>("");

  const helperText = useMemo(() => {
    if (!file) {
      return "Accepted formats: WAV, MP3, M4A, or WebM. Target duration: 30-45 seconds.";
    }

    return `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`;
  }, [file]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!file) {
      setState("error");
      setMessage("Choose an audio file before submitting.");
      return;
    }

    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      setState("error");
      setMessage(`Audio files must be ${MAX_FILE_SIZE_MB} MB or smaller.`);
      return;
    }

    if (file.type && !ACCEPTED_AUDIO_TYPES.includes(file.type)) {
      setState("error");
      setMessage("Use a WAV, MP3, M4A, or WebM audio file.");
      return;
    }

    setState("submitting");
    setMessage("");

    try {
      await createAssessment(file);
      setState("idle");
      setMessage("");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Assessment request failed.";

      setState(errorMessage.includes("not implemented") ? "not-implemented" : "error");
      setMessage(errorMessage);
    }
  }

  return (
    <form
      className="w-full rounded-lg border border-[#d8ded3] bg-white p-5 shadow-sm sm:p-6"
      onSubmit={handleSubmit}
    >
      <div className="space-y-5">
        <div>
          <label
            className="block text-sm font-semibold text-[#17211f]"
            htmlFor="audio"
          >
            English audio recording
          </label>
          <div className="mt-3 flex min-h-44 flex-col items-center justify-center rounded-lg border border-dashed border-[#9bad9f] bg-[#fbfcf8] px-4 py-8 text-center">
            <input
              id="audio"
              accept="audio/*"
              className="w-full max-w-sm cursor-pointer rounded-md border border-[#d8ded3] bg-white px-3 py-2 text-sm text-[#17211f] file:mr-3 file:rounded-md file:border-0 file:bg-[#1f6f5b] file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white"
              name="audio"
              type="file"
              onChange={(event) => {
                setFile(event.target.files?.[0] ?? null);
                setState("idle");
                setMessage("");
              }}
            />
            <p className="mt-4 max-w-md text-sm leading-6 text-[#5e6b66]">
              {helperText}
            </p>
          </div>
        </div>

        <button
          className="inline-flex h-11 w-full items-center justify-center rounded-md bg-[#1f6f5b] px-4 text-sm font-semibold text-white transition hover:bg-[#185747] disabled:cursor-not-allowed disabled:bg-[#8aa69d]"
          disabled={state === "submitting"}
          type="submit"
        >
          {state === "submitting" ? "Preparing upload..." : "Submit recording"}
        </button>

        {message ? (
          <p
            className={`rounded-md px-3 py-2 text-sm ${
              state === "not-implemented"
                ? "bg-[#fff7df] text-[#725300]"
                : "bg-[#fff0ed] text-[#8f2f1f]"
            }`}
            role="status"
          >
            {message}
          </p>
        ) : null}
      </div>
    </form>
  );
}

