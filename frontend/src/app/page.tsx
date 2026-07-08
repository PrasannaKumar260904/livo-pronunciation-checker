import { AudioUploadForm } from "@/components/audio-upload-form";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f7f2]">
      <section className="mx-auto flex min-h-screen w-full max-w-5xl flex-col justify-center px-5 py-10 sm:px-8">
        <div className="grid gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
          <div className="space-y-5">
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#346c5d]">
              AI pronunciation assessment
            </p>
            <div className="space-y-4">
              <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-[#17211f] sm:text-5xl">
                Livo Pronunciation Checker
              </h1>
              <p className="max-w-xl text-base leading-7 text-[#4d5c57] sm:text-lg">
                Upload a short English recording to prepare it for scoring,
                issue highlighting, and actionable feedback once the assessment
                engine is connected.
              </p>
            </div>
          </div>

          <AudioUploadForm />
        </div>
      </section>
    </main>
  );
}

