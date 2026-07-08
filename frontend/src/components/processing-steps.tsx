const STEPS = [
  "Uploading...",
  "Validating audio...",
  "Transcribing speech...",
  "Analyzing pronunciation...",
  "Generating AI feedback...",
];

type ProcessingStepsProps = {
  activeStep: number;
};

export function ProcessingSteps({ activeStep }: ProcessingStepsProps) {
  const progress = ((activeStep + 1) / STEPS.length) * 100;

  return (
    <div className="rounded-lg border border-[#d8ded3] bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-[#17211f]">
            Processing recording
          </p>
          <p className="mt-1 text-sm text-[#5e6b66]">{STEPS[activeStep]}</p>
        </div>
        <div className="h-10 w-10 shrink-0 rounded-full border-4 border-[#d9e4df] border-t-[#1f6f5b] animate-spin" />
      </div>

      <div className="mt-5 h-2 overflow-hidden rounded-full bg-[#e7ece5]">
        <div
          className="h-full rounded-full bg-[#1f6f5b] transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="mt-5 grid gap-2 sm:grid-cols-5">
        {STEPS.map((step, index) => (
          <div
            className={`rounded-md border px-2 py-2 text-xs font-medium ${
              index <= activeStep
                ? "border-[#b6d6ca] bg-[#edf7f3] text-[#1f6f5b]"
                : "border-[#e3e7df] bg-[#fbfcf8] text-[#7b8782]"
            }`}
            key={step}
          >
            {step.replace("...", "")}
          </div>
        ))}
      </div>
    </div>
  );
}

