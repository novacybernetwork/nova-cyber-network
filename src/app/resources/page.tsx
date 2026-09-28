import type { Metadata } from "next";
import { PageHeader } from "@/components/layout/PageHeader";
import { ResourceCategorySection } from "@/components/resources/ResourceCategorySection";
import { resourceCategories } from "@/data/resources";

export const metadata: Metadata = {
  title: "Resources",
  description:
    "Curated cybersecurity learning resources for CyberPatriot, National Cyber League, CTF practice, and core technical skills.",
};

export default function ResourcesPage() {
  return (
    <>
      <PageHeader
        eyebrow="Resources"
        title="A curated library, organized by skill."
        description="Resources are curated for educational use in legal and authorized cybersecurity environments."
      />

      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {resourceCategories.map((category, index) => (
              <ResourceCategorySection
                key={category.id}
                category={category}
                delayMs={(index % 3) * 60}
              />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
