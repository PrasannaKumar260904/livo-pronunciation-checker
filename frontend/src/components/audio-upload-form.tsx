"use client";

import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import {
  AssessmentApiError,
  createAssessment,
} from "@/api/assessments";
import { AssessmentResults } from "@/components/assessment-results";
import { ProcessingSteps } from "@/components/processing-steps";
import type { AssessmentResponse } from "@/types/assessment";

const ACCEPTED_AUDIO_TYPES = [
  "audio/mpeg",
  "audio/mp3",
  "audio/mp4",
  "audio/wav",
  "audio/wave",
  "audio/webm",
  "audio/x-m4a",
  "audio/x-wav",
];
const ACCEPTED_EXTENSIONS = [".wav", ".mp3", ".m4a", ".webm"];
const MAX_FILE_SIZE_MB = 25;
const STEP_INTERVAL_MS = 1300;

type SubmissionState = "idle" | "processing" | "complete" | "error";

export function AudioUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [state, setState] = useState<SubmissionState>("idle");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [activeStep, setActiveStep] = useState(0);
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [fileInputKey, setFileInputKey] = useState(0);
  const resultsRef = useRef<HTMLDivElement | null>(null);

  const isProcessing = state === "processing";

  const helperText = useMemo(() => {
    if (!file) {
      return "Accepted formats: WAV, MP3, M4A, or WebM. Target duration: 30-45 seconds.";
    }

    return `${file.name} · ${(file.size / 1024 / 1024).toFixed(2)} MB`;
  }, [file]);

  useEffect(() => {
    if (!isProcessing) {
      return;
    }

    setActiveStep(0);
    const interval = window.setInterval(() => {
      setActiveStep((currentStep) => Math.min(currentStep + 1, 4));
    }, STEP_INTERVAL_MS);

    return () => window.clearInterval(interval);
  }, [isProcessing]);

  useEffect(() => {
    if (assessment && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [assessment]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (isProcessing) {
      return;
    }

    if (!file) {
      setState("error");
      setErrorMessage("Choose an audio file before submitting.");
      return;
    }

    if (file.size > MAX_FILE_SIZE_MB * 1024 * 1024) {
      setState("error");
      setErrorMessage(`Audio files must be ${MAX_FILE_SIZE_MB} MB or smaller.`);
      return;
    }

    if (file.type && !ACCEPTED_AUDIO_TYPES.includes(file.type)) {
      setState("error");
      setErrorMessage("Use a WAV, MP3, M4A, or WebM audio file.");
      return;
    }

    if (!hasAcceptedExtension(file.name)) {
      setState("error");
      setErrorMessage("Use a file ending in .wav, .mp3, .m4a, or .webm.");
      return;
    }

    setState("processing");
    setErrorMessage("");
    setAssessment(null);

    try {
      const response = await createAssessment(file);
      setActiveStep(4);
      setAssessment(response);
      setState("complete");
    } catch (error) {
      setState("error");
      setErrorMessage(formatSubmissionError(error));
    }
  }

  return (
    <div className="space-y-8">
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
                key={fileInputKey}
                accept=".wav,.mp3,.m4a,.webm,audio/*"
                className="w-full max-w-sm cursor-pointer rounded-md border border-[#d8ded3] bg-white px-3 py-2 text-sm text-[#17211f] file:mr-3 file:rounded-md file:border-0 file:bg-[#1f6f5b] file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white disabled:cursor-not-allowed disabled:opacity-60"
                disabled={isProcessing}
                name="audio"
                type="file"
                onChange={(event) => {
                  setFile(event.target.files?.[0] ?? null);
                  setState("idle");
                  setErrorMessage("");
                }}
              />
              <p className="mt-4 max-w-md text-sm leading-6 text-[#5e6b66]">
                {helperText}
              </p>
            </div>
          </div>

          <button
            className="inline-flex h-11 w-full items-center justify-center rounded-md bg-[#1f6f5b] px-4 text-sm font-semibold text-white transition hover:bg-[#185747] disabled:cursor-not-allowed disabled:bg-[#8aa69d]"
            disabled={isProcessing}
            type="submit"
          >
            {isProcessing ? "Processing recording..." : "Submit recording"}
          </button>

          {errorMessage ? (
            <div
              className="rounded-md border border-[#efc4bb] bg-[#fff0ed] px-3 py-3 text-sm leading-6 text-[#8f2f1f]"
              role="alert"
            >
              {errorMessage}
            </div>
          ) : null}
        </div>
      </form>

      {isProcessing ? <ProcessingSteps activeStep={activeStep} /> : null}

      {assessment ? (
        <div ref={resultsRef}>
          <AssessmentResults
            assessment={assessment}
            onReset={() => {
              setAssessment(null);
              setFile(null);
              setFileInputKey((currentKey) => currentKey + 1);
              setState("idle");
              setErrorMessage("");
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
          />
        </div>
      ) : null}
    </div>
  );
}

function hasAcceptedExtension(filename: string) {
  const lowerFilename = filename.toLowerCase();
  return ACCEPTED_EXTENSIONS.some((extension) =>
    lowerFilename.endsWith(extension),
  );
}

function formatSubmissionError(error: unknown) {
  if (error instanceof AssessmentApiError) {
    if (typeof error.detail === "object" && error.detail?.message) {
      return error.detail.message;
    }

    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "We could not process that recording. Please try again.";
}
