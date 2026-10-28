"use client";

export default function ErrorBoundary({
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <main className="route-error" role="alert">
      <span className="error-mark" aria-hidden="true">
        !
      </span>
      <div>
        <h1>We couldn’t open this view</h1>
        <p>Your workflow records are safe. Try loading the Recovery Studio again.</p>
        <button className="setup-button" type="button" onClick={() => reset()}>
          Try again
        </button>
      </div>
    </main>
  );
}
