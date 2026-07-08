import type {
  AssessmentFeedback,
  AssessmentResponse,
  PronunciationIssue,
} from "@/types/assessment";

type AssessmentResultsProps = {
  assessment: AssessmentResponse;
  onReset: () => void;
};

const severityStyles: Record<string, string> = {
  high: "border-[#e8b6ae] bg-[#fff2ef] text-[#8f2f1f]",
  medium: "border-[#e8d29a] bg-[#fff8e7] text-[#735300]",
  low: "border-[#b8d3e8] bg-[#eef7ff] text-[#23567c]",
};

export function AssessmentResults({
  assessment,
  onReset,
}: AssessmentResultsProps) {
  const { analysis, feedback, transcription } = assessment;

  return (
    <section className="space-y-8">
      <div className="flex flex-col gap-4 border-t border-[#d8ded3] pt-8 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#346c5d]">
            Assessment complete
          </p>
          <h2 className="mt-2 text-3xl font-semibold text-[#17211f]">
            Pronunciation Results
          </h2>
        </div>
        <button
          className="inline-flex h-10 items-center justify-center rounded-md border border-[#b9c8c1] bg-white px-4 text-sm font-semibold text-[#1f4f44] transition hover:bg-[#f1f6f4]"
          onClick={onReset}
          type="button"
        >
          Upload another recording
        </button>
      </div>

      <ScoreCard score={analysis.score} />
      <MetricsGrid assessment={assessment} />
      <IssuesList issues={analysis.issues} />
      <TranscriptCard text={transcription.text} />
      <FeedbackPanel feedback={feedback} />
    </section>
  );
}

function ScoreCard({ score }: { score: number }) {
  return (
    <section className="rounded-lg border border-[#cad8d2] bg-[#17211f] p-6 text-white shadow-sm sm:p-8">
      <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#9ed6c3]">
        Pronunciation Score
      </p>
      <div className="mt-5 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="text-6xl font-semibold leading-none sm:text-7xl">
          {score}
          <span className="text-3xl text-[#b8c9c3]"> / 100</span>
        </div>
        <p className="max-w-sm text-sm leading-6 text-[#d7e3df]">
          This score is based on deterministic pacing, pause, transcript length,
          and segment-duration heuristics from the backend analysis.
        </p>
      </div>
    </section>
  );
}

function MetricsGrid({ assessment }: { assessment: AssessmentResponse }) {
  const metrics = assessment.analysis.metrics;
  const cards = [
    {
      label: "Speaking Rate",
      value: metrics.speaking_rate_wpm.toFixed(1),
      unit: "WPM",
      accent: "bg-[#edf7f3] text-[#1f6f5b]",
    },
    {
      label: "Word Count",
      value: metrics.total_word_count.toString(),
      unit: "words",
      accent: "bg-[#eef4ff] text-[#285b9a]",
    },
    {
      label: "Pause Count",
      value: metrics.pause_count.toString(),
      unit: "pauses",
      accent: "bg-[#fff8e7] text-[#735300]",
    },
    {
      label: "Avg Segment",
      value: metrics.average_segment_duration_seconds.toFixed(1),
      unit: "sec",
      accent: "bg-[#fff1f5] text-[#8c2e58]",
    },
  ];

  return (
    <section>
      <h3 className="text-xl font-semibold text-[#17211f]">Analysis Metrics</h3>
      <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((card) => (
          <div
            className="rounded-lg border border-[#d8ded3] bg-white p-5 shadow-sm"
            key={card.label}
          >
            <p className="text-sm font-medium text-[#5e6b66]">{card.label}</p>
            <div className="mt-4 flex items-end gap-2">
              <span className="text-3xl font-semibold text-[#17211f]">
                {card.value}
              </span>
              <span
                className={`mb-1 rounded-md px-2 py-1 text-xs font-semibold ${card.accent}`}
              >
                {card.unit}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

function IssuesList({ issues }: { issues: PronunciationIssue[] }) {
  return (
    <section>
      <h3 className="text-xl font-semibold text-[#17211f]">Potential Issues</h3>
      <div className="mt-4 space-y-3">
        {issues.length ? (
          issues.map((issue) => (
            <div
              className={`rounded-lg border p-4 ${
                severityStyles[issue.severity.toLowerCase()] ??
                "border-[#d8ded3] bg-white text-[#17211f]"
              }`}
              key={`${issue.category}-${issue.message}`}
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="rounded-md bg-white/70 px-2 py-1 text-xs font-semibold uppercase tracking-[0.12em]">
                  {issue.category.replaceAll("_", " ")}
                </span>
                <span className="rounded-md bg-white/70 px-2 py-1 text-xs font-semibold uppercase tracking-[0.12em]">
                  {issue.severity}
                </span>
              </div>
              <p className="mt-3 text-sm font-medium leading-6">{issue.message}</p>
            </div>
          ))
        ) : (
          <div className="rounded-lg border border-[#c8ddcf] bg-[#f2fbf5] p-4 text-sm font-medium text-[#27633c]">
            No potential issues were detected by the current analysis.
          </div>
        )}
      </div>
    </section>
  );
}

function TranscriptCard({ text }: { text: string }) {
  return (
    <section>
      <h3 className="text-xl font-semibold text-[#17211f]">Transcript</h3>
      <div className="mt-4 rounded-lg border border-[#d8ded3] bg-white p-5 shadow-sm">
        <p className="whitespace-pre-wrap text-base leading-8 text-[#2d3b37]">
          {text || "No transcript text was returned."}
        </p>
      </div>
    </section>
  );
}

function FeedbackPanel({ feedback }: { feedback: AssessmentFeedback | null }) {
  if (!feedback) {
    return (
      <section>
        <h3 className="text-xl font-semibold text-[#17211f]">AI Feedback</h3>
        <div className="mt-4 rounded-lg border border-[#e8d29a] bg-[#fff8e7] p-5 text-sm font-medium text-[#735300]">
          AI coaching is temporarily unavailable. Your pronunciation analysis was completed successfully.
        </div>
      </section>
    );
  }

  return (
    <section>
      <h3 className="text-xl font-semibold text-[#17211f]">AI Feedback</h3>
      <div className="mt-4 grid gap-4 lg:grid-cols-2">
        <FeedbackBlock
          items={[feedback.overall_summary]}
          title="Overall Summary"
        />
        <FeedbackBlock items={feedback.strengths} title="Strengths" />
        <FeedbackBlock
          items={feedback.improvement_suggestions}
          title="Improvement Suggestions"
        />
        <FeedbackBlock
          items={feedback.practice_recommendations}
          title="Practice Recommendations"
        />
      </div>
    </section>
  );
}

function FeedbackBlock({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-lg border border-[#d8ded3] bg-white p-5 shadow-sm">
      <h4 className="text-sm font-semibold uppercase tracking-[0.14em] text-[#346c5d]">
        {title}
      </h4>
      <ul className="mt-4 space-y-3">
        {items.length ? (
          items.map((item) => (
            <li className="text-sm leading-6 text-[#2d3b37]" key={item}>
              {item}
            </li>
          ))
        ) : (
          <li className="text-sm leading-6 text-[#6b7772]">
            No feedback was returned for this section.
          </li>
        )}
      </ul>
    </div>
  );
}

