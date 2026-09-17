import AppShell from "@/components/layout/AppShell";


export default function GoalsPage() {
  return (
    <AppShell>
      <div>
        <h1 className="text-3xl font-bold text-strong">
          Learning Goals
        </h1>

        <p className="mt-2 text-muted">
          Your personalized learning goals will
          appear here.
        </p>
      </div>
    </AppShell>
  );
}