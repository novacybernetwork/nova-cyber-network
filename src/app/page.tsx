import { Hero } from "@/components/home/Hero";
import { StatsSection } from "@/components/home/StatsSection";
import { WhatWeDo } from "@/components/home/WhatWeDo";
import { UpcomingEventPreview } from "@/components/home/UpcomingEventPreview";
import { MissionSection } from "@/components/home/MissionSection";
import { LeadershipPreview } from "@/components/home/LeadershipPreview";
import { JoinCTA } from "@/components/home/JoinCTA";

export default function HomePage() {
  return (
    <>
      <Hero />
      <StatsSection />
      <WhatWeDo />
      <UpcomingEventPreview />
      <MissionSection />
      <LeadershipPreview />
      <JoinCTA />
    </>
  );
}
