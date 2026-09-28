interface PageHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
}

export function PageHeader({ eyebrow, title, description }: PageHeaderProps) {
  return (
    <section className="relative overflow-hidden border-b border-border bg-radial-glow pt-36 pb-16">
      <div className="bg-cyber-grid pointer-events-none absolute inset-0" aria-hidden="true" />
      <div className="relative mx-auto max-w-4xl px-6 text-center">
        {eyebrow && (
          <p className="mb-3 font-mono text-xs font-medium tracking-[0.2em] text-accent uppercase">
            {eyebrow}
          </p>
        )}
        <h1 className="text-balance text-4xl font-semibold tracking-tight text-foreground sm:text-5xl">
          {title}
        </h1>
        {description && (
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-muted">
            {description}
          </p>
        )}
      </div>
    </section>
  );
}
