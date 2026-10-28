export default function Loading() {
  return (
    <main className="route-loading" role="status" aria-live="polite">
      <span className="loading-mark" aria-hidden="true">
        F
      </span>
      <span>Opening your Recovery Studio…</span>
    </main>
  );
}
