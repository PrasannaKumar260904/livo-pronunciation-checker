import { AudioUploadForm } from "@/components/audio-upload-form";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f7f2]">
      <section className="mx-auto w-full max-w-6xl px-5 py-8 sm:px-8 sm:py-12">
        <div className="space-y-8">
          <div className="max-w-3xl space-y-5">
            <p className="text-sm font-semibold uppercase tracking-[0.18em] text-[#346c5d]">
              AI pronunciation assessment
            </p>
            <h1 className="text-4xl font-semibold leading-tight text-[#17211f] sm:text-5xl">
              Livo Pronunciation Checker
            </h1>
            <p className="max-w-2xl text-base leading-7 text-[#4d5c57] sm:text-lg">
              Upload a 30-45 second English recording to receive a
              pronunciation score, transcript, analysis metrics, potential
              issues, and AI feedback.
            </p>
          </div>

          <AudioUploadForm />
        </div>
      </section>
    </main>
  );
}
